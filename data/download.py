import pandas as pd

# Lire le fichier Excel
df = pd.read_excel('online_retail_II.xlsx', sheet_name='Year 2010-2011')

# Sauvegarder le fichier en CSV
df.to_csv('ecommerce_data.csv', index=False)

print("✅ Conversion terminée : le fichier CSV est sauvegardé sous 'ecommerce_data.csv'")
