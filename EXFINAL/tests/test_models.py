import unittest
from models import Cuenta

class TestCuenta(unittest.TestCase):

    def setUp(self):
        self.cuenta1 = Cuenta("21345", "Arnaldo", 200, ["123", "456"])
        self.cuenta2 = Cuenta("123", "Luisa", 400, ["456"])
        self.cuenta3 = Cuenta("456", "Andrea", 300, ["21345"])
        self.operaciones = []

    #Prueba de envío de dinero exitosa.
    def test_enviar_dinero_exito(self):
        operacion = self.cuenta1.enviar_dinero("123", 50)
        self.operaciones.append(operacion)
        self.assertEqual(self.cuenta1.saldo, 150)
        self.assertEqual(operacion.valor, 50)
        self.assertEqual(operacion.numero_origen, "21345")
        self.assertEqual(operacion.numero_destino, "123")

    #Prueba de transferencia con dinero exacto.
    def test_enviar_dinero_saldo_exacto(self):
        operacion = self.cuenta1.enviar_dinero("456", 200)
        self.operaciones.append(operacion)
        self.assertEqual(self.cuenta1.saldo, 0)
        self.assertEqual(operacion.valor, 200)
        self.assertEqual(operacion.numero_origen, "21345")
        self.assertEqual(operacion.numero_destino, "456")

    #Transferencia a Contacto que no existe.
    def test_enviar_dinero_contacto_no_existente(self):
        with self.assertRaises(ValueError) as context:
            self.cuenta1.enviar_dinero("789", 50)
        self.assertTrue("El contacto no está en la lista de contactos." in str(context.exception))

    #Transferencia con saldo insuficiente.
    def test_enviar_dinero_saldo_insuficiente(self):
        with self.assertRaises(ValueError) as context:
            self.cuenta1.enviar_dinero("123", 250)
        self.assertTrue("Saldo insuficiente." in str(context.exception))

    #Transferencia a uno mismo.
    def test_enviar_dinero_a_si_mismo(self):
        with self.assertRaises(ValueError) as context:
            self.cuenta1.enviar_dinero("21345", 50)
        self.assertTrue("El contacto no está en la lista de contactos." in str(context.exception))

if __name__ == '__main__':
    unittest.main()
