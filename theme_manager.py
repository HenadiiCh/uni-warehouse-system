import customtkinter as ctk

# Початкове налаштування (зміниться через налаштування)
ctk.set_appearance_mode("Light")

class AppTheme:
    _mode = "Light" # Light або Dark

    @classmethod
    def set_mode(cls, mode):
        cls._mode = mode
        ctk.set_appearance_mode(mode)

    @classmethod
    def get_mode(cls):
        return cls._mode

    # Динамічні кольори (повертають значення залежно від режиму)
    @property
    def BACKGROUND(self):
        return "#EEFBF9" if self._mode == "Light" else "#121212"

    @property
    def SURFACE(self):
        return "#FFFFFF" if self._mode == "Light" else "#1E1E1E"

    @property
    def TEXT_MAIN(self):
        return "#1A1A1A" if self._mode == "Light" else "#E0E0E0"

    @property
    def TEXT_SEC(self):
        return "gray" if self._mode == "Light" else "#A0A0A0"

    # Статичні кольори (однакові для обох тем)
    PRIMARY = "#87A600"
    SECONDARY = "#81AD85"
    SUCCESS = "#2E7D32"
    DANGER = "#C62828"
    TEXT_LIGHT = "#FFFFFF" # Текст на кнопках завжди білий
    
    COLOR_A = "#4CAF50"
    COLOR_B = "#FFA000"
    COLOR_C = "#D32F2F"
    COLOR_DEAD = "#9E9E9E"

# Створюємо екземпляр теми для зручного доступу
theme = AppTheme()

