import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import sys

# 1. Funkcje do pobierania danych (ZAIMPLEMENTUJ WEDŁUG POTRZEB)
@st.cache_data  # Cache, aby unikać ponownego pobierania danych przy każdej zmianie w panelu
def pobierz_dane_gus():
    """
    Pobiera dane z Głównego Urzędu Statystycznego (GUS).
    TODO: Zastąp ten przykładowy kod własnym kodem do pobierania danych z GUS.
    Pamiętaj o obsłudze błędów (try...except) i ewentualnym logowaniu.
    :return: pandas.DataFrame z danymi sprzedaży detalicznej.
    """
    # PRZYKŁADOWE DANE - ZASTĄP SWOIMI!!!
    data = {'Okres': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01']),
            'Sprzedaż_Detaliczna': [100, 110, 95, 120, 115]}
    df = pd.DataFrame(data)
    return df

@st.cache_data  # Cache danych z firmy
def pobierz_dane_firmowe():
    """
    Pobiera dane z systemów firmowych (CRM, ERP, bazy danych).
    TODO: Zastąp ten przykładowy kod własnym kodem do pobierania danych firmowych.
    Pamiętaj o obsłudze błędów i logowaniu.
    :return: pandas.DataFrame z danymi sprzedaży firmowej.
    """
    # PRZYKŁADOWE DANE - ZASTĄP SWOIMI!!!
    data = {'Okres': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01']),
            'Sprzedaż_Online': [60, 70, 55, 80, 75],
            'Sprzedaż_Offline': [40, 40, 40, 40, 40],
            'Kategoria': ['A', 'B', 'A', 'C', 'B']}  # Dodatkowa kategoria
    df = pd.DataFrame(data)
    return df

# 2. Funkcje do przetwarzania danych
def przetworz_dane(df_gus, df_firmowe):
    """
    Przetwarza dane z GUS i systemów firmowych.
    Łączy dane, wypełnia braki, oblicza dodatkowe kolumny.
    :param df_gus: pandas.DataFrame z danymi z GUS.
    :param df_firmowe: pandas.DataFrame z danymi firmowymi.
    :return: pandas.DataFrame z przetworzonymi danymi.
    """
    # Łączenie danych po kolumnie 'Okres' (outer join, aby zachować wszystkie dane)
    df = pd.merge(df_gus, df_firmowe, on='Okres', how='outer')
    df = df.fillna(0)  # Wypełnienie brakujących wartości zerami

    # Obliczanie całkowitej sprzedaży firmowej
    df['Sprzedaż_Firmowa'] = df['Sprzedaż_Online'] + df['Sprzedaż_Offline']

    # Dodanie kolumn z rokiem i miesiącem dla łatwiejszego filtrowania
    df['Rok'] = df['Okres'].dt.year
    df['Miesiąc'] = df['Okres'].dt.month

    return df

# 3. Funkcje do wizualizacji (używamy Plotly Express do interaktywnych wykresów)
def wizualizuj_dynamike_sprzedaży(df, kategoria=None):
    """
    Wizualizuje dynamikę sprzedaży w czasie.
    :param df: pandas.DataFrame z danymi.
    :param kategoria: (opcjonalne) Kategoria produktu do wyświetlenia.
    :return: plotly.graph_objects.Figure
    """
    if kategoria:
        df = df[df['Kategoria'] == kategoria]  # Filtrowanie po kategorii, jeśli została podana

    fig = px.line(df, x='Okres', y=['Sprzedaż_Detaliczna', 'Sprzedaż_Firmowa'],
                  labels={'value': 'Sprzedaż', 'variable': 'Źródło'},
                  title=f"Dynamika Sprzedaży (Kategoria: {kategoria if kategoria else 'Wszystkie'})")  # Tytuł wykresu
    fig.update_layout(xaxis_title="Okres", yaxis_title="Sprzedaż")  # Etykiety osi
    return fig

def wizualizuj_udzial_kanałów(df, rok=None):
    """
    Wizualizuje udział kanałów sprzedaży (online vs. offline) za pomocą wykresu kołowego.
    :param df: pandas.DataFrame z danymi.
    :param rok: (opcjonalne) Rok do wyświetlenia.
    :return: plotly.graph_objects.Figure
    """
    if rok:
        df = df[df['Rok'] == rok]  # Filtrowanie po roku, jeśli został podany

    # Obliczenie sumy sprzedaży online i offline
    total_online = df['Sprzedaż_Online'].sum()
    total_offline = df['Sprzedaż_Offline'].sum()

    # Przygotowanie danych do wykresu kołowego
    data = {'Kanał': ['Online', 'Offline'], 'Sprzedaż': [total_online, total_offline]}
    df_pie = pd.DataFrame(data)

    fig = px.pie(df_pie, values='Sprzedaż', names='Kanał',
                 title=f"Udział Kanałów Sprzedaży (Rok: {rok if rok else 'Wszystkie'})")  # Tytuł wykresu
    return fig

