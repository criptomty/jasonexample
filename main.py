from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from fastapi.responses import HTMLResponse
import json
from data import mapping

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

def process_mapping(mapping_data: list):
    try:
        # Validar mapping
        if len(mapping_data) < 2:
            raise ValueError("El mapping debe contener al menos 2 elementos")

        # Obtener valores individuales
        valor1 = int(mapping_data[0]["ClaUbicacion"])
        valor2 = int(mapping_data[1]["ClaUbicacion"])

        # Calcular valores
        suma_cla_ubicacion = valor1 + valor2
        producto_cla_ubicacion = valor1 * valor2
        
        # Formatear valores
        SumK = suma_cla_ubicacion / 1000
        ProductK = producto_cla_ubicacion / 1000

        return valor1, valor2, suma_cla_ubicacion, producto_cla_ubicacion, SumK, ProductK
        
    except Exception as e:
        raise Exception(f"Error en el procesamiento: {str(e)}")

# Endpoints de la API
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de procesamiento JSON"}

@app.get("/calculations", response_model=CalculationResponse)
async def get_calculations():
    try:
        valor1, valor2, suma, producto, sum_k, product_k = process_mapping(mapping)
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
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mapping")
async def get_mapping():
    return {"mapping": mapping}

@app.get("/view-results", response_class=HTMLResponse)
async def view_results():
    try:
        valor1, valor2, suma, producto, sum_k, product_k = process_mapping(mapping)
        
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
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Resultados de Cálculos</h1>
                    
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

# Si se ejecuta directamente el script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
