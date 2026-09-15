import streamlit as st
import json, os, time

st.set_page_config(page_title="VamyR Premium", layout="centered", page_icon="🚢")
DB_SHIPS, DB_ORDERS, ADMIN_PASSWORD = "db_ships.json", "db_orders.json", "vamyradmin777"

def load_data(f):
    if os.path.exists(f):
        try:
            with open(f, "r", encoding="utf-8") as file: return json.load(file)
        except: return []
    return []

def save_data(d, f):
    with open(f, "w", encoding="utf-8") as file: json.dump(d, file, ensure_ascii=False, indent=2)

# ЖЕСТКАЯ ОЧИСТКА: Если файл базы старый, сносим его принудительно, чтобы убрать тест-корабль
if not st.sidebar.get("db_cleaned", False):
    if os.path.exists(DB_SHIPS):
        try:
            os.remove(DB_SHIPS)
        except: pass
    st.sidebar("db_cleaned", value=True)

ships, orders = load_data(DB_SHIPS), load_data(DB_ORDERS)
if "cart" not in st.session_state: st.session_state.cart = []

# Премиум-стили VamyR
st.markdown("""<style>
    .stApp { background-color: #08080c !important; color: #f3f4f6 !important; font-family: sans-serif !important; }
    .main-title { font-size: 42px !important; font-weight: 800 !important; background: linear-gradient(135deg, #fef08a 0%, #ca8a04 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .sub-title { font-size: 18px !important; color: #a1a1aa !important; text-align: center; font-style: italic; margin-bottom: 30px; }
    div[data-testid="stBlock"] { background: #12121a !important; border: 1px solid #27272a !important; border-radius: 16px !important; padding: 20px !important; margin-bottom: 25px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important; }
    div[data-testid="stBlock"]:hover { border-color: #ca8a04 !important; box-shadow: 0 10px 30px rgba(202, 138, 4, 0.15) !important; }
    div[data-testid="stExpander"] { background-color: #12121a !important; border: 1px solid #27272a !important; border-radius: 12px !important; }
    .stButton>button { background: linear-gradient(135deg, #eab308 0%, #a16207 100%) !important; color: #000000 !important; font-weight: 700 !important; border: none !important; border-radius: 10px !important; padding: 12px 24px !important; width: 100% !important; }
    .stButton>button:hover { background: linear-gradient(135deg, #fef08a 0%, #eab308 100%) !important; transform: scale(1.01) !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton>button { background: #27272a !important; color: #ef4444 !important; border: 1px solid #44403c !important; }
    input, textarea { background-color: #181825 !important; color: white !important; border: 1px solid #3f3f46 !important; border-radius: 8px !important; }
</style>""", unsafe_allow_html=True)

