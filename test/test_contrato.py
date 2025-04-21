import unittest
from src.contrato import calcular_pago

class TestCalculoPago(unittest.TestCase):

    def test_horas_normales(self):
        resultado = calcular_pago("Tiempo Completo", 40, 0, 0)
        self.assertIsNotNone(resultado)
        self.assertGreater(resultado["pago_neto"], 0)

    def test_horas_nocturnas(self):
        resultado = calcular_pago("Tiempo Completo", 0, 20, 0)
        self.assertIsNotNone(resultado)
        self.assertGreater(resultado["pago_neto"], 0)

    def test_horas_dominicales(self):
        resultado = calcular_pago("Tiempo Completo", 0, 0, 10)
        self.assertIsNotNone(resultado)
        self.assertGreater(resultado["pago_neto"], 0)

    def test_horas_negativas(self):
        resultado = calcular_pago("Tiempo Completo", -10, 5, 5)
        self.assertIsNone(resultado)

    def test_exceso_horas(self):
        resultado = calcular_pago("Tiempo Completo", 1000, 0, 0)
        self.assertIsNone(resultado)

    def test_pago_total_correcto(self):
        tipo_contrato = "Tiempo Completo"
        horas_normales = 100
        horas_nocturnas = 20
        horas_dominicales = 10

        tarifa_hora = 1423500 / 192
        pago_bruto_esperado = (
            horas_normales * tarifa_hora +
            horas_nocturnas * tarifa_hora * 1.35 +
            horas_dominicales * tarifa_hora * 1.75
        )
        descuento_salud_esperado = pago_bruto_esperado * 0.04
        descuento_pension_esperado = pago_bruto_esperado * 0.04
        descuento_arl_esperado = pago_bruto_esperado * 0.0522
        total_descuentos_esperado = (
            descuento_salud_esperado + descuento_pension_esperado + descuento_arl_esperado
        )
        pago_neto_esperado = pago_bruto_esperado - total_descuentos_esperado

        resultado = calcular_pago(tipo_contrato, horas_normales, horas_nocturnas, horas_dominicales)

        self.assertAlmostEqual(resultado["pago_bruto"], pago_bruto_esperado, places=2)
        self.assertAlmostEqual(resultado["descuento_salud"], descuento_salud_esperado, places=2)
        self.assertAlmostEqual(resultado["descuento_pension"], descuento_pension_esperado, places=2)
        self.assertAlmostEqual(resultado["descuento_arl"], descuento_arl_esperado, places=2)
        self.assertAlmostEqual(resultado["total_descuentos"], total_descuentos_esperado, places=2)
        self.assertAlmostEqual(resultado["pago_neto"], pago_neto_esperado, places=2)

    def test_descuento_salud_correcto(self):
        tipo_contrato = "Tiempo Completo"
        horas_normales = 50
        horas_nocturnas = 10
        horas_dominicales = 5

        tarifa_hora = 1423500 / 192
        pago_bruto = (
            horas_normales * tarifa_hora +
            horas_nocturnas * tarifa_hora * 1.35 +
            horas_dominicales * tarifa_hora * 1.75
        )
        descuento_salud_esperado = pago_bruto * 0.04

        resultado = calcular_pago(tipo_contrato, horas_normales, horas_nocturnas, horas_dominicales)
        
        self.assertAlmostEqual(resultado["descuento_salud"], descuento_salud_esperado, places=2)

    def test_descuento_pension_correcto(self):
        tipo_contrato = "Tiempo Completo"
        horas_normales = 50
        horas_nocturnas = 10
        horas_dominicales = 5

        tarifa_hora = 1423500 / 192
        pago_bruto = (
            horas_normales * tarifa_hora +
            horas_nocturnas * tarifa_hora * 1.35 +
            horas_dominicales * tarifa_hora * 1.75
        )
        descuento_pension_esperado = pago_bruto * 0.04

        resultado = calcular_pago(tipo_contrato, horas_normales, horas_nocturnas, horas_dominicales)
        
        self.assertAlmostEqual(resultado["descuento_pension"], descuento_pension_esperado, places=2)

    def test_descuento_arl_solo_tiempo_completo(self):
        resultado_tiempo_completo = calcular_pago("Tiempo Completo", 40, 0, 0)
        resultado_medio_tiempo = calcular_pago("Medio Tiempo", 40, 0, 0)
        
        self.assertGreater(resultado_tiempo_completo["descuento_arl"], 0)
        self.assertEqual(resultado_medio_tiempo["descuento_arl"], 0)

    def test_salario_alto_descuentos_proporcionales(self):
        resultado = calcular_pago("Tiempo Completo", 100, 50, 42)  # 192 horas
        
        self.assertGreater(resultado["descuento_salud"], 0)
        self.assertGreater(resultado["descuento_pension"], 0)
        self.assertGreater(resultado["descuento_arl"], 0)
        self.assertAlmostEqual(resultado["descuento_salud"], resultado["pago_bruto"] * 0.04, places=2)
        self.assertAlmostEqual(resultado["descuento_pension"], resultado["pago_bruto"] * 0.04, places=2)
        self.assertAlmostEqual(resultado["descuento_arl"], resultado["pago_bruto"] * 0.0522, places=2)

    def test_tipo_contrato_invalido(self):
        resultado = calcular_pago("Freelance", 10, 5, 2)
        self.assertIsNone(resultado)

    def test_horas_totales_exactamente_maximo(self):
        resultado = calcular_pago("Tiempo Completo", 100, 50, 42)  # total = 192
        self.assertIsNotNone(resultado)
        self.assertGreater(resultado["pago_neto"], 0)

    def test_horas_totales_superan_maximo(self):
        resultado = calcular_pago("Tiempo Completo", 100, 50, 50)  # total = 200
        self.assertIsNone(resultado)

    def test_pago_cero_horas(self):
        resultado = calcular_pago("Tiempo Completo", 0, 0, 0)
        self.assertEqual(resultado["pago_neto"], 0)

    def test_nocturnas_dominicales_negativas(self):
        resultado = calcular_pago("Tiempo Completo", 20, -5, -3)
        self.assertIsNone(resultado)

    def test_pago_neto_nunca_negativo(self):
        resultado = calcular_pago("Tiempo Completo", 10, 5, 3)
        self.assertGreaterEqual(resultado["pago_neto"], 0)

    def test_descuentos_igual_suma_individual(self):
        resultado = calcular_pago("Tiempo Completo", 30, 10, 5)
        suma_descuentos = resultado["descuento_salud"] + resultado["descuento_pension"] + resultado["descuento_arl"]
        self.assertAlmostEqual(resultado["total_descuentos"], suma_descuentos, places=2)

    def test_medios_tiempo_no_tiene_arl(self):
        resultado = calcular_pago("Medio Tiempo", 30, 5, 2)
        self.assertEqual(resultado["descuento_arl"], 0)

    def test_todos_descuentos_cero_si_pago_bruto_cero(self):
        resultado = calcular_pago("Tiempo Completo", 0, 0, 0)
        self.assertEqual(resultado["descuento_salud"], 0)
        self.assertEqual(resultado["descuento_pension"], 0)
        self.assertEqual(resultado["descuento_arl"], 0)
        self.assertEqual(resultado["total_descuentos"], 0)

    def test_calculo_precision_decimal(self):
        resultado = calcular_pago("Tiempo Completo", 33, 17, 11)
        self.assertIsInstance(resultado["pago_bruto"], float)
        self.assertIsInstance(resultado["pago_neto"], float)

if __name__ == "__main__":
    unittest.main()
