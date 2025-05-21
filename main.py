import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import ZapimoveisScrapper as zap
import time
import PlotTeste

show_order = ['city','neighborhood','street','price','period','Condo','IPTU','Area','Quartos','Banheiros','Vagas','URL']
st.sidebar.title("Buscador ZapImoveis")

# Inicializa session_state se ainda não existir
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "graf" not in st.session_state:
    st.session_state.graf = []

df_estados = pd.read_csv("estados.csv")

st.text("Resultado Tabelado")
placeholder = st.empty()

estado_escolhido = st.sidebar.selectbox("Selecione um estado:", df_estados["Estado"].tolist(), index=23)
user_input = st.sidebar.text_input("Cidade", value='florianopolis')
search_word = str(df_estados[df_estados["Estado"] == estado_escolhido]["Sigla"].values[0]) + "+" + user_input
n_paginas = st.sidebar.number_input("Número de páginas", min_value=1, step=1)
st.sidebar.text(search_word)

search = st.sidebar.button("Search")

graf_container = st.container()

if search:
    df_total = pd.DataFrame()
    progress_bar = st.progress(0, text="Carregando páginas...")

    try:
        for i, df_page in enumerate(zap.search_yield(localization=search_word, num_pages=n_paginas)):
            if not df_page.empty and {"price", "Condo", "IPTU"}.issubset(df_page.columns):
                df_page[["price", "Condo", "IPTU"]] = df_page[["price", "Condo", "IPTU"]].applymap(
                    lambda x: f"R${x:,.2f}" if isinstance(x, (int, float)) else x)

            df_page = df_page.rename(columns={
                'propertyArea': 'Area',
                'bedroomQuantity': 'Quartos',
                'bathroomQuantity': 'Banheiros',
                'parkingSpacesQuantity': 'Vagas'
            })

            df_page = df_page[df_page['period'] == 'mês']
            df_total = pd.concat([df_total, df_page], ignore_index=True)
            placeholder.dataframe(df_total[show_order], use_container_width=True)

            # Atualiza barra de progresso
            progress_bar.progress((i + 1) / n_paginas, text=f"Carregando página {i + 1} de {n_paginas}")

        # Após terminar, limpa a barra e salva estado
        progress_bar.empty()
        st.session_state.df = df_total
        st.session_state.graf = []

    except Exception as e:
        progress_bar.empty()
        st.error(f"Erro ao processar a busca: {e}")



# Só mostra o botão refresh se houver dados
if not st.session_state.df.empty:
    # Garante que a tabela continua visível
    #st.text("Resultado Tabelado")
    placeholder.dataframe(st.session_state.df[show_order], use_container_width=True)

    if st.sidebar.button("Refresh gráficos"):
        st.session_state.graf = []  # Limpa lista
        figs = PlotTeste.graficos(st.session_state.df)
        with graf_container:
            for fig in figs:
                st.session_state.graf.append(st.plotly_chart(fig, use_container_width=True))
    else:
        if not st.session_state.graf:
            figs = PlotTeste.graficos(st.session_state.df)
            with graf_container:
                for fig in figs:
                    st.session_state.graf.append(st.plotly_chart(fig, use_container_width=True))
        else:
            with graf_container:
                for fig in st.session_state.graf:
                    st.plotly_chart(fig, use_container_width=True)