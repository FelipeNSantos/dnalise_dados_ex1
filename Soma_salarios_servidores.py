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

# In[2]:


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

# In[9]:


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
for arq in os.listdir(Ult_Path):
    df1 = camelot.read_pdf(Ult_Path+arq, pages='1')
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

# In[3]:


with zipfile.ZipFile('Servidores.zip') as BigFile:
    print(BigFile.namelist(),sep='\n')


# <br>
# 
# ### Preparação do Arquivo selecionado dentro do zip como DataFrame
# 
# <br>

# In[26]:


with zipfile.ZipFile('Servidores.zip') as BigFile:
    with BigFile.open('Servidores/202001_Remuneracao.csv') as data:
        dfBig = pd.read_csv(data, sep=';', decimal=",", low_memory=False, encoding='ISO-8859-1') #testar com nrows=10000 primeiro


# <br>
# 
# ### Filtragem dos Dados
# 
# <br>

# In[11]:


dfBig.columns


# In[16]:


#Extração do subconjunto de dados
dfSEL = dfBig.loc[dfBig['NOME'].isin(Lista_Completa['NOME'])] 
dfSEL


# In[27]:


#Filtragem inicial do campo a ser processado
dfWork = pd.DataFrame(dfSEL['REMUNERAÇÃO BÁSICA BRUTA (R$)'])
dfWork


# <br>
# 
# ### Eliminando registros inválidos
# 
# <br>

# In[21]:


dfWork.loc[dfWork["REMUNERAÇÃO BÁSICA BRUTA (R$)"].isnull()]  #verificando valores nulos para elaborar a melhor estratégia


# In[8]:


#Não há valores nulos


# In[24]:


Transformando em dfloat32 para economizar memória no processamento
dfWork['REMUNERAÇÃO BÁSICA BRUTA (R$)'].astype(np.float32)


# <br>
# 
# ### Soma Final da Remuneração dos Servidores da Lista
# 
# <br>

# In[28]:


SOMA = dfWork['REMUNERAÇÃO BÁSICA BRUTA (R$)'].sum()
print("A soma de todas as reminerações da lista é: ")
print(SOMA)


# In[ ]:




