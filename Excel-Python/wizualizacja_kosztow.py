import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

excel_file = pd.ExcelFile("C:/Users/mperz/Desktop/sales-data-PL-panel/Excel-Python/przykladowe_dane_produkcja.xlsx")
df_robocizna = excel_file.parse("Robocizna")
df_pakowanie = excel_file.parse("Pakowanie")

# Załaduj dane z Excela
excel_file = pd.ExcelFile("przykladowe_dane_produkcja.xlsx")
df_robocizna = excel_file.parse("Robocizna")
df_pakowanie = excel_file.parse("Pakowanie")

#Przetwarzanie Danych
df_robocizna['Koszty Robocizny'] = df_robocizna['Godziny Pracy'] * df_robocizna['Koszt na Godzinę'] + df_robocizna['Premie'] + df_robocizna['Dodatkowe Koszty']
df_pakowanie['Koszty Pakowania'] = df_pakowanie['Ilość Opakowań'] * df_pakowanie['Koszt Jednostkowy'] + df_pakowanie['Koszty Dodatkowe']

# Wizualizacja Kosztów Robocizny
plt.figure(figsize=(12, 6))
sns.barplot(x='Miesiąc', y='Koszty Robocizny', hue='Dział', data=df_robocizna)
plt.title('Koszty Robocizny w Podziale na Działy i Miesiące')
plt.xlabel('Miesiąc')
plt.ylabel('Koszty Robocizny')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Wizualizacja Kosztów Pakowania
plt.figure(figsize=(12, 6))
sns.barplot(x='Miesiąc', y='Koszty Pakowania', hue='Rodzaj Opakowania', data=df_pakowanie)
plt.title('Koszty Pakowania w Podziale na Rodzaj Opakowania i Miesiące')
plt.xlabel('Miesiąc')
plt.ylabel('Koszty Pakowania')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Porównanie Kosztów Robocizny i Pakowania w czasie
koszty_robocizny_miesiac = df_robocizna.groupby('Miesiąc')['Koszty Robocizny'].sum()
koszty_pakowania_miesiac = df_pakowanie.groupby('Miesiąc')['Koszty Pakowania'].sum()

plt.figure(figsize=(12, 6))
plt.plot(koszty_robocizny_miesiac.index, koszty_robocizny_miesiac.values, marker='o', label='Robocizna')
plt.plot(koszty_pakowania_miesiac.index, koszty_pakowania_miesiac.values, marker='o', label='Pakowanie')
plt.title('Porównanie Kosztów Robocizny i Pakowania w Czasie')
plt.xlabel('Miesiąc')
plt.ylabel('Koszty')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Udział Kosztów Robocizny w Kosztach Całkowitych na Dział
koszty_robocizny_dzial = df_robocizna.groupby('Dział')['Koszty Robocizny'].sum()
plt.figure(figsize=(8, 8))
plt.pie(koszty_robocizny_dzial, labels=koszty_robocizny_dzial.index, autopct='%1.1f%%', startangle=140)
plt.title('Udział Kosztów Robocizny w Podziale na Działy')
plt.tight_layout()
plt.show()

# Udział Kosztów Pakowania w Kosztach Całkowitych na Rodzaj Opakowania
koszty_pakowania_rodzaj = df_pakowanie.groupby('Rodzaj Opakowania')['Koszty Pakowania'].sum()
plt.figure(figsize=(8, 8))
plt.pie(koszty_pakowania_rodzaj, labels=koszty_pakowania_rodzaj.index, autopct='%1.1f%%', startangle=140)
plt.title('Udział Kosztów Pakowania w Podziale na Rodzaj Opakowania')
plt.tight_layout()
plt.show()

# Analiza Skumulowanych Kosztów Robocizny dla każdego działu
df_robocizna['Suma Skumulowana'] = df_robocizna.groupby('Dział')['Koszty Robocizny'].cumsum()

plt.figure(figsize=(12, 6))
sns.lineplot(x='Miesiąc', y='Suma Skumulowana', hue='Dział', data=df_robocizna, marker='o')
plt.title('Skumulowane Koszty Robocizny dla każdego działu w czasie')
plt.xlabel('Miesiąc')
plt.ylabel('Suma Skumulowana Kosztów Robocizny')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Analiza Kosztów Pakowania na Jednostkę
df_pakowanie['Koszt na Jednostkę'] = df_pakowanie['Koszty Pakowania'] / df_pakowanie['Ilość Opakowań']

plt.figure(figsize=(12, 6))
sns.barplot(x='Miesiąc', y='Koszt na Jednostkę', hue='Rodzaj Opakowania', data=df_pakowanie)
plt.title('Koszt Pakowania na Jednostkę (na opakowanie)')
plt.xlabel('Miesiąc')
plt.ylabel('Koszt na Jednostkę')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()