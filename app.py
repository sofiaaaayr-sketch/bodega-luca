import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Bodega Luca", page_icon="📦")

# Cargar archivos
inventario = pd.read_csv("inventario.csv")
ventas = pd.read_csv("ventas.csv")

st.title("📦 Sistema de Inventario - Bodega Luca")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    ["Ver Inventario", "Registrar Venta", "Historial de Ventas"]
)

# INVENTARIO
if menu == "Ver Inventario":

    st.subheader("📋 Inventario")

    st.dataframe(inventario, use_container_width=True)

    st.metric("Productos", len(inventario))
    st.metric("Stock Total", int(inventario["Stock"].sum()))

# REGISTRAR VENTA
elif menu == "Registrar Venta":

    st.subheader("💰 Registrar Venta")

    producto = st.selectbox(
        "Seleccione producto",
        inventario["Producto"]
    )

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        step=1
    )

    if st.button("Registrar Venta"):

        fila = inventario[inventario["Producto"] == producto]

        stock_actual = int(fila["Stock"].iloc[0])
        precio = float(fila["Precio"].iloc[0])
        codigo = fila["Código"].iloc[0]

        if cantidad <= stock_actual:

            nuevo_stock = stock_actual - cantidad

            inventario.loc[
                inventario["Producto"] == producto,
                "Stock"
            ] = nuevo_stock

            total = cantidad * precio

            nueva_venta = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Código": codigo,
                "Producto": producto,
                "Cantidad": cantidad,
                "Total": total
            }])

            ventas = pd.concat(
                [ventas, nueva_venta],
                ignore_index=True
            )

            inventario.to_csv(
                "inventario.csv",
                index=False
            )

            ventas.to_csv(
                "ventas.csv",
                index=False
            )

            st.success(
                f"Venta registrada. Stock restante: {nuevo_stock}"
            )

        else:

            st.error(
                f"Stock insuficiente. Disponible: {stock_actual}"
            )

# HISTORIAL
elif menu == "Historial de Ventas":

    st.subheader("📅 Historial de Ventas")

    if len(ventas) > 0:

        st.dataframe(
            ventas,
            use_container_width=True
        )

    else:

        st.info("Aún no hay ventas registradas.")
