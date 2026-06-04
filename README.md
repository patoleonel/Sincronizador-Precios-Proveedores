# Sincronizador Dinámico de Precios - Tiendanube

Este proyecto es una solución automatizada para mantener actualizados los precios de venta en una tienda de Tiendanube. Su objetivo principal es evitar la venta a pérdida provocada por la asimetría de información y los aumentos de costos no notificados por parte de los proveedores.

## Arquitectura del Proyecto

El sistema funciona como un pipeline de datos que se encarga de:
1. **Ingesta:** Leer listas de precios de proveedores desde distintos orígenes (archivos Excel/CSV enviados por email y web scraping de catálogos online).
2. **Procesamiento:** Cruzar los costos actualizados con una base de datos local relacional y calcular el precio final de venta aplicando reglas de negocio (markup + impuestos).
3. **Sincronización:** Comunicarse vía API REST con Tiendanube para actualizar el catálogo en tiempo real.

## Tecnologías Utilizadas
* Python 3
* `requests` (Cliente HTTP para API Tiendanube y Web Scraping)
* `python-dotenv` (Gestión de variables de entorno y credenciales)
* *Próximamente: Pandas/Openpyxl (Manejo de Excel) y SQLite/PostgreSQL (Base de datos local).*

## Instalación y Configuración Local

1. Clonar el repositorio.
2. Crear un entorno virtual (Conda o Venv) e instalar las dependencias:
   ```bash
   pip install requests python-dotenv
3. Crear un archivo .env en la raíz del proyecto (este archivo está ignorado por Git por seguridad) con las siguientes variables:
- TIENDANUBE_ACCESS_TOKEN=tu_access_token_generado
- TIENDANUBE_USER_ID=tu_id_de_tienda

## Uso

Para verificar la conexión inicial con la API de la tienda:
- python sincronizador.py

## Arquitectura del Proyecto

El sistema funciona como un pipeline de datos que se encarga de...

![Arquitectura Global del Sistema](docs/arquitectura_global.png)

## Modelo de Datos (DER)

![Diagrama Entidad-Relación](docs/der_egolf.png)

### Diccionario de Datos

El sistema utiliza un modelo relacional (SQLite/PostgreSQL) centrado en el producto, separando la información estructural de las variables comerciales volátiles.

* **`Producto` (Entidad Central):** Almacena la estructura inmutable del catálogo. El `SKU` actúa como identificador principal, vinculando el sistema físico con los IDs internos de la API de Tiendanube (`id_tiendanube`, `id_variante_tiendanube`).
* **`Regla_Precio` (1:1 con Producto):** Aísla la lógica comercial. Utiliza el SKU como PK/FK compartida para garantizar que cada producto tenga un único margen de rentabilidad (`porcentaje_markup`). Permite actualizaciones masivas de precios sin riesgo de corromper la tabla estructural.
* **`Proveedor` (Entidad de Origen):** Cataloga a los emisores de listas de precios, definiendo su canal de ingesta (`Método_actualizacion`: web, excel, mail).
* **`Costo` (Tabla Transaccional / Historial):** Resuelve la relación N:M entre proveedores y productos. Registra cada variación de precio (`costo_base`) en el tiempo (`fecha_actualizacion`), permitiendo auditoría y evitando la pérdida de datos históricos.