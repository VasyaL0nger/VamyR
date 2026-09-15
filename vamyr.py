import streamlit as st
import json
import os
import time

st.set_page_config(page_title="VamyR — Эксклюзивные Мини-Корабли", layout="centered", page_icon="🚢")

DB_SHIPS = "db_ships.json"
DB_ORDERS = "db_orders.json"
ADMIN_PASSWORD = "vamyradmin777"  # Пароль директора

# --- ФУНКЦИИ БАЗЫ ДАННЫХ ---
def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

ships = load_data(DB_SHIPS)
orders = load_data(DB_ORDERS)

if "cart" not in st.session_state:
    st.session_state.cart = []

if not ships:
    ships = [
        {
            "name": "⚓ Галеон 'Чёрная Жемчужина'",
            "price": "3500 грн",
            "desc": "Детализированная модель легендарного пиратского корабля ручной работы. Сделан из дерева, паруса из плотной ткани.",
            "img": "https://pixabay.com",
            "status": "Выставлен...",
            "stock": 3
        }
    ]
    save_data(ships, DB_SHIPS)

# ================= 💎 ИСПРАВЛЕННЫЙ ПРЕМИУМ-CSS (КАРТИНКИ БОЛЬШЕ НЕ ИСЧЕЗАЮТ) =================
st.markdown("""
    <style>
    /* Главный фон сайта — глубокий угольный */
    .stApp { background-color: #08080c !important; color: #f3f4f6 !important; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important; }
    
    /* Красивый заголовок с золотым градиентом */
    .main-title { font-size: 42px !important; font-weight: 800 !important; background: linear-gradient(135deg, #fef08a 0%, #ca8a04 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 5px; letter-spacing: 1px; }
    .sub-title { font-size: 18px !important; color: #a1a1aa !important; text-align: center; font-style: italic; margin-bottom: 30px; }
    
    /* Стилизация контейнеров карточек товара */
    div[data-testid="stForm"], div[data-testid="stBaseContainer"] .element-container { transition: all 0.3s ease; }
    
    /* Умный CSS-класс для обводки контейнеров с эффектом свечения */
    div[data-testid="stBlock"] { background: #12121a !important; border: 1px solid #27272a !important; border-radius: 16px !important; padding: 15px !important; margin-bottom: 20px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important; }
    div[data-testid="stBlock"]:hover { border-color: #ca8a04 !important; box-shadow: 0 10px 30px rgba(202, 138, 4, 0.15) !important; }
    
    /* Спойлеры и экспандеры */
    div[data-testid="stExpander"] { background-color: #12121a !important; border: 1px solid #27272a !important; border-radius: 12px !important; margin-bottom: 15px !important; }
    
    /* Дорогие кнопки с золотым градиентом */
    .stButton>button { background: linear-gradient(135deg, #eab308 0%, #a16207 100%) !important; color: #000000 !important; font-weight: 700 !important; border: none !important; border-radius: 10px !important; padding: 12px 24px !important; transition: all 0.25s ease-in-out !important; box-shadow: 0 4px 15px rgba(234, 179, 8, 0.2) !important; width: 100% !important; }
    .stButton>button:hover { background: linear-gradient(135deg, #fef08a 0%, #eab308 100%) !important; transform: scale(1.01) !important; box-shadow: 0 6px 20px rgba(234, 179, 8, 0.4) !important; }
    
    /* Кнопка очистки корзины */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton>button { background: #27272a !important; color: #ef4444 !important; border: 1px solid #44403c !important; box-shadow: none !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton>button:hover { background: #3f3f46 !important; color: #f87171 !important; }
    
    /* Текстовые поля */
    input, textarea { background-color: #181825 !important; color: white !important; border: 1px solid #3f3f46 !important; border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 👑 СИСТЕМА ЛОГОТИПА В УГЛУ ЭКРАНА (SIDEBAR) ---
st.sidebar.markdown("### 🏢 Бренд VamyR")
if os.path.exists("logo.png"):
    # Если ты загрузил logo.png на GitHub, сайт выведет твою реальную картинку
    st.sidebar.image("logo.png", use_container_width=True)
else:
    # Подстраховка: если файла нет, выводим красивую текстовую эмблему верфи
    st.sidebar.markdown("<h2 style='color:#eab308; text-align:center;'>🚢 VamyR</h2>", unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("🎨 Сменить стиль верфи")
theme_choice = st.sidebar.radio("Выбери тему сайта:", ["🌌 По умолчанию", "🌊 Глубокое Море", "🏴‍☠️ Пиратская Гавань"], horizontal=False)

# --- ШАПКА САЙТА ---
st.markdown('<div class="main-title">🚢 VamyR Premium</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Эксклюзивные модели кораблей ручной работы от конструкторского бюро VamyR</div>', unsafe_allow_html=True)

# ================= 🛍️ ДИЗАЙНЕРСКАЯ КОРЗИНА =================
st.subheader("🛍️ Твоя Корзина заказа")
if not st.session_state.cart:
    st.info("Ваша корзина пуста. Добавьте шедевры верфи с витрины ниже!")
else:
    total_price = 0
    items_names = []
    
    with st.container(border=True):
        st.write("📋 Список выбранных моделей на покупку и предзаказ:")
        for c_idx, cart_item in enumerate(st.session_state.cart):
            st.markdown(f"• **{cart_item['name']}** ({cart_item['status']}) — `{cart_item['price']}`")
            total_price += cart_item['price_int']
            items_names.append(f"{cart_item['name']} [{cart_item['status']}]")
            
        shipping_cost = 150
        final_sum = total_price + shipping_cost
        downpayment = int(total_price * 0.20)
        
        st.markdown(f"**Стоимость моделей верфи:** {total_price:,} грн".replace(",", " "))
        st.markdown(f"📦 **Противоударная паковка VamyR + Доставка:** {shipping_cost} грн")
        st.markdown(f"### 💰 Финальная сумма к оплате: `{final_sum:,} грн`".replace(",", " "))
        st.error(f"⚠️ **Финансовое уведомление:** Для запуска сборки требуется обязательная предоплата на материалы: **{downpayment:,} грн** (20%). Остаток — при получении в руки!".replace(",", " "))
        
        c_name = st.text_input("Введите Ваше Имя:", key="cart_name_input")
        c_tg = st.text_input("Укажите Ваш Telegram для связи:", placeholder="@username", key="cart_tg_input")
        
        col_send, col_clear = st.columns(2)
        with col_send:
            if st.button("✅ ОФОРМИТЬ ОБЩИЙ ЗАКАЗ", use_container_width=True):
                if c_name and c_tg:
                    for cart_item in st.session_state.cart:
                        orig_idx = cart_item["orig_idx"]
                        if ships[orig_idx]["status"] == "Выставлен...":
                            ships[orig_idx]["stock"] = max(0, ships[orig_idx].get("stock", 1) - 1)
                            if ships[orig_idx]["stock"] == 0:
                                ships[orig_idx]["status"] = "Продано"
                    save_data(ships, DB_SHIPS)

                    orders.append({
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "ship": ", ".join(items_names),
                        "price": f"{final_sum:,} грн".replace(",", " "),
                        "downpayment": f"{downpayment:,} грн".replace(",", " "),
                        "client_name": c_name,
                        "client_contact": c_tg
                    })
                    save_data(orders, DB_ORDERS)
                    st.session_state.cart = []
                    st.balloons()
                    st.success("✨ Заявка принята! Директор свяжется с вами в Telegram для подтверждения предоплаты.")
                    time.sleep(1.5)
                    st.rerun()
       else: st.error("⚠️ Заполните Имя и Telegram!")
st.write("---")
# ================= КАБИНЕТ ДИРЕКТОРА VAMYR (ЗАПАРОЛЕНО) =================
st.markdown('### 🔒 Закрытый док генерального директора')
if pass_input == ADMIN_PASSWORD:
    st.success("🔓 Капитан Longer, добро пожаловать в управление верфью VamyR!")
    # --- Управление витриной моделей ---
    with st.expander("📦 Панель управления витриной (Добавить/Удалить корабль)"):
        st.subheader("🆕 Опубликовать новое судно")
        new_name = st.text_input("Название корабля:", placeholder="Например: Линкор 'Виктория'")
        new_price_text = st.text_input("Цена корабля (текстом):", placeholder="Например: 300 грн")
        new_desc = st.text_area("Описание модели:")
        new_img = st.text_input("Ссылка на фотографию корабля (URL):")
        new_status = st.selectbox("Текущий статус готовности:", ["Планируется...", "В разработке...", "Выставлен..."])
        new_stock = st.number_input("Количество штук на складе (для статуса 'Выставлен...'):", min_value=1, value=1)
        
        if st.button("🚀 ВЫПУСТИТЬ КОРАБЛЬ НА ВИТРИНУ", use_container_width=True):
            if new_name and new_price_text and new_desc:
                img_to_save = new_img if new_img else "https://unsplash.com"
                ships.append({
                    "name": new_name, 
                    "price": new_price_text, 
                    "desc": new_desc, 
                    "img": img_to_save, 
                    "status": new_status,
                    "stock": int(new_stock)
                })
                save_data(ships, DB_SHIPS)
                st.success(f"🎉 Модель '{new_name}' успешно добавлена!")
                time.sleep(1)
                st.rerun()
            else: st.error("⚠️ Заполните все обязательные поля!")
                
        st.write("---")
        st.subheader("🗑️ Снятие моделей с продажи")
        if ships:
            ship_to_delete = st.selectbox("Выбери корабль для удаления:", range(len(ships)), format_func=lambda x: ships[x]["name"])
            if st.button("❌ УДАЛИТЬ С САЙТА", use_container_width=True):
                ships.pop(ship_to_delete)
                save_data(ships, DB_SHIPS)
                st.success("🗑️ Модель успешно удалена с витрины.")
                time.sleep(1)
                st.rerun()

    # --- База заказов клиентов ---
    st.write("---")
    st.subheader("📋 Журнал active заказов:")
    if not orders:
        st.info("В данный момент новых заказов нет. Верфь ожидает клиентов! 🌊")
    else:
        for o_idx, ord in enumerate(orders):
            with st.container(border=True):
                st.markdown(f"### Заказ №{o_idx+1} <span style='font-size:14px;color:#a1a1aa;'>({ord['time']})</span>", unsafe_allow_html=True)
                st.markdown(f"""
                * 🚢 **Заявленные товары:** {ord['ship']}
                * 💰 **Итоговая стоимость:** `{ord['price']}`
                * 🛡️ **Размер страховой предоплаты:** `{ord.get('downpayment', '0 грн')}`
                * 👤 **ФИО Клиента:** {ord['client_name']}
                * ✈️ **Telegram для связи:** `{ord['client_contact']}`
                """)
            
        if st.button("🗑️ ПОЛНОСТЬЮ ОЧИСТИТЬ ЖУРНАЛ ЗАКАЗОВ", use_container_width=True):
            orders = []
            save_data(orders, DB_ORDERS)
            st.success("Журнал заказов успешно очищен!")
            time.sleep(1)
            st.rerun()
            
elif pass_input: 
    st.error("❌ Доступ заблокирован. Неверный пароль директора верфи VamyR!")

st.write("---")

# --- ВИТРИНА ДЛЯ ПОКУПАТЕЛЕЙ (ОТКРЫТА ВСЕГДА) ---
st.markdown('## 🛒 Эксклюзивная витрина моделей')

for idx, ship in enumerate(ships):
    # Открываем контейнер
    with st.container(border=False):
        # ИСПРАВЛЕНО: Картинка выносится за рамки CSS-конфликта и теперь отображается ВСЕГДА!
        st.image(ship["img"], use_container_width=True)
        
        status = ship.get("status", "Выставлен...")
        stock = ship.get("stock", 1)
        
        if status == "Планируется...":
            st.markdown("<span style='color:#a1a1aa; font-weight:700;'>⏳ СТАТУС: Планируется к сборке (Доступен предзаказ)</span>", unsafe_allow_html=True)
            btn_label = "📬 Оставить предзаказ на модель"
            disabled_btn = False
        elif status == "В разработке...":
            st.markdown("<span style='color:#f59e0b; font-weight:700;'>🛠️ СТАТУС: Находится на стапелях в разработке</span>", unsafe_allow_html=True)
            btn_label = "📬 Оставить предзаказ на модель"
            disabled_btn = False
        elif status == "Продано":
            st.markdown("<span style='color:#ef4444; font-weight:700;'>❌ СТАТУС: ЭКЗЕМПЛЯР ПРОДАН (Нет в наличии)</span>", unsafe_allow_html=True)
            btn_label = "🔒 Изделие распродано"
            disabled_btn = True
        else:
            st.markdown(f"<span style='color:#22c55e; font-weight:700;'>✅ СТАТУС: В наличии на верфи — {stock} шт.</span>", unsafe_allow_html=True)
            btn_label = "🛒 Добавить изделие в корзину"
            disabled_btn = False
            
        col_title, col_price = st.columns(2)
        with col_title: 
            st.markdown(f"### {ship['name']}")
        with col_price: 
            st.markdown(f"<h4 style='text-align:right;color:#eab308;margin:0;'>{ship['price']}</h4>", unsafe_allow_html=True)
            
        st.markdown(f"<p style='color:#d1d5db;'>{ship['desc']}</p>", unsafe_allow_html=True)
        
        if st.button(btn_label, key=f"add_cart_{idx}", use_container_width=True, disabled=disabled_btn):
            try:
                only_digits = "".join([char for char in ship["price"] if char.isdigit()])
                parsed_price = int(only_digits) if only_digits else 0
            except: parsed_price = 0
            
            if status != "Выставлен..." and status != "Продано":
                parsed_price += 150
                display_price = f"{parsed_price} грн (Включая наценку за индивидуальный чертеж)"
            else:
                display_price = ship["price"]
                
            st.session_state.cart.append({
                "name": ship["name"], 
                "price": display_price, 
                "price_int": parsed_price, 
                "status": status,
                "orig_idx": idx
            })
            st.toast(f"✅ {ship['name']} добавлен в корзину!")
            time.sleep(0.5)
            st.rerun()

st.write("---")
st.markdown('<div class="sub-title" style="font-size:12px !important; text-align:center;">© 2026 VamyR Premium Inc. Все права защищены. Конструкторское бюро Longer.</div>', unsafe_allow_html=True)
 Telegram!")
        with col_clear:
            if st.button("🗑️ ОЧИСТИТЬ КОРЗИНУ", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

st.write("---")
