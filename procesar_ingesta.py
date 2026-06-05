import pandas as pd
import sqlite3
from datetime import datetime

# Definino nombre de la DB.
DB_NAME = "sincronizador.db"

def procesar_y_guardar_ingesta():
    try:
        df_ingesta = pd.read_csv('ingesta.csv', sep=',')
        df_equiv = pd.read_csv('equivalencias.csv', sep=',')
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo. {e}")
        return

    df_ingesta.columns = df_ingesta.columns.str.strip()
    df_equiv.columns = df_equiv.columns.str.strip()

    print("--- Analizando y limpiando lista de ingesta ---")

    # 1. REGLA AUTOMÁTICA: PROMOS TAYLORMADE
    duplicados = df_ingesta[df_ingesta.duplicated(subset=['SKU_proveedor'], keep=False)]
    if not duplicados.empty:
        skus_repetidos = duplicados['SKU_proveedor'].unique()
        for sku in skus_repetidos:
            filas_conflicto = df_ingesta[df_ingesta['SKU_proveedor'] == sku]
            if len(filas_conflicto) == 2:
                idx_promo = filas_conflicto['Costo_lista'].idxmax()
                nuevo_sku = str(sku) + '-3X2'
                df_ingesta.at[idx_promo, 'SKU_proveedor'] = nuevo_sku
                print(f"🔧 Transformación Automática: '{sku}' duplicado. Renombrado a '{nuevo_sku}'")

    # 2. VALIDACIÓN DEFENSIVA
    duplicados_restantes = df_ingesta[df_ingesta.duplicated(subset=['SKU_proveedor'], keep=False)]
    if not duplicados_restantes.empty:
        print("\nERROR INESPERADO: Se encontraron duplicados no controlados. Ingesta abortada.")
        print(duplicados_restantes[['SKU_proveedor', 'Costo_lista', 'Precio_sugerido']])
        return

    print("\n--- Iniciando Cruce de Datos ---")
    
    # 3. CRUCE DE DATOS
    df_final = pd.merge(df_ingesta, df_equiv, left_on='SKU_proveedor', right_on='ID_SKU_PROVEEDOR', how='inner')
    if df_final.empty:
        print("Error: No se encontró ninguna coincidencia entre la ingesta y las equivalencias.")
        return

    # 4. MATEMÁTICA Y REGLAS DE NEGOCIO
    resultados = []
    for index, fila in df_final.iterrows():
        sku_interno = fila['SKU_interno_equivalencia']
        proveedor_nombre = fila['ID_proveedor_equivalencia'] 
        costo_lista = float(fila['Costo_lista'])
        precio_sug = float(fila['Precio_sugerido'])
        cotizacion = float(fila['Cotizacion_USD'])
        
        multiplicador_iva = 1.0 
        id_proveedor = 2 # Por defecto Callaway u otro
        
        if "Taylormade" in str(proveedor_nombre):
            multiplicador_iva = 1.21
            id_proveedor = 1 # ID de TaylorMade en la tabla Proveedor
            
        costo_final_ars = (costo_lista * multiplicador_iva) * cotizacion
        precio_sug_ars = precio_sug * cotizacion
        markup = (precio_sug_ars / costo_final_ars) - 1

        resultados.append({
            'SKU_Interno': sku_interno,
            'ID_Proveedor': id_proveedor,
            'Costo_Base_ARS': round(costo_final_ars, 2),
            'Markup_Calculado': round(markup, 4)
        })

    df_resultados = pd.DataFrame(resultados)
    print(df_resultados.to_string(index=False))

    # =====================================================================
    # 5. INSERCIÓN EN BASE DE DATOS SQLITE
    # =====================================================================
    print("\n--- Conectando a SQLite y guardando datos ---")
    
    conn = None # Inicialización de seguridad
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registros_insertados = 0

        for index, fila in df_resultados.iterrows():
            sku_interno = fila['SKU_Interno']
            id_prov = fila['ID_Proveedor']
            costo = fila['Costo_Base_ARS']
            markup = fila['Markup_Calculado']

            # Insertar en tabla Costo
            cursor.execute("""
                INSERT INTO Costo (SKU_interno_costo, ID_PROVEEDOR_costo, costo_base, fecha_actualizacion)
                VALUES (?, ?, ?, ?)
            """, (sku_interno, id_prov, costo, fecha_actual))

            # Insertar o actualizar Regla_Precio
            cursor.execute("""
                INSERT OR REPLACE INTO Regla_Precio (SKU_INTERNO, porcentaje_markup, impuesto)
                VALUES (?, ?, ?)
            """, (sku_interno, markup, 0.0))

            registros_insertados += 1

        conn.commit()
        print(f"Éxito: Se guardaron {registros_insertados} registros en '{DB_NAME}'.")

    except sqlite3.Error as e:
        if conn:
            conn.rollback() # Solo hace rollback si la conexión se estableció
        print(f"Error en la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    procesar_y_guardar_ingesta()