
import sqlite3
import re
from Mi_regex import MisRegex

objmiregex = MisRegex()

class ViajesDB:
    def __init__(self, db_path="viajes.db"):
        try:
            self.con = sqlite3.connect(db_path)
            self.db_path = db_path
            self._crear_tabla()
        except sqlite3.Error as e:
            raise Exception(f"Error al conectar con la base de datos: {str(e)}")

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _crear_tabla(self):
        try:
            cursor = self.con.cursor()
            sql = """
            CREATE TABLE IF NOT EXISTS viajes (
                dni TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                pasaje TEXT,
                horario TEXT,
                destino TEXT,
                fecha TEXT
            )
            """
            cursor.execute(sql)
            self.con.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al crear la tabla: {str(e)}")

    def agregar(self, dni, nombre, apellido, pasaje, horario, destino, fecha):
        try:
            if not dni or not nombre or not apellido or not pasaje or not horario or not destino or not fecha:
                raise ValueError("Todos los campos son obligatorios")
            
            cursor = self.con.cursor()
            sql = "INSERT INTO viajes (dni, nombre, apellido, pasaje, horario, destino, fecha) VALUES (?, ?, ?, ?, ?, ?, ?)"
            data = (dni, nombre, apellido, pasaje, horario, destino, fecha)
            cursor.execute(sql, data)
            self.con.commit()
            return "Viaje agregado correctamente"
        except sqlite3.IntegrityError as e:
            return f"Error: El DNI {dni} ya existe"
        except sqlite3.Error as e:
            return f"Error en la base de datos: {str(e)}"
        except ValueError as e:
            return f"Error de validación: {str(e)}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"

    def borrar(self, dni):
        try:
            assert dni, "El DNI no puede estar vacío"
            
            cursor = self.con.cursor()
            
            # Verificar si existe el registro
            sql_check = "SELECT * FROM viajes WHERE dni = ?"
            cursor.execute(sql_check, (dni,))
            if not cursor.fetchone():
                raise ValueError(f"No existe un viaje con DNI {dni}")
            
            sql = "DELETE FROM viajes WHERE dni = ?"
            cursor.execute(sql, (dni,))
            self.con.commit()
            return "Viaje eliminado correctamente"
        except sqlite3.Error as e:
            return f"Error en la base de datos: {str(e)}"
        except (ValueError, AssertionError) as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"

    def obtener_registros(self):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM viajes ORDER BY dni ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error al consultar registros: {str(e)}")

    def modificar(self, dni_original, nombre, apellido, pasaje, horario, destino, fecha):
        try:
            if not dni_original or not nombre or not apellido or not pasaje or not horario or not destino or not fecha:
                raise ValueError("Todos los campos son obligatorios")
            
            cursor = self.con.cursor()
            sql = "UPDATE viajes SET nombre=?, apellido=?, pasaje=?, horario=?, destino=?, fecha=? WHERE dni=?"
            data = (nombre, apellido, pasaje, horario, destino, fecha, dni_original)
            cursor.execute(sql, data)
            self.con.commit()
            return "Viaje modificado correctamente"
        except sqlite3.Error as e:
            return f"Error en la base de datos: {str(e)}"
        except ValueError as e:
            return f"Error de validación: {str(e)}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"

    def consultar_por_dni(self, dni):
        try:
            if not dni:
                raise ValueError("Debe ingresar un DNI para buscar")
            
            cursor = self.con.cursor()
            sql = "SELECT * FROM viajes WHERE dni LIKE ?"
            cursor.execute(sql, ('%' + dni + '%',))
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error al consultar por DNI: {str(e)}")
        except ValueError as e:
            raise e