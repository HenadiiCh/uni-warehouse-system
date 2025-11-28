import customtkinter as ctk
from PIL import Image, ImageTk 
import threading
import time
import uuid
import ctypes # ДЛЯ ІКОНКИ WINDOWS

from theme_manager import theme, locale, AppTheme # Імпортуємо оновлену тему
from models import Product, InventoryManager

# --- ФІКС ІКОНКИ ДЛЯ WINDOWS ---
try:
    myappid = 'mycompany.optistock.pro.1.0' # Довільний унікальний ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

# --- Діалог Додавання/Редагування (Оновлені кольори) ---
class ProductDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_save_callback, product_to_edit=None):
        super().__init__(parent)
        self.on_save_callback = on_save_callback
        self.product = product_to_edit
        
        title_key = "btn_edit" if product_to_edit else "btn_add"
        self.title(locale.get(title_key))
        self.geometry("450x700")
        self.configure(fg_color=theme.BACKGROUND) # Dynamic Color
        self.attributes("-topmost", True)
        self.grab_set()

        # Баркод
        self.create_input(locale.get("col_barcode"), "barcode_entry", 
                          default=product_to_edit.id_code if product_to_edit else str(uuid.uuid4())[:8].upper())
        if product_to_edit: self.barcode_entry.configure(state="disabled")

        self.create_input(locale.get("col_name"), "name_entry", 
                          default=product_to_edit.name if product_to_edit else "")
        
        lbl_type = ctk.CTkLabel(self, text=locale.get("col_type"), text_color=theme.TEXT_MAIN)
        lbl_type.pack(pady=(10, 0))
        self.type_var = ctk.StringVar(value=product_to_edit.type_id if product_to_edit else "goods")
        ctk.CTkSegmentedButton(self, values=["goods", "prod"], variable=self.type_var,
                               selected_color=theme.PRIMARY, text_color="black").pack(pady=5)

        self.create_input(locale.get("lbl_price"), "price_entry", 
                          default=str(product_to_edit.price) if product_to_edit else "")
        self.create_input(locale.get("lbl_qty"), "qty_entry", 
                          default=str(product_to_edit.quantity) if product_to_edit else "")
        self.create_input(locale.get("lbl_discount"), "disc_entry", 
                          default=str(product_to_edit.discount) if product_to_edit else "0")
        
        self.create_input("Order Cost (L)", "order_cost_entry", 
                          default=str(product_to_edit.ordering_cost) if product_to_edit else "50")
        self.create_input("Holding Cost % (H)", "hold_cost_entry", 
                          default=str(product_to_edit.holding_cost_percent) if product_to_edit else "0.2")

        ctk.CTkButton(self, text=locale.get("btn_save"), fg_color=theme.PRIMARY, 
                      command=self.save_product).pack(pady=30)

    def create_input(self, label, attr, default=""):
        ctk.CTkLabel(self, text=label, text_color=theme.TEXT_MAIN).pack(pady=(5,0))
        # Input fields are usually white/light grey even in dark mode for contrast, or adapt
        entry = ctk.CTkEntry(self, width=250, fg_color="white", text_color="black")
        entry.pack(pady=2)
        if default: entry.insert(0, default)
        setattr(self, attr, entry)

    def save_product(self):
        try:
            history = self.product.sales_history if self.product else [10, 10, 10, 10]
            new_product = Product(
                id_code=self.barcode_entry.get(),
                name=self.name_entry.get(),
                price=float(self.price_entry.get()),
                quantity=int(self.qty_entry.get()),
                type_id=self.type_var.get(),
                ordering_cost=float(self.order_cost_entry.get()),
                holding_cost_percent=float(self.hold_cost_entry.get()),
                discount=float(self.disc_entry.get()),
                sales_history=history
            )
            self.on_save_callback(new_product, is_edit=bool(self.product))
            self.destroy()
        except ValueError:
            print("Validation Error")

# --- Info Dialog (Виправлено) ---
class InfoDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(locale.get("info_title"))
        self.geometry("600x500")
        self.configure(fg_color=theme.BACKGROUND)
        self.attributes("-topmost", True)
        
        ctk.CTkLabel(self, text="OptiStock Guide", font=("Arial", 20, "bold"), text_color=theme.PRIMARY).pack(pady=10)
        
        # Текстове поле
        txt = ctk.CTkTextbox(self, width=550, height=400, fg_color=theme.SURFACE, 
                             text_color=theme.TEXT_MAIN, font=("Arial", 12))
        txt.pack(pady=10, padx=20)
        txt.insert("0.0", locale.get("help_text"))
        txt.configure(state="disabled")

