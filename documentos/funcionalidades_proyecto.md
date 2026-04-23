# Documento de Funcionalidades del Proyecto

Objetivo general del proyecto: crear una simulación de Ciclo de conversión de efectivo (CCC), que sea interactiva para el usuario y le permita ver representado los resultados en un gráfico dinámico.

La aplicación debe ayudar a entender el Ciclo de conversión de efectivo de forma clara y didactica.

---
## Funcionalidad 1: Controles de variables

**Objetivo**: Capturar las variables para los días con los que se procederá a hacer el calculo

**Alcance**:
-Entrada mediante **sliders** de 3 variables:
 -Días de inventario (DI)
 -Días de Cuentas por cobrar (DSO)
 -Días de Cuentas por Pagar (DPO)
-El rango para las 3 variables es de 0 a 100.
-Fórmula a utilizar:
 -CCC = DI + DSO - DPO
-Visualización de resultados con una descripción para el usuario de forma sencilla y comprensible:
 -Un **mensaje** que se adapte al resultado (positivo, cero o negativo).

---
## Funcionalidad 2: Visualización gráfica del CCC

**Objetivo**: Representar gráficamente el valor de las variables y el resultado obtenido

**Alcance**:
-Construcción de un gráfico e barra horizontal apilado de:
 - CCC
 - DI
 - DSO
 - DPO
-El gráfico deberá actualizarce dinamicamente cuando cambien las variables de entrada.
-Etiquetas y ejes explicativos que refuercen la interpretación
