#!/usr/bin/env python
# coding: utf-8

# ### Análise de dados exploratória - Incidentes no Aeródromo Brasil

# In[67]:


import pandas as pd
import pandera as pa  ### serve para validar tipos de dados do dataset


# In[68]:


# Carregando arquivo, definindo separador, convertendo e ajustando datas
# Campos vazios são representados com "Nan" para texto e "Nat" para datas
valores_ausentes = ['**','###!','####','****','*****','NULL']
df = pd.read_csv("C:\DataSets\python\ocorrencia.csv", sep=";", parse_dates=['ocorrencia_dia'], dayfirst=True, na_values=valores_ausentes)
df.head(10)


# In[69]:


df.info()


# In[11]:


# Validando o schema proposto utilizando "Expressões Regulares"

schema = pa.DataFrameSchema(
    columns = {
        "codigo_ocorrencia":pa.Column(pa.Int),
        "codigo_ocorrencia2":pa.Column(pa.Int),
        "ocorrencia_classificacao":pa.Column(pa.String),
        "ocorrencia_cidade":pa.Column(pa.String),
        "ocorrencia_uf":pa.Column(pa.String, pa.Check.str_length(2,2), nullable=True),
        "ocorrencia_aerodromo":pa.Column(pa.String, nullable=True),
        "ocorrencia_dia":pa.Column(pa.DateTime),
        "ocorrencia_hora":pa.Column(pa.String, 
                          pa.Check.str_matches(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$') ,nullable=True),
        "total_recomendacoes":pa.Column(pa.Int)
    }
)  


# In[66]:


schema.validate(df)


# In[13]:


df.dtypes


# In[14]:


df.tail()


# In[15]:


# Busca por índice
df.iloc[10:15]


# In[16]:


# Busca por Label
df.loc[10:15]


# In[17]:


# Busca de dados referenciando a coluna
df.loc[:,'ocorrencia_uf']


# In[18]:


# Busca de dados referenciando a coluna de forma mais simples
df['ocorrencia_uf']


# In[19]:


# Função IsNA - soma de valores Não Disponíveis
df.isna().sum()


# In[20]:


# Função IsNA - soma de valores Não Disponíveis
df.isnull().sum()


# In[21]:


# Filtrando os valores Não Disponíveis em coluna específica
df.ocorrencia_uf.isnull()


# In[22]:


# Identificando registros com valores Não Disponíveis
df.loc[df.ocorrencia_uf.isnull()]


# In[23]:


# Aumentando a capacidade de análise usando filtros
filtro = df.ocorrencia_uf.isnull()
df.loc[filtro]


# ### Utiliizando Filtros

# In[24]:


filtro = df.ocorrencia_aerodromo.isnull()
df.loc[filtro]


# In[25]:


filtro = df.ocorrencia_hora.isnull()
df.loc[filtro]


# In[26]:


# Identificando valores Nulos
df.count()


# In[27]:


# Ocorrências com mais de 10 Recomendações
filtro = df.total_recomendacoes > 10
df.loc[filtro]


# In[28]:


# Ocorrências com mais de 10 Recomendações em coluna específica
filtro = df.total_recomendacoes > 10
df.loc[filtro, 'ocorrencia_cidade']


# In[29]:


# Ocorrências com mais de 10 Recomendações em várias colunas
filtro = df.total_recomendacoes > 10
df.loc[filtro, ['ocorrencia_cidade', 'total_recomendacoes']]


# In[30]:


# Ocorrências cuja classificação  == INCIDENTE GRAVE
filtro = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
df.loc[filtro]


# In[31]:


# Ocorrências cuja classificação  == INCIDENTE GRAVE e o Estado == SP (dois filtros)
filtro1 = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 & filtro2]


# In[32]:


# Ocorrências cuja classificação  == INCIDENTE GRAVE ou Estado == SP (dois filtros)
filtro1 = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 | filtro2]


# In[33]:


# Ocorrências cuja classificação  == INCIDENTE GRAVE ou CLASSIFICAÇÃO == INCIDENTE e Estado == SP (três filtros)
filtro1 = ((df.ocorrencia_classificacao == 'INCIDENTE GRAVE') | (df.ocorrencia_classificacao == 'INCIDENTE'))
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 & filtro2]


# In[34]:


# Ocorrências cuja classificação  == INCIDENTE GRAVE ou CLASSIFICAÇÃO == INCIDENTE e Estado == SP (usando método IsIn)
filtro1 = df.ocorrencia_classificacao.isin (['INCIDENTE GRAVE', 'INCIDENTE'])
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 & filtro2]


# In[35]:


# Ocorrências cuja Cidade começem com a letra C
filtro = df.ocorrencia_cidade.str[0] == 'C'
df.loc[filtro]


# In[36]:


# Ocorrências cuja Cidade terminam com a letra A
filtro = df.ocorrencia_cidade.str[-1] == 'A'
df.loc[filtro]


# In[37]:


# Ocorrências cuja Cidade terminam com caracteres NA
filtro = df.ocorrencia_cidade.str[-2:] == 'NA'
df.loc[filtro]


# ### Aplicando Métodos

# In[38]:


# Ocorrências cuja Cidade comtém os caracteres REC
filtro = df.ocorrencia_cidade.str.contains('REC')
df.loc[filtro]


# In[39]:


# Ocorrências cuja Cidade comtém os caracteres REC ou AL
filtro = df.ocorrencia_cidade.str.contains('REC|AL')
df.loc[filtro]


# ### Filtrando Datas

# In[40]:


# Ocorrências do Ano 2015 utilizando o Operador de Acesso "dt"
filtro = df.ocorrencia_dia.dt.year == 2015
df.loc[filtro]


# In[41]:


# Ocorrências do Ano 2015 e Mês 12 (utilizando o Operador de Acesso "dt")
filtro1 = df.ocorrencia_dia.dt.year == 2015
filtro2 = df.ocorrencia_dia.dt.month == 12
df.loc[filtro1 & filtro2]


# In[42]:


# Ocorrências do Ano 2015 e Mês 12 (utilizando o Operador de Acesso "dt")
filtro =(df.ocorrencia_dia.dt.year == 2015) & (df.ocorrencia_dia.dt.month == 12)
df.loc[filtro]


# In[43]:


# Ocorrências do Ano 2015 e Mês 12 e dias entre 3 e 8(utilizando o Operador de Acesso "dt")
filtro_ano = df.ocorrencia_dia.dt.year == 2015
filtro_mes = df.ocorrencia_dia.dt.month == 12
filtro_dia_inicio = df.ocorrencia_dia.dt.day > 2 
filtro_dia_fim = df.ocorrencia_dia.dt.day < 9
df.loc[filtro_ano & filtro_mes & filtro_dia_inicio & filtro_dia_fim]


# ### Concatenando colunas

# In[44]:


# Concatenando e Convertendo colunas do tipo (string & data/hora) para (datetime64) usando o método "astype"
df['ocorrencia_dia_hora'] = pd.to_datetime(df.ocorrencia_dia.astype(str) + ' ' + df.ocorrencia_hora)
df.head()


# In[45]:


df.dtypes


# In[46]:


# Visualizando a coluna Data/Hora no formato "datetime64"
filtro_ano = df.ocorrencia_dia_hora.dt.year == 2015
filtro_mes = df.ocorrencia_dia_hora.dt.month == 12
filtro_dia_inicio = df.ocorrencia_dia_hora.dt.day > 2 
filtro_dia_fim = df.ocorrencia_dia_hora.dt.day < 9
df.loc[filtro_ano & filtro_mes & filtro_dia_inicio & filtro_dia_fim]


# In[47]:


# Fazendo a busca de Data/Hora após a concatenação
filtro1 = df.ocorrencia_dia_hora >= '2015-12-03 11:00:00'
filtro2 = df.ocorrencia_dia_hora <= '2015-12-08 14:30:00'
df.loc[filtro1 & filtro2]


# ### Agrupamento de Dados

# In[48]:


# Ocorrências do Ano 2015 e Mês 03
filtro1 = df.ocorrencia_dia.dt.year == 2015
filtro2 = df.ocorrencia_dia.dt.month == 3
df201503 = df.loc[filtro1 & filtro2]
df201503


# In[49]:


df201503.count()


# In[50]:


# Verificando registros agrupados SEM valores nulos
df201503.groupby(['ocorrencia_classificacao']).codigo_ocorrencia.count()


# In[51]:


# Verificando registros agrupados COM valores nulos
df201503.groupby(['ocorrencia_classificacao']).ocorrencia_aerodromo.count()


# In[52]:


# Contando número de linhas agrupadas
df201503.groupby(['ocorrencia_classificacao']).size()


# In[53]:


# Contando número de linhas agrupadas em ordem crescente
df201503.groupby(['ocorrencia_classificacao']).size().sort_values()


# In[54]:


# Contando número de linhas agrupadas em ordem decrescente
df201503.groupby(['ocorrencia_classificacao']).size().sort_values(ascending=False)


# In[55]:


# Agrupando ocorrências pelo Ano == 2010 e Região Sudeste
filtro1 = df.ocorrencia_dia.dt.year == 2010
filtro2 = df.ocorrencia_uf.isin(['SP', 'MG', 'ES', 'RJ'])
dfsudeste2010 = df.loc[filtro1 & filtro2]
dfsudeste2010


# In[56]:


# Agrupando Incidentes na Região Sudeste por 'ocorrencia_classificacao'
dfsudeste2010.groupby(['ocorrencia_classificacao']).size()


# In[57]:


dfsudeste2010.count()


# In[58]:


# Agrupando Incidentes na Região Sudeste por 'ocorrencia_classificacao' e Estado
dfsudeste2010.groupby(['ocorrencia_classificacao', 'ocorrencia_uf']).size()


# In[59]:


# Agrupando Incidentes na Região Sudeste por 'ocorrencia_classificacao' e Cidade
dfsudeste2010.groupby(['ocorrencia_cidade']).size().sort_values(ascending=False)


# In[60]:


filtro1 = dfsudeste2010.ocorrencia_cidade == 'RIO DE JANEIRO'
filtro2 = dfsudeste2010.total_recomendacoes > 0
dfsudeste2010.loc[filtro1 & filtro2]


# In[61]:


filtro = dfsudeste2010.ocorrencia_cidade == 'RIO DE JANEIRO'
dfsudeste2010.loc[filtro].total_recomendacoes.sum()


# In[62]:


# Agrupando "total_recomendacoes" por Cidade
filtro = dfsudeste2010.total_recomendacoes > 0
dfsudeste2010.loc[filtro].groupby(['ocorrencia_cidade']).total_recomendacoes.sum().sort_values()


# In[63]:


# Agrupando totais utilizando a coluna COM valores nulos (agrupa valores nulos no final)
filtro = dfsudeste2010.total_recomendacoes > 0
dfsudeste2010.loc[filtro].groupby(['ocorrencia_aerodromo'], dropna=False).total_recomendacoes.sum().sort_values()


# In[64]:


# Agrupando "total_recomendacoes" por Meses
dfsudeste2010.loc[filtro].groupby(['ocorrencia_cidade', dfsudeste2010.ocorrencia_dia.dt.month]).total_recomendacoes.sum()


# In[65]:


filtro1 = dfsudeste2010.total_recomendacoes > 0
filtro2 = dfsudeste2010.ocorrencia_cidade == 'SÃO PAULO'
dfsudeste2010.loc[filtro1 & filtro2]


# In[ ]:




