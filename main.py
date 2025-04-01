import json

# Datos JSON embebidos en el código (request + mapping)
request = {
    "destination": "89408",
    "shipping_type": "Z2",
    "detail": [
        {
            "origin": "CG31",   # Se reemplazará por "443"
            "item": "000010",
            "product_herarchy": "006000800096",
            "quantity_weight": 9,
            "volume": 3.3333,
            "oum": "ton"
        }
    ]
}

mapping = [
    {
        "ClaUbicacion": "442",
        "ClaSapUbicacion": "DE31",
        "Descripcion": "101 west 52th Ave, Denver, Colorado, USA, 80221"
    },
    {
        "ClaUbicacion": "443",
        "ClaSapUbicacion": "CG31",
        "Descripcion": "804 W Gila Bend HWY, Casa Grande, Arizona, USA, 85122"
    }
]

# Lógica para reemplazar "CG31" por "443"
for item in mapping:
    if item["ClaSapUbicacion"] == request["detail"][0]["origin"]:
        request["detail"][0]["origin"] = item["ClaUbicacion"]
        break

# Mostrar resultado
print(json.dumps(request, indent=2))
