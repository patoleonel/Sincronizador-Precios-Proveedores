import pandas as pd
import sqlite3

DB_NAME = "sincronizador.db"

def cargar_catalogo():
    # 1. Leer el CSV exportado de Tiendanube
    try:
        df_tn = pd.read_csv('tiendanube.csv', sep=';') 
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'tiendanube.csv'.")
        return

    # Limpiar espacios invisibles en los nombres de los encabezados
    df_tn.columns = df_tn.columns.str.strip()
    print(f"--- Leídas {len(df_tn)} filas del CSV de Tiendanube ---")

    # =================================================================
    # 2. MAPEO DE COLUMNAS
    # =================================================================
    # La clave (izquierda) es cómo se llama la columna en el archivo CSV de Tiendanube.
    # El valor (derecha) es cómo se llama la columna en la tabla SQLite.
    
    mapa_columnas = {
        'SKU': 'SKU_INTERNO',
        'Nombre': 'nombre',
        'Identificador URL': 'id_tiendanube', 
        'ID de variante': 'id_variante_tiendanube' 
    }
    
    # -----------------------------------------------------------------

    columnas_a_renombrar = {k: v for k, v in mapa_columnas.items() if k in df_tn.columns}
    
    if 'SKU' not in df_tn.columns:
        print("Error crítico: No se encontró la columna 'SKU' en el archivo de Tiendanube.")
        print(f"Columnas detectadas: {list(df_tn.columns)}")
        return

    # Filtrar filas vacías (productos sin SKU asignado)
    df_tn = df_tn.dropna(subset=['SKU'])

    # Renombrar las columnas al formato de la base de datos
    df_tn = df_tn.rename(columns=columnas_a_renombrar)

    # Filtrar el DataFrame final solo con las columnas que nos interesan
    columnas_db = ['SKU_INTERNO', 'nombre', 'id_tiendanube', 'id_variante_tiendanube']
    columnas_existentes = [col for col in columnas_db if col in df_tn.columns]
    df_final = df_tn[columnas_existentes]

    # 3. Inserción en SQLite
    print("\n--- Conectando a SQLite e insertando catálogo ---")
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        registros = 0
        
        for index, fila in df_final.iterrows():
            # Usamos INSERT OR REPLACE por si en el futuro vuelvo a correr 
            # este script con un CSV nuevo para actualizar nombres o IDs
            cursor.execute("""
                INSERT OR REPLACE INTO Producto (SKU_INTERNO, nombre, id_tiendanube, id_variante_tiendanube)
                VALUES (?, ?, ?, ?)
            """, (
                str(fila.get('SKU_INTERNO', '')), 
                str(fila.get('nombre', '')), 
                str(fila.get('id_tiendanube', '')), 
                str(fila.get('id_variante_tiendanube', ''))
            ))
            registros += 1

        conn.commit()
        print(f"Catálogo actualizado: {registros} productos insertados en la tabla 'Producto'.")

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print(f"Error en la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    cargar_catalogo()