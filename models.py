from abc import ABC, abstractmethod
import math
from theme_manager import locale

class IAnalyzable(ABC):
    @abstractmethod
    def calculate_turnover(self) -> float:
        pass

class BaseItem:
    def __init__(self, id_code, name, price, quantity):
        self.id_code = str(id_code)
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

class Product(BaseItem, IAnalyzable):
    def __init__(self, id_code, name, price, quantity, type_id="goods", 
                 ordering_cost=50.0, holding_cost_percent=0.2, discount=0.0, 
                 sales_history=None, min_stock=0, max_stock=0, reorder_point=0, strategy="jit"):
        super().__init__(id_code, name, price, quantity)
        
        self.type_id = type_id 
        self.ordering_cost = float(ordering_cost)       
        self.holding_cost_percent = float(holding_cost_percent)
        self.discount = float(discount)
        
        self.min_stock = int(min_stock)
        self.max_stock = int(max_stock)
        self.reorder_point = int(reorder_point)
        self.strategy = strategy
        
        self.sales_history = sales_history if sales_history else []
        
        self.abc_category = None
        self.xyz_category = None
        self.abc_share = 0.0 # Зберігаємо частку для пояснень
        self.xyz_coeff = 0.0 # Зберігаємо коефіцієнт для пояснень
        self.is_dead_stock = False

    def calculate_turnover(self) -> float:
        real_price = self.price * (1 - self.discount / 100)
        return real_price * self.quantity

    def __add__(self, other):
        if isinstance(other, int):
            self.quantity += other
            return self
        return NotImplemented

    # --- XYZ ---
    def calculate_xyz_coefficient(self):
        if not self.sales_history or sum(self.sales_history) == 0:
            self.is_dead_stock = True
            return float('inf')
        
        self.is_dead_stock = False
        n = len(self.sales_history)
        avg_x = sum(self.sales_history) / n
        variance_sum = sum((x - avg_x) ** 2 for x in self.sales_history)
        sigma = math.sqrt(variance_sum / n)
        if avg_x == 0: return 0
        coeff = (sigma / avg_x) * 100 
        return coeff

    def assign_xyz(self):
        self.xyz_coeff = self.calculate_xyz_coefficient()
        
        if self.is_dead_stock:
            self.xyz_category = "-"
        elif self.xyz_coeff < 10:
            self.xyz_category = "X"
        elif self.xyz_coeff < 25:
            self.xyz_category = "Y"
        else:
            self.xyz_category = "Z"

    # --- EOQ ---
    def calculate_eoq(self):
        if not self.sales_history or self.is_dead_stock: return 0
        avg_sales = sum(self.sales_history) / len(self.sales_history)
        annual_demand_D = avg_sales * 4 
        real_price = self.price * (1 - self.discount / 100)
        holding_cost_H = real_price * self.holding_cost_percent
        if holding_cost_H == 0: return 0
        try:
            eoq = math.sqrt((2 * annual_demand_D * self.ordering_cost) / holding_cost_H)
            return round(eoq, 2)
        except ValueError:
            return 0

    def calculate_safety_stock(self, service_factor=1.65): 
        if not self.sales_history or self.is_dead_stock: return 0
        n = len(self.sales_history)
        avg = sum(self.sales_history) / n
        sigma = math.sqrt(sum((x - avg) ** 2 for x in self.sales_history) / n)
        return round(service_factor * sigma, 2)

    def check_replenishment_needs(self):
        if self.strategy == "jit":
            if self.quantity <= self.reorder_point:
                order_size = self.calculate_eoq()
                if order_size == 0: order_size = 50 
                return True, order_size, f"Event Trigger! Stock ({self.quantity}) <= ROP ({self.reorder_point})"
            return False, 0, "OK"
        elif self.strategy == "interval":
            if self.max_stock > 0:
                needed = self.max_stock - self.quantity
                if needed > 0:
                    return True, needed, f"Cron Job! Top up to Max ({self.max_stock})"
            return False, 0, "OK (Full)"
        elif self.strategy == "minmax":
            if self.quantity <= self.min_stock:
                needed = self.max_stock - self.quantity
                return True, needed, f"Min-Max Trigger! {self.quantity} <= Min ({self.min_stock})"
            else:
                return False, 0, f"Wait. {self.quantity} > Min ({self.min_stock})"
        return False, 0, "No Strategy"

    # --- МЕТОДИ ПОЯСНЕНЬ (INSIGHTS) ---
    def get_abc_explanation(self):
        return locale.get("insight_abc").format(group=self.abc_category, share=round(self.abc_share, 2))

    def get_xyz_explanation(self):
        val = round(self.xyz_coeff, 1) if self.xyz_coeff != float('inf') else "∞"
        return locale.get("insight_xyz").format(group=self.xyz_category, coeff=val)

    def get_eoq_explanation(self):
        qty = self.calculate_eoq()
        return locale.get("insight_eoq").format(qty=qty, order_cost=self.ordering_cost, hold_cost=f"{self.holding_cost_percent*100}%")

class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def remove_product(self, product_id):
        self.products = [p for p in self.products if str(p.id_code) != str(product_id)]

    def perform_abc_analysis(self):
        active_products = [p for p in self.products if not p.is_dead_stock]
        if not active_products: return

        sorted_products = sorted(active_products, key=lambda p: p.calculate_turnover(), reverse=True)
        total_value = sum(p.calculate_turnover() for p in active_products)
        
        if total_value == 0: return

        current_sum = 0
        for p in sorted_products:
            turnover = p.calculate_turnover()
            current_sum += turnover
            
            # Зберігаємо частку цього товару у загальному обороті (не накопичувальну, а індивідуальну)
            # Або для пояснення краще накопичувальну? Зазвичай цікавить внесок.
            # Зробимо відсоток від загального
            p.abc_share = (turnover / total_value) * 100
            
            cumulative_share = (current_sum / total_value) * 100
            
            if cumulative_share <= 75: 
                p.abc_category = "A"
            elif cumulative_share <= 95: 
                p.abc_category = "B"
            else: 
                p.abc_category = "C"
                
        for p in self.products:
            if p.is_dead_stock: p.abc_category = "C"