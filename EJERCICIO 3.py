import unittest

# Error de consumo negativo
def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
  if consumo_kwh < 0:
    raise ValueError("El consumo no puede ser negativo.")
  return consumo_kwh * factor_emision


# Clase de prueba para calcular emisiones
class TestCalculoEmisiones(unittest.TestCase):

  # CASOS  

  # 1. Consumo normal y factor por defecto (100 * 0.4)
  def test_calculo_pordefecto(self):
    resultado = calcular_emisiones_carbono(100)
    self.assertAlmostEqual(resultado, 40.0)

  # 2. Factor de emisión personalizado (100 * 0.5)
  def test_calculo_factor_personalizado(self):
    resultado = calcular_emisiones_carbono(100, factor_emision=0.5)
    self.assertAlmostEqual(resultado, 50.0)

  # 3. Consumo igual a cero o sin consumo
  def test_calculo_consumo_cero(self):
    resultado = calcular_emisiones_carbono(0)
    self.assertAlmostEqual(resultado, 0.0)

  # 4. Consumo negativo
  def test_error_consumo_negativo(self):
    with self.assertRaises(ValueError):
      calcular_emisiones_carbono(-50)


# DJANGO (ver)

def obtener_metricas_consumo(registros):
  # Si no hay registros, todo da 0
  if len(registros) == 0:
    return {
        "total_emisiones": 0.0,
        "planta_mayor_consumo": "Sin datos",
        "mayor_consumo_kwh": 0.0,
    }

  total_emisiones = 0.0
  planta_mayor = ""
  maximo_consumo = -1.0

  for registro in registros:
    planta = registro["planta"]
    consumo = registro["consumo_kwh"]

    # Función del punto A
    emision_planta = calcular_emisiones_carbono(consumo)
    total_emisiones += emision_planta

    # Comparamos para encontrar la planta con mayor consumo
    if consumo > maximo_consumo:
      maximo_consumo = consumo
      planta_mayor = planta
  
  # Devolvemos el resumen en un diccionario
  return {
      "total_emisiones": round(total_emisiones, 2),
      "planta_mayor_consumo": planta_mayor,
      "mayor_consumo_kwh": maximo_consumo,
  }


# Vista de Django para plantillas HTML

try:
  from django.shortcuts import render
except ImportError:
  render = None


def vista_panel_sustentabilidad(request):
  # Base de datos o historial
  historial_plantas = [
      {"planta": "Planta Norte", "consumo_kwh": 1200.0},
      {"planta": "Planta Sur", "consumo_kwh": 3450.5},
      {"planta": "Planta Este", "consumo_kwh": 890.0},
  ]

  # 2. Funcio de métricas 
  metricas = obtener_metricas_consumo(historial_plantas)

  # 3. Diccionario de contexto para HTML
  context = {
      "titulo_panel": "Panel de Sustentabilidad de EcoTech",
      "registros": historial_plantas,
      "total_emisiones": metricas["total_emisiones"],
      "planta_mayor_consumo": metricas["planta_mayor_consumo"],
      "mayor_consumo_kwh": metricas["mayor_consumo_kwh"],
  }

  # 4. Plantilla final HTML
  return render(request, "sustentabilidad/panel.html", context)


#  EJECUCIÓN DE PRUEBAS (ver)

if __name__ == "__main__":
  print("Ejecutando auditoría de pruebas unitarias...")
  unittest.main()
