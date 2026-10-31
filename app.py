import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="PMIS Híbrido — Torres del Parque", layout="wide", initial_sidebar_state="expanded")

st.title("🏗️ PMIS Híbrido: Control Predictivo & Ágil de Obra")
st.caption("Caso de Sustentación PMP — Grupo 5 | Integración EVM (PMBOK) y Flujo Ágil / Kanban")

# ==============================================================================
# 1. BASE DE DATOS Y ESTADO DE SESIÓN (INICIALIZACIÓN LIMPIA)
# ==============================================================================
if 'historias' not in st.session_state:
    st.session_state.historias = [
        {
            "id": "H21",
            "epica": "E1 Registro",
            "titulo": "Como residente quiero registrar una no conformidad con foto para documentarla en el sitio",
            "puntos": 5,
            "estado": "Hecho",
            "responsable": "Ana María · Planificación",
        },
        {
            "id": "H22",
            "epica": "E1 Registro",
            "titulo": "Como residente quiero marcar la ubicación en el plano del piso para localizar el hallazgo",
            "puntos": 5,
            "estado": "Hecho",
            "responsable": "Ana María · Planificación",
        },
        {
            "id": "H23",
            "epica": "E2 Offline",
            "titulo": "Como residente quiero trabajar sin conexión para no perder datos en el sótano",
            "puntos": 5,
            "estado": "En revisión",
            "responsable": "Michael · Cierre",
        },
        {
            "id": "H24",
            "epica": "E3 Seguimiento",
            "titulo": "Como inspector quiero asignar la no conformidad a un contratista para que la corrija",
            "puntos": 5,
            "estado": "En curso",
            "responsable": "Brayan Nicolás · Ejecución",
        },
        {
            "id": "H25",
            "epica": "E3 Seguimiento",
            "titulo": "Como director de obra quiero recibir un correo cuando se cierre un hallazgo crítico",
            "puntos": 3,
            "estado": "En curso",
            "responsable": "Fernando · Inicio",
        },
        {
            "id": "H26",
            "epica": "E3 Seguimiento",
            "titulo": "Como inspector quiero cerrar un hallazgo con foto de evidencia para liberar el área",
            "puntos": 3,
            "estado": "En curso",
            "responsable": "Brayan Nicolás · Ejecución",
        },
        {
            "id": "H27",
            "epica": "E4 Reportes",
            "titulo": "Como director quiero ver un tablero con hallazgos abiertos por contratista",
            "puntos": 2,
            "estado": "Por hacer",
            "responsable": "Yeison Ramón · Sustentación",
        },
        {
            "id": "H28",
            "epica": "E5 Administración",
            "titulo": "Como administrador quiero crear usuarios y roles para controlar el acceso",
            "puntos": 2,
            "estado": "Por hacer",
            "responsable": "Astrid Tatiana · Cambio",
        },
    ]

# ==============================================================================
# 2. BARRA LATERAL: CONTROL DE PROYECTOS Y LÍMITES ÁGILES
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Portafolio y Configuración")
    proyecto_activo = st.selectbox("Proyecto Seleccionado:", ["Torres del Parque (Construcción + App Móvil)"])
    
    st.markdown("---")
    st.subheader("🎯 Gobernanza Ágil")
    wip_limit = st.slider("Límite WIP en «En curso»:", min_value=1, max_value=5, value=3)
    
    st.markdown("---")
    if st.button("🔄 Reiniciar Datos a Estado Inicial"):
        del st.session_state.historias
        st.rerun()

# ==============================================================================
# 3. COMPONENTE ÁGIL: SPRINT & TABLERO KANBAN
# ==============================================================================
st.subheader("📱 Componente Adaptativo: App Móvil de Inspección («ObraCheck»)")
st.write("Demo de clase · Sprint 5 de 1 semana (lunes a sábado)")

col_dia, col_btn = st.columns([4, 1])
with col_dia:
    dia_sprint = st.slider("Día del sprint:", min_value=1, max_value=6, value=3, format="Día %d de 6")
with col_btn:
    st.write("")
    st.write("")
    if st.button("▶ Simular el sprint"):
        st.info("Simulación de avance de historias ejecutada.")

st.info("🎯 **Meta del Sprint 5:** «Un residente puede registrar una no conformidad con foto y ubicación, asignarla y cerrarla desde el celular, aunque no haya señal»")

# Cálculo de Métricas Ágiles
total_pts = sum(h["puntos"] for h in st.session_state.historias)
hechos_pts = sum(h["puntos"] for h in st.session_state.historias if h["estado"] == "Hecho")
en_curso_pts = sum(h["puntos"] for h in st.session_state.historias if h["estado"] == "En curso")
en_curso_count = sum(1 for h in st.session_state.historias if h["estado"] == "En curso")
restante_pts = total_pts - hechos_pts

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Compromiso", f"{total_pts} pts", f"{len(st.session_state.historias)} historias")
m2.metric("Terminado", f"{hechos_pts} pts", f"{(hechos_pts/total_pts)*100:.0f}% cumplido")
m3.metric("Restante", f"{restante_pts} pts", f"Ideal hoy: {total_pts - (total_pts/6)*dia_sprint:.1f}")
m4.metric("WIP", f"{en_curso_count}", f"Límite: {wip_limit}")
m5.metric("Impedimentos", "0", "Ninguno abierto")
m6.metric("Sprints restantes", "≈ 3", "Vel. promedio: 29")

# Alerta de límite WIP
if en_curso_count > wip_limit:
    st.error(f"⚠️ **¡Alerta de Cuello de Botella!** La columna «En curso» tiene {en_curso_count} tareas, superando el límite WIP fijado de {wip_limit}.")

st.markdown("### Tablero Kanban — Sprint Backlog")

columnas_kanban = ["Por hacer", "En curso", "En revisión", "Hecho"]
col_k1, col_k2, col_k3, col_k4 = st.columns(4)
cols_map = {"Por hacer": col_k1, "En curso": col_k2, "En revisión": col_k3, "Hecho": col_k4}

for estado in columnas_kanban:
    with cols_map[estado]:
        items_estado = [h for h in st.session_state.historias if h["estado"] == estado]
        pts_estado = sum(h["puntos"] for h in items_estado)
        st.markdown(f"**{estado.upper()}** ({len(items_estado)} · {pts_estado} PTS)")
        
        for idx, historia in enumerate(st.session_state.historias):
            if historia["estado"] == estado:
                with st.container(border=True):
                    st.caption(f"{historia['id']} · {historia['epica']}")
                    st.write(f"**{historia['titulo']}**")
                    st.markdown(f"👤 `{historia['responsable']}` | ⚖️ **{historia['puntos']} pts**")
                    
                    # Controles de avance entre columnas
                    c_izq, c_der = st.columns(2)
                    pos_actual = columnas_kanban.index(estado)
                    if pos_actual > 0:
                        if c_izq.button("◀", key=f"btn_izq_{historia['id']}"):
                            st.session_state.historias[idx]["estado"] = columnas_kanban[pos_actual - 1]
                            st.rerun()
                    if pos_actual < len(columnas_kanban) - 1:
                        if c_der.button("▶", key=f"btn_der_{historia['id']}"):
                            st.session_state.historias[idx]["estado"] = columnas_kanban[pos_actual + 1]
                            st.rerun()

st.markdown("---")

# ==============================================================================
# 4. COMPONENTE PREDICTIVO: CURVA S & GESTIÓN DEL VALOR GANADO (EVM)
# ==============================================================================
st.subheader("🏗️ Componente Predictivo: Control de Obra Civil (EVM & Curva S)")

BAC = 1000.0
PV_serie = [50, 120, 220, 350, 500, 650, 780, 880, 950, 1000]
mes_corte = 5
PV = float(PV_serie[mes_corte - 1])
EV = 400.0
AC = 450.0

CV = EV - AC
SV = EV - PV
CPI = EV / AC
SPI = EV / PV
EAC = BAC / CPI
VAC = BAC - EAC
TCPI = (BAC - EV) / (BAC - AC)

# Semáforo de Gobernanza
if CPI >= 1.0 and SPI >= 1.0:
    st.success("🟢 **SEMÁFORO VERDE:** Proyecto en equilibrio o ahorro.")
elif CPI >= 0.90 and SPI >= 0.90:
    st.warning("🟡 **SEMÁFORO AMARILLO:** Alerta preventiva en costos o cronograma.")
else:
    st.error(f"🔴 **SEMÁFORO ROJO: Desviación Crítica** (CPI: {CPI:.2f} | SPI: {SPI:.2f}). Se requiere trámite formal de cambio ante el Comité de Obra.")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Eficiencia Costo (CPI)", f"{CPI:.2f}", f"CV: {CV:+.0f} M COP")
k2.metric("Eficiencia Cronograma (SPI)", f"{SPI:.2f}", f"SV: {SV:+.0f} M COP")
k3.metric("Estimado al Cierre (EAC)", f"${EAC:,.0f} M", f"VAC: {VAC:+.0f} M COP")
k4.metric("Desempeño Restante (TCPI)", f"{TCPI:.2f}", "Meta: BAC ($1,000 M)")

# Gráfica Curva S
meses = [f"Mes {i}" for i in range(1, 11)]
ev_serie = [PV_serie[i] * (EV / PV) for i in range(mes_corte)]
ac_serie = [PV_serie[i] * (AC / PV) for i in range(mes_corte)]

fig = go.Figure()
fig.add_trace(go.Scatter(x=meses, y=PV_serie, mode='lines+markers', name='Valor Planificado (PV)', line=dict(color='gray', dash='dash')))
fig.add_trace(go.Scatter(x=meses[:mes_corte], y=ev_serie, mode='lines+markers', name='Valor Ganado (EV)', line=dict(color='#2563eb', width=3)))
fig.add_trace(go.Scatter(x=meses[:mes_corte], y=ac_serie, mode='lines+markers', name='Costo Real (AC)', line=dict(color='#dc2626', width=3)))

fig.update_layout(
    title="Curva S Acumulada de Desempeño — Obra Civil Torres del Parque",
    xaxis_title="Mes de Control",
    yaxis_title="COP Millones",
    template="plotly_white",
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# Acciones de Gobernanza
st.markdown("### 🛠️ Gobernanza y Respuestas Prescriptivas")
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("⚡ Simular Crashing / Fast-tracking"):
        st.warning("Compresión evaluada: doblar turno en cuadrillas de estructura para recuperar holgura negativa.")
with b2:
    if st.button("🛡️ Liberar Reserva de Contingencia"):
        st.info("Reserva solicitada: asignación para fluctuación de precios de acero y concreto.")
with b3:
    if st.button("📑 Emitir Acta de Comité Directivo"):
        st.success("Acta consolidada lista para firma de la Junta y la fiduciaria.")
