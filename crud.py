import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="6399",
        database="Hidroponica"
    )

# Función para insertar registros en una tabla específica
def ventana_insertar():
    def insertar():
        tabla = entry_tabla.get()
        datos = entry_datos.get().split(", ")
        placeholders = ", ".join(["%s"] * len(datos))
        sql = f"INSERT INTO {tabla} VALUES ({placeholders})"
        try:
            conexion = conectar_mysql()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Insertar", "Registro insertado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Insertar Registro")
    tk.Label(ventana, text="Tabla").grid(row=0, column=0)
    entry_tabla = tk.Entry(ventana)
    entry_tabla.grid(row=0, column=1)
    tk.Label(ventana, text="Datos (separados por coma)").grid(row=1, column=0)
    entry_datos = tk.Entry(ventana)
    entry_datos.grid(row=1, column=1)
    tk.Button(ventana, text="Insertar", command=insertar).grid(row=2, column=0, columnspan=2)

# Función para consultar registros
def ventana_consultar():
    def consultar():
        tabla = entry_tabla.get()
        try:
            conexion = conectar_mysql()
            cursor = conexion.cursor()
            cursor.execute(f"SELECT * FROM {tabla}")
            resultados = cursor.fetchall()
            text_resultados.delete("1.0", tk.END)
            for fila in resultados:
                text_resultados.insert(tk.END, f"{fila}\n")
            cursor.close()
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Consultar Registros")
    tk.Label(ventana, text="Tabla").grid(row=0, column=0)
    entry_tabla = tk.Entry(ventana)
    entry_tabla.grid(row=0, column=1)
    tk.Button(ventana, text="Consultar", command=consultar).grid(row=1, column=0, columnspan=2)
    text_resultados = tk.Text(ventana)
    text_resultados.grid(row=2, column=0, columnspan=2)

# Función para actualizar un registro
def ventana_actualizar():
    def actualizar():
        tabla = entry_tabla.get()
        columna = entry_columna.get()
        nuevo_valor = entry_nuevo_valor.get()
        condicion = entry_condicion.get()
        sql = f"UPDATE {tabla} SET {columna} = %s WHERE {condicion}"
        try:
            conexion = conectar_mysql()
            cursor = conexion.cursor()
            cursor.execute(sql, (nuevo_valor,))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Actualizar", "Registro actualizado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Actualizar Registro")
    tk.Label(ventana, text="Tabla").grid(row=0, column=0)
    entry_tabla = tk.Entry(ventana)
    entry_tabla.grid(row=0, column=1)
    tk.Label(ventana, text="Columna").grid(row=1, column=0)
    entry_columna = tk.Entry(ventana)
    entry_columna.grid(row=1, column=1)
    tk.Label(ventana, text="Nuevo valor").grid(row=2, column=0)
    entry_nuevo_valor = tk.Entry(ventana)
    entry_nuevo_valor.grid(row=2, column=1)
    tk.Label(ventana, text="Condición (e.g., Id_Cultivo = 1)").grid(row=3, column=0)
    entry_condicion = tk.Entry(ventana)
    entry_condicion.grid(row=3, column=1)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=4, column=0, columnspan=2)

# Función para eliminar un registro
def ventana_eliminar():
    def eliminar():
        tabla = entry_tabla.get()
        condicion = entry_condicion.get()
        sql = f"DELETE FROM {tabla} WHERE {condicion}"
        try:
            conexion = conectar_mysql()
            cursor = conexion.cursor()
            cursor.execute(sql)
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Eliminar", "Registro eliminado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Eliminar Registro")
    tk.Label(ventana, text="Tabla").grid(row=0, column=0)
    entry_tabla = tk.Entry(ventana)
    entry_tabla.grid(row=0, column=1)
    tk.Label(ventana, text="Condición (e.g., Id_Cultivo = 3)").grid(row=1, column=0)
    entry_condicion = tk.Entry(ventana)
    entry_condicion.grid(row=1, column=1)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=2, column=0, columnspan=2)

# Ventana principal
root = tk.Tk()
root.title("CRUD MySQL")

tk.Button(root, text="Insertar Registro", command=ventana_insertar).grid(row=0, column=0)
tk.Button(root, text="Consultar Registros", command=ventana_consultar).grid(row=0, column=1)
tk.Button(root, text="Actualizar Registro", command=ventana_actualizar).grid(row=1, column=0)
tk.Button(root, text="Eliminar Registro", command=ventana_eliminar).grid(row=1, column=1)

root.mainloop()
