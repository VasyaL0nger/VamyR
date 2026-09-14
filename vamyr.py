import streamlit as st
import json
import os
import time

st.set_page_config(page_title="VamyR — Мини-Корабли", layout="centered", page_icon="🚢")

DB_SHIPS = "db_ships.json"
DB_ORDERS = "db_orders.json"
ADMIN_PASSWORD = "vamyradmin777"  # ТВОЙ ПАРОЛЬ ДЛЯ ПРОСМОТРА ЗАКАЗОВ

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

# Инициализация корзины в памяти сессии
if "cart" not in st.session_state:
    st.session_state.cart = []

# Стартовый контент
if not ships:
    ships = [
        {
            "name": "⚓ Галеон 'Чёрная Жемчужина'",
            "price": "3500 грн",
            "desc": "Детализированная mini-модель пиратского корабля. Сделан из дерева, паруса из плотной ткани.",
            "img": "https://unsplash.com"
        }
    ]
    save_data(ships, DB_SHIPS)

# ================= СИСТЕМА КАСТОМНЫХ ТЕМ ОФОРМЛЕНИЯ VAMYR =================
st.sidebar.subheader("🎨 Сменить стиль верфи")
theme_choice = st.sidebar.radio("Выбери тему сайта:", ["🌌 По умолчанию", "🌊 Глубокое Море", "🏴‍☠️ Пиратская Гавань"], horizontal=False)

if theme_choice == "🌊 Глубокое Море":
    st.markdown("""
        <style>
        .stApp { background-color: #0b2545 !important; color: #eef4f8 !important; }
        div[data-testid="stExpander"] { background-color: #134074 !important; border: 1px solid #8da9c4 !important; }
        div[data-testid="stForm"] { background-color: #134074 !important; }
        .stButton>button { background-color: #0077b6 !important; color: white !important; border-radius: 20px !important; border: 1px solid #90e0ef !important; }
        h1, h2, h3, h4 { color: #90e0ef !important; }
        </style>
    """, unsafe_allow_html=True)
elif theme_choice == "🏴‍☠️ Пиратская Гавань":
    st.markdown("""
        <style>
        .stApp { background-color: #1c1917 !important; color: #f5f5f4 !important; font-family: 'Courier New', Courier, monospace !important; }
        div[data-testid="stExpander"] { background-color: #292524 !important; border: 1px solid #ca8a04 !important; }
        div[data-testid="stForm"] { background-color: #292524 !important; }
        .stButton>button { background-color: #854d0e !important; color: #fef08a !important; border-radius: 4px !important; border: 2px solid #ca8a04 !important; font-weight: bold !important; }
        h1, h2, h3, h4 { color: #eab308 !important; }
        code { color: #fef08a !important; background-color: #44403c !important; }
        </style>
    """, unsafe_allow_html=True)

# --- ГЛАВНАЯ ШАПКА САЙТА VAMYR ---
st.title("🚢 VamyR — Мастерская Mini-Кораблей")
st.markdown("### *Эксклюзивные модели кораблей ручной работы от компании VamyR*")
st.write("---")

# --- ИНТЕРАКТИВНЫЙ БЛОК КОРЗИНЫ НАВЕРХУ СТРАНИЦЫ ---
st.subheader("🛍️ Твоя Корзина")
if not st.session_state.cart:
    st.info("Корзина пуста. Добавьте модели с витрины ниже! 🌊")
