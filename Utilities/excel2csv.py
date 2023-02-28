import pandas as pd

df = pd.DataFrame(pd.read_excel('Spis Biblioteczny.xlsx'))

df = df[['Nazwa', 'Autor', 'Ilość', 'Dział']]

print(df)

df.to_csv('spis.csv', index = None, header=True)