# --- ГОЛОВНИЙ ЗАСТОСУНОК ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OptiStock")
        self.geometry("1200x750")
        self.configure(fg_color=theme.BACKGROUND)
        
        self.manager = InventoryManager()
        # Демо дані можна закоментувати, щоб перевірити Empty State
        # self.seed_demo_data() 
        
        self.sidebar = None
        self.main_area = None
        self.btn_info = None
        self.notification_label = None
        self.current_view = "dashboard"
        
        self.sort_column = "name"
        self.sort_reverse = False
        
        self.img_logo_large = None
        self.img_logo_small = None
        self.icon_tk = None 
        self.load_images()
        
        self.show_splash_screen()
        
        self.after(200, self.set_app_icon)

    def load_images(self):
        try:
            def get_resized(path, width):
                pil = Image.open(path)
                h = int(width * (pil.size[1] / pil.size[0]))
                return ctk.CTkImage(light_image=pil, size=(width, h)), pil

            self.img_logo_large, _ = get_resized("logo_large.png", 300)
            self.img_logo_small, pil_small = get_resized("logo_small.png", 40)
            self.icon_tk = ImageTk.PhotoImage(pil_small)
            
        except Exception as e:
            print(f"Error loading images: {e}")

    def set_app_icon(self):
        if self.icon_tk:
            self.iconphoto(True, self.icon_tk)

    def seed_demo_data(self):
        self.manager.add_product(Product("A1001", "MacBook Air M2", 45000, 8, "goods", sales_history=[20, 22, 19, 21])) 
        self.manager.add_product(Product("B2050", "Winter Tires R16", 2000, 100, "prod", sales_history=[5, 80, 50, 10])) 
        self.recalc_analytics()

    def recalc_analytics(self):
        for p in self.manager.products: p.assign_xyz()
        self.manager.perform_abc_analysis()

    # --- Notification ---
    def show_notification(self, message, is_error=False):
        if self.notification_label: self.notification_label.destroy()
        color = theme.DANGER if is_error else theme.SUCCESS
        self.notification_label = ctk.CTkLabel(self, text=message, fg_color=color, 
                                               text_color="white", corner_radius=10, height=40, width=200)
        self.notification_label.place(relx=0.5, rely=0.05, anchor="n")
        self.after(2500, self.notification_label.destroy)

    # --- Splash Screen ---
    def show_splash_screen(self):
        self.splash_frame = ctk.CTkFrame(self, fg_color=theme.BACKGROUND)
        self.splash_frame.pack(fill="both", expand=True)

        if self.img_logo_large:
            ctk.CTkLabel(self.splash_frame, text="", image=self.img_logo_large).pack(expand=True, pady=(50, 20))
        
        ctk.CTkLabel(self.splash_frame, text="OptiStock", font=("Arial", 40, "bold"), text_color=theme.PRIMARY).pack()
        self.progress = ctk.CTkProgressBar(self.splash_frame, progress_color=theme.PRIMARY)
        self.progress.pack(pady=40)
        self.progress.set(0)

        threading.Thread(target=self._animate_loading).start()

    def _animate_loading(self):
        for i in range(21):
            time.sleep(0.01)
            self.progress.set(i / 20)
        self.splash_frame.destroy()
        self.build_ui_structure()

    def clear_ui(self):
        if self.sidebar: self.sidebar.destroy()
        if self.main_area: self.main_area.destroy()
        if self.btn_info: self.btn_info.destroy()

    def build_ui_structure(self):
        self.configure(fg_color=theme.BACKGROUND) # Update background on theme change
        self.clear_ui()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=theme.SURFACE)
        self.sidebar.pack(side="left", fill="y")

        # Logo
        logo_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_box.pack(pady=30, padx=20, anchor="w")
        
        lbl_img = ctk.CTkLabel(logo_box, text="", image=self.img_logo_small)
        lbl_txt = ctk.CTkLabel(logo_box, text="OptiStock", font=("Arial", 22, "bold"), text_color=theme.PRIMARY)
        if self.img_logo_small: lbl_img.pack(side="left", padx=(0, 10))
        lbl_txt.pack(side="left")

        for widget in [logo_box, lbl_img, lbl_txt]:
            widget.bind("<Button-1>", lambda e: self.switch_view("dashboard"))
            widget.configure(cursor="hand2")

        # Menu
        self.create_menu_btn(locale.get("menu_main"), lambda: self.switch_view("dashboard"), "dashboard")
        self.create_menu_btn(f"+ {locale.get('btn_add')}", lambda: self.open_product_dialog(), "add")
        self.create_menu_btn(locale.get("menu_settings"), lambda: self.switch_view("settings"), "settings")

        # Main Area
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Info Button
        self.btn_info = ctk.CTkButton(self, text="?", width=50, height=50, corner_radius=25, 
                      fg_color=theme.PRIMARY, font=("Arial", 24, "bold"),
                      text_color="white",
                      command=self.open_info_dialog)
        self.btn_info.place(relx=0.96, rely=0.96, anchor="se")

        self.switch_view(self.current_view)

    # --- Navigation ---
    def switch_view(self, view_name, product_data=None):
        self.current_view = view_name
        
        # ФІКС БАГА: Очищаємо Main Area перед малюванням нового контенту
        if self.main_area:
            for widget in self.main_area.winfo_children(): widget.destroy()

        if view_name == "dashboard":
            self.draw_dashboard_content()
        elif view_name == "settings":
            self.draw_settings_content()
        elif view_name == "details" and product_data:
            self.draw_product_details(product_data)

    # --- 1. DASHBOARD ---
    def draw_dashboard_content(self):
        # Header
        ctk.CTkLabel(self.main_area, text=locale.get("header_dashboard"), 
                     font=("Arial", 28, "bold"), text_color=theme.TEXT_MAIN).pack(anchor="w", pady=(0, 20))

        # --- EMPTY STATE (Якщо нема товарів) ---
        if not self.manager.products:
            empty_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
            empty_frame.pack(expand=True)
            
            ctk.CTkLabel(empty_frame, text="📦", font=("Arial", 100)).pack()
            ctk.CTkLabel(empty_frame, text=locale.get("empty_title"), 
                         font=("Arial", 24, "bold"), text_color=theme.TEXT_MAIN).pack(pady=10)
            ctk.CTkLabel(empty_frame, text=locale.get("empty_text"), 
                         font=("Arial", 14), text_color=theme.TEXT_SEC).pack()
            
            ctk.CTkButton(empty_frame, text=locale.get("btn_add"), fg_color=theme.PRIMARY,
                          command=self.open_product_dialog).pack(pady=20)
            return # Виходимо, таблицю не малюємо

        # Stats
        stats_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        stats_frame.pack(anchor="w", fill="x", pady=(0, 20))
        self.create_stat_card(stats_frame, locale.get("total_items"), str(len(self.manager.products)))
        dead_count = sum(1 for p in self.manager.products if p.is_dead_stock)
        self.create_stat_card(stats_frame, locale.get("dead_stock"), str(dead_count), theme.COLOR_DEAD)

        # Table
        table_frame = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)
        
        self.sort_products_list()

        cols = [
            (locale.get("col_barcode"), "id_code"),
            (locale.get("col_name"), "name"),
            ("ABC", "abc_category"),
            (locale.get("col_stock"), "quantity"),
            (locale.get("lbl_price"), "price"),
            (locale.get("col_action"), None)
        ]
        self.create_table_header(table_frame, cols)
        
        for p in self.manager.products:
            self.create_table_row(table_frame, p)

    def sort_products_list(self):
        def get_key(obj):
            val = getattr(obj, self.sort_column)
            if val is None: return "" 
            if isinstance(val, str) and val.replace(".", "").isdigit():
                return float(val)
            return val
        try:
            self.manager.products.sort(key=get_key, reverse=self.sort_reverse)
        except AttributeError: pass

    def on_header_click(self, col_key):
        if not col_key: return
        if self.sort_column == col_key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col_key
            self.sort_reverse = False
        
        # Перемальовуємо Dashboard (вже з очищенням)
        self.draw_dashboard_content()

    # --- 2. DETAILS ---
    def draw_product_details(self, product: Product):
        curr = locale.get_currency_symbol()
        
        top_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkButton(top_frame, text=locale.get("btn_back"), width=100, fg_color="gray",
                      command=lambda: self.switch_view("dashboard")).pack(side="left")
        
        ctk.CTkLabel(top_frame, text=product.name, font=("Arial", 32, "bold"), 
                     text_color=theme.PRIMARY).pack(side="left", padx=20)

        btn_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text=locale.get("btn_edit"), width=100, fg_color=theme.PRIMARY,
                      command=lambda: self.open_product_dialog(product)).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text=locale.get("btn_delete"), width=100, fg_color=theme.DANGER,
                      command=lambda: self.delete_product(product)).pack(side="left", padx=5)

        grid_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        
        left_col = ctk.CTkFrame(grid_frame, fg_color=theme.SURFACE, corner_radius=15)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.create_detail_row(left_col, "ID / Barcode", product.id_code)
        self.create_detail_row(left_col, locale.get("col_type"), product.type_id.upper())
        self.create_detail_row(left_col, locale.get("det_price"), f"{product.price} {curr}")
        if product.discount > 0:
            self.create_detail_row(left_col, locale.get("lbl_discount"), f"{product.discount}%", color=theme.DANGER)
        
        self.create_detail_row(left_col, locale.get("col_stock"), str(product.quantity))
        self.create_detail_row(left_col, locale.get("det_turnover"), f"{product.calculate_turnover():.2f} {curr}")
        
        right_col = ctk.CTkFrame(grid_frame, fg_color=theme.SURFACE, corner_radius=15)
        right_col.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        abc_col = theme.COLOR_A if product.abc_category == "A" else theme.COLOR_B
        if product.abc_category == "C": abc_col = theme.COLOR_C

        self.create_detail_row(right_col, locale.get("det_abc"), str(product.abc_category), color=abc_col)
        self.create_detail_row(right_col, locale.get("det_xyz"), str(product.xyz_category))
        self.create_detail_row(right_col, "EOQ", str(product.calculate_eoq()))
        self.create_detail_row(right_col, locale.get("col_strategy"), product.get_strategy_recommendation())

    # --- 3. SETTINGS ---
    def draw_settings_content(self):
        ctk.CTkLabel(self.main_area, text=locale.get("header_settings"), 
                     font=("Arial", 28, "bold"), text_color=theme.TEXT_MAIN).pack(anchor="w", pady=(0, 20))

        container = ctk.CTkFrame(self.main_area, fg_color=theme.SURFACE, corner_radius=15)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Language
        ctk.CTkLabel(container, text=locale.get("set_lang"), font=("Arial", 16, "bold"), text_color=theme.TEXT_MAIN).pack(anchor="w", padx=30, pady=(30, 10))
        lang_var = ctk.StringVar(value=locale.get_current_lang())
        ctk.CTkSegmentedButton(container, values=["uk", "en"], variable=lang_var, 
                               selected_color=theme.PRIMARY, command=self.change_language).pack(anchor="w", padx=30)
        
        # Theme (NEW)
        ctk.CTkLabel(container, text=locale.get("set_theme"), font=("Arial", 16, "bold"), text_color=theme.TEXT_MAIN).pack(anchor="w", padx=30, pady=(20, 10))
        theme_var = ctk.StringVar(value=theme.get_mode())
        ctk.CTkSegmentedButton(container, values=["Light", "Dark"], variable=theme_var,
                               selected_color=theme.PRIMARY, command=self.change_theme).pack(anchor="w", padx=30)

        # Currency
        ctk.CTkLabel(container, text=locale.get("set_curr"), font=("Arial", 16, "bold"), text_color=theme.TEXT_MAIN).pack(anchor="w", padx=30, pady=(20, 10))
        curr_var = ctk.StringVar(value="UAH" if locale.get_currency_symbol() == "₴" else "USD")
        ctk.CTkSegmentedButton(container, values=["UAH", "USD"], variable=curr_var,
                               selected_color=theme.PRIMARY, command=self.change_currency).pack(anchor="w", padx=30)

        ctk.CTkButton(container, text=locale.get("btn_save_set"), fg_color=theme.PRIMARY, height=40,
                      command=lambda: self.show_notification(locale.get("msg_saved"))).pack(pady=40)

    # --- Actions ---
    def change_language(self, value):
        locale.set_language(value)
        self.build_ui_structure()
        self.show_notification("Language changed / Мову змінено")

    def change_theme(self, value):
        theme.set_mode(value)
        self.build_ui_structure() # Перемальовуємо все під нові кольори

    def change_currency(self, value):
        locale.set_currency(value)
        self.switch_view("settings")
        self.show_notification(locale.get("msg_saved"))

    def open_info_dialog(self):
        InfoDialog(self)

    def open_product_dialog(self, product_to_edit=None):
        ProductDialog(self, on_save_callback=self.on_product_saved, product_to_edit=product_to_edit)

    def on_product_saved(self, product, is_edit):
        if is_edit:
            for i, p in enumerate(self.manager.products):
                if p.id_code == product.id_code:
                    self.manager.products[i] = product
                    break
        else:
            self.manager.add_product(product)
        
        self.recalc_analytics()
        self.switch_view("dashboard")
        self.show_notification(locale.get("msg_saved"))

    def delete_product(self, product):
        self.manager.remove_product(product.id_code)
        self.recalc_analytics()
        self.switch_view("dashboard")
        self.show_notification(locale.get("msg_deleted"), is_error=True)

    # --- Helpers ---
    def create_menu_btn(self, text, command, view_tag):
        is_active = (self.current_view == view_tag)
        color = theme.PRIMARY if is_active else "transparent"
        text_col = theme.TEXT_LIGHT if is_active else theme.TEXT_MAIN
        if view_tag == "add":
            is_active = False; color = "transparent"; text_col = theme.TEXT_MAIN
        ctk.CTkButton(self.sidebar, text=text, fg_color=color, text_color=text_col, 
                      hover_color=theme.SECONDARY, height=45, corner_radius=8, anchor="w", 
                      command=command).pack(fill="x", padx=15, pady=5)

    def create_stat_card(self, parent, title, value, val_color=theme.PRIMARY):
        card = ctk.CTkFrame(parent, fg_color=theme.SURFACE, corner_radius=15, width=200, height=100)
        card.pack(side="left", padx=(0, 20))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Arial", 12), text_color=theme.TEXT_SEC).pack(pady=(15, 5), padx=15, anchor="w")
        ctk.CTkLabel(card, text=value, font=("Arial", 32, "bold"), text_color=val_color).pack(padx=15, anchor="w")

    def create_table_header(self, parent, cols):
        row = ctk.CTkFrame(parent, fg_color=theme.SECONDARY, height=40)
        row.pack(fill="x", pady=2)
        widths = [100, 140, 50, 60, 80, 80]
        
        for i, (name, key) in enumerate(cols):
            w = widths[i] if i < len(widths) else 100
            lbl = ctk.CTkLabel(row, text=str(name), font=("Arial", 13, "bold"), text_color="white", width=w, anchor="w")
            lbl.pack(side="left", padx=5)
            if key:
                lbl.bind("<Button-1>", lambda e, k=key: self.on_header_click(k))
                lbl.configure(cursor="hand2")

    def create_table_row(self, parent, product):
        row = ctk.CTkFrame(parent, fg_color=theme.SURFACE, height=40)
        row.pack(fill="x", pady=2)
        
        txt_col = theme.TEXT_MAIN
        if product.is_dead_stock: txt_col = theme.COLOR_DEAD

        vals = [product.id_code, product.name, product.abc_category, 
                str(product.quantity), f"{product.price}"]
        widths = [100, 140, 50, 60, 80]
        
        for i, val in enumerate(vals):
            col = txt_col
            if i == 2:
                if val == "A": col = theme.COLOR_A
                elif val == "B": col = theme.COLOR_B
                elif val == "C": col = theme.COLOR_C
            
            w = widths[i] if i < len(widths) else 100
            ctk.CTkLabel(row, text=str(val), font=("Arial", 13), text_color=col, width=w, anchor="w").pack(side="left", padx=5)

        ctk.CTkButton(row, text=locale.get("btn_view"), width=60, height=25, 
                      fg_color=theme.PRIMARY, text_color="white",
                      command=lambda: self.switch_view("details", product)).pack(side="left", padx=5)

    def create_detail_row(self, parent, label, value, color=None):
        if color is None: color = theme.TEXT_MAIN
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(f, text=label, text_color=theme.TEXT_SEC, font=("Arial", 14)).pack(side="left")
        ctk.CTkLabel(f, text=str(value), text_color=color, font=("Arial", 16, "bold")).pack(side="right")
        # Line separator color also needs to adapt (optional)
        ctk.CTkFrame(parent, height=1, fg_color="gray").pack(fill="x", padx=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()