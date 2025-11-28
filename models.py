from abc import ABC, abstractmethod
import math
from theme_manager import locale

class IAnalyzable(ABC):
    @abstractmethod
    def calculate_turnover(self) -> float:
        pass

class BaseItem:
    def __init__(self, id_code, name, price, quantity):
        self.id_code = str(id_code) # Робимо рядком для баркоду
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

class Product(BaseItem, IAnalyzable):
    def __init__(self, id_code, name, price, quantity, type_id="goods", 
                 ordering_cost=50.0, holding_cost_percent=0.2, discount=0.0, sales_history=None):
        super().__init__(id_code, name, price, quantity)
        
        self.type_id = type_id 
        self.ordering_cost = float(ordering_cost)       
        self.holding_cost_percent = float(holding_cost_percent)
        self.discount = float(discount) # Нове поле: Знижка у відсотках
        
        self.sales_history = sales_history if sales_history else []
        
        self.abc_category = None
        self.xyz_category = None
        self.is_dead_stock = False

    def calculate_turnover(self) -> float:
        # Оборот = (Ціна - Знижка) * Кількість
        real_price = self.price * (1 - self.discount / 100)
        return real_price * self.quantity

    def __add__(self, other):
        if isinstance(other, int):
            self.quantity += other
            return self
        return NotImplemented

    # --- XYZ Analysis ---
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
        coeff = self.calculate_xyz_coefficient()
        
        if self.is_dead_stock:
            self.xyz_category = "-"
        elif coeff < 10:
            self.xyz_category = "X"
        elif coeff < 25:
            self.xyz_category = "Y"
        else:
            self.xyz_category = "Z"

    # --- EOQ ---
    def calculate_eoq(self):
        if not self.sales_history or self.is_dead_stock: return 0
        
        avg_sales = sum(self.sales_history) / len(self.sales_history)
        annual_demand_D = avg_sales * 4 
        
        # Використовуємо реальну ціну (зі знижкою) для витрат на зберігання
        real_price = self.price * (1 - self.discount / 100)
        holding_cost_H = real_price * self.holding_cost_percent
        
        if holding_cost_H == 0: return 0
        
        try:
            eoq = math.sqrt((2 * annual_demand_D * self.ordering_cost) / holding_cost_H)
            return round(eoq, 2)
        except ValueError:
            return 0

    # --- Safety Stock ---
    def calculate_safety_stock(self, service_factor=1.65): 
        if not self.sales_history or self.is_dead_stock: return 0
        n = len(self.sales_history)
        avg = sum(self.sales_history) / n
        sigma = math.sqrt(sum((x - avg) ** 2 for x in self.sales_history) / n)
        return round(service_factor * sigma, 2)

    # --- Strategy ---
    def get_strategy_recommendation(self):
        if self.is_dead_stock: return "Dead Stock"
        
        if self.abc_category == "A": return "Fix Order Size (JIT)"
        elif self.abc_category == "C" and self.xyz_category == "X": return "Fix Interval"
        elif self.xyz_category == "Z": return "Min-Max System"
        else: return "General Control"

# Manager
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
            share = (current_sum / total_value) * 100
            
            if share <= 75: p.abc_category = "A"
            elif share <= 95: p.abc_category = "B"
            else: p.abc_category = "C"
                
        for p in self.products:
            if p.is_dead_stock: p.abc_category = "C"