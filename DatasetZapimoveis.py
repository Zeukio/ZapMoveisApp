import ZapimoveisScrapper as zap
import pandas as pd 
#Busca_string  = "sc+florianopolis++ingleses-do-rio-vermelho"
Busca_string  = "sc+florianopolis"
n_paginas  =  1
Resultado_da_busca = zap.search(localization = Busca_string, num_pages = n_paginas)
print(Resultado_da_busca)
Resultado_da_busca.to_csv("Resultado_da_busca7.csv")

