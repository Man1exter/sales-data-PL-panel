import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import sys
from datetime import datetime

# 1. Funkcje do pobierania danych (ZAIMPLEMENTUJ WEDŁUG POTRZEB)
@st.cache_data
def pobierz_dane_gus():
    """
    Pobiera dane z Głównego Urzędu Statystycznego (GUS).
    """
    # PRZYKŁADOWE DANE - ZASTĄP SWOIMI!!!
    data = {'Okres': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01',
                                      '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01',
                                      '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01',
                                      '2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01',
                                      '2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01']),
            'Sprzedaż_Detaliczna': [100, 110, 95, 120, 115, 105, 115, 100, 125, 120, 110, 120, 105, 130, 125,
                                      115, 125, 110, 135, 130, 120, 130, 115, 140, 135]}
    df = pd.DataFrame(data)
    return df

@st.cache_data
def pobierz_dane_firmowe():
    """
    Pobiera dane z systemów firmowych (CRM, ERP, bazy danych).
    """
    # PRZYKŁADOWE DANE - ZASTĄP SWOIMI!!!
    data = {'Okres': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01',
                                      '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01',
                                      '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01',
                                      '2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01',
                                      '2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01']),
            'Sprzedaż_Online': [60, 70, 55, 80, 75, 65, 75, 60, 85, 80, 70, 80, 65, 90, 85, 75, 85, 70, 95, 90,
                                 80, 90, 75, 100, 95],
            'Sprzedaż_Offline': [40, 40, 40, 40, 40, 45, 45, 45, 45, 45, 50, 50, 50, 50, 50, 55, 55, 55, 55, 55,
                                  60, 60, 60, 60, 60],
            'Kategoria': ['A', 'B', 'A', 'C', 'B', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'A', 'C', 'B', 'A', 'B',
                          'A', 'C', 'B', 'A', 'B', 'A', 'C', 'B']}
    df = pd.DataFrame(data)
    return df

# 2. Funkcje do przetwarzania danych
def przetworz_dane(df_gus, df_firmowe):
    """
    Przetwarza dane z GUS i systemów firmowych.
    """
    df = pd.merge(df_gus, df_firmowe, on='Okres', how='outer')
    df = df.fillna(0)
    df['Sprzedaż_Firmowa'] = df['Sprzedaż_Online'] + df['Sprzedaż_Offline']
    df['Rok'] = df['Okres'].dt.year
    df['Miesiąc'] = df['Okres'].dt.month
    return df

# 3. Funkcje do wizualizacji
def wizualizuj_dynamike_sprzedaży(df, kategoria=None):
    """
    Wizualizuje dynamikę sprzedaży w czasie.
    """
    if kategoria:
        df = df[df['Kategoria'] == kategoria]

    fig = px.line(df, x='Okres', y=['Sprzedaż_Detaliczna', 'Sprzedaż_Firmowa'],
                  labels={'value': 'Sprzedaż', 'variable': 'Źródło'},
                  title=f"Dynamika Sprzedaży (Kategoria: {kategoria if kategoria else 'Wszystkie'})")
    fig.update_layout(xaxis_title="Okres", yaxis_title="Sprzedaż")
    return fig

def wizualizuj_udzial_kanałów(df, rok=None):
    """
    Wizualizuje udział kanałów sprzedaży (online vs. offline).
    """
    if rok:
        df = df[df['Rok'] == rok]

    total_online = df['Sprzedaż_Online'].sum()
    total_offline = df['Sprzedaż_Offline'].sum()
    data = {'Kanał': ['Online', 'Offline'], 'Sprzedaż': [total_online, total_offline]}
    df_pie = pd.DataFrame(data)

    fig = px.pie(df_pie, values='Sprzedaż', names='Kanał',
                 title=f"Udział Kanałów Sprzedaży (Rok: {rok if rok else 'Wszystkie'})")
    return fig

def wizualizuj_sprzedaż_wg_kategorii(df):
    """
    Wizualizuje sprzedaż według kategorii produktów.
    """
    sales_by_category = df.groupby('Kategoria')['Sprzedaż_Firmowa'].sum().reset_index()

    fig = px.bar(sales_by_category, x='Kategoria', y='Sprzedaż_Firmowa',
                 title="Sprzedaż Według Kategorii")
    fig.update_layout(xaxis_title="Kategoria", yaxis_title="Sprzedaż")
    return fig

def wizualizuj_sprzedaż_w_czasie(df, kategoria=None):
    """
    Wizualizuje sprzedaż w czasie dla wybranej kategorii produktów.
    """
    if kategoria:
        df = df[df['Kategoria'] == kategoria]

    fig = px.line(df, x='Okres', y='Sprzedaż_Firmowa',
                 title=f"Sprzedaż w Czasie (Kategoria: {kategoria if kategoria else 'Wszystkie'})")
    fig.update_layout(xaxis_title="Okres", yaxis_title="Sprzedaż")
    return fig

# 4. Funkcja do wyświetlania statystyk na większym panelu
def wyświetl_statystyki(df, rok_początkowy, rok_końcowy):
    """
    Wyświetla zagregowane statystyki sprzedaży w wybranym okresie.
    """
    df_filtered = df[(df['Rok'] >= rok_początkowy) & (df['Rok'] <= rok_końcowy)]

    total_sales = df_filtered['Sprzedaż_Firmowa'].sum()
    avg_monthly_sales = df_filtered['Sprzedaż_Firmowa'].mean()
    max_sales = df_filtered['Sprzedaż_Firmowa'].max()
    min_sales = df_filtered['Sprzedaż_Firmowa'].min()

    st.subheader(f"Statystyki Sprzedaży od {rok_początkowy} do {rok_końcowy}")
    st.markdown(f"""
    <div style="font-size: 1.2em;">
        Całkowita sprzedaż: <b>{total_sales:.2f}</b><br>
        Średnia miesięczna sprzedaż: <b>{avg_monthly_sales:.2f}</b><br>
        Maksymalna sprzedaż: <b>{max_sales:.2f}</b><br>
        Minimalna sprzedaż: <b>{min_sales:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

# 5. Główna funkcja aplikacji Streamlit
def main():
    """
    Główna funkcja aplikacji Streamlit.
    """
    st.set_page_config(layout="wide") # Ustawienie szerokiego layoutu

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
    kategoria_filter = st.sidebar.selectbox("Wybierz kategorię", options=[None] + list(df['Kategoria'].unique()))

    # Dodanie przycisków do wyboru zakresu lat
    col1, col2 = st.sidebar.columns(2)
    with col1:
        rok_początkowy = st.selectbox("Rok Początkowy", options=list(range(2020, 2025)), index=0)
    with col2:
        rok_końcowy = st.selectbox("Rok Końcowy", options=list(range(2020, 2025)), index=4)

    # Filtrowanie danych
    df_filtered = df[(df['Okres'].dt.date >= okres_start) & (df['Okres'].dt.date <= okres_koniec)]
    if kategoria_filter:
        df_filtered = df_filtered[df_filtered['Kategoria'] == kategoria_filter]

    # Wyświetlanie statystyk
    wyświetl_statystyki(df_filtered, rok_początkowy, rok_końcowy)

    # Wizualizacje (wyświetlane w dwóch kolumnach)
    col1, col2 = st.columns(2)

    with col1:
        st.header("Dynamika Sprzedaży")
        st.plotly_chart(wizualizuj_dynamike_sprzedaży(df_filtered), use_container_width=True)

        st.header("Sprzedaż Według Kategorii")
        st.plotly_chart(wizualizuj_sprzedaż_wg_kategorii(df_filtered), use_container_width=True)

    with col2:
        st.header("Udział Kanałów Sprzedaży")
        st.plotly_chart(wizualizuj_udzial_kanałów(df_filtered, rok=None), use_container_width=True)

        st.header("Sprzedaż w Czasie")
        st.plotly_chart(wizualizuj_sprzedaż_w_czasie(df_filtered, kategoria=kategoria_filter), use_container_width=True)

    st.subheader("Dane po filtracji")
    st.dataframe(df_filtered)

    # Opcja ręcznego zatrzymania aplikacji
    if st.button("Zatrzymaj Aplikację"):
        st.write("Zamykanie aplikacji...")
        sys.exit()

# 6. Uruchomienie aplikacji
if __name__ == "__main__":
    main()
    
# streamlit run pre-demo.py