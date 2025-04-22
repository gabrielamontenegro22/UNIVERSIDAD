def calcular_pago(tipo_contrato, horas_normales, horas_nocturnas, horas_dominicales):
    try:
        horas_normales = int(horas_normales)
        horas_nocturnas = int(horas_nocturnas)
        horas_dominicales = int(horas_dominicales)

        if tipo_contrato not in ["Tiempo Completo", "Medio Tiempo"]:
            return None

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