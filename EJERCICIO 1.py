
def limpiar_registro_sensor(registro_raw):
  # Limpieza  
  id_raw = registro_raw.get("sensor_id", "SIN-ID")
  sensor_id_limpio = str(id_raw).strip()

  # Temperatura
  temp_raw = str(registro_raw.get("temperatura", 0.0))
  temp_sin_unidad = temp_raw.replace("°C", "").replace("C", "").strip()
  temperatura_limpia = float(temp_sin_unidad)

  # Ubicacion
  ubicacion_raw = registro_raw.get("ubicacion")
  if ubicacion_raw is None or str(ubicacion_raw).strip() == "":
    ubicacion_limpia = "Desconocida"
  else:
    ubicacion_limpia = str(ubicacion_raw).strip()

  return {
      "sensor_id": sensor_id_limpio,
      "temperatura": temperatura_limpia,
      "ubicacion": ubicacion_limpia,
  }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    lista_sensores_alerta = []
    suma_temperaturas = 0.0
    cantidad_sensores = 0 

    for sensor in lista_sensores_limpios:
        temp_actual = sensor["temperatura"]
        suma_temperaturas += temp_actual
        cantidad_sensores += 1  

        if temp_actual > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    # Evitar la div por cero
    if cantidad_sensores == 0:
        return ([], 0.0)

    promedio_temperatura = suma_temperaturas / cantidad_sensores

    # Tupla
    return (lista_sensores_alerta, promedio_temperatura)


# EJECUCION
if __name__ == "__main__":
  # Datos
  lecturas = [
      {
          "sensor_id": " SENSOR-001 ",
          "temperatura": "24.5C",
          "ubicacion": "Planta Norte",
      },
      {
          "sensor_id": "SENSOR-002  ",
          "temperatura": " 28.9 °C",
          "ubicacion": "Planta Sur",
      },
       # Sin ubicación
      {"sensor_id": "  SENSOR-003", "temperatura": "21.0C"},  

       # Ubicacion vacia
      {
          "sensor_id": "SENSOR-004 ",
          "temperatura": "31.2C",
          "ubicacion": "",
      }
  ]

  # Aplicar punto A
  sensores_limpios = []
  for registro in lecturas:
    registro_estandar = limpiar_registro_sensor(registro)
    sensores_limpios.append(registro_estandar)

  # Aplicar punto B
  umbral_maximo = 25.0

  # Alerta
  alertas, promedio_global = generar_resumen_sensores(
      sensores_limpios, umbral_maximo
  )

  # Reporte final
  print("REPORTE TÉRMICO DE ECOTECH SOLUTIONS")
  print(f"Total de sensores procesados: {len(sensores_limpios)}")
  print(f"Umbral máximo permitido: {umbral_maximo} °C")
  print(f"Temperatura promedio de la planta: {promedio_global:.2f} °C")

  if len(alertas) > 0:
    print(f"ALERTA - Sensores sobre el umbral ({len(alertas)}):")
    for sensor_id in alertas:
      print(f"  -> {sensor_id}")

