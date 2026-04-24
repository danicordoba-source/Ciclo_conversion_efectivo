"""
Aplicación Streamlit — Ciclo de conversión de efectivo (CCC)
Funcionalidad 1: controles y mensaje interpretativo.
Funcionalidad 2: gráfico Plotly en cascada alineado con la fórmula de la Func. 1.

CCC = DI + DSO - DPO
"""

import streamlit as st
import plotly.graph_objects as go

# Paleta pastel por variable (DI, DSO, DPO, CCC) — misma codificación en sliders y gráfico.
COLOR_DI = "#FFDCC4"
COLOR_DSO = "#C8EFD0"
COLOR_DPO = "#DDD0F5"
COLOR_CCC = "#C4E9FF"
BORDE_DI = "#E8955A"
BORDE_DSO = "#5CBF7A"
BORDE_DPO = "#9B7ED9"
BORDE_CCC = "#4DAFE0"


def calcular_ccc(di: int, dso: int, dpo: int) -> int:
    """Calcula el Ciclo de conversión de efectivo en días."""
    return di + dso - dpo


def mensaje_interpretacion(ccc: int) -> str:
    """
    Devuelve un texto didáctico según el signo del CCC.
    Positivo: la empresa financia el capital de trabajo con recursos propios o deuda.
    Cero: coinciden plazos de cobro, pago y permanencia en inventario.
    Negativo: se cobra antes o al ritmo de pagar proveedores (caso atípico pero posible en modelos de negocio concretos).
    """
    if ccc > 0:
        return (
            "📈 "
            f"**CCC positivo ({ccc} días):** el ciclo indica cuántos días, en conjunto, "
            "permanecen invertidos en inventario y cuentas por cobrar **antes** de que el "
            "aplazamiento a proveedores (DPO) compense ese desfase. Un CCC mayor implica "
            "más días de capital de trabajo vinculados al ciclo operativo."
        )
    if ccc == 0:
        return (
            "⚖️ "
            "**CCC igual a cero:** la suma de días de inventario y de cobro coincide con "
            "los días de pago a proveedores; no hay desfase neto en términos de la fórmula "
            "utilizada (interpretación simplificada del modelo)."
        )
    return (
        "📉 "
        f"**CCC negativo ({ccc} días):** el aplazamiento a proveedores (y/o la combinación "
        "de plazos) supera el tiempo que la empresa mantiene recursos en inventario y en "
        "cuentas por cobrar. En la práctica suele asociarse a modelos con cobros muy rápidos "
        "o fuertes condiciones de pago a proveedores; conviene contrastarlo con el contexto "
        "sectorial y la política comercial real."
    )


def panel_descripcion_sidebar() -> None:
    """Texto orientativo en el panel lateral, con jerarquía visual clara."""
    st.sidebar.markdown("## 📋 Guía de la pantalla")
    st.sidebar.markdown(
        "🎯 Use esta vista para **simular** el Ciclo de conversión de efectivo (CCC) "
        "a partir de tres magnitudes expresadas en **días**."
    )
    st.sidebar.divider()
    st.sidebar.markdown("### ✏️ Qué introduce usted")
    st.sidebar.markdown(
        "- 📦 **DI** — días de inventario: tiempo medio que el stock permanece en la empresa.\n"
        "- 📨 **DSO** — días de cuentas por cobrar: plazo medio de cobro a clientes.\n"
        "- 🧾 **DPO** — días de cuentas por pagar: plazo medio de pago a proveedores."
    )
    st.sidebar.divider()
    st.sidebar.markdown("### 🧮 Qué calcula la aplicación")
    st.sidebar.markdown(
        "**CCC = DI + DSO − DPO** (resultado en días). "
        "En el área principal verá el valor del CCC y una **interpretación** "
        "según sea positivo, cero o negativo."
    )
    st.sidebar.divider()
    st.sidebar.markdown("### 📊 Visualización")
    st.sidebar.markdown(
        "El **diagrama de cascada** recorre la fórmula **CCC = DI + DSO − DPO** "
        "paso a paso y se actualiza dinámicamente con los deslizadores."
    )
    st.sidebar.info(
        "💡 Los tres deslizadores comparten el rango **0 a 100 días**. "
        "Ajuste los valores para explorar distintos escenarios operativos."
    )
    st.sidebar.caption(
        "Colores: DI naranja · DSO verde · DPO morado · CCC celeste (pastel)."
    )


