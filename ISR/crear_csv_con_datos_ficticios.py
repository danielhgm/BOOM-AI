import pandas as pd
import numpy as np

# Simular datos para el ejemplo
np.random.seed(42)

# Generar datos ficticios
data = {
    'ingresos': np.random.randint(100000, 1000000, 100),
    'deducciones': np.random.randint(10000, 100000, 100),
    'creditos_fiscales': np.random.randint(5000, 50000, 100),
    'tipo_contribuyente': np.random.choice(['Persona Física', 'Persona Moral'], 100),
    'impuesto_a_pagar': np.random.randint(5000, 200000, 100)
}

# Crear el DataFrame
df = pd.DataFrame(data)

# Guardar como CSV
csv_path = '../data/datos_impuestos.csv'
df.to_csv(csv_path, index=False)

csv_path