else:
    total_price = 0
    items_names = []
    
    with st.container(border=True):
        st.write("📋 Список выбранных кораблей:")
        for c_idx, cart_item in enumerate(st.session_state.cart):
            st.markdown(f"• **{cart_item['name']}** — `{cart_item['price']}`")
            total_price += cart_item['price_int']
            items_names.append(cart_item['name'])
            
        st.markdown(f"### 💰 Общая сумма: `{total_price:,} грн`".replace(",", " "))
        
        c_name = st.text_input("Ваше Имя:", key="cart_name_input")
        c_tg = st.text_input("Ваш Telegram для связи:", placeholder="@username", key="cart_tg_input")
        
        col_send, col_clear = st.columns(2)
        with col_send:
            if st.button("✅ ОФОРМИТЬ ЗАКАЗ КОРЗИНЫ", use_container_width=True):
                if c_name and c_tg:
                    orders.append({
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "ship": ", ".join(items_names),
                        "price": f"{total_price:,} грн".replace(",", " "),
                        "client_name": c_name,
                        "client_contact": c_tg
                    })
                    save_data(orders, DB_ORDERS)
                    st.session_state.cart = []
                    st.balloons()
                    st.success("✨ Отлично! Общий заказ передан генеральному директору VamyR.")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("⚠️ Введите имя и Telegram!")
        with col_clear:
            if st.button("🗑️ ОЧИСТИТЬ КОРЗИНУ", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

st.write("---")

# --- СКРЫТАЯ АДМИН-ПАНЕЛЬ (УПРАВЛЕНИЕ ОБЪЯВЛЕНИЯМИ) ---
with st.expander("🛠️ Панель управления VamyR (Добавить объявление)"):
    st.subheader("🆕 Опубликовать новый корабль на витрину")
    new_name = st.text_input("Название корабля:", placeholder="Например: Линкор 'Виктория'")
    new_price_text = st.text_input("Цена корабля (пиши просто число или с текстом):", placeholder="Например: 300 грн")
    new_desc = st.text_area("Описание модели:", placeholder="Материалы, размеры...")
    new_img = st.text_input("Ссылка на photo корабля (URL):")
    
    if st.button("🚀 ОПУБЛИКОВАТЬ ОБЪЯВЛЕНИЕ", use_container_width=True):
        if new_name and new_price_text and new_desc:
            img_to_save = new_img if new_img else "https://unsplash.com"
            
            # Добавляем объявление
            ships.append({
                "name": new_name, 
                "price": new_price_text, 
                "desc": new_desc, 
                "img": img_to_save
            })
            save_data(ships, DB_SHIPS)
            st.success(f"🎉 Корабль '{new_name}' успешно выставлен на витрину!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("⚠️ Заполните все поля поля!")
            
    st.write("---")
    st.subheader("🗑️ Удаление объявлений")
    if ships:
        ship_to_delete = st.selectbox("Выбери корабль для удаления с витрины:", range(len(ships)), format_func=lambda x: ships[x]["name"])
        if st.button("❌ УДАЛИТЬ С ВИТРИНЫ", use_container_width=True):
            deleted_name = ships[ship_to_delete]["name"]
            ships.pop(ship_to_delete)
            save_data(ships, DB_SHIPS)
            st.success(f"🗑️ '{deleted_name}' удален.")
            time.sleep(1)
            st.rerun()

st.write("---")

# --- ВИТРИНА ДЛЯ ПОКУПАТЕЛЕЙ ---
st.subheader("🛒 Модели в наличии:")

for idx, ship in enumerate(ships):
    with st.container(border=True):
        st.image(ship["img"], use_container_width=True)
        
        col_title, col_price = st.columns(2)
        with col_title: st.markdown(f"### {ship['name']}")
        with col_price: st.markdown(f"#### `{ship['price']}`")
        st.write(ship["desc"])
        
        if st.button(f"🛒 Добавить в корзину", key=f"add_cart_{idx}", use_container_width=True):
            # УМНОЕ ИЗВЛЕЧЕНИЕ ЦЕНЫ: вытаскиваем только цифры из любого текста цены
            try:
                only_digits = "".join([char for char in ship["price"] if char.isdigit()])
                parsed_price = int(only_digits) if only_digits else 0
            except:
                parsed_price = 0
                
            st.session_state.cart.append({
                "name": ship["name"], 
                "price": ship["price"], 
                "price_int": parsed_price
            })
            st.toast(f"✅ {ship['name']} добавлен в корзину!")
            time.sleep(0.5)
            st.rerun()

st.write("---")

# ================= СЕКРЕТНЫЙ СПИСОК ЗАКАЗОВ =================
st.subheader("🔒 Вход для генерального директора VamyR")
pass_input = st.text_input("Введите секретный пароль директора:", type="password")

if pass_input == ADMIN_PASSWORD:
    st.success("🔓 Доступ разрешен. База данных заказов загружена!")
    st.subheader("📋 Список активных заказов:")
    
    if not orders:
        st.info("Пока нет новых заказов. Ждем клиентов! 🌊")
    else:
        for o_idx, ord in enumerate(orders):
            st.markdown(f"""
            **Заказ №{o_idx+1}** ({ord['time']})
            *   🚢 **Выбранные товары:** {ord['ship']}
            *   💰 **Общая стоимость:** `{ord['price']}`
            *   👤 **Клиент:** {ord['client_name']}
            *   ✈️ **Telegram для связи:** `{ord['client_contact']}`
            """)
            st.write("---")
            
        if st.button("🗑️ ОЧИСТИТЬ ВСЕ ЗАКАЗЫ", use_container_width=True):
            orders = []
            save_data(orders, DB_ORDERS)
            st.success("Список заказов успешно очищен!")
            time.sleep(1)
            st.rerun()
elif pass_input:
    st.error("❌ Неверный пароль директора!")
