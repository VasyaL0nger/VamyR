import streamlit as st
import json
import os
import time

st.set_page_config(page_title="VamyR — Мини-Корабли", layout="centered", page_icon="🚢")

DB_SHIPS = "db_ships.json"
DB_ORDERS = "db_orders.json"
ADMIN_PASSWORD = "vamyradmin777"  # ТВОЙ СЕКРЕТНЫЙ ПАРОЛЬ ДЛЯ ПРОСМОТРА ЗАКАЗОВ (МОЖЕШЬ ИЗМЕНИТЬ)

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

# Стартовый контент
if not ships:
    ships = [
        {
            "name": "⚓ Галеон 'Чёрная Жемчужина'",
            "price": "3,500 грн",
            "desc": "Детализированная мини-модель пиратского корабля. Сделан из дерева, паруса из плотной ткани.",
            "img": "https://unsplash.com"
        }
    ]
    save_data(ships, DB_SHIPS)

# --- ГЛАВНАЯ ШАПКА САЙТА VAMYR ---
st.title("🚢 VamyR — Мастерская Мини-Кораблей")
st.markdown("### *Эксклюзивные модели кораблей ручной работы от компании VamyR*")
st.write("---")

# --- СКРЫТАЯ АДМИН-ПАНЕЛЬ (УПРАВЛЕНИЕ ОБЪЯВЛЕНИЯМИ) ---
with st.expander("🛠️ Панель управления VamyR (Добавить объявление)"):
    st.subheader("🆕 Опубликовать новый корабль на витрину")
    new_name = st.text_input("Название корабля:", placeholder="Например: Линкор 'Виктория'")
    new_price = st.text_input("Цена:", placeholder="Например: 1,500 грн")
    new_desc = st.text_area("Описание модели:", placeholder="Материалы, размеры...")
    new_img = st.text_input("Ссылка на фото корабля (URL):")
    
    if st.button("🚀 ОПУБЛИКОВАТЬ ОБЪЯВЛЕНИЕ", use_container_width=True):
        if new_name and new_price and new_desc:
            img_to_save = new_img if new_img else "https://unsplash.com"
            ships.append({"name": new_name, "price": new_price, "desc": new_desc, "img": img_to_save})
            save_data(ships, DB_SHIPS)
            st.success(f"🎉 Корабль '{new_name}' успешно выставлен на витрину!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("⚠️ Заполните Название, Цену и Описание!")
            
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
        col_title, col_price = st.columns()
        with col_title: st.markdown(f"### {ship['name']}")
        with col_price: st.markdown(f"#### `{ship['price']}`")
        st.write(ship["desc"])
        
        # Окно формы заказа для каждого корабля индивидуально под спойлером
        with st.expander(f"🛍️ Оформить заказ на {ship['name']}"):
            c_name = st.text_input("Ваше Имя:", key=f"name_{idx}")
            c_phone = st.text_input("Ваш Телефон / Telegram:", key=f"phone_{idx}")
            
            if st.button("✅ ПОДТВЕРДИТЬ ЗАКАЗ", key=f"btn_{idx}", use_container_width=True):
                if c_name and c_phone:
                    orders.append({
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "ship": ship["name"],
                        "price": ship["price"],
                        "client_name": c_name,
                        "client_contact": c_phone
                    })
                    save_data(orders, DB_ORDERS)
                    st.balloons()
                    st.success("✨ Заявка принята! Компания VamyR свяжется с вами для подтверждения заказа.")
                else:
                    st.error("⚠️ Пожалуйста, введите имя и контактные данные, чтобы мы могли связаться!")

st.write("---")

# ================= СЕКРЕТНЫЙ СПИСОК ЗАКАЗОВ ДЛЯ ТЕБЯ =================
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
            *   🚢 **Товар:** {ord['ship']} (Цена: `{ord['price']}`)
            *   👤 **Клиент:** {ord['client_name']}
            *   📞 **Контакты:** `{ord['client_contact']}`
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
