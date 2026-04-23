"""
Aplicación Streamlit — Funcionalidad 1: Controles de variables del CCC
Ciclo de conversión de efectivo (Cash Conversion Cycle).

CCC = DI + DSO - DPO
"""

import streamlit as st


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
    st.sidebar.info(
        "💡 Los tres deslizadores comparten el rango **0 a 100 días**. "
        "Ajuste los valores para explorar distintos escenarios operativos."
    )


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
        di = st.slider("📦 Días de inventario (DI)", min_value=0, max_value=100, value=45, step=1)
        dso = st.slider(
            "📨 Días de cuentas por cobrar (DSO)",
            min_value=0,
            max_value=100,
            value=30,
            step=1,
        )
        dpo = st.slider(
            "🧾 Días de cuentas por pagar (DPO)",
            min_value=0,
            max_value=100,
            value=35,
            step=1,
        )

    ccc = calcular_ccc(di, dso, dpo)

    with col_resultado:
        st.subheader("📊 Resultado")
        st.metric(
            label="📐 Ciclo de conversión de efectivo (CCC)",
            value=f"{ccc} días",
            help="CCC = DI + DSO − DPO",
        )
        st.markdown("#### 💬 Interpretación")
        st.markdown(mensaje_interpretacion(ccc))

    with st.expander("📌 Nota metodológica"):
        st.markdown(
            "- 🔢 Los tres controles usan el mismo rango **0–100** días, según especificación.\n"
            "- 📅 El **CCC** se expresa en **días**; valores extremos pueden requerir validación "
            "con datos contables reales."
        )


if __name__ == "__main__":
    main()