def _bloque_titulo_pastel(fondo: str, borde: str, titulo_html: str) -> None:
    """Franja con color de variable encima del control (Streamlit no colorea el riel por slider)."""
    st.markdown(
        f'<div style="background-color:{fondo}; border-left: 5px solid {borde}; '
        f"padding: 10px 14px; border-radius: 8px; margin-bottom: 6px;\">{titulo_html}</div>",
        unsafe_allow_html=True,
    )


def _slider_variable_pastel(
    *,
    key: str,
    fondo: str,
    borde: str,
    titulo_html: str,
    ayuda: str,
    valor_default: int,
) -> int:
    """Slider con franja vertical del mismo tono que la barra en el gráfico (días ingresados)."""
    col_strip, col_body = st.columns([0.06, 0.94])
    with col_strip:
        st.markdown(
            f'<div style="background:linear-gradient(180deg,{borde},{fondo});'
            'min-height:96px;border-radius:8px;margin-top:4px;"></div>',
            unsafe_allow_html=True,
        )
    with col_body:
        _bloque_titulo_pastel(fondo, borde, titulo_html)
        return st.slider(
            "Valor (días)",
            min_value=0,
            max_value=100,
            value=valor_default,
            step=1,
            key=key,
            label_visibility="collapsed",
            help=ayuda,
        )


def figura_descomposicion_ccc(di: int, dso: int, dpo: int, ccc: int) -> go.Figure:
    """
    Funcionalidad 2 — construcción enlazada a la Funcionalidad 1.

    Diagrama de cascada (waterfall) horizontal para representar el cálculo
    **CCC = DI + DSO − DPO** con la secuencia DI, DSO, DPO (resta) y resultado CCC.
    """
    fig = go.Figure(
        go.Waterfall(
            name="CCC",
            orientation="h",
            measure=["relative", "relative", "relative", "total"],
            y=[
                "Días de inventario (DI)",
                "DSO (cuentas por cobrar)",
                "DPO (cuentas por pagar)",
                "CCC (resultado neto)",
            ],
            x=[di, dso, -dpo, ccc],
            text=[str(di), str(dso), str(-dpo), str(ccc)],
            textposition="outside",
            connector={"line": {"color": "rgb(80, 80, 80)"}},
            increasing={"marker": {"color": "#2E7D32"}},
            decreasing={"marker": {"color": "#C62828"}},
            totals={"marker": {"color": "#1565C0"}},
        )
    )
    # Ajuste fino del eje X para lectura más precisa de valores del recorrido acumulado.
    acumulados = [0, di, di + dso, ccc]
    min_x = min(acumulados)
    max_x = max(acumulados)
    padding = max(5, int((max_x - min_x) * 0.1))

    fig.update_layout(
        title=dict(
            text="Descomposición del CCC a partir de DI, DSO y DPO (días)",
            font=dict(size=18),
        ),
        xaxis=dict(
            title="Días — construcción según CCC = DI + DSO − DPO",
            range=[min_x - padding, max_x + padding],
            tickmode="linear",
            tick0=0,
            dtick=5,
            tickformat="d",
            zeroline=True,
            zerolinewidth=1.2,
            zerolinecolor="rgba(0,0,0,0.35)",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            griddash="dot",
        ),
        yaxis=dict(title="", autorange="reversed"),
        showlegend=False,
        height=440,
        margin=dict(l=8, r=48, t=72, b=64),
        font=dict(size=12),
    )
    return fig


