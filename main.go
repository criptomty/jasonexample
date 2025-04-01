package main

import (
	"encoding/json"
	"fmt"
)

// Estructuras para el JSON (simples y descriptivas)
type Request struct {
	Destination  string   `json:"destination"`
	ShippingType string   `json:"shipping_type"`
	Detail       []Detail `json:"detail"`
}

type Detail struct {
	Origin          string  `json:"origin"`
	Item            string  `json:"item"`
	ProductHerarchy string  `json:"product_herarchy"`
	QuantityWeight  float64 `json:"quantity_weight"`
	Volume          float64 `json:"volume"`
	Oum             string  `json:"oum"`
}

type MappingItem struct {
	ClaUbicacion    string `json:"ClaUbicacion"`
	ClaSapUbicacion string `json:"ClaSapUbicacion"`
	Descripcion     string `json:"Descripcion"`
}

func main() {
	// 1. Datos de entrada (simplificados)
	requestJSON := `{
		"destination": "89408",
		"shipping_type": "Z2",
		"detail": [{
			"origin": "CG31",
			"item": "000010",
			"product_herarchy": "006000800096",
			"quantity_weight": 9,
			"volume": 3.3333,
			"oum": "ton"
		}]
	}`

	mappingJSON := `[{
		"ClaUbicacion": "442",
		"ClaSapUbicacion": "DE31",
		"Descripcion": "Dirección 1"
	}, {
		"ClaUbicacion": "443",
		"ClaSapUbicacion": "CG31",
		"Descripcion": "Dirección 2"
	}]`

	// 2. Convertir JSON a estructuras de Go
	var request Request
	var mapping []MappingItem

	err := json.Unmarshal([]byte(requestJSON), &request)
	if err != nil {
		fmt.Println("Error al parsear request:", err)
		return
	}

	err = json.Unmarshal([]byte(mappingJSON), &mapping)
	if err != nil {
		fmt.Println("Error al parsear mapping:", err)
		return
	}

	// 3. Buscar el valor a reemplazar ("CG31" -> "443")
	originToReplace := request.Detail[0].Origin
	var newOrigin string

	for _, item := range mapping {
		if item.ClaSapUbicacion == originToReplace {
			newOrigin = item.ClaUbicacion
			break
		}
	}

	// 4. Reemplazar el valor
	if newOrigin != "" {
		request.Detail[0].Origin = newOrigin
	}

	// 5. Mostrar el resultado (formateado)
	resultJSON, err := json.MarshalIndent(request, "", "  ")
	if err != nil {
		fmt.Println("Error al generar resultado:", err)
		return
	}

	fmt.Println("Resultado final:")
	fmt.Println(string(resultJSON))
}
