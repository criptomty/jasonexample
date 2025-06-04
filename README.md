# API de Procesamiento JSON

Esta API procesa datos de ubicación y realiza cálculos con los valores de ClaUbicacion.

## Características

- Cálculo de suma y producto de valores ClaUbicacion
- Formateo de valores (división por 1000)
- Visualización de resultados en formato JSON y HTML
- Documentación interactiva con Swagger UI

## Requisitos

- Python 3.8 o superior
- FastAPI
- Uvicorn

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd apijason-phyton
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
jasonexample/
├── main.py          # Lógica principal de la API
├── data.py          # Datos de mapping
├── requirements.txt # Dependencias del proyecto
└── README.md        # Este archivo
```

## Uso

1. Iniciar el servidor:
```bash
python main.py
```

2. Acceder a la API:
- Documentación interactiva: http://127.0.0.1:8000/docs
- Vista HTML de resultados: http://127.0.0.1:8000/view-results
- Endpoint de cálculos: http://127.0.0.1:8000/calculations
- Endpoint de mapping: http://127.0.0.1:8000/mapping

## Endpoints

### GET /
Muestra un mensaje de bienvenida.

### GET /calculations
Retorna los cálculos realizados con los valores de ClaUbicacion:
- Valores originales (primer valor, segundo valor, suma y producto)
- Valores formateados (SumK y ProductK)

Ejemplo de respuesta:
```json
{
  "original_values": {
    "primer_valor": 442,
    "segundo_valor": 443,
    "suma_cla_ubicacion": 885,
    "producto_cla_ubicacion": 195806
  },
  "formatted_values": {
    "SumK": 0.885,
    "ProductK": 195.806
  }
}
```

### GET /mapping
Retorna los datos de mapping utilizados para los cálculos.

### GET /view-results
Muestra una página HTML con los resultados de los cálculos, incluyendo:
- Valores individuales
- Operaciones realizadas
- Resultados formateados

## Desarrollo

Para desarrollo local, el servidor se ejecuta con recarga automática:
```bash
python main.py
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

# jasonexample 

Jason data extraction example

Contenido:
  Ejemplo de extracciòn de datos y sustituciòn de informaciòn de un Jason en Go y Phyton
  
