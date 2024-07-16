# models.py
from datetime import datetime

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos

    def enviar_dinero(self, destino, valor):
        if destino in self.contactos:
            if self.saldo >= valor:
                operacion = Operacion(self.numero, destino, valor)
                self.saldo -= valor
                return operacion
            else:
                raise ValueError("Saldo insuficiente.")
        else:
            raise ValueError("El contacto no está en la lista de contactos.")

class Operacion:
    def __init__(self, numero_origen, numero_destino, valor):
        self.numero_origen = numero_origen
        self.numero_destino = numero_destino
        self.fecha = datetime.now()
        self.valor = valor
