# Diccionario de Integración de Proveedores (Reglas ETL)

Este documento define las reglas de negocio, formatos de origen y transformaciones matemáticas necesarias para ingestar los datos de cada proveedor en la base de datos central de Egolf.

## 1. Proveedores con Ingesta Estructurada (Vía Excel/CSV)

### Underpar (TaylorMade / Stuburt)
* **Origen:** Excel recibido por email.
* **Calidad de SKU:** Alta (Posee códigos definidos).
* **Moneda de Origen:** USD (Requiere multiplicar por cotización manual informada por mail).
* **Regla de Costo (IVA):** Los costos vienen **SIN IVA**. 
  * *Transformación Python:* `Costo_Final = (Costo_Origen * 1.21) * Cotizacion_USD`
* **Regla de Venta:** Informa Precio Sugerido de Venta (PVP) en USD.

### N3Golf (Titleist / FootJoy)
* **Origen:** Excel recibido por email.
* **Calidad de SKU:** Baja/Nula (Casi sin códigos estructurados).
* **Moneda de Origen:** USD (Requiere multiplicar por cotización manual informada por mail).
* **Regla de Costo:** Costo neto informado en planilla.
  * *Transformación Python:* `Costo_Final = Costo_Origen * Cotizacion_USD`
* **Regla de Venta:** Informa Precio Sugerido de Venta (PVP) en USD.

### Callaway
* **Origen:** Excel recibido por email.
* **Calidad de SKU:** Alta.
* **Moneda de Origen:** Bimonetario (Informa en ARS y USD en la misma planilla).
* **Regla de Costo:** Leer la columna en pesos para evitar cálculos cambiarios innecesarios.
* **Regla de Venta:** Informa Precio Sugerido de Venta (PVP) en ambas monedas.

### Kaddy Golf
* **Origen:** Excel recibido por email.
* **Calidad de SKU:** **CRÍTICA**. Códigos repetidos para distintos productos (Ej: "Caddytek" agrupa múltiples modelos).
* **Moneda de Origen:** ARS.
* **Regla de Costo:** Costo neto en pesos.
* **Regla de Venta (Markup Fijo):** No informa PVP claro. 
  * *Transformación Python:* Se asume un markup estándar del **43%**. `Regla_Precio = 1.43`

---

## 2. Proveedores No Estructurados (Ingesta Manual / Scraping)

### Riera Golf
* **Origen:** Extracción manual desde `rieragolf.com.ar`.
* **Moneda de Origen:** ARS.
* **Regla de Costo (Descuento Comercial):** El costo es un 25% menos del precio publicado.
  * *Transformación Python:* `Costo_Final = Precio_Web * 0.75`

### Rafa (Grips)
* **Origen:** Extracción manual desde `golffitting.com.ar`.
* **Moneda de Origen:** ARS / USD (Según publicación).

---

## 3. Proveedores de Importación Directa

### Luna
* **Origen:** Trato directo / Importador.
* **Moneda de Origen:** USD.
* **Regla de Costo:** Aplicar cotización del día de la operación.

### Laska
* **Origen:** Trato directo.
* **Moneda de Origen:** ARS.