class LocalizationManager:
    _instance = None
    _language = "uk"
    _currency = "UAH"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalizationManager, cls).__new__(cls)
        return cls._instance

    def set_language(self, lang_code):
        if lang_code in ["uk", "en"]:
            self._language = lang_code

    def get_current_lang(self):
        return self._language

    def set_currency(self, currency):
        self._currency = currency

    def get_currency_symbol(self):
        return "₴" if self._currency == "UAH" else "$"

    def get(self, key):
        translations = {
            "uk": {
                "slogan": "Ваші 20% зусиль для 80% результату",
                "loading": "Завантаження...",
                "menu_main": "Головна",
                "menu_settings": "Налаштування",
                "menu_products": "Товари",
                "header_dashboard": "Панель управління складом",
                "header_settings": "Налаштування застосунку",
                "header_details": "Картка товару",
                "btn_add": "Додати товар",
                "btn_edit": "Редагувати",
                "btn_delete": "Видалити",
                "btn_save": "Зберегти",
                "btn_back": "← Назад",
                "btn_view": "Огляд",
                
                "msg_saved": "Зміни успішно збережено!",
                "msg_deleted": "Товар видалено.",
                "confirm_del": "Видалити цей товар?",
                
                "empty_title": "Склад порожній... 🦗",
                "empty_text": "Схоже, тут гуляє лише вітер. Час додати перші товари!",
                
                "total_items": "Всього товарів",
                "dead_stock": "Неліквіди",
                "info_title": "Довідка користувача",
                
                "set_lang": "Мова інтерфейсу",
                "set_theme": "Тема оформлення", # NEW
                "theme_light": "Світла",
                "theme_dark": "Темна",
                "set_curr": "Валюта",
                "set_acc": "Акаунт",
                "btn_save_set": "Зберегти налаштування",

                "col_barcode": "Баркод (ID)",
                "col_name": "Назва",
                "col_type": "Тип",
                "col_stock": "Запас",
                "col_eoq": "EOQ",
                "col_safety": "Страх. запас",
                "col_strategy": "Стратегія",
                "col_action": "Дія",
                
                "lbl_discount": "Знижка (%)",
                "lbl_price": "Ціна",
                "lbl_qty": "Кількість",
                
                "type_prod": "Виробничий",
                "type_goods": "Товарний",

                "det_price": "Ціна одиниці",
                "det_turnover": "Оборот (Грошовий)",
                "det_holding": "Витрати на зберігання",
                "det_ordering": "Витрати на замовлення",
                "det_abc": "Група ABC",
                "det_xyz": "Група XYZ",
                
                # ПОВНИЙ ТЕКСТ ДОВІДКИ
                "help_text": """
                \n1. АВС-аналіз (Правило Парето):
                [cite_start]Дозволяє класифікувати ресурси фірми залежно від ступеня їх важливості[cite: 14].
                - Група А: Найважливіші (80% вартості запасів). [cite_start]Вимагають ретельного планування, щоденного обліку та контролю[cite: 15, 36].
                - Група В: Середні (наступні 15% вартості). [cite_start]Звичайний контроль[cite: 17].
                - Група С: Другорядні (останні 5% вартості). [cite_start]Велика частина асортименту, перевірка раз на півроку[cite: 20, 24].

                2. XYZ-аналіз (Стабільність попиту):
                [cite_start]Групування ресурсів залежно від характеру споживання та точності прогнозування[cite: 27].
                - X: Стабільний попит (коефіцієнт варіації v < 10%). [cite_start]Висока точність прогнозу[cite: 29].
                - Y: Сезонні коливання (10% <= v < 25%). [cite_start]Середні можливості прогнозування[cite: 30].
                - Z: Нерегулярний попит (v >= 25%). [cite_start]Низька точність[cite: 31].

                3. Нормування запасів (EOQ):
                [cite_start]Розрахунок оптимального розміру замовлення за формулою Уілсона для мінімізації сукупних витрат на замовлення та зберігання[cite: 349, 370].
                Формула: Q* = sqrt((2 * D * L) / H).

                4. Стратегії управління:
                - Фіксований розмір (JIT): Для групи А або AX. [cite_start]Замовлення при досягненні точки замовлення[cite: 39, 386].
                - Фіксований інтервал: Для групи С. [cite_start]Замовлення за графіком (наприклад, щовівторка)[cite: 433].
                - Мінімум-Максимум: Для нестабільного попиту (Z). [cite_start]Замовлення тільки якщо запас впав нижче мінімуму[cite: 488].
                """
            },
            "en": {
                "slogan": "Your 20% effort for 80% results",
                "loading": "Loading...",
                "menu_main": "Dashboard",
                "menu_settings": "Settings",
                "menu_products": "Products",
                "header_dashboard": "Warehouse Dashboard",
                "header_settings": "App Settings",
                "header_details": "Product Details",
                "btn_add": "Add Item",
                "btn_edit": "Edit",
                "btn_delete": "Delete",
                "btn_save": "Save",
                "btn_back": "← Back",
                "btn_view": "View",

                "msg_saved": "Changes saved successfully!",
                "msg_deleted": "Item deleted.",
                "confirm_del": "Delete this item?",

                "empty_title": "Warehouse is empty... 🦗",
                "empty_text": "Looks like only the wind lives here. Time to add some products!",

                "total_items": "Total Items",
                "dead_stock": "Dead Stock",
                "info_title": "User Guide",

                "set_lang": "Interface Language",
                "set_theme": "App Theme",
                "theme_light": "Light",
                "theme_dark": "Dark",
                "set_curr": "Currency",
                "set_acc": "Account",
                "btn_save_set": "Save Settings",
                
                "col_barcode": "Barcode (ID)",
                "col_name": "Name",
                "col_type": "Type",
                "col_stock": "Stock",
                "col_eoq": "EOQ",
                "col_safety": "Safety Stock",
                "col_strategy": "Strategy",
                "col_action": "Action",

                "lbl_discount": "Discount (%)",
                "lbl_price": "Price",
                "lbl_qty": "Quantity",

                "type_prod": "Production",
                "type_goods": "Goods",

                "det_price": "Unit Price",
                "det_turnover": "Turnover (Value)",
                "det_holding": "Holding Cost",
                "det_ordering": "Ordering Cost",
                "det_abc": "ABC Group",
                "det_xyz": "XYZ Group",

                "help_text": """
                \n1. ABC Analysis (Pareto Rule):
                [cite_start]Classifies resources based on their importance[cite: 14].
                - Group A: Vital items (80% value). [cite_start]Strict daily control[cite: 15, 36].
                - Group B: Medium importance (15% value). [cite_start]Regular control[cite: 17].
                - Group C: Low importance (5% value). [cite_start]Periodic review[cite: 20].

                2. XYZ Analysis (Demand Stability):
                [cite_start]Based on consumption regularity[cite: 27].
                - X: Stable demand (v < 10%). [cite_start]High forecast accuracy[cite: 29].
                - [cite_start]Y: Seasonal fluctuations (10% <= v < 25%)[cite: 30].
                - [cite_start]Z: Irregular demand (v >= 25%)[cite: 31].

                3. Norming (EOQ):
                [cite_start]Calculates Economic Order Quantity using Wilson's formula to minimize total costs[cite: 349].

                4. Management Strategies:
                - [cite_start]Fixed Order Size (JIT): For Group A/AX[cite: 39].
                - [cite_start]Fixed Interval: For Group C[cite: 433].
                - [cite_start]Min-Max: For irregular demand (Z)[cite: 488].
                """
            }
        }
        return translations[self._language].get(key, key)

locale = LocalizationManager()