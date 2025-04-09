import json
import tkinter as tk
from tkinter import messagebox

def guardar():
    nombre = entry_nombre.get()
    total = entry_total.get()
    diario = entry_diario.get()
    fecha = entry_fecha.get()
    
    try:
        nuevo = {
            "nombre": nombre,
            "cantidad_total": int(total),
            "uso_diario": int(diario),
            "fecha_inicio": fecha
        }
        
        with open("suplementos.json", "r") as f:
            suplementos = json.load(f)
            
        suplementos.append(nuevo)
        
        with open("suplementos.json", "w") as f:
            json.dump(suplementos, f, indent=4)
            
            
        messagebox.showinfo("Guardado", "Suplemento añadido correctamente")
        window.destroy()
        
    except Exception as e:
        messagebox.showerror("Error", str(e))
        

window = tk.Tk()
window.title("Añadir Suplemento")

tk.Label(window, text="Nombre").pack()
entry_nombre = tk.Entry(window)
entry_nombre.pack()


tk.Label(window, text="Cantidad total (g)").pack()
entry_total = tk.Entry(window)
entry_total.pack()


tk.Label(window, text="Uso diario (g)").pack()
entry_diario = tk.Entry(window)
entry_diario.pack()

tk.Label(window, text="Fecha de inicio (YYYY-MM-DD)").pack()
entry_fecha = tk.Entry(window)
entry_fecha.pack()

tk.Button(window, text="Guardar", command=guardar).pack(pady=10)


window.mainloop()