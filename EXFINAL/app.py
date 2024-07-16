# app.py
from flask import Flask, request, jsonify
from models import Cuenta, Operacion

app = Flask(__name__)

# Almacenamiento en memoria de las cuentas
cuentas = {
    "21345": Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    "123": Cuenta("123", "Luisa", 400, ["456"]),
    "456": Cuenta("456", "Andrea", 300, ["21345"])
}

# Almacenamiento en memoria de las operaciones
operaciones = []

# Ruta para listar los contactos de una cuenta
@app.route('/billetera/contactos', methods=['GET'])
def listar_contactos():
    numero = request.args.get('minumero')
    cuenta = cuentas.get(numero)
    if cuenta:
        contactos = {contacto: cuentas[contacto].nombre for contacto in cuenta.contactos if contacto in cuentas}
        return jsonify(contactos), 200
    else:
        return "Cuenta no encontrada", 404

# Ruta para realizar un pago
@app.route('/billetera/pagar', methods=['POST'])
def pagar():
    numero_origen = request.args.get('minumero')
    numero_destino = request.args.get('numerodestino')
    valor = float(request.args.get('valor'))
    
    cuenta_origen = cuentas.get(numero_origen)
    cuenta_destino = cuentas.get(numero_destino)
    
    if cuenta_origen and cuenta_destino:
        try:
            operacion = cuenta_origen.enviar_dinero(numero_destino, valor)
            cuenta_destino.saldo += valor
            
            # Agregar operación a la lista de operaciones
            operaciones.append(operacion)

            return f"Realizado en {operacion.fecha.strftime('%d/%m/%Y')}.", 200
        except ValueError as e:
            return str(e), 400
    elif not cuenta_origen:
        return "Cuenta de origen no encontrada", 404
    else:
        return "El contacto no está en la lista de contactos.", 400

# Ruta para mostrar el historial de una cuenta
@app.route('/billetera/historial', methods=['GET'])
def historial():
    numero = request.args.get('minumero')
    cuenta = cuentas.get(numero)
    if cuenta:
        operaciones_enviadas = [{'tipo': 'Pago realizado', 'numero_destino': op.numero_destino, 'fecha': op.fecha, 'valor': op.valor} for op in operaciones if op.numero_origen == numero]
        operaciones_recibidas = [{'tipo': 'Pago recibido', 'numero_origen': op.numero_origen, 'fecha': op.fecha, 'valor': op.valor} for op in operaciones if op.numero_destino == numero]
        historial = operaciones_enviadas + operaciones_recibidas
        historial.sort(key=lambda x: x['fecha'])
        return jsonify({'saldo': cuenta.saldo, 'historial': historial}), 200
    else:
        return "Cuenta no encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)
