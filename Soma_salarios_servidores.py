#!/usr/bin/env python
# coding: utf-8

# # Exercício de Análise de Dados 
# *** 
# <br>
# 
# ### Cálculo da soma de remunerações em um dataframe a partir de uma lista importada de arquivos PDF.
# <br>

# <br>
# 
# ### Importação dos Módulos
# 
# <br>

# In[1]:


#utilizei o camelot pela sintaxe simples e eficiência
import os
import numpy as np
import pandas as pd
import camelot
import zipfile


# <br>
# 
# ### Importação dos Arquivos PDF e Concatenação da Listagem
# <br>
# Obs. O Camelot possui um bug: a seleção de várias páginas, (ex. pages='1-3' ou 'all'), não funciona. Então foi necessaŕio repetir a rotina de extração para cada página.
# 
# <br>
# 
# Isso também fez com que a rotina não funcionasse para o último arquivo, que só possui uma página, gerando erro de índice e obrigando a tratar esse último arquivo separadamente. 
# <br>
# <br>

# In[2]:


List_Path = './Lista_Completa/Arquivos/'
Ult_Path = './Lista_Completa/ult/'
Lista_Completa = pd.DataFrame()
df3 = pd.DataFrame(columns=[0,1,2,3,4,5,6,7,8])

# Leitura dos arquivos de 3 páginas
for arq in os.listdir(List_Path):
    df1 = camelot.read_pdf(List_Path+arq, pages='1') 
    df2 = df1[0].df
    df3 = df3.append(df2)
    df1 = camelot.read_pdf(List_Path+arq, pages='2') 
    df2 = df1[0].df
    df3 = df3.append(df2)
    df1 = camelot.read_pdf(List_Path+arq, pages='3') 
    df2 = df1[0].df
    df3 = df3.append(df2)
    
#Leitura do último arquivo com uma só página
df1 = camelot.read_pdf(List_Path+arq, pages='1')
df2 = df1[0].df
df3 = df3.append(df2)

df3.rename(columns=df3.iloc[0]).drop(df3.index[0])
df3.columns = ['A', 'B', 'C', 'NOME', 'E', 'F', 'G', 'H', 'I']
df3.drop(df3[['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I']], axis=1, inplace=True)
df3.drop(df3.index[0], axis=0, inplace=True)

#Criação da Lista Completa
Lista_Completa = Lista_Completa.append(df3)
Lista_Completa


# <br>
# 
# ### Explorando o Arquivo Geral zipado
# 
# <br>

# In[21]:


with zipfile.ZipFile('./202001_Servidores.zip') as BigFile:
    print(BigFile.namelist(),sep='\n')


# <br>
# 
# ### Preparação do Arquivo selecionado dentro do zip como DataFrame
# 
# <br>

# In[4]:


with zipfile.ZipFile('202001_Servidores.zip') as BigFile:
    with BigFile.open('202001_Remuneracao.csv') as data:
        dfBig = pd.read_csv(data, sep=';', decimal=",", low_memory=False, encoding='ISO-8859-1') #testar com nrows=10000 primeiro


# <br>
# 
# ### Filtragem dos Dados
# 
# <br>

# In[5]:


dfBig.columns


# In[6]:


dfBig[['REMUNERAÇÃO BÁSICA BRUTA (R$)']] #Seleção do campo a ser processado


# <br>
# 
# ### Eliminando registros inválidos
# 
# <br>

# In[7]:


dfBig.loc[dfBig["REMUNERAÇÃO BÁSICA BRUTA (R$)"].isnull()]  #verificando valores nulos para elaborar a melhor estratégia


# In[8]:


dfBig = dfBig.drop(dfBig.index[554388]) #como só há um valor nulo é melhor simplesmente excuí-lo


# In[9]:


dfBig.drop_duplicates()  #Eliminando valores duplicados, se houver


# In[10]:


dfBig.loc[dfBig["REMUNERAÇÃO BÁSICA BRUTA (R$)"] == 0] # verificando registros com remuneração = zero


# <br>
# 
# ## Substituir valores "zero" pela média.
# 
# <br>
# 
# Obs. Não há o campo "Órgão"na lista geral, mas como todos da lista de origem são do Ministério da Economia, com uma média salarial muito mais alta que a geral (~20.000 ao invés de ~8.000). Talvez fosse mais preciso substituir pela média da própria lista.
# 
# <br>

# In[11]:


SalMedia = dfBig["REMUNERAÇÃO BÁSICA BRUTA (R$)"].median()
SalMedia


# In[12]:


dfBig['REMUNERAÇÃO BÁSICA BRUTA (R$)'] = dfBig['REMUNERAÇÃO BÁSICA BRUTA (R$)'].replace(0,SalMedia) #Substituindo valores zero pela média


# In[13]:


dfWork = pd.DataFrame(dfBig, columns= ['NOME','REMUNERAÇÃO BÁSICA BRUTA (R$)'])
dfWork


# In[14]:


dfWork['REMUNERAÇÃO BÁSICA BRUTA (R$)'].astype(np.float32)


# In[15]:


dfFinal = dfWork.loc[dfBig['NOME'].isin(Lista_Completa['NOME'])]
dfFinal


# <br>
# 
# ### Soma Final da Remuneração dos Servidores da Lista
# 
# <br>

# In[25]:


SOMA = dfFinal['REMUNERAÇÃO BÁSICA BRUTA (R$)'].sum()
print("A soma de todas as reminerações da lista é: ")
print(SOMA)


# In[ ]:




