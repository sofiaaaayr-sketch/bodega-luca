import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Bodega Luca",
    page_icon="📦",
    layout="wide"
)

# Cargar datos
inventario = pd.read_csv("inventario.csv")
ventas = pd.read_csv("ventas.csv")

st.title("📦 SISTEMA DE INVENTARIO - BODEGA LUCA")

menu = st.sidebar.selectbox(
    "MENÚ",
    [
        "📋 Ver Inventario",
        "🔍 Buscar Producto",
        "➕ Registrar Producto",
        "💰 Registrar Venta",
        "📅 Historial de Ventas"
    ]
)

# ==========================
# INVENTARIO
# ==========================

if menu == "📋 Ver Inventario":

    st.subheader("📋 Inventario General")

    st.dataframe(
        inventario,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Productos Registrados",
            len(inventario)
        )

    with col2:
        st.metric(
            "Stock Total",
            int(inventario["Stock"].sum())
        )

# ==========================
# BUSCAR PRODUCTO
# ==========================

elif menu == "🔍 Buscar Producto":

    st.subheader("🔍 Buscar Producto")

    buscar = st.text_input(
        "Ingrese el nombre del producto"
    )

    if buscar:

        resultado = inventario[
            inventario["Producto"].str.contains(
                buscar,
                case=False,
                na=False
            )
        ]

        if len(resultado) > 0:

            st.success("Producto encontrado")

            st.dataframe(
                resultado,
                use_container_width=True
            )

        else:

            st.error("Producto no encontrado")

# ==========================
# REGISTRAR PRODUCTO
# ==========================

elif menu == "➕ Registrar Producto":

    st.subheader("➕ Registrar Nuevo Producto")

    codigo = st.text_input("Código")

    nombre = st.text_input("Nombre del producto")

    precio = st.number_input(
        "Precio",
        min_value=0.0,
        step=0.10
    )

    stock = st.number_input(
        "Stock inicial",
        min_value=0,
        step=1
    )

    if st.button("Guardar Producto"):

        nuevo = pd.DataFrame([{
            "Código": codigo,
            "Producto": nombre,
            "Precio": precio,
            "Stock": stock
        }])

        inventario = pd.concat(
            [inventario, nuevo],
            ignore_index=True
        )

        inventario.to_csv(
            "inventario.csv",
            index=False
        )

        st.success(
            "Producto registrado correctamente"
        )

# ==========================
# REGISTRAR VENTA
# ==========================

elif menu == "💰 Registrar Venta":

    st.subheader("💰 Registrar Venta")

    producto = st.selectbox(
        "Seleccione producto",
        inventario["Producto"]
    )

    cantidad = st.number_input(
        "Cantidad vendida",
        min_value=1,
        step=1
    )

    if st.button("Registrar Venta"):

        fila = inventario[
            inventario["Producto"] == producto
        ]

        stock_actual = int(
            fila["Stock"].iloc[0]
        )

        precio = float(
            fila["Precio"].iloc[0]
        )

        codigo = fila["Código"].iloc[0]

        if cantidad <= stock_actual:

            nuevo_stock = stock_actual - cantidad

            inventario.loc[
                inventario["Producto"] == producto,
                "Stock"
            ] = nuevo_stock

            total = cantidad * precio

            nueva_venta = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Código": codigo,
                "Producto": producto,
                "Cantidad": cantidad,
                "Total": round(total, 2)
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
                f"Venta registrada correctamente. Stock restante: {nuevo_stock}"
            )

            st.info(
                f"Total pagado: S/ {round(total,2)}"
            )

        else:

            st.error(
                f"Stock insuficiente. Disponible: {stock_actual}"
            )

# ==========================
# HISTORIAL
# ==========================

elif menu == "📅 Historial de Ventas":

    st.subheader("📅 Historial de Ventas")

    if len(ventas) > 0:

        st.dataframe(
            ventas,
            use_container_width=True
        )

        total_ventas = ventas["Total"].sum()

        st.metric(
            "Ingresos Totales",
            f"S/ {round(total_ventas,2)}"
        )

    else:

        st.info(
            "Aún no existen ventas registradas."
        )
