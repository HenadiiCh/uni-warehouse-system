import customtkinter as ctk

# Початкове налаштування
ctk.set_appearance_mode("Light")

class AppTheme:
    _mode = "Light"

    @classmethod
    def set_mode(cls, mode):
        cls._mode = mode
        ctk.set_appearance_mode(mode)

    @classmethod
    def get_mode(cls):
        return cls._mode

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

    PRIMARY = "#87A600"
    SECONDARY = "#81AD85"
    SUCCESS = "#2E7D32"
    DANGER = "#C62828"
    INFO = "#0288D1"
    TEXT_LIGHT = "#FFFFFF"
    
    COLOR_A = "#4CAF50"
    COLOR_B = "#FFA000"
    COLOR_C = "#D32F2F"
    COLOR_DEAD = "#9E9E9E"

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
                "set_theme": "Тема оформлення",
                "set_curr": "Валюта",
                "btn_save_set": "Зберегти налаштування",

                # Підказки
                "help_type_title": "Типи запасів",
                "help_type_text": "• Goods (Товарний): Готова продукція для продажу.\n• Prod (Виробничий): Сировина або деталі для виробництва.",
                "help_strat_title": "Стратегії",
                "help_strat_text": "• JIT: Замовлення точно в строк (для дорогих товарів).\n• Interval: Поповнення за графіком (для дешевих).\n• MinMax: Замовлення тільки при досягненні мінімуму.",

                # Пояснення
                "insight_abc": "Чому група {group}?\nТовар генерує {share}% від загального обороту складу.\n(Порогові значення: A=75%, B=20%, C=5%)",
                "insight_xyz": "Чому група {group}?\nКоефіцієнт варіації попиту = {coeff}%.\n(X < 10%, 10% <= Y < 25%, Z >= 25%)",
                "insight_eoq": "Розрахунок EOQ:\nОптимальна партія = {qty} од.\nЦе баланс між вартістю замовлення ({order_cost}) та зберігання ({hold_cost}).",

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
                "lbl_min": "Мін. запас",
                "lbl_max": "Макс. запас",
                "lbl_rop": "Точка замовлення (ROP)",
                "lbl_strat": "Стратегія поповнення",

                "type_prod": "Виробничий",
                "type_goods": "Товарний",

                "det_abc": "Група ABC",
                "det_xyz": "Група XYZ",
                "det_status": "Статус замовлення",
                "status_ok": "✅ Запас в нормі",
                "status_order": "⚠️ Потрібно замовити: ",
                
                # --- ВИПРАВЛЕНО: ПОВНИЙ ТЕКСТ ДОВІДКИ ---
                "help_text": """
=== ІНСТРУКЦІЯ КОРИСТУВАЧА OPTISTOCK ===

1. [cite_start]АВС-АНАЛІЗ (Правило Парето) [cite: 14]
Метод дозволяє класифікувати ресурси фірми за ступенем їх важливості:
• Група А: Найважливіші (80% вартості запасів). [cite_start]Вимагають ретельного планування та щоденного контролю[cite: 15, 16].
• Група В: Середні (наступні 15% вартості). [cite_start]Звичайний контроль[cite: 17].
• Група С: Другорядні (останні 5% вартості). [cite_start]Велика частина асортименту, перевірка раз на півроку[cite: 20].

2. [cite_start]XYZ-АНАЛІЗ (Стабільність попиту) [cite: 27]
Групування ресурсів залежно від характеру споживання:
• X: Стабільний попит (коефіцієнт варіації v < 10%). [cite_start]Висока точність прогнозу[cite: 29].
• Y: Сезонні коливання (10% <= v < 25%). [cite_start]Середні можливості прогнозування[cite: 30].
• Z: Нерегулярний попит (v >= 25%). [cite_start]Низька точність, робота під замовлення[cite: 31].

3. [cite_start]НОРМУВАННЯ (EOQ) [cite: 349]
Розрахунок оптимального розміру замовлення за формулою Уілсона для мінімізації сукупних витрат на замовлення та зберігання.
Формула: Q* = sqrt((2 * D * L) / H).

4. [cite_start]СТРАТЕГІЇ УПРАВЛІННЯ [cite: 379]
• Фіксований розмір (JIT): Для групи А. [cite_start]Замовлення створюється, коли запас падає до точки перезамовлення[cite: 386].
• Фіксований інтервал: Для групи С. [cite_start]Замовлення робляться за графіком (наприклад, щовівторка) до максимального рівня[cite: 434].
• Мінімум-Максимум: Для нестабільного попиту (Z). [cite_start]Замовлення тільки якщо запас впав нижче мінімуму[cite: 488].
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
                "set_curr": "Currency",
                "btn_save_set": "Save Settings",

                "help_type_title": "Stock Types",
                "help_type_text": "• Goods: Ready-to-sell products.\n• Prod: Raw materials for production.",
                "help_strat_title": "Strategies",
                "help_strat_text": "• JIT: Just-In-Time (for high value).\n• Interval: Scheduled replenishment.\n• MinMax: Order only when below minimum.",

                "insight_abc": "Why Group {group}?\nGenerates {share}% of total warehouse turnover.\n(Thresholds: A=75%, B=20%, C=5%)",
                "insight_xyz": "Why Group {group}?\nDemand variation coefficient = {coeff}%.\n(X < 10%, 10% <= Y < 25%, Z >= 25%)",
                "insight_eoq": "EOQ Logic:\nOptimal Batch = {qty} units.\nBalances Order Cost ({order_cost}) vs Holding Cost ({hold_cost}).",

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
                "lbl_min": "Min Stock",
                "lbl_max": "Max Stock",
                "lbl_rop": "Reorder Point",
                "lbl_strat": "Replenishment Strategy",

                "type_prod": "Production",
                "type_goods": "Goods",

                "det_abc": "ABC Group",
                "det_xyz": "XYZ Group",
                "det_status": "Order Status",
                "status_ok": "✅ Stock OK",
                "status_order": "⚠️ Need to order: ",

                # --- FIXED: FULL HELP TEXT ---
                "help_text": """