def wizualizuj_sprzedaż_wg_kategorii(df):
    """
    Wizualizuje sprzedaż według kategorii produktów za pomocą wykresu słupkowego.
    :param df: pandas.DataFrame z danymi.
    :return: plotly.graph_objects.Figure
    """
    # Agregacja sprzedaży po kategorii
    sales_by_category = df.groupby('Kategoria')['Sprzedaż_Firmowa'].sum().reset_index()

    fig = px.bar(sales_by_category, x='Kategoria', y='Sprzedaż_Firmowa',
                 title="Sprzedaż Według Kategorii")  # Tytuł wykresu
    fig.update_layout(xaxis_title="Kategoria", yaxis_title="Sprzedaż")  # Etykiety osi
    return fig

def wizualizuj_sprzedaż_w_czasie(df, kategoria=None):
    """
    Wizualizuje sprzedaż w czasie dla wybranej kategorii produktów.
    :param df: pandas.DataFrame z danymi.
    :param kategoria: (opcjonalne) Kategoria produktu do wyświetlenia.
    :return: plotly.graph_objects.Figure
    """
    if kategoria:
        df = df[df['Kategoria'] == kategoria]  # Filtrowanie po kategorii, jeśli została podana

    fig = px.line(df, x='Okres', y='Sprzedaż_Firmowa',
                 title=f"Sprzedaż w Czasie (Kategoria: {kategoria if kategoria else 'Wszystkie'})")  # Tytuł wykresu
    fig.update_layout(xaxis_title="Okres", yaxis_title="Sprzedaż")  # Etykiety osi
    return fig

# 4. Główna funkcja aplikacji Streamlit
def main():
    """
    Główna funkcja aplikacji Streamlit.
    Definiuje interfejs użytkownika, pobiera dane, przetwarza je i wyświetla wizualizacje.
    """
    st.title("Panel Analityczny Sprzedaży w Polsce (od 2020)")  # Tytuł aplikacji

    # Pobierz dane
    df_gus = pobierz_dane_gus()
    df_firmowe = pobierz_dane_firmowe()

    # Przetwórz dane
    df = przetworz_dane(df_gus, df_firmowe)

    # Sidebar - Filtry
    st.sidebar.header("Filtry")  # Nagłówek w sidebar
    okres_start = st.sidebar.date_input("Początek okresu", df['Okres'].min().date())  # Filtr daty początkowej
    okres_koniec = st.sidebar.date_input("Koniec okresu", df['Okres'].max().date())  # Filtr daty końcowej

    kategoria_filter = st.sidebar.selectbox("Wybierz kategorię", options=[None] + list(df['Kategoria'].unique()))  # Filtr kategorii

    rok_filter = st.sidebar.selectbox("Wybierz rok", options=[None] + list(df['Rok'].unique()))  # Filtr roku

    # Filtrowanie danych na podstawie wybranych opcji
    df_filtered = df[(df['Okres'].dt.date >= okres_start) & (df['Okres'].dt.date <= okres_koniec)]
    if kategoria_filter:
        df_filtered = df_filtered[df_filtered['Kategoria'] == kategoria_filter]
    if rok_filter:
        df_filtered = df_filtered[df['Rok'] == rok_filter]

    # Wizualizacje
    st.header("Dynamika Sprzedaży")  # Nagłówek sekcji
    st.plotly_chart(wizualizuj_dynamike_sprzedaży(df_filtered))  # Wyświetlenie wykresu dynamiki sprzedaży

    st.header("Udział Kanałów Sprzedaży")  # Nagłówek sekcji
    st.plotly_chart(wizualizuj_udzial_kanałów(df_filtered, rok=rok_filter))  # Wyświetlenie wykresu udziału kanałów

    st.header("Sprzedaż Według Kategorii")  # Nagłówek sekcji
    st.plotly_chart(wizualizuj_sprzedaż_wg_kategorii(df_filtered))  # Wyświetlenie wykresu sprzedaży wg kategorii

    st.header("Sprzedaż w Czasie")  # Nagłówek sekcji
    st.plotly_chart(wizualizuj_sprzedaż_w_czasie(df_filtered, kategoria=kategoria_filter))  # Wyświetlenie wykresu sprzedaży w czasie

    st.subheader("Dane po filtracji")  # Nagłówek sekcji
    st.dataframe(df_filtered)  # Wyświetlenie przefiltrowanych danych w tabeli

    # Opcja ręcznego zatrzymania aplikacji
    if st.button("Zatrzymaj Aplikację"):
        st.write("Zamykanie aplikacji...")
        sys.exit()  # Zakończenie działania skryptu

# Uruchomienie aplikacji
if __name__ == "__main__":
    main()
    
    
# streamlit run main.py
# streamlit run main.py