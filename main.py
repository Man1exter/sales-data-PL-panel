import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px # Do interaktywnych wykresów
import datetime

# 1. Funkcje do pobierania danych (ZAIMPLEMENTUJ WEDŁUG POTRZEB)
@st.cache_data # Cache, aby nie pobierać danych za każdym razem
def pobierz_dane_gus():
    # TODO: Zaimplementuj pobieranie danych z GUS (np. przez web scraping lub API, jeśli dostępne)
    # Pamiętaj o obsłudze błędów i logowaniu
    # To jest tylko przykład - zastąp go swoim kodem
    data = {'Okres': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01']),
            'Sprzedaż_Detaliczna': [100, 110, 95, 120, 115]}
    df = pd.DataFrame(data)
    return df

@st.cache_data # Cache, aby nie pobierać danych za każdym razem
def pobierz_dane_firmowe():
    # TODO: Zaimplementuj pobieranie danych z Twojego systemu CRM/ERP/bazy danych
    # Pamiętaj o obsłudze błędów i logowaniu
    # To jest tylko przykład - zastąp go swoim kodem
    data = {'Okres': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01']),
            'Sprzedaż_Online': [60, 70, 55, 80, 75],
            'Sprzedaż_Offline': [40, 40, 40, 40, 40],
            'Kategoria': ['A', 'B', 'A', 'C', 'B']} # Dodatkowa kategoria
    df = pd.DataFrame(data)
    return df


# 2. Funkcje do przetwarzania danych
def przetworz_dane(df_gus, df_firmowe):
    # Łączenie danych
    df = pd.merge(df_gus, df_firmowe, on='Okres', how='outer')
    df = df.fillna(0) # Wypełnij braki danych zerami

    # Obliczanie całkowitej sprzedaży firmowej
    df['Sprzedaż_Firmowa'] = df['Sprzedaż_Online'] + df['Sprzedaż_Offline']

    # Dodanie kolumny z rokiem i miesiącem
    df['Rok'] = df['Okres'].dt.year
    df['Miesiąc'] = df['Okres'].dt.month

    return df

# 3. Funkcje do wizualizacji
def wizualizuj_dynamike_sprzedaży(df, kategoria=None):
    if kategoria:
        df = df[df['Kategoria'] == kategoria]

    fig = px.line(df, x='Okres', y=['Sprzedaż_Detaliczna', 'Sprzedaż_Firmowa'],
                  labels={'value': 'Sprzedaż', 'variable': 'Źródło'},
                  title=f"Dynamika Sprzedaży (Kategoria: {kategoria if kategoria else 'Wszystkie'})")
    fig.update_layout(xaxis_title="Okres", yaxis_title="Sprzedaż")
    return fig

def wizualizuj_udzial_kanałów(df, rok=None):
    if rok:
        df = df[df['Rok'] == rok]

    total_online = df['Sprzedaż_Online'].sum()
    total_offline = df['Sprzedaż_Offline'].sum()
    data = {'Kanał': ['Online', 'Offline'], 'Sprzedaż': [total_online, total_offline]}
    df_pie = pd.DataFrame(data)

    fig = px.pie(df_pie, values='Sprzedaż', names='Kanał', title=f"Udział Kanałów Sprzedaży (Rok: {rok if rok else 'Wszystkie'})")
    return fig

def wizualizuj_sprzedaż_wg_kategorii(df):
    # Agregacja sprzedaży po kategorii
    sales_by_category = df.groupby('Kategoria')['Sprzedaż_Firmowa'].sum().reset_index()

    fig = px.bar(sales_by_category, x='Kategoria', y='Sprzedaż_Firmowa',
                 title="Sprzedaż Według Kategorii")
    fig.update_layout(xaxis_title="Kategoria", yaxis_title="Sprzedaż")
    return fig

def wizualizuj_sprzedaż_w_czasie(df, kategoria=None):
    if kategoria:
        df = df[df['Kategoria'] == kategoria]

    fig = px.line(df, x='Okres', y='Sprzedaż_Firmowa', title=f"Sprzedaż w Czasie (Kategoria: {kategoria if kategoria else 'Wszystkie'})")
    fig.update_layout(xaxis_title="Okres", yaxis_title="Sprzedaż")
    return fig

# 4. Streamlit App
def main():
    st.title("Panel Analityczny Sprzedaży w Polsce (od 2020)")

    # Pobierz dane
    df_gus = pobierz_dane_gus()
    df_firmowe = pobierz_dane_firmowe()

    # Przetwórz dane
    df = przetworz_dane(df_gus, df_firmowe)

    # Sidebar - Filtry
    st.sidebar.header("Filtry")
    okres_start = st.sidebar.date_input("Początek okresu", df['Okres'].min().date())
    okres_koniec = st.sidebar.date_input("Koniec okresu", df['Okres'].max().date())

    # Filtr kategorii
    kategoria_filter = st.sidebar.selectbox("Wybierz kategorię", options=[None] + list(df['Kategoria'].unique()))

    # Filtr roku
    rok_filter = st.sidebar.selectbox("Wybierz rok", options=[None] + list(df['Rok'].unique()))


    # Filtrowanie danych
    df_filtered = df[(df['Okres'].dt.date >= okres_start) & (df['Okres'].dt.date <= okres_koniec)]
    if kategoria_filter:
        df_filtered = df_filtered[df_filtered['Kategoria'] == kategoria_filter]

    # Wizualizacje
    st.header("Dynamika Sprzedaży")
    st.plotly_chart(wizualizuj_dynamike_sprzedaży(df_filtered))

    st.header("Udział Kanałów Sprzedaży")
    st.plotly_chart(wizualizuj_udzial_kanałów(df_filtered, rok=rok_filter))

    st.header("Sprzedaż Według Kategorii")
    st.plotly_chart(wizualizuj_sprzedaż_wg_kategorii(df_filtered))

    st.header("Sprzedaż w Czasie")
    st.plotly_chart(wizualizuj_sprzedaż_w_czasie(df_filtered, kategoria=kategoria_filter))

    st.subheader("Dane po filtracji")
    st.dataframe(df_filtered) # Wyświetl dane w tabeli

if __name__ == "__main__":
    main()
    
    
# streamlit run main.py