=== OPTISTOCK USER GUIDE ===

1. [cite_start]ABC ANALYSIS (Pareto Rule) [cite: 14]
Classifies resources based on their importance:
• Group A: Vital items (80% value). [cite_start]Strict daily control and planning[cite: 15].
• Group B: Medium importance (15% value). [cite_start]Regular control[cite: 17].
• Group C: Low importance (5% value). [cite_start]Periodic review every 6 months[cite: 20].

2. [cite_start]XYZ ANALYSIS (Demand Stability) [cite: 27]
Based on consumption regularity and forecast accuracy:
• X: Stable demand (v < 10%). [cite_start]High forecast accuracy[cite: 29].
• Y: Seasonal fluctuations (10% <= v < 25%). [cite_start]Medium forecast accuracy[cite: 30].
• Z: Irregular demand (v >= 25%). [cite_start]Low accuracy, order on request[cite: 31].

3. [cite_start]NORMING (EOQ) [cite: 349]
Calculates Economic Order Quantity using Wilson's formula to minimize total costs (Ordering + Holding).
Formula: Q* = sqrt((2 * D * L) / H).

4. [cite_start]MANAGEMENT STRATEGIES [cite: 379]
[cite_start]• Fixed Size (JIT): For Group A. Orders placed when stock hits Reorder Point[cite: 386].
[cite_start]• Fixed Interval: For Group C. Scheduled orders (e.g., weekly) up to Max Level[cite: 434].
• Min-Max: For irregular demand (Z). [cite_start]Orders placed only if stock drops below Min[cite: 488].
                """
            }
        }
        return translations[self._language].get(key, key)

locale = LocalizationManager()