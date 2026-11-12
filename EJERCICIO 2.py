import json

# INVENTARIO Y STOCK

# En caso de stock negativo - excepcion
class StockInvalidoError(Exception):
  """Se lanza cuando se intenta asignar un stock negativo."""
  pass


# Clase base
class DispositivoEcologico:

  def __init__(self, codigo, nombre, precio, stock):
    self.codigo = codigo
    self.nombre = nombre
    self.precio = precio
    self.stock = stock

  # Encapsulamiento 
  @property
  def stock(self):
    return self.__stock

  @stock.setter
  def stock(self, nuevo_stock):
    if nuevo_stock < 0:
      raise StockInvalidoError(
          f"Error en '{self.nombre}': El stock no puede ser negativo"
          f" ({nuevo_stock})."
      )
    self.__stock = nuevo_stock

  # Polimorfismo
  def obtener_ficha_tecnica(self):
    return (
        f"[{self.codigo}] {self.nombre} | Precio: ${self.precio:.2f} | Stock:"
        f" {self.stock} u."
    )

  # Conversión a JSON
  def a_diccionario(self):
    return {
        "tipo": "DispositivoEcologico",
        "codigo": self.codigo,
        "nombre": self.nombre,
        "precio": self.precio,
        "stock": self.stock,
    }


# 3. Clase Especializada 
class PanelSolar(DispositivoEcologico):

  def __init__(self, codigo, nombre, precio, stock, potencia_watts, eficiencia):
    super().__init__(codigo, nombre, precio, stock)
    self.potencia_watts = potencia_watts
    self.eficiencia = eficiencia

  # Polimorfismo para ficha tecnica
  def obtener_ficha_tecnica(self):
    ficha_base = super().obtener_ficha_tecnica()
    return (
        f"{ficha_base} | Potencia: {self.potencia_watts}W | Eficiencia:"
        f" {self.eficiencia}%"
    )

  # Extendemos el diccionario para incluir los atributos propios del panel
  def a_diccionario(self):
    datos = super().a_diccionario()
    datos["tipo"] = "PanelSolar"
    datos["potencia_watts"] = self.potencia_watts
    datos["eficiencia"] = self.eficiencia
    return datos


# CATALOGO


class GestorInventario:

  def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
    catalogo_serializable = []
    for dispositivo in lista_dispositivos:
      catalogo_serializable.append(dispositivo.a_diccionario())

    # Para guardar JSON
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
      json.dump(catalogo_serializable, archivo, indent=4, ensure_ascii=False)

    print(f"Catálogo guardado exitosamente en '{ruta_archivo}'.")


# PRUEBA

if __name__ == "__main__":
  catalogo_valido = []

  print(" 1. PRODUCTOS DISPONIBLES ")
  panel_1 = PanelSolar(
      "SOL-101", "Panel 1A", 250.0, 15, 450, 21.5
  )
  panel_2 = PanelSolar(
      "SOL-102", "Panel 2A", 180.0, 8, 330, 18.0
  )

  catalogo_valido.append(panel_1)
  catalogo_valido.append(panel_2)

  for prod in catalogo_valido:
    print(prod.obtener_ficha_tecnica())

  print( "PRUEBA DE STOCK NEGATIVO" )
  # Stock negativo
  try:
    panel_negativo = PanelSolar(
        "SOL-900", "Panel negativo", 100.0, -55, 200, 15.0
    )
  except StockInvalidoError as error:
    print(f"Excepción capturada al crear: {error}")


  print("EXPORTAR A JSON ")
  gestor = GestorInventario()
  gestor.guardar_catalogo_json(catalogo_valido, "catalogo_ecotech.json")
