import sqlite3

def inicializar_base_datos():
    # Crea (o se conecta si ya existe) al archivo de la base de datos
    conexion = sqlite3.connect('sincronizador.db')
    cursor = conexion.cursor()

    # 1. Tabla Proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Proveedor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            metodo_actualizacion TEXT
        )
    ''')

    # 2. Tabla Productos (Estructura central que mapea el SKU con la API)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Producto (
            sku TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            id_tiendanube TEXT,
            id_variante_tiendanube TEXT
        )
    ''')

    # 3. Tabla Costos (Historial y costo actual por proveedor)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Costo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT,
            proveedor_id INTEGER,
            costo_base REAL NOT NULL,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku) REFERENCES Producto(sku),
            FOREIGN KEY (proveedor_id) REFERENCES Proveedor(id)
        )
    ''')

    # 4. Tabla Reglas de Precio (Markup dinámico por SKU)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Regla_Precio (
            sku TEXT PRIMARY KEY,
            porcentaje_markup REAL NOT NULL,
            impuesto REAL DEFAULT 0,
            FOREIGN KEY (sku) REFERENCES Producto(sku)
        )
    ''')

    # Guardar los cambios y cerrar
    conexion.commit()
    conexion.close()
    print("Base de datos 'sincronizador.db' creada con éxito. Estructura relacional lista.")

if __name__ == "__main__":
    inicializar_base_datos()