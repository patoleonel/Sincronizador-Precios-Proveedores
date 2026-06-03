import os
import requests
from dotenv import load_dotenv

# Carga las variables del archivo .env en el entorno del sistema
load_dotenv()

# Recupera las variables de entorno
ACCESS_TOKEN = os.getenv("TIENDANUBE_ACCESS_TOKEN")
USER_ID = os.getenv("TIENDANUBE_USER_ID")

# Configura los headers para autentición en la API de Tiendanube
headers = {
    "Authentication": f"bearer {ACCESS_TOKEN}",
    "User-Agent": "Sincronizador Precios (lucero.stellmaris@yahoo.com.ar)"
}

# URL base de la API de Tiendanube para consultar productos
url_productos = f"https://api.tiendanube.com/v1/{USER_ID}/products"

def probar_conexion():
    try:
        response = requests.get(url_productos, headers=headers)
        if response.status_code == 200:
            print("¡Conexión exitosa! La API de Tiendanube respondió correctamente.")
            productos = response.json()
            print(f"Se encontraron {len(productos)} productos en la primera página de tu catálogo.")
        else:
            print(f"Error al conectar. Código de estado: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Ocurrió un error en la petición técnica: {e}")

if __name__ == "__main__":
    probar_conexion()