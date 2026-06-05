import sqlite3

def inicializar_base_datos():
    # Crea (o se conecta si ya existe) al archivo de la base de datos
    conexion = sqlite3.connect('sincronizador.db')
    cursor = conexion.cursor()

    # 1. Tabla Proveedor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Proveedor (
            ID_PROVEEDOR INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Metodo_actualizacion TEXT
        )
    ''')

    # 2. Tabla Producto (Estructura central)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Producto (
            SKU_INTERNO TEXT PRIMARY KEY,
            nombre TEXT,
            id_tiendanube TEXT,
            id_variante_tiendanube TEXT
        )
    ''')

    # 3. Tabla Equivalencia_SKU (El puente/diccionario)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Equivalencia_SKU (
            ID_SKU_PROVEEDOR TEXT PRIMARY KEY,
            Id_proveedor_equivalencia INTEGER,
            SKU_interno_equivalencia TEXT,
            FOREIGN KEY (Id_proveedor_equivalencia) REFERENCES Proveedor(ID_PROVEEDOR),
            FOREIGN KEY (SKU_interno_equivalencia) REFERENCES Producto(SKU_INTERNO)
        )
    ''')

    # 4. Tabla Costo (Alineada con el script de Pandas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Costo (
            ID_COSTO INTEGER PRIMARY KEY AUTOINCREMENT,
            SKU_interno_costo TEXT,
            ID_PROVEEDOR_costo INTEGER,
            costo_base REAL NOT NULL,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (SKU_interno_costo) REFERENCES Producto(SKU_INTERNO),
            FOREIGN KEY (ID_PROVEEDOR_costo) REFERENCES Proveedor(ID_PROVEEDOR)
        )
    ''')

    # 5. Tabla Reglas de Precio (Alineada con el script de Pandas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Regla_Precio (
            SKU_INTERNO TEXT PRIMARY KEY,
            porcentaje_markup REAL NOT NULL,
            impuesto REAL DEFAULT 0,
            FOREIGN KEY (SKU_INTERNO) REFERENCES Producto(SKU_INTERNO)
        )
    ''')

    # Guardar los cambios y cerrar
    conexion.commit()
    conexion.close()
    print("Base de datos 'sincronizador.db' creada con éxito. Estructura relacional lista.")

if __name__ == "__main__":
    inicializar_base_datos()