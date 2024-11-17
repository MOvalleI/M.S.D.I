import datetime

class Ejemplo:
    def __new__(cls, *args, **kwargs):
      obj = cls.super().__init__()
      return obj
    
    def __init__(self, valor):
      self.valor = valor

ejemplo = Ejemplo(4)
print(ejemplo)