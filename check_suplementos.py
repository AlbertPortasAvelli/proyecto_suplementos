import json
import datetime
from plyer import notification
import os
import tkinter as tk
from tkinter import ttk
from win10toast import ToastNotifier


def calcular_fecha_fin(fecha_inicio, usos_restantes):
    dia = fecha_inicio
    usados = 0
    
    
    while usados < usos_restantes:
        if dia.weekday() in [0, 1, 2, 3]: #Lunes a Jueves
            usados += 1
        dia += datetime.timedelta(days=1)
    return dia

#Verificar archivo de datos

if not os.path.exists("suplementos.json"):
    with open("suplementos.json", "w") as f:
        json.dump([], f)

#Cargar suplementos

with open("suplementos.json", "r") as f:
    suplementos = json.load(f)
    
hoy = datetime.date.today()
info_suplementos = []

#Proceso principal

for suplemento in suplementos:
    nombre = suplemento["nombre"]
    cantidad_total = suplemento["cantidad_total"]
    uso_diario = suplemento["uso_diario"]
    fecha_inicio = datetime.datetime.strptime(suplemento["fecha_inicio"], "%Y-%m-%d").date()
    
    usos_restantes = int(cantidad_total / uso_diario)
    fecha_fin = calcular_fecha_fin(fecha_inicio, usos_restantes)
    
    #Calcular cuantos dias utiles (lunes-jueves) quedan desde hoy
    
    dia=hoy
    dias_utiles_restantes = 0
    
    while dia < fecha_fin:
        if dia.weekday() in [0, 1, 2, 3]:
            dias_utiles_restantes += 1
        dia += datetime.timedelta(days=1)
      
    #Guardar info para mostrar en tabla  
        
    info_suplementos.append({
            "nombre": nombre,
            "dias_restantes": dias_utiles_restantes,
            "fecha_fin": fecha_fin.strftime("%Y-%m-%d")
        })    
    
    #Norificacion si quedan 14 o 7 dias utiles
    toaster = ToastNotifier()
    if dias_utiles_restantes in [14, 7]:
        toaster.show_toast(
            "⚠️ Suplemento por agotarse",
            f"{nombre} se terminará en {dias_utiles_restantes} días de uso (lunes-jueves).",
            duration=10,  # duración en segundos
            threaded=True  # permite que no bloquee la interfaz
    )

#Crear ventana con tabla
root = tk.Tk()
root.title("📊 Estado de suplementos")


tree = ttk.Treeview(root, columns=("nombre", "dias", "fin"), show="headings")
tree.heading("nombre", text="Suplemento")
tree.heading("dias", text="Días útiles restantes")
tree.heading("fin", text="Fecha estimada de fin")


for item in info_suplementos:
    tree.insert("", tk.END, values=(item["nombre"], item["dias_restantes"], item["fecha_fin"]))


tree.pack(padx=20, pady=20)
root.mainloop()