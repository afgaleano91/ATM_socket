import socket #Se importa libreria para sockets
import json #Se importa libreria para manejo de json
import views #Importamos las funciones que necesitamos para las diferentes acciones
import time #Se importa para establecer tiempo de actividad del socket

def serverProgram():
    print(views.version()) #llama a la funcion version para mostrar la version de postgres
    print(views.create_db()) #llama a la funcion para crear tablas en la base de datos
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
    s.bind((socket.gethostname(), 12345))
    s.listen(5)
    clientSocket, address = s.accept()
    print(f"Conection from {address} has been established!")
    while True:
        data = clientSocket.recv(1024).decode()
        print(">>", data)
        if data:
            data_c = json.loads(data)
            if data_c["option"] == "1":
                re = views.create_client(data_c)
                clientSocket.send(bytes(re, "utf-8"))
            elif data_c["option"] == "2":
                re = views.consultValue(data_c)
                clientSocket.send(bytes(re, "utf-8"))
            elif data_c["option"] == "3":
                re = views.consignment(data_c)
                clientSocket.send(bytes(re, "utf-8"))
            elif data_c["option"] == "4":
                re = views.retirement(data_c)
                clientSocket.send(bytes(re, "utf-8"))
        if not data:
            break
    clientSocket.close()
    time.sleep(3)

if __name__ == '__main__':
    serverProgram()