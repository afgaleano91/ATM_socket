import socket
import json

def createClient(option):
    nombre = input("Escriba el nombre: ")
    apellidos = input("Escriba sus apellidos: ")
    email = input("Escriba su email: ")
    ciudad = input("Seleccione su ciudad, 1: bogota, 2: medellin: ")
    telefono = input("Escriba su numero de telefono: ")
    dicc = {"option": option, "nombres": nombre, "apellidos":apellidos, "email": email, "ciudad": ciudad, "telefono": telefono}
    return dicc

def consult(option):
    email = input("Escriba su email: ")
    dicc = { "option": option, "email": email}
    return dicc

def consignment(option):
    email = input("Escriba su email: ")
    value = input("Valor a consignar: ")
    dicc = { "option": option, "email": email, "valor": value}
    return dicc

def retirement(option):
    email = input("Escriba su email: ")
    value = input("Valor a retirar: ")
    dicc = { "option": option, "email": email, "valor": value}
    return dicc

def send_recv(s, func, option):
    s.send(bytes(json.dumps(func(option)), 'utf-8'))
    data = s.recv(1024).decode()
    return ('Received from server: ' + data)

def clientProgram():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 12345))
    print(" 1: crear cliente \n 2: consultar saldo \n 3: consignar \n 4: retirar")
    option = input("Digite la opcion: ")
    while option != "0":
        if option == "1":
            print(send_recv(s, createClient, option))
        elif option == "2":
            print(send_recv(s, consult, option))
        elif option == "3":
            print(send_recv(s, consignment, option))
        elif option == "4":
            print(send_recv(s, retirement, option))
        else:
            print('Opcion no valida.')
        print(" 1: crear cliente \n 2: consultar saldo \n 3: consignar \n 4: retirar")
        option = input("Digite la opcion: ")
    s.close()

if __name__ == '__main__':
    clientProgram()