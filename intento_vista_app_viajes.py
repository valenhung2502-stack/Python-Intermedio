from tkinter import Tk, Label, StringVar, DoubleVar, Entry, Button, W, E
from tkinter import ttk, messagebox

class Ventana():
    def __init__(self):
        root = Tk()
        Label(root, text="Ingrese sus datos", bg="DarkOrchid3", fg="thistle1", width=60).grid(row=0, column=0, columnspan=4, sticky=W+E)
        Label(root, text="NOMBRE").grid(row=1, column=0, sticky=W)
        Label(root, text="APELLIDO").grid(row=2, column=0, sticky=W)
        Label(root, text="TELEFONO").grid(row=3, column=0, sticky=W)

        a_val, b_val, c_val = StringVar(), StringVar(), StringVar()
        w_ancho = 20

        Entry(root, textvariable=a_val, width=w_ancho).grid(row=1, column=1)
        Entry(root, textvariable=b_val, width=w_ancho).grid(row=2, column=1)
        Entry(root, textvariable=c_val, width=w_ancho).grid(row=3, column=1)

        tree = ttk.Treeview(root)
        tree["columns"] = ("col1", "col2", "col3")
        tree.column("#0", width=90, anchor=W)
        tree.column("col1", width=200)
        tree.column("col2", width=200)
        tree.column("col3", width=200)
        tree.heading("#0", text="ID")
        tree.heading("col1", text="Nombre")
        tree.heading("col2", text="Apellido")
        tree.heading("col3", text="Telefono")
        tree.grid(row=10, column=0, columnspan=4)

        Button(root, text="Alta", command=lambda: self.alta_vista(a_val, b_val, c_val, tree)).grid(row=6, column=0)
        Button(root, text="Consultar", command=lambda: self.consultar_vista(a_val, tree)).grid(row=6, column=1)
        Button(root, text="Borrar", command=lambda: self.borrar_vista(tree)).grid(row=6, column=2)
        
        try:
            self.actualizar_treeview(tree)
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar: {str(e)}")
        
        root.mainloop()

    def actualizar_treeview(self, tree):
        try:
            tree.delete(*tree.get_children())
            resultados = objcont.obtener_todos()
            for fila in resultados:
                tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la lista: {str(e)}")

    def alta_vista(self, a_val, b_val, c_val, tree):
        try:
            nombre = a_val.get().strip()
            apellido = b_val.get().strip()
            telefono = c_val.get().strip()
            
            if not nombre or not apellido or not telefono:
                raise ValueError("Todos los campos son obligatorios")
            
            resultado = objcont.alta_controlador(nombre, apellido, telefono)
            
            if "correctamente" in resultado:
                messagebox.showinfo("Alta", resultado)
                # Limpiar campos solo si fue exitoso
                a_val.set("")
                b_val.set("")
                c_val.set("")
                self.actualizar_treeview(tree)
            else:
                messagebox.showerror("Error", resultado)
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def borrar_vista(self, tree):
        try:
            seleccion = tree.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un contacto para borrar")
            
            item = tree.item(seleccion)
            mi_id = item['text']
            
            # Confirmación antes de borrar
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este contacto?")
            if not confirmacion:
                return
            
            resultado = objcont.borrar_controlador(mi_id)
            
            if "correctamente" in resultado:
                messagebox.showinfo("Borrado", resultado)
                self.actualizar_treeview(tree)
            else:
                messagebox.showerror("Error", resultado)
                
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al borrar: {str(e)}")

    def consultar_vista(self, a_val, tree):
        try:
            nombre = a_val.get().strip()
            
            if not nombre:
                raise ValueError("Debe ingresar un nombre para buscar")
            
            resultados = objcont.consultar_controlador(nombre)
            
            if resultados:
                # Actualizar el treeview solo con los resultados
                tree.delete(*tree.get_children())
                for fila in resultados:
                    tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))
                messagebox.showinfo("Consulta", f"Se encontraron {len(resultados)} resultado(s)")
            else:
                messagebox.showinfo("Consulta", "No se encontraron coincidencias.")
                # Restaurar todos los registros
                self.actualizar_treeview(tree)
                
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error en la consulta: {str(e)}")