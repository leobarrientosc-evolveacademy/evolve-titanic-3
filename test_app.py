import unittest
import pandas as pd
import numpy as np
from app import cargar_datos

class TestTitanicApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial que se ejecuta una vez antes de todas las pruebas"""
        try:
            cls.df = cargar_datos()
        except Exception as e:
            raise Exception(f"Error al cargar los datos: {e}")

    def test_carga_datos(self):
        """Prueba que los datos se carguen correctamente"""
        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertTrue(len(self.df) > 0)
        
    def test_columnas_requeridas(self):
        """Prueba que el DataFrame tenga todas las columnas necesarias"""
        columnas_requeridas = [
            'Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 
            'Parch', 'Fare', 'Embarked'
        ]
        for columna in columnas_requeridas:
            self.assertIn(columna, self.df.columns)

    def test_tipos_datos(self):
        """Prueba que los tipos de datos sean correctos"""
        self.assertEqual(self.df['Survived'].dtype, np.int64)
        self.assertEqual(self.df['Pclass'].dtype, np.int64)
        self.assertEqual(self.df['Sex'].dtype, object)
        self.assertEqual(self.df['Fare'].dtype, np.float64)

    def test_valores_survived(self):
        """Prueba que los valores de supervivencia sean válidos"""
        self.assertTrue(all(self.df['Survived'].isin([0, 1])))

    def test_valores_pclass(self):
        """Prueba que las clases de pasajeros sean válidas"""
        self.assertTrue(all(self.df['Pclass'].isin([1, 2, 3])))

    def test_valores_fare(self):
        """Prueba que las tarifas sean valores no negativos"""
        self.assertTrue(all(self.df['Fare'] >= 0))

    def test_calculo_familia(self):
        """Prueba el cálculo del tamaño de familia"""
        df_test = self.df.copy()
        df_test['FamilySize'] = df_test['SibSp'] + df_test['Parch'] + 1
        self.assertTrue(all(df_test['FamilySize'] >= 1))
        
    def test_no_valores_nulos_criticos(self):
        """Prueba que no haya valores nulos en columnas críticas"""
        columnas_criticas = ['Survived', 'Pclass', 'Sex', 'Fare']
        for columna in columnas_criticas:
            self.assertFalse(self.df[columna].isnull().any())

if __name__ == '__main__':
    unittest.main() 