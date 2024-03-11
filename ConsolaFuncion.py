from Funcion import Funcion
from MongoDBManager import MongoDBManager

class ConsolaFuncion():
    def __init__ (self, useJson=None):
        super().__init__()
        if useJson:
            self.funciones = Funcion()
            self.useJson = useJson
            self.init_Json()
        else:
            self.funciones = Funcion()
            self.useJson = useJson
        
        
    def init_Json(self):
        self.funciones.isolate_funciones_objetos(self.funciones.read_json("json/funciones.json"))
    

    def mostrar(self):
        self.funciones.show()


    def add(self):
        cycle = True
        while cycle:
            Nfuncion = input(f"Ingrese el número de la función: ")
            hora_inicio = input("Ingrese la hora de inicio (HH:MM): ")
            pelicula = input("Ingrese el nombre de la película: ")
            fecha_estreno = input("Ingrese la fecha (DD/MM/YYYY): ")
            hora_fin = input("Ingrese la hora de fin (HH:MM): ")
            costo_boleto = input("Ingrese el precio: ")


            instancia = Funcion(int(Nfuncion), hora_inicio, pelicula, fecha_estreno, hora_fin, costo_boleto)
            self.funciones.agregar(instancia)

            if self.useJson:
                self.guardarJson()
                self.guardarMongoDB(json_path="json/funciones.json")

            opt = input("¿Desea agregar otra Funcion? [y][n]").lower()
            if opt == "n":
                cycle = False

        return self.funciones


    def eliminar(self):
        id_eliminar = input("Ingrese el indice de la función a eliminar: ")
        self.funciones.eliminar(int(id_eliminar))
        if self.useJson:
            self.guardarJson()


    def modificar(self):
        indice = int(input("Ingrese el indice de la función a modificar: "))
        funcion_modificar = self.funciones.showIndex(int(indice))

        if funcion_modificar:

            print("Función a modificar:")
            print(funcion_modificar)
            print("Seleccione qué atributo desea modificar:")
            print("1. Hora de inicio")
            print("2. Nombre de la película")
            print("3. Fecha")
            print("4. Hora de fin")
            print("5. Precio")

            opcion_modificar = input("Ingrese el número de la opción que desea modificar: ")

            if opcion_modificar == "1":
                funcion_modificar.hora_inicio = input("Ingrese la nueva hora de inicio (HH:MM): ")
            elif opcion_modificar == "2":
                funcion_modificar.pelicula = input("Ingrese el nuevo nombre de la película: ")
            elif opcion_modificar == "3":
                funcion_modificar.fecha_estreno = input("Ingrese la nueva fecha (DD/MM/YYYY): ")
            elif opcion_modificar == "4":
                funcion_modificar.hora_fin = input("Ingrese la nueva hora de fin (HH:MM): ")
            elif opcion_modificar == "5":
                funcion_modificar.costo_boleto = int(input("Ingrese el nuevo precio: "))
            else:
                print("Opción no válida. No se realizaron modificaciones.")
        else:
            print("No se encontró ninguna función con ese ID.")

        if self.useJson:
            self.guardarJson()
            self.guardarMongoDB(json_path="json/funciones.json")

    def guardarJson(self):
        funciones_info = [] 
        for f in self.funciones.informacion:
            funciones_info.append(f.to_dictionary())
        self.funciones.save_json("json/funciones.json", data=funciones_info)

        
    def isolate_objetos(self):
        data = self.funciones.read_json("json/funciones.json")
        self.funciones.isolate_objetos(data)
        for f in self.funciones.informacion_iso:
            self.funciones.agregar(f)

    def guardarMongoDB(self, json_path=None):
        data = self.funciones.read_json(json_path)
        mongo = MongoDBManager(collection_name="functions")
        mongo.insert(data)
        print("Datos recuperados del archivo JSON")

    def init_main(self):
        result = None
        while True:
            print("\n *** Menu Funciones  ***")
            print("[1]. Agregar")
            print("[2]. Mostrar")
            print("[3]. Eliminar")
            print("[4]. Modificar")
            print("[5]. Guardar en JSON")
            print("[7]. Salir")
            opcion = input("Opción> ")

            if opcion == "1":
                result = self.add()
            elif opcion == "2":
                print("Funciones:")
                self.mostrar()
            elif opcion == "3":
                self.eliminar()
            elif opcion == "4":
                self.modificar()
            elif opcion == "5":
                self.guardarJson()
            elif opcion == "7":
                print("Saliendo...")
                break
        return result

        
            
if __name__ == "__main__":
    consola = ConsolaFuncion()
    consola.init_main()

