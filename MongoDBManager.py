from pymongo import MongoClient
import requests


class MongoDBManager:
    def __init__(self,
                 connection_string="mongodb+srv://admin:token1234@cluster0.9hkyufi.mongodb.net/?retryWrites=true&w=majority",database_name="data_cinemas", collection_name="cine"):

        self.connection = self.check_connection()

        if self.connection is True:
            print("Si hay conexion a internet.")
            try:
                print("Conectando a la base de datos...")
                self.client = MongoClient(connection_string)
                self.db = self.client[database_name]
                self.collection = self.db[collection_name]
                print("Conexión exitosa")
            except:
                print("Error al conectarse a la base de datos")
        elif self.connection is False:
            print("No hay conexión a internet.")

    def insert(self, data):
        try:
            for item in data:
                if not self.collection.find_one(item):
                    self.collection.insert_one(item)
            print("Datos guardados en MongoDB")
        except Exception as e:
            print(f"Error al guardar datos en MongoDB: {e}")

    def check_connection(self):
        url = "http://www.google.com"
        timeout = 5
        try:
            print("Verificando conexion a internet...")
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False

    def find(self):
        try:
            data = self.collection.find()
            data = list(data)
            for item in data:
                print("\n")
                for key, value in item.items():
                    print(f"{key}: {value}")
        except Exception as e:
            print(f"Error al buscar datos: {e}")

    def update(self, query, new_values):
        try:
            document = self.collection.find_one(query)
            if document is not None:
                print(document)
                self.collection.update_one(query, {"$set": new_values})
                print("Datos actualizados")
            else:
                print("No se encontró el documento para actualizar")
        except Exception as e:
            print(f"Error al actualizar datos: {e}")

    def menu(self):
        print("\n *** Menu MongoDB ***")
        print("[2] Buscar")
        print("[3] Actualizar")
        print("[4] Salir")
        opcion = input("Opción> ")
        return opcion

    def main(self):
        kaka = None
        while True:
            opcion = self.menu()
            if opcion == "2":
                kaka = self.find()
            elif opcion == "3":
                kaka = self.update()
            elif opcion == "4":
                print("Saliendo...")
                break
            else:
                print("Opción no válida")


if __name__ == "__main__":
    mongo = MongoDBManager(collection_name="cinemas")
    mongo.find()

    mongo.update({"_id": "65ceba9af04e3167d4eead63"}, {"name": "Cinepolis, CDMX.", "ubicacion": "CDMX"})
    mongo.find()