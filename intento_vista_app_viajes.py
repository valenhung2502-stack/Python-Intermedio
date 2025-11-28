from tkinter import Tk, Label, StringVar, DoubleVar, Entry, Button, W, E
from tkinter import ttk, messagebox
from borrador_controlador_app import Controlador

objcont = Controlador()
db = objcont.modelo


class Ventana():
    def __init__(self):
        root = Tk()
        root.title("Administrar Viajes")
        root.geometry("900x600")
        
        Label(root, text="Ingrese los datos del viaje", bg="DarkOrchid3", fg="thistle1", width=60, height=1).grid(row=0, column=0, columnspan=4, sticky=W+E, padx=1, pady=1)
        
        Label(root, text="NOMBRE").grid(row=1, column=0, sticky=W, padx=5)
        Label(root, text="APELLIDO").grid(row=2, column=0, sticky=W, padx=5)
        Label(root, text="PASAJE").grid(row=3, column=0, sticky=W, padx=5)
        Label(root, text="HORARIO").grid(row=4, column=0, sticky=W, padx=5)
        Label(root, text="DNI").grid(row=5, column=0, sticky=W, padx=5)
        
        Label(root, text="DESTINO").grid(row=1, column=2, sticky=W, padx=5)
        Label(root, text="FECHA").grid(row=2, column=2, sticky=W, padx=5)

        a_val, b_val, c_val, d_val, e_val, f_val, g_val = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        w_ancho = 20

        Entry(root, textvariable=a_val, width=w_ancho).grid(row=1, column=1, padx=5, pady=5)
        Entry(root, textvariable=b_val, width=w_ancho).grid(row=2, column=1, padx=5, pady=5)
        Entry(root, textvariable=c_val, width=w_ancho).grid(row=3, column=1, padx=5, pady=5)
        Entry(root, textvariable=d_val, width=w_ancho).grid(row=4, column=1, padx=5, pady=5)
        Entry(root, textvariable=e_val, width=w_ancho).grid(row=5, column=1, padx=5, pady=5)
        
        Entry(root, textvariable=f_val, width=w_ancho).grid(row=1, column=3, padx=5, pady=5)
        Entry(root, textvariable=g_val, width=w_ancho).grid(row=2, column=3, padx=5, pady=5)

        tree = ttk.Treeview(root)
        tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        tree.column("#0", width=90, anchor=W)
        tree.column("col1", width=120)
        tree.column("col2", width=120)
        tree.column("col3", width=120)
        tree.column("col4", width=100)
        tree.column("col5", width=120)
        tree.column("col6", width=100)
        tree.heading("#0", text="DNI")
        tree.heading("col1", text="Nombre")
        tree.heading("col2", text="Apellido")
        tree.heading("col3", text="Pasaje")
        tree.heading("col4", text="Horario")
        tree.heading("col5", text="Destino")
        tree.heading("col6", text="Fecha")
        tree.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky=W+E)

        Button(root, text="Guardar", command=lambda: self.guardar_vista(a_val, b_val, c_val, d_val, e_val, f_val, g_val, tree), bg="green", fg="white").grid(row=6, column=0, padx=5, pady=5)
        Button(root, text="Modificar", command=lambda: self.modificar_vista(a_val, b_val, c_val, d_val, e_val, f_val, g_val, tree), bg="blue", fg="white").grid(row=6, column=1, padx=5, pady=5)
        Button(root, text="Eliminar", command=lambda: self.eliminar_vista(tree), bg="red", fg="white").grid(row=6, column=2, padx=5, pady=5)
        Button(root, text="Limpiar", command=lambda: self.limpiar_vista(a_val, b_val, c_val, d_val, e_val, f_val, g_val), bg="gray", fg="white").grid(row=6, column=3, padx=5, pady=5)
        
        try:
            self.actualizar_treeview(tree)
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar: {str(e)}")
        
        root.mainloop()

    def actualizar_treeview(self, tree):
        try:
            tree.delete(*tree.get_children())
            resultados = db.obtener_registros()
            for fila in resultados:
                tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la lista: {str(e)}")

    def guardar_vista(self, a_val, b_val, c_val, d_val, e_val, f_val, g_val, tree):
        try:
            nombre = a_val.get().strip()
            apellido = b_val.get().strip()
            pasaje = c_val.get().strip()
            horario = d_val.get().strip()
            dni = e_val.get().strip()
            destino = f_val.get().strip()
            fecha = g_val.get().strip()
            
            if not nombre or not apellido or not pasaje or not horario or not dni or not destino or not fecha:
                raise ValueError("Todos los campos son obligatorios")
            
            resultado = db.agregar(dni, nombre, apellido, pasaje, horario, destino, fecha)
            
            if "correctamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
                self.limpiar_vista(a_val, b_val, c_val, d_val, e_val, f_val, g_val)
                self.actualizar_treeview(tree)
            else:
                messagebox.showerror("Error", resultado)
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def eliminar_vista(self, tree):
        try:
            seleccion = tree.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un viaje para eliminar")
            
            item = tree.item(seleccion)
            dni = item['text']
            
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este viaje?")
            if not confirmacion:
                return
            
            resultado = db.borrar(dni)
            
            if "correctamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
                self.actualizar_treeview(tree)
            else:
                messagebox.showerror("Error", resultado)
                
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al borrar: {str(e)}")

    def modificar_vista(self, a_val, b_val, c_val, d_val, e_val, f_val, g_val, tree):
        try:
            seleccion = tree.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un viaje para modificar")
            
            nombre = a_val.get().strip()
            apellido = b_val.get().strip()
            pasaje = c_val.get().strip()
            horario = d_val.get().strip()
            dni = e_val.get().strip()
            destino = f_val.get().strip()
            fecha = g_val.get().strip()
            
            if not nombre or not apellido or not pasaje or not horario or not dni or not destino or not fecha:
                raise ValueError("Todos los campos son obligatorios")
            
            item = tree.item(seleccion)
            dni_original = item['text']
            
            resultado = db.modificar(dni_original, nombre, apellido, pasaje, horario, destino, fecha)
            
            if "correctamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
                self.limpiar_vista(a_val, b_val, c_val, d_val, e_val, f_val, g_val)
                self.actualizar_treeview(tree)
            else:
                messagebox.showerror("Error", resultado)
                
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def limpiar_vista(self, a_val, b_val, c_val, d_val, e_val, f_val, g_val):
        a_val.set("")
        b_val.set("")
        c_val.set("")
        d_val.set("")
        e_val.set("")
        f_val.set("")
        g_val.set("")


if __name__ == "__main__":
    app = Ventana()