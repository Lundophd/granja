import pyodbc
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Conexión a SQL Server
def conectar_sqlserver():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=LUNDOP;"
        "DATABASE=Hidroponica;"
        "UID=sa;"
        "PWD=12345678"
    )

# Funciones CRUD
def insertar_registro(tabla, datos):
    # Suponiendo que la tabla tiene 3 columnas, y por eso hay 3 "?"
    placeholders = ", ".join("?" * len(datos))  # len(datos) debe coincidir con el número de columnas de la tabla
    sql = f"INSERT INTO {tabla} VALUES ({placeholders})"
    conexion = conectar_sqlserver()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    cursor.close()
    conexion.close()


def consultar_tabla(tabla):
    conexion = conectar_sqlserver()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM {tabla}")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados

def actualizar_registro(tabla, columna, nuevo_valor, condicion):
    sql = f"UPDATE {tabla} SET {columna} = ? WHERE {condicion}"
    conexion = conectar_sqlserver()
    cursor = conexion.cursor()
    cursor.execute(sql, (nuevo_valor,))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_registro(tabla, condicion):
    sql = f"DELETE FROM {tabla} WHERE {condicion}"
    conexion = conectar_sqlserver()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()
    cursor.close()
    conexion.close()

# Ventana de inserción
def ventana_insertar():
    def insertar():
        tabla = entry_tabla.get()
        datos = entry_datos.get().split(", ")
        try:
            insertar_registro(tabla, datos)
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

# Ventana de consulta
def ventana_consultar():
    def consultar():
        tabla = entry_tabla.get()
        try:
            resultados = consultar_tabla(tabla)
            ventana_resultados(resultados)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Consultar Registros")
    tk.Label(ventana, text="Tabla").grid(row=0, column=0)
    entry_tabla = tk.Entry(ventana)
    entry_tabla.grid(row=0, column=1)
    tk.Button(ventana, text="Consultar", command=consultar).grid(row=1, column=0, columnspan=2)

# Ventana de actualización
def ventana_actualizar():
    def actualizar():
        tabla = entry_tabla.get()
        columna = entry_columna.get()
        nuevo_valor = entry_nuevo_valor.get()
        condicion = entry_condicion.get()
        try:
            actualizar_registro(tabla, columna, nuevo_valor, condicion)
            messagebox.showinfo("Actualizar", "Registro actualizado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Actualizar Registro")
    tk.Label(ventana, text="Tabla").grid(row=0, column=0)
    entry_tabla = tk.Entry(ventana)
    entry_tabla.grid(row=0, column=1)
    tk.Label(ventana, text="Columna a actualizar").grid(row=1, column=0)
    entry_columna = tk.Entry(ventana)
    entry_columna.grid(row=1, column=1)
    tk.Label(ventana, text="Nuevo valor").grid(row=2, column=0)
    entry_nuevo_valor = tk.Entry(ventana)
    entry_nuevo_valor.grid(row=2, column=1)
    tk.Label(ventana, text="Condición").grid(row=3, column=0)
    entry_condicion = tk.Entry(ventana)
    entry_condicion.grid(row=3, column=1)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=4, column=0, columnspan=2)

# Ventana de eliminación
def ventana_eliminar():
    def eliminar():
        tabla = entry_tabla.get()
        condicion = entry_condicion.get()
        try:
            eliminar_registro(tabla, condicion)
            messagebox.showinfo("Eliminar", "Registro eliminado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Eliminar Registro")
    tk.Label(ventana, text="Tabla").grid(row=0, column=0)
    entry_tabla = tk.Entry(ventana)
    entry_tabla.grid(row=0, column=1)
    tk.Label(ventana, text="Condición").grid(row=1, column=0)
    entry_condicion = tk.Entry(ventana)
    entry_condicion.grid(row=1, column=1)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=2, column=0, columnspan=2)

# Ventana de consulta de ventas
def ventana_consultar_ventas():
    def consultar_ventas():
        fecha_inicio = entry_fecha_inicio.get()
        fecha_fin = entry_fecha_fin.get()
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use AAAA-MM-DD.")
            return

        query = """
            SELECT C.Tipo_Planta, COUNT(V.Id_Venta) AS Total_Vendido, SUM(V.Total) AS Ingresos
            FROM Venta V
            JOIN Detalle_Venta DV ON V.Id_Venta = DV.Id_Venta
            JOIN Cultivo C ON DV.Id_Cultivo = C.Id_Cultivo
            WHERE V.Fecha_Venta BETWEEN ? AND ?
            GROUP BY C.Tipo_Planta
        """
        try:
            conexion = conectar_sqlserver()
            cursor = conexion.cursor()
            cursor.execute(query, (fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()
            ventana_resultados(resultados)
            cursor.close()
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = tk.Toplevel()
    ventana.title("Consultar Ventas por Tipo de Cultivo")
    tk.Label(ventana, text="Fecha inicio (YYYY-MM-DD)").grid(row=0, column=0)
    entry_fecha_inicio = tk.Entry(ventana)
    entry_fecha_inicio.grid(row=0, column=1)
    tk.Label(ventana, text="Fecha fin (YYYY-MM-DD)").grid(row=1, column=0)
    entry_fecha_fin = tk.Entry(ventana)
    entry_fecha_fin.grid(row=1, column=1)
    tk.Button(ventana, text="Consultar Ventas", command=consultar_ventas).grid(row=2, column=0, columnspan=2)

# Función para mostrar resultados en una nueva ventana
def ventana_resultados(resultados):
    resultados_window = tk.Toplevel()
    resultados_window.title("Resultados")
    for i, fila in enumerate(resultados):
        tk.Label(resultados_window, text=str(fila)).grid(row=i, column=0)

# Ventana principal
root = tk.Tk()
root.title("CRUD SQL Server")

# Botones principales para cada operación
tk.Button(root, text="Insertar", command=ventana_insertar).grid(row=0, column=0)
tk.Button(root, text="Consultar", command=ventana_consultar).grid(row=0, column=1)
tk.Button(root, text="Actualizar", command=ventana_actualizar).grid(row=1, column=0)
tk.Button(root, text="Eliminar", command=ventana_eliminar).grid(row=1, column=1)
tk.Button(root, text="Consultar Ventas", command=ventana_consultar_ventas).grid(row=2, column=0, columnspan=2)

root.mainloop()
