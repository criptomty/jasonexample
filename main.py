from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from fastapi.responses import HTMLResponse
import json
import socket
import sys
import os
from datetime import datetime

# Cargar datos del archivo JSON
def load_json_data():
    try:
        file_path = 'data.json'
        file_stats = os.stat(file_path)
        with open(file_path, 'r') as file:
            data = json.load(file)
            return {
                'data': data,
                'file_info': {
                    'name': file_path,
                    'size': file_stats.st_size,
                    'last_modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
            }
    except FileNotFoundError:
        raise RuntimeError("No se encontró el archivo data.json")
    except json.JSONDecodeError:
        raise RuntimeError("El archivo data.json no contiene un JSON válido")

# Cargar datos
json_data = load_json_data()
request_data = json_data['data']['request']
file_info = json_data['file_info']

# Crear la aplicación FastAPI
app = FastAPI(
    title="JSON Processing API",
    description="API para procesar datos JSON y realizar cálculos",
    version="1.0.0"
)

# Modelo de respuesta
class CalculationResponse(BaseModel):
    original_values: Dict[str, Any]
    formatted_values: Dict[str, float]
    addresses: Dict[str, str]

def format_address(address: str) -> str:
    """Extrae la dirección hasta la primera coma."""
    return address.split(',')[0].strip()

def process_request(request_data: list):
    try:
        # Validar request
        if len(request_data) < 2:
            raise ValueError("El request debe contener al menos 2 elementos")

        # Obtener valores individuales
        valor1 = int(request_data[0]["ClaUbicacion"])
        valor2 = int(request_data[1]["ClaUbicacion"])

        # Obtener y formatear direcciones
        direccion1 = format_address(request_data[0]["Descripcion"])
        direccion2 = format_address(request_data[1]["Descripcion"])
        direcciones_combinadas = f"{direccion1} | {direccion2}"

        # Calcular valores
        suma_cla_ubicacion = valor1 + valor2
        producto_cla_ubicacion = valor1 * valor2
        
        # Formatear valores
        SumK = suma_cla_ubicacion / 1000
        ProductK = producto_cla_ubicacion / 1000

        return valor1, valor2, suma_cla_ubicacion, producto_cla_ubicacion, SumK, ProductK, direcciones_combinadas
        
    except Exception as e:
        raise Exception(f"Error en el procesamiento: {str(e)}")

# Endpoints de la API
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de procesamiento JSON",
        "file_info": file_info
    }

@app.get("/calculations", response_model=CalculationResponse)
async def get_calculations():
    try:
        valor1, valor2, suma, producto, sum_k, product_k, direcciones = process_request(request_data)
        return {
            "original_values": {
                "primer_valor": valor1,
                "segundo_valor": valor2,
                "suma_cla_ubicacion": suma,
                "producto_cla_ubicacion": producto
            },
            "formatted_values": {
                "SumK": sum_k,
                "ProductK": product_k
            },
            "addresses": {
                "combined": direcciones
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/request")
async def get_request():
    return {
        "request": request_data,
        "file_info": file_info
    }

@app.get("/view-results", response_class=HTMLResponse)
async def view_results():
    try:
        valor1, valor2, suma, producto, sum_k, product_k, direcciones = process_request(request_data)
        
        html_content = f"""
        <html>
            <head>
                <title>Resultados de Cálculos</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .container {{ max-width: 800px; margin: 0 auto; }}
                    .section {{ margin-bottom: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                    h1 {{ color: #333; }}
                    h2 {{ color: #666; }}
                    .value {{ font-weight: bold; color: #0066cc; }}
                    .operation {{ color: #666; margin: 10px 0; }}
                    .address {{ 
                        background-color: #f5f5f5;
                        padding: 10px;
                        border-radius: 4px;
                        margin: 10px 0;
                    }}
                    .file-info {{
                        background-color: #e9ecef;
                        padding: 10px;
                        border-radius: 4px;
                        margin: 10px 0;
                        font-size: 0.9em;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Resultados de Cálculos</h1>
                    
                    <div class="section">
                        <h2>Información del Archivo</h2>
                        <div class="file-info">
                            <p>Archivo: {file_info['name']}</p>
                            <p>Tamaño: {file_info['size']} bytes</p>
                            <p>Última modificación: {file_info['last_modified']}</p>
                        </div>
                    </div>

                    <div class="section">
                        <h2>Direcciones</h2>
                        <div class="address">
                            {direcciones}
                        </div>
                    </div>

                    <div class="section">
                        <h2>Valores Originales</h2>
                        <p>Primer valor: <span class="value">{valor1}</span></p>
                        <p>Segundo valor: <span class="value">{valor2}</span></p>
                        <div class="operation">
                            {valor1} + {valor2} = <span class="value">{suma}</span>
                        </div>
                        <div class="operation">
                            {valor1} × {valor2} = <span class="value">{producto}</span>
                        </div>
                    </div>

                    <div class="section">
                        <h2>Valores Formateados (K)</h2>
                        <p>SumK: <span class="value">{sum_k}</span></p>
                        <p>ProductK: <span class="value">{product_k}</span></p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html_content
    except Exception as e:
        return HTMLResponse(f"""
        <html>
            <body>
                <h1>Error</h1>
                <p style="color: red;">{str(e)}</p>
            </body>
        </html>
        """)

def find_available_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """Busca un puerto disponible empezando desde start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No se pudo encontrar un puerto disponible después de {max_attempts} intentos")

# Si se ejecuta directamente el script
if __name__ == "__main__":
    import uvicorn
    try:
        port = find_available_port()
        print(f"Iniciando servidor en http://127.0.0.1:{port}")
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
    except Exception as e:
        print(f"Error al iniciar el servidor: {str(e)}")
        sys.exit(1)
