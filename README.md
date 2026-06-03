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