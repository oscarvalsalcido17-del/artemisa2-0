import streamlit as st
import pandas as pd
import os

# =========================
# 🎨 Estilos personalizados con paleta floral más oscura y texto negro
# =========================
st.markdown("""
<style>
    /* Tipografías */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
        color: #000000; /* Texto negro para máxima legibilidad */
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #5E2A3B; /* Rosa malva más oscuro */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }

    /* Fondo principal más oscuro */
    [data-testid="stAppViewContainer"] {
        background-color: #EED6D3; /* Rosa empolvado más oscuro */
        color: #000000;
    }

    /* Sidebar más oscuro */
    [data-testid="stSidebar"] {
        background-color: #E6B8B0; /* Rosa pastel más intenso */
        color: #000000;
    }

    /* Tablas */
    table {
        background-color: #ffffff;
        border-radius: 8px;
        overflow: hidden;
    }

    th {
        background-color: #8B4B5E; /* Encabezado rosa malva oscuro */
        color: white !important;
    }

    td {
        color: #000000 !important; /* Texto negro en celdas */
    }

    /* Botones */
    button[kind="primary"] {
        background-color: #7FAF8B !important; /* Verde eucalipto más oscuro */
        color: white !important;
        border-radius: 8px;
        border: none;
    }
    button[kind="primary"]:hover {
        background-color: #6B9E78 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 🌸 Logo centrado
# =========================
logo_path = "logo.png"
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo_path, use_container_width=False, width=150)
else:
    st.warning("⚠ No se encontró el archivo 'logo.png' en la carpeta del proyecto.")

# 📦 Catálogo de productos
productos = {
    "Rosa": 30,
    "Lisianthus": 40,
    "Clavel": 20,
    "Margarita": 20,
    "Mini rosa": 35,
    "Tulipan": 100,
    "Hortencia": 200,
    "Gerbera": 40,
    "Mini gerbera": 45,
    "Ranunculos": 120,
    "Anemona": 120,
    "delphinum": 75,
    "Perrito": 25,
    "Roxana": 30,
    "Eucalipto": 10,
    "Miller": 25,
    "Encaje": 30,
    "Escabriosa": 30,
    "Craspedia": 30,
    "Girasol": 75,
    "Rosa Inglesa": 75,
    "Rosa Ohara": 35
}
productos = dict(sorted(productos.items(), key=lambda x: x[0]))

# =========================
# 📌 Inicializar pedido en session_state
# =========================
if "pedido" not in st.session_state:
    st.session_state.pedido = {}

# 🏷 Encabezado
st.title("🌷 Artemisa Florería")
st.write("""
Bienvenido a **Artemisa Florería**.  
Usa el panel lateral para elegir las flores y cantidades que deseas cotizar.  
Tu resumen de pedido y el total aparecerán aquí.
""")

# =========================
# ✨ Apartado para promociones/paquetes
# =========================
st.sidebar.subheader("Promociones y Paquetes")
promociones_texto = st.sidebar.text_area(
    "Escribe aquí las promociones o paquetes disponibles",
    placeholder="Ejemplo:\n- Ramo de 12 rosas por $300\n- Combo margaritas + gerberas $150"
)

if promociones_texto.strip():
    st.subheader("🌟 Promociones y Paquetes")
    st.markdown(promociones_texto)

# 📋 Mostrar catálogo
st.subheader("Catálogo de flores")
df_catalogo = pd.DataFrame({
    "Flor": list(productos.keys()),
    "Precio (MXN)": list(productos.values())
})
df_catalogo["Precio (MXN)"] = df_catalogo["Precio (MXN)"].apply(lambda x: f"${x:,.2f}")
st.dataframe(df_catalogo, use_container_width=True)

# 🛒 Panel lateral: pedido
st.sidebar.header("Tu pedido")
for flor, precio in productos.items():
    cantidad = st.sidebar.number_input(
        label=f"{flor} (MXN {precio})",
        min_value=0,
        max_value=100,
        value=st.session_state.pedido.get(flor, {}).get("cantidad", 0),
        step=1
    )
    if cantidad > 0:
        st.session_state.pedido[flor] = {
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": cantidad * precio
        }
    elif flor in st.session_state.pedido:
        del st.session_state.pedido[flor]

# Botón para limpiar pedido
if st.sidebar.button("🗑 Limpiar pedido"):
    st.session_state.pedido.clear()
    st.rerun()

# 📊 Resumen y total
if st.session_state.pedido:
    st.subheader("Resumen de tu pedido")
    df_pedido = pd.DataFrame.from_dict(st.session_state.pedido, orient="index").reset_index().rename(columns={
        "index": "Flor",
        "cantidad": "Cantidad",
        "precio_unitario": "Precio unitario (MXN)",
        "subtotal": "Subtotal (MXN)"
    })
    df_pedido["Precio unitario (MXN)"] = df_pedido["Precio unitario (MXN)"].apply(lambda x: f"${x:,.2f}")
    df_pedido["Subtotal (MXN)"] = df_pedido["Subtotal (MXN)"].apply(lambda x: f"${x:,.2f}")
    st.table(df_pedido.set_index("Flor"))

    total = sum(item["subtotal"] for item in st.session_state.pedido.values())
    st.markdown(f"## 💰 Total: ${total:,.2f} MXN")
    st.sidebar.markdown(f"### 💰 Total: ${total:,.2f} MXN")
else:
    st.info("Aún no has seleccionado ninguna flor.")