# Боковое меню с логотипом
st.sidebar.markdown("### 🏢 Бренд VamyR")
if os.path.exists("logo.png"): st.sidebar.image("logo.png", use_container_width=True)
else: st.sidebar.markdown("<h2 style='color:#eab308; text-align:center;'>🚢 VamyR</h2>", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚢 VamyR Premium</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Эксклюзивные модели кораблей ручной работы от конструкторского бюро VamyR</div>', unsafe_allow_html=True)

# Корзина заказа
st.subheader("🛍️ Твоя Корзина заказа")
if not st.session_state.cart: st.info("Ваша корзина пуста. Добавьте модели с витрины ниже!")
else:
    total_price, items_names = 0, []
    with st.container(border=True):
        for c_idx, cart_item in enumerate(st.session_state.cart):
            st.markdown(f"• **{cart_item['name']}** ({cart_item['status']}) — `{cart_item['price']}`")
            total_price += cart_item['price_int']
            items_names.append(f"{cart_item['name']} [{cart_item['status']}]")
        final_sum, downpayment = total_price + 150, int(total_price * 0.20)
        st.markdown(f"**Стоимость моделей:** {total_price:,} грн | Упаковка + Доставка: 150 грн")
        st.markdown(f"### 💰 Финальная сумма к оплате: `{final_sum:,} грн`".replace(",", " "))
        st.error(f"⚠️ **Предоплата на материалы:** {downpayment:,} грн (20%). Остаток — при получении в руки!")
        c_name = st.text_input("Введите Ваше Имя:", key="cart_name_input")
        c_tg = st.text_input("Укажите Ваш Telegram для связи:", placeholder="@username", key="cart_tg_input")
        col_send, col_clear = st.columns(2)
        with col_send:
            if st.button("✅ ОФОРМИТЬ ОБЩИЙ ЗАКАЗ", use_container_width=True):
                if c_name and c_tg:
                    for cart_item in st.session_state.cart:
                        orig_idx = cart_item["orig_idx"]
                        if orig_idx < len(ships) and ships[orig_idx]["status"] == "Выставлен...":
                            ships[orig_idx]["stock"] = max(0, ships[orig_idx].get("stock", 1) - 1)
                            if ships[orig_idx]["stock"] == 0: ships[orig_idx]["status"] = "Продано"
                    save_data(ships, DB_SHIPS)
                    orders.append({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "ship": ", ".join(items_names), "price": f"{final_sum:,} грн", "downpayment": f"{downpayment:,} грн", "client_name": c_name, "client_contact": c_tg})
                    save_data(orders, DB_ORDERS)
                    st.session_state.cart = []
                    st.balloons()
                    st.success("✨ Заявка принята! Директор свяжется с вами.")
                    time.sleep(1.5)
                    st.rerun()
                else: st.error("⚠️ Заполните Имя и Telegram!")
        with col_clear:
            if st.button("🗑️ ОЧИСТИТЬ КОРЗИНУ", use_container_width=True): st.session_state.cart = []; st.rerun()

st.write("---")
st.markdown('### 🔒 Закрытый док генерального директора')
pass_input = st.text_input("Введите секретный пароль:", type="password", key="main_admin_pass")

if pass_input == ADMIN_PASSWORD:
    st.success("🔓 Капитан Longer, добро пожаловать!")
    with st.expander("📦 Панель управления витриной"):
        new_name = st.text_input("Название корабля:")
        new_price_text = st.text_input("Цена корабля (пиши просто число, например 300):")
        new_desc = st.text_area("Описание модели:")
        new_img = st.text_input("Ссылка на фото (URL):")
        new_status = st.selectbox("Статус:", ["Планируется...", "В разработке...", "Выставлен..."])
        new_stock = st.number_input("Количество штук:", min_value=1, value=1)
        if st.button("🚀 ВЫПУСТИТЬ КОРАБЛЬ НА ВИТРИНУ"):
            if new_name and new_price_text and new_desc:
                img_to_save = new_img if new_img else "https://unsplash.com"
                ships.append({"name": new_name, "price": f"{new_price_text} грн", "desc": new_desc, "img": img_to_save, "status": new_status, "stock": int(new_stock)})
                save_data(ships, DB_SHIPS); st.success("🎉 Успешно добавлено!"); time.sleep(1); st.rerun()
            else: st.error("⚠️ Заполните поля!")
        if ships:
            ship_to_delete = st.selectbox("Выбери корабль для удаления:", range(len(ships)), format_func=lambda x: ships[x]["name"])
            if st.button("❌ УДАЛИТЬ С САЙТА"): ships.pop(ship_to_delete); save_data(ships, DB_SHIPS); st.success("🗑️ Удалено."); time.sleep(1); st.rerun()
    st.subheader("📋 Журнал активных заказов:")
    if not orders: st.info("Новых заказов нет.")
    else:
        for o_idx, ord in enumerate(orders):
            with st.container(border=True): st.markdown(f"**Заказ №{o_idx+1}** ({ord['time']})\n* Товары: {ord['ship']}\n* Цена: `{ord['price']}`\n* Предоплата: `{ord.get('downpayment', '0 грн')}`\n* Клиент: {ord['client_name']} | Telegram: `{ord['client_contact']}`")
        if st.button("🗑️ ПОЛНОСТЬЮ ОЧИСТИТЬ ЖУРНАЛ ЗАКАЗОВ"): orders = []; save_data(orders, DB_ORDERS); st.rerun()
elif pass_input: st.error("❌ Неверный пароль!")

st.write("---")
st.markdown('## 🛒 Эксклюзивная витрина моделей')

if not ships:
    st.info("⚓ Витрина пуста. Введите пароль директора выше и выставьте свой первый корабль по новой системе!")
else:
    for idx, ship in enumerate(ships):
        with st.container(border=False):
            st.image(ship["img"], use_container_width=True)
            status, stock = ship.get("status", "Выставлен..."), ship.get("stock", 1)
            already_in_cart = sum(1 for item in st.session_state.cart if item.get("orig_idx") == idx)
            
            if status == "Планируется...": 
                st.markdown("<span style='color:#a1a1aa; font-weight:700;'>⏳ СТАТУС: Планируется к сборке</span>", unsafe_allow_html=True)
                btn_label, disabled_btn = "📬 Оставить предзаказ", False
            elif status == "В разработке...": 
                st.markdown("<span style='color:#f59e0b; font-weight:700;'>🛠️ СТАТУС: На стапелях в разработке</span>", unsafe_allow_html=True)
                btn_label, disabled_btn = "📬 Оставить предзаказ", False
            elif status == "Продано" or stock <= 0: 
                st.markdown("<span style='color:#ef4444; font-weight:700;'>❌ СТАТУС: ЭКЗЕМПЛЯР ПРОДАН</span>", unsafe_allow_html=True)
                btn_label, disabled_btn = "🔒 Распродано", True
            elif already_in_cart >= stock:
                st.markdown(f"<span style='color:#eab308; font-weight:700;'>⚠️ СТАТУС: В наличии {stock} шт. (Весь доступный остаток уже в твоей корзине!)</span>", unsafe_allow_html=True)
                btn_label, disabled_btn = "🚫 Достигнут лимит склада", True
            else: 
                st.markdown(f"<span style='color:#22c55e; font-weight:700;'>✅ СТАТУС: В наличии на верфи — {stock - already_in_cart} шт.</span>", unsafe_allow_html=True)
                btn_label, disabled_btn = "🛒 Добавить в корзину", False
                
            col_title, col_price = st.columns(2)
            with col_title: st.markdown(f"### {ship['name']}")
            with col_price: 
                st.markdown(f"{ship['price']}", unsafe_allow_html=True)
            st.markdown(f"{ship['desc']}", unsafe_allow_html=True)
            
            if st.button(btn_label, key=f"add_cart_{idx}", use_container_width=True, disabled=disabled_btn):
                try:
                    only_digits = "".join([c for c in ship["price"] if c.isdigit()])
                    parsed_price = int(only_digits) if only_digits else 0
                except: 
                    parsed_price = 0
                display_price = f"{parsed_price+150} грн (Включая наценку)" if status != "Выставлен..." and status != "Продано" else ship["price"]
                st.session_state.cart.append({"name": ship["name"], "price": display_price, "price_int": parsed_price, "status": status, "orig_idx": idx})
                st.toast(f"✅ Добавлено!")
                time.sleep(0.5)
                st.rerun()
st.write("---")
st.markdown('© 2026 VamyR Premium Inc. Конструкторское бюро Longer.', unsafe_allow_html=True)
