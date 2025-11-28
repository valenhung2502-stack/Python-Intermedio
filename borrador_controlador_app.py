from borrador_modelo_app import ViajesDB

class Controlador:
    def __init__(self):
        self.modelo = ViajesDB()

    def obtener_todos(self):
        try:
            cursor = self.modelo.con.cursor()
            cursor.execute("SELECT dni, nombre, apellido, pasaje, horario, destino, fecha FROM viajes")
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener los viajes: {str(e)}")

    def agregar_viaje(self, dni, nombre, apellido, pasaje, horario, destino, fecha):

        if not self.modelo.validar_dni(dni):
            raise Exception("El DNI no es válido")

        if not self.modelo.validar_nombre(nombre):
            raise Exception("El nombre no es válido")

        return self.modelo.agregar(dni, nombre, apellido, pasaje, horario, destino, fecha)

    def borrar_viaje(self, dni):

        if not self.modelo.validar_dni(dni):
            raise Exception("DNI inválido")

        return self.modelo.borrar(dni)

if __name__ == '__main__':
    from intento_vista_app_viajes import App_viajes
    app = App_viajes()
    app.mainloop()