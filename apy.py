import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bodega Luca", page_icon="📦")

st.title("📦 Sistema de Inventario - Bodega Luca")

productos = [
    ["P001", "Arroz", 4.50, 20],
    ["P002", "Azúcar", 5.00, 15],
    ["P003", "Aceite", 12.50, 10],
    ["P004", "Leche", 4.20, 18],
    ["P005", "Fideos", 2.80, 25],
    ["P006", "Inca Kola 500ml", 3.50, 30],
    ["P007", "Coca Cola 500ml", 3.50, 30],
    ["P008", "Galletas Oreo", 2.00, 20],
    ["P009", "Atún en lata", 6.50, 12],
    ["P010", "Papel higiénico", 3.00, 16],
    ["P011", "Agua mineral", 1.50, 24],
    ["P012", "Chocolate Sublime", 1.50, 35],
    ["P013", "Jabón Bolívar", 2.50, 14],
    ["P014", "Detergente Bolívar", 8.00, 10],
    ["P015", "Sal de mesa", 1.20, 18]
]

df = pd.DataFrame(
    productos,
    columns=["Código", "Producto", "Precio (S/)", "Stock"]
)

st.subheader("📋 Inventario de Productos")
st.dataframe(df, use_container_width=True)

st.subheader("🔍 Buscar Producto")

buscar = st.text_input("Ingrese el nombre del producto")

if buscar:
    resultado = df[df["Producto"].str.contains(buscar, case=False)]

    if len(resultado) > 0:
        st.success("Producto encontrado")
        st.dataframe(resultado, use_container_width=True)
    else:
        st.error("Producto no encontrado")

st.subheader("📊 Resumen")

st.metric("Total de productos", len(df))
st.metric("Stock total", int(df["Stock"].sum()))

st.success("Sistema de Inventario de la Bodega Luca funcionando correctamente ✅")
