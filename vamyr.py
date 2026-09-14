import streamlit as st
import json
import os

st.set_page_config(page_title="VamyR — Мини-Корабли", layout="centered", page_icon="🚢")

DB_SHIPS = "db_ships.json"

# Функция загрузки базы объявлений
def load_ships():
    if os.path.exists(DB_SHIPS):
        try:
            with open(DB_SHIPS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# Функция сохранения базы объявлений
def save_ships(data):
    with open(DB_SHIPS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

ships = load_ships()

# Стартовый контент, чтобы сайт не был пустым при первом запуске
if not ships:
    ships = [
        {
            "name": "⚓ Галеон 'Чёрная Жемчужина'",
            "price": "3,500 грн",
            "desc": "Детализированная мини-модель пиратского корабля. Сделан из дерева, паруса из плотной ткани.",
            "img": "https://unsplash.com"
        }
    ]
    save_ships(ships)

# --- ГЛАВНАЯ ШАПКА САЙТА VAMYR ---
st.title("🚢 VamyR — Мастерская Мини-Кораблей")
st.markdown("### *Эксклюзивные модели кораблей ручной работы от компании VamyR*")
st.write("---")

# --- СКРЫТАЯ АДМИН-ПАНЕЛЬ ДЛЯ ТЕБЯ ---
with st.expander("🛠️ Панель управления VamyR (Добавить объявление)"):
    st.subheader("🆕 Опубликовать новый корабль на витрину")
    new_name = st.text_input("Название корабля:", placeholder="Например: Линкор 'Виктория'")
    new_price = st.text_input("Цена:", placeholder="Например: 1,500 грн")
    new_desc = st.text_area("Описание модели:", placeholder="Материалы, размеры, особенности работы...")
    new_img = st.text_input("Ссылка на фото корабля (URL):", placeholder="Вставь ссылку на фотографию")
    
    if st.button("🚀 ОПУБЛИКОВАТЬ ОБЪЯВЛЕНИЕ", use_container_width=True):
        if new_name and new_price and new_desc:
            img_to_save = new_img if new_img else "https://unsplash.com"
            ships.append({
                "name": new_name,
                "price": new_price,
                "desc": new_desc,
                "img": img_to_save
            })
            save_ships(ships)
            st.success(f"🎉 Корабль '{new_name}' успешно выставлен на витрину!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("⚠️ Заполните Название, Цену и Описание!")

st.write("---")

# --- ВИТРИНА ДЛЯ ПОКУПАТЕЛЕЙ ---
st.subheader("🛒 Модели в наличии:")

for idx, ship in enumerate(ships):
    with st.container(border=True):
        # Отображение фотографии корабля
        st.image(ship["img"], use_container_width=True)
        
        # Название и цена
        col_title, col_price = st.columns([3, 1])
        with col_title:
            st.markdown(f"### {ship['name']}")
        with col_price:
            st.markdown(f"#### `{ship['price']}`")
            
        st.write(ship["desc"])
        
        # Кнопка покупки
        if st.button(f"🛍️ Заказать {ship['name']}", key=f"order_{idx}", use_container_width=True):
            st.balloons()
            st.success("✨ Заявка принята! Компания VamyR свяжется с вами для подтверждения заказа.")

st.write("---")
st.caption("© 2026 VamyR Inc. Все права защищены. Сделано с любовью к морю.")
