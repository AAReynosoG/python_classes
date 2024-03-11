from ConsolaFuncion import ConsolaFuncion
from sala import Sala
from MongoDBManager import MongoDBManager
class SalaConsola(Sala):
    def __init__(self, useJson=None):
        super().__init__()
        self.salas = Sala()
        self.useJson = useJson        
        if useJson:
            self.init_Json()        
        
    def init_Json(self):
        self.salas.isolate_objetos(self.salas.read_json("json/salas.json"))

        
    def mostrar(self):
        self.salas.show()

    def add(self):
        dsa = True
        while dsa:
            numero = input("Ingrese el número de la sala: ")

            num_asientos = input("Ingrese el número de asientos: ")
            hora_limpieza = input("Ingrese la hora de limpieza: ")
            max_personas = input("Ingrese el número máximo de personas: ")

            consola = ConsolaFuncion(useJson=self.useJson)
            funciones = consola.init_main()

            sala = Sala(numero, int(num_asientos), hora_limpieza, int(max_personas), funciones)
            self.salas.agregar(sala)

            if self.useJson:
                self.guardarJson()
                self.guardarMongoDB(json_path="json/salas.json")

            asd = input("¿Desea agregar otra sala? [y][n]").lower()
            if asd == "n":
                dsa = False

        return self.salas

    def eliminar (self):
        index = input("Ingrese el indice de la sala a eliminar: ")
        self.salas.eliminar(int(index))

    def modificar(self):
        index = int(input("Ingrese el índice de la sala a modificar: "))
        sala_modificar = self.salas.showIndex(int(index))
        if sala_modificar:
            print("Sala a modificar:")
            print(sala_modificar)
            print("Seleccione qué atributo desea modificar:")
            print("1. Número de la sala")
            print("2. Número de asientos")
            print("3. Hora de limpieza")
            print("4. Número máximo de personas")
            print("5. Funciones")

            opcion_modificar = input("Ingrese el número de la opción que desea modificar: ")

            if opcion_modificar == "1":
                sala_modificar.numero = input("Ingrese el nuevo número de la sala: ")
            elif opcion_modificar == "2":
                sala_modificar.num_asientos = input("Ingrese el nuevo número de asientos: ")
            elif opcion_modificar == "3":
                sala_modificar.hora_limpieza = input("Ingrese la nueva hora de limpieza: ")
            elif opcion_modificar == "4":
                sala_modificar.max_personas = input("Ingrese el nuevo número máximo de personas: ")
            elif opcion_modificar == "5":

                consola = ConsolaFuncion(useJson=False)
                consola.funciones = sala_modificar.funciones
                consola.init_main()
                self.salas.modificar(index, sala_modificar)
            else:
                print("Opción no válida. No se realizaron modificaciones.")
        else:
            print("No se encontró ninguna sala con ese ID.")

        if self.useJson:
            self.guardarJson()
            self.guardarMongoDB(json_path="json/salas.json")


    
    def guardarJson(self):
        salas_info = []
        for s in self.salas.informacion:
            salas_info.append(s.to_dictionary())
        self.salas.save_json("json/salas.json", data=salas_info)

    def guardarMongoDB(self, json_path=None):
        data = self.salas.read_json(json_path)
        mongo = MongoDBManager(collection_name="rooms")
        mongo.insert(data)
        print("Datos recuperados del archivo JSON")

    def init_main(self):
        result = None
        while True:
            print("\n *** Menu Salas  ***")
            print("[1] Agregar")
            print("[2] Mostrar")
            print("[3] Eliminar")
            print("[4] Modificar")
            print("[5] Guardar Json")
            print("[6] Salir")

            opcion = input("Opción> ")

            if opcion == "1":
                result = self.add()
            elif opcion == "2":
                print("Salas:")
                self.mostrar()
            elif opcion == "3":
                self.eliminar()
            elif opcion == "4":
                self.modificar()
            elif opcion == "5":
                self.guardarJson()
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
        return result

if __name__ == "__main__":
    from SalaConsola import SalaConsola
    from sala import Sala
    consola = SalaConsola()
    consola.init_main()
    


    
        