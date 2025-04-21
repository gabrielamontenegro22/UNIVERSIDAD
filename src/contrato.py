import tkinter as tk
from tkinter import ttk, messagebox

def calcular_pago(tipo_contrato, horas_normales, horas_nocturnas, horas_dominicales):
    try:
        horas_normales = int(horas_normales)
        horas_nocturnas = int(horas_nocturnas)
        horas_dominicales = int(horas_dominicales)

        if tipo_contrato not in ["Tiempo Completo", "Medio Tiempo"]:
            return None

        # Nueva validación importante:
        if horas_normales + horas_nocturnas + horas_dominicales > 192:
            return None

        if any(h < 0 or h > 720 for h in [horas_normales, horas_nocturnas, horas_dominicales]):
            return None

        tarifa_hora = 1423500 / 192
        pago_bruto = (horas_normales * tarifa_hora) + (horas_nocturnas * tarifa_hora * 1.35) + (horas_dominicales * tarifa_hora * 1.75)

        descuento_salud = pago_bruto * 0.04
        descuento_pension = pago_bruto * 0.04
        descuento_arl = pago_bruto * 0.0522 if tipo_contrato == "Tiempo Completo" else 0

        total_descuentos = descuento_salud + descuento_pension + descuento_arl
        pago_neto = pago_bruto - total_descuentos

        return {
            "pago_bruto": pago_bruto,
            "descuento_salud": descuento_salud,
            "descuento_pension": descuento_pension,
            "descuento_arl": descuento_arl,
            "total_descuentos": total_descuentos,
            "pago_neto": pago_neto
        }

    except ValueError:
        return None



# --------------- INTERFAZ GRÁFICA ---------------
def calcular_desde_ui():
    tipo_contrato = contrato_var.get()
    horas_normales = entry_horas_normales.get()
    horas_nocturnas = entry_horas_nocturnas.get()
    horas_dominicales = entry_horas_dominicales.get()

    resultado = calcular_pago(tipo_contrato, horas_normales, horas_nocturnas, horas_dominicales)

    if resultado:
        resultado_texto = f"""
        Pago Bruto: ${resultado['pago_bruto']:,.2f} COP
        Descuento Salud: ${resultado['descuento_salud']:,.2f} COP
        Descuento Pensión: ${resultado['descuento_pension']:,.2f} COP
        Descuento ARL: ${resultado['descuento_arl']:,.2f} COP
        Total Descuentos: ${resultado['total_descuentos']:,.2f} COP
        Pago Neto: ${resultado['pago_neto']:,.2f} COP
        """
        messagebox.showinfo("Sueldo del docente", resultado_texto)
    else:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# --------------------- SOLO SE EJECUTA SI CORREMOS contrato.py ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("CALCULANDO EL SUELDO FET")
    root.geometry("500x400")
    root.configure(bg="#dbb5ee")

    # Frame principal
    frame = tk.Frame(root, bg="#dbb5ee")
    frame.pack(pady=20)

    # Tipo de contrato
    tk.Label(frame, text="Tipo de Contrato:", bg="#dbb5ee").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    contrato_var = ttk.Combobox(frame, values=["Medio Tiempo", "Tiempo Completo"])
    contrato_var.grid(row=0, column=1, padx=10, pady=5)
    contrato_var.current(0)

    # Campos de entrada
    tk.Label(frame, text="Horas Trabajadas:", bg="#dbb5ee").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_horas_normales = tk.Entry(frame, bg="#d8b2ff", fg="black")
    entry_horas_normales.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Horas Nocturnas:", bg="#dbb5ee").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_horas_nocturnas = tk.Entry(frame, bg="#d8b2ff", fg="black")
    entry_horas_nocturnas.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame, text="Horas Dominicales y Festivas:", bg="#dbb5ee").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_horas_dominicales = tk.Entry(frame, bg="#d8b2ff", fg="black")
    entry_horas_dominicales.grid(row=3, column=1, padx=10, pady=5)

    # Botón para calcular
    tk.Button(root, text="Calcular Pago", command=calcular_desde_ui, bg="blue", fg="white").pack(pady=10)

    # Ejecutar la aplicación
    root.mainloop()