def main() -> None:
    st.set_page_config(
        page_title="CCC — Controles de variables",
        page_icon="📊",
        layout="wide",
    )

    panel_descripcion_sidebar()

    st.title("💹 Ciclo de conversión de efectivo (CCC)")

    col_sliders, col_resultado = st.columns([1, 1.2])

    with col_sliders:
        st.subheader("🎛️ Parámetros (días)")
        st.markdown(
            "<p style='font-size:0.92rem;margin-bottom:12px;'>"
            f"<span style='background:{COLOR_DI};padding:2px 8px;border-radius:4px;margin-right:6px;'>DI</span>"
            f"<span style='background:{COLOR_DSO};padding:2px 8px;border-radius:4px;margin-right:6px;'>DSO</span>"
            f"<span style='background:{COLOR_DPO};padding:2px 8px;border-radius:4px;margin-right:6px;'>DPO</span>"
            f"<span style='background:{COLOR_CCC};padding:2px 8px;border-radius:4px;'>CCC</span>"
            " — tonos pastel en controles y gráfico.</p>",
            unsafe_allow_html=True,
        )
        di = _slider_variable_pastel(
            key="slider_di",
            fondo=COLOR_DI,
            borde=BORDE_DI,
            titulo_html="<strong>📦 Días de inventario (DI)</strong> — naranjo pastel",
            ayuda="Días de inventario (DI)",
            valor_default=45,
        )
        dso = _slider_variable_pastel(
            key="slider_dso",
            fondo=COLOR_DSO,
            borde=BORDE_DSO,
            titulo_html="<strong>📨 Días de cuentas por cobrar (DSO)</strong> — verde pastel",
            ayuda="Días de cuentas por cobrar (DSO)",
            valor_default=30,
        )
        dpo = _slider_variable_pastel(
            key="slider_dpo",
            fondo=COLOR_DPO,
            borde=BORDE_DPO,
            titulo_html="<strong>🧾 Días de cuentas por pagar (DPO)</strong> — morado pastel",
            ayuda="Días de cuentas por pagar (DPO)",
            valor_default=35,
        )

    ccc = calcular_ccc(di, dso, dpo)

    with col_resultado:
        st.subheader("📊 Resultado")
        st.markdown(
            f'<div style="background-color:{COLOR_CCC}; border-left: 6px solid {BORDE_CCC}; '
            "padding: 14px 18px; border-radius: 10px; margin-bottom: 12px;\">"
            '<div style="font-size:0.9rem;opacity:0.88;">📐 Ciclo de conversión de efectivo (CCC)</div>'
            f'<div style="font-size:2rem;font-weight:700;line-height:1.2;">{ccc} días</div>'
            "<div style=\"font-size:0.82rem;opacity:0.75;margin-top:6px;\">CCC = DI + DSO − DPO</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("#### 💬 Interpretación")
        st.markdown(mensaje_interpretacion(ccc))

    st.divider()
    st.subheader("📊 Visualización gráfica del CCC")
    st.caption(
        "Diagrama de **cascada horizontal** (waterfall): el recorrido DI → DSO → DPO (resta) "
        "construye el **CCC** con la misma fórmula de la Funcionalidad 1."
    )
    st.plotly_chart(
        figura_descomposicion_ccc(di, dso, dpo, ccc),
        use_container_width=True,
        config={"displayModeBar": True, "responsive": True},
    )

    with st.expander("📌 Nota metodológica"):
        st.markdown(
            "- 🔢 Los tres controles usan el mismo rango **0–100** días, según especificación.\n"
            "- 📅 El **CCC** se expresa en **días**; valores extremos pueden requerir validación "
            "con datos contables reales.\n"
            "- 📊 La **cascada** materializa la **Funcionalidad 1** con las mismas magnitudes; "
            "el paso **DPO** aparece como **resta** en la fórmula."
        )


if __name__ == "__main__":
    main()
