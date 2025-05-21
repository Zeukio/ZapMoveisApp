import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def graficos(df):
    #df = pd.read_csv("2025-04-30T16-53_export.csv")

    #df[["price", "Condo", "IPTU"]] = df[["price", "Condo", "IPTU"]].applymap(
       # lambda x: f"R${x:,.2f}" if isinstance(x, (int, float)) else x)

    colunas_monetarias = ["price", "Condo", "IPTU"]
    for col in colunas_monetarias:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("R$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(".", ".", regex=False)
            .str.strip()
            .astype(float)
        )

    df = df.rename(columns={'propertyArea': 'Area', 'bedroomQuantity': 'Quartos', 'bathroomQuantity': 'Banheiros',
                            'parkingSpacesQuantity': 'Vagas'})
    df = df[df['period'] == 'mês']

    df['valortotal'] = df['price'] + df['IPTU'] + df['Condo']

    df['m2total'] = df['valortotal']/df['Area']

    ## coloeque aqui a parte de analise dos dados;

    k = set(df['neighborhood'])
    k = list(k)
    #for i in set(df['neighborhood']):
    pm2 = px.scatter(df, x="neighborhood", y="m2total",color="neighborhood")
    #fig = px.histogram(df, x="neighborhood", y="m2total", title="Preço por Bairro", histfunc="avg")
    #fig = px.scatter(df, x="Area", y="price",color="neighborhood")
    df_analizes = pd.DataFrame()
    neighborhoods = list(df['neighborhood'].dropna().unique())
    dict_temp = {}

    for neighborhood in neighborhoods:
        dict_temp['Bairro'] = neighborhood
        dict_temp['Media'] =  df[df['neighborhood'] == neighborhood]['valortotal'].mean()
        df_analizes = pd.concat([df_analizes,pd.DataFrame([dict_temp])])

    med = px.bar(df_analizes, x="Bairro", y="Media", color="Bairro")

    return [pm2, med]
