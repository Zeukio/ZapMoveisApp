# 📊 ZapImóveis Scraper & Dashboard

Este projeto é uma aplicação desenvolvida com **Streamlit**, **Plotly** e **BeautifulSoup** para realizar buscas de imóveis no site [ZapImóveis](https://www.zapimoveis.com.br/), extrair os dados, armazená-los em `DataFrames`, e gerar visualizações interativas para análise de preços de aluguel.

---

## 🚀 Funcionalidades

- 🔍 Busca automatizada de imóveis por **estado e cidade**, com múltiplas páginas.
- 📄 Extração de dados como bairro, preço, área, condomínio, IPTU, número de quartos, banheiros, vagas, entre outros.
- 📊 Visualização dos dados tabulados e gráficos com análise do valor total e preço por m².
- 🌎 Interface simples via **Streamlit**, com filtros e atualização dinâmica.

---

## 🧱 Estrutura dos Arquivos

| Arquivo                  | Descrição |
|--------------------------|-----------|
| `main.py`                | Aplicação principal com interface Streamlit. Controla entrada do usuário, chama a busca e gera gráficos. |
| `ZapimoveisScrapper.py`  | Módulo responsável por acessar e extrair os dados diretamente do site ZapImóveis usando BeautifulSoup. |
| `DatasetZapimoveis.py`   | Script de teste para executar a função `search()` e salvar os dados em CSV. |
| `PlotTeste.py`           | Geração dos gráficos usando Plotly com análise por bairro e valor por m². |
| `estados.csv`            | Arquivo auxiliar com os nomes e siglas dos estados brasileiros. |

---

## ⚙️ Como Executar Localmente

### Pré-requisitos

- Python 3.8 ou superior
- Instale as dependências:

```bash
pip install -r requirements.txt
```

### Executar a aplicação

```bash
streamlit run main.py
```

---

## 📌 Observações

- O scraper pode ser afetado por mudanças no layout do site do ZapImóveis.
- As buscas são feitas por estado e cidade (ex: `SC` + `florianopolis`).
- Apenas imóveis com aluguel mensal são considerados.

---

## 📄 Licença

Este projeto está sob a licença MIT.
