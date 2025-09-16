#!/usr/bin/env python
# coding: utf-8

# In[1]:


##BIBLIOTECAS 
import plotly.io as pio
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import yfinance as yf
from binance.client import Client
from transformers import pipeline

get_ipython().run_line_magic('matplotlib', 'inline')

pio.renderers.default = "iframe_connected"


# ## 1) Aquisição dos dados de ações

# In[2]:


ticket = yf.Ticker("BTC-USD")
#df = ticket.history(period='3y', interval='1mo')
df = ticket.history(interval='1d', start='2018-01-01', end='2024-12-31')


# In[3]:


df


# In[4]:


df.tail(15)


# ## 2) Decomposição de uma série temporal 
# 
# ## Modelo matemático
# - Additive Model
#     - y(t) = Trend_t + Seasonality_t + Noise_t
# - Multiplicative Model
#     - y(t) = Trend_t * Seasonality_t * Noise_t

# In[5]:


df[['Close']].head()


# In[6]:


decomposicao = seasonal_decompose(df[['Close']], model='additive', period=18, extrapolate_trend=30)


# In[7]:


df[['Close']].plot()


# In[8]:


df['Close'].head()


# In[9]:


decomposicao.seasonal + decomposicao.resid + decomposicao.trend


# In[10]:


decomposicao.trend.iloc[0:5]


# In[11]:


decomposicao.plot();


# In[12]:


decomposicao_multi = seasonal_decompose(df[['Close']], model='multiplicative', period=18, extrapolate_trend=30)


# In[13]:


decomposicao.seasonal


# In[14]:


decomposicao_multi.seasonal


# In[15]:


max(decomposicao_multi.resid)


# In[16]:


ax, fig = plt.subplots(figsize=(15,8))
plt.plot(decomposicao.observed)
plt.plot(decomposicao.trend)


# In[17]:


fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1, figsize=(12,8))
decomposicao.observed.plot(ax=ax1)
decomposicao.trend.plot(ax=ax2)
decomposicao.seasonal.plot(ax=ax3)
decomposicao.resid.plot(ax=ax4)
plt.tight_layout()


# ## 3) Cálculo da média móvel

# In[18]:


df ['Close']


# In[19]:


df['Close'].rolling(7).mean()


# In[20]:


media_movel7d = df['Close'].rolling(7).mean()
media_movel14d = df['Close'].rolling(14).mean()
media_movel21d = df['Close'].rolling(21).mean()


# In[21]:


fig, ax = plt.subplots(figsize=(14,5))
plt.plot(media_movel7d, 'orange')
plt.plot(media_movel14d, 'red')
plt.plot(media_movel21d, 'black')
plt.plot(df['Close'])


# ## 4) Extração de features

# In[22]:


df.head()


# In[23]:


df.reset_index(inplace=True)


# In[24]:


df.head()


# In[25]:


# criar features para cada período
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
df['day'] = df['Date'].dt.day


# In[26]:


df.head()


# In[27]:


# Cálculo da rentabilidade: preço atual/ preço anterior * 100 - 100
df[['Close']]


# In[28]:


df['Close'].head()


# In[29]:


df['Close'].shift()


# In[30]:


df['rentabilidade'] = df['Close'] / df['Close'].shift() * 100 - 100


# In[31]:


df.head()


# In[32]:


def features_extraction(df_):
    #criar features para cada período de forma diferente
    df_['year'] = df_['Date'].dt.year
    df_['month'] = df_['Date'].dt.month
    df_['day'] = df_['Date'].dt.day
    df_['rentabilidade'] = df_['Close'] / df_['Close'].shift() * 100 - 100


# In[33]:


df.reset_index(inplace=True)


# In[34]:


features_extraction(df)


# In[35]:


df.head()


# ## Hipotese: 1) Existe um melhor mês para investir no ativo?

# #### Verificar o mês com menor rentabilidade, ou seja, período de baixa (nos últimos 7 anos):

# In[36]:


df.groupby('month').agg({'rentabilidade':'sum'}).plot(kind='bar')


# In[37]:


df.set_index('Date', inplace=True)


# In[38]:


media_movel30d = df['Close'].rolling(30).mean()
media_movel90d = df['Close'].rolling(90).mean()
fig, ax = plt.subplots(figsize=(8,4))
plt.plot(df['Close'])
plt.plot(media_movel30d, 'orange')
plt.plot(media_movel90d, 'green')


# ## Hipotese: 2) Existe um melhor dia para investir no BTC?

# In[39]:


df.groupby('day').agg({'rentabilidade':'sum'}).plot(kind='bar')


# ##### OBS: Quanto menor a sua rentabilidade, melhor oportunidade de compra.

# In[40]:


df.iloc[0]


# ## 5) Correlação de séries temporais

# In[41]:


tickets = ['ETH-USD', 'SOL-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 'USDBRL=X']


# In[42]:


dfs = []

for t in tickets:
    print('Reading ticker {}...' .format(t))
    ticket = yf.Ticker(t)
    aux = ticket.history(interval='1d', start='2021-01-01', end='2024-12-31')
    aux.reset_index(inplace=True)
    aux['ticket'] = t
    dfs.append(aux)


# In[43]:


dfs[1]


# In[44]:


for d in dfs:
    features_extraction(d)


# In[45]:


dfs[0]


# In[46]:


correlacao = pd.DataFrame()
for d in dfs:
    correlacao[d['ticket'].iloc[0]] = d['rentabilidade']


# In[47]:


correlacao.head()


# In[48]:


correlacao.corr()


# ##### OBS: Quanto mais próximos de 1, mais correlacionados são os ativos.

# ## Visualização de dados usando Seaborn

# In[49]:


import seaborn as sns


# In[50]:


ax, fig = plt.subplots(figsize=(20,5))
ax = sns.heatmap(correlacao.corr(), annot=True)


# ## Visualização de dados usando Plotly

# In[51]:


import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = 'notebook'


# In[52]:


def plot_lines(df_, columns=['Open', 'Close', 'High', 'Low']):

    fig = go.Figure()
    for c in columns:
        fig.add_trace(go.Scatter(x = list(df_.index),
                            y = df_[c],
                            mode = 'markers+lines',
                            name = c))
        fig.show()


# In[53]:


plot_lines(df)


# In[54]:


def plotCandleStick(df, acao='tickets'):
    tracel = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [tracel]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    fig.show() 


# In[55]:


plotCandleStick(df)


# ### Automação de Relatórios com IA (modelo pronto Hugging Face)

# In[36]:


from transformers import pipeline

# Usando o FLAN-T5 no modo correto (text2text-generation)
report_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1
)

# Texto base (igual ao seu, mas sem alterar nada)
texto_base = """
Você é um assistente que escreve apenas em português.
Escreva um relatório claro e objetivo sobre a análise abaixo.

Análise de séries temporais de criptomoedas:
- Maior correlação entre BTC e ETH
- Melhor mês de rentabilidade: Março
- Piores meses: Junho e Setembro
- Média móvel indica tendência de alta em 2025

Escreva o relatório em português, em 3 parágrafos, explicando:
1. Tendências principais
2. Riscos identificados
3. Recomendação geral para investidores iniciantes
"""

# Geração de resposta
resposta = report_generator(
    texto_base,
    max_new_tokens=350,
    temperature=0.7,
    top_p=0.9,
    num_return_sequences=1
)

print(resposta[0]['generated_text'])


# ## Previsão de Séries Temporais com IA: Análise do Preço do Bitcoin (BTC) - (modelo pronto Hugging Face)

# ### Previsão com Prophet 
# 
# - Mostra os preços históricos do Bitcoin (pontos pretos) e a previsão futura (linha azul).
# - A área sombreada azul indica a incerteza da previsão (intervalo de confiança).
# - Serve para analisar a tendência futura do preço com base no histórico.

# In[37]:


# Previsão de BTC com Prophet
import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 1) Baixar dados do BTC
df = yf.download("BTC-USD", start="2018-01-01", end="2025-01-01", interval="1mo")
df = df[['Close']].dropna()  # vamos usar apenas o preço de fechamento


# 2) Preparar dados para Prophet
df_prophet = df.reset_index()[['Date', 'Close']]
df_prophet.columns = ['ds', 'y']  # Prophet exige colunas ds (data) e y (valor)


# 3) Criar e treinar modelo
model = Prophet(daily_seasonality=False, yearly_seasonality=True, weekly_seasonality=False)
model.fit(df_prophet)


# 4) Criar datas futuras para previsão (12 meses à frente)
future = model.make_future_dataframe(periods=12, freq='MS')


# 5) Fazer previsão
forecast = model.predict(future)


# 6) Visualização da previsão
fig1 = model.plot(forecast)
plt.title("Previsão de BTC com Prophet")
plt.xlabel("Data")
plt.ylabel("Preço de fechamento (USD)")
plt.show()


# ### Tendência (trend)
# 
# - Mostra a direção geral que o preço do Bitcoin tende a seguir ao longo do tempo, sem se preocupar com oscilações do dia a dia.
# - Se a linha está subindo, significa que o modelo enxerga uma tendência de crescimento no preço.
# - Ajuda a perceber se, no horizonte analisado, o ativo tende mais a valorizar ou a cair.

# In[27]:


import matplotlib.dates as mdates

last_hist = df_prophet['ds'].max()
future_mask = forecast['ds'] > last_hist

plt.figure(figsize=(10,4))
plt.plot(forecast.loc[future_mask, 'ds'], forecast.loc[future_mask, 'trend'], linewidth=2)

plt.title("Tendência prevista (próximos 12 meses)")
plt.xlabel("Data")
plt.ylabel("Trend (USD)")

# Formatando o eixo X para mostrar meses
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# ### Sazonalidade Anual (yearly)
# - Mostra como o preço do Bitcoin tende a variar ao longo de um ano típico.
# - Valores acima de zero indicam meses em que o preço tende a ficar acima da tendência.
# - Valores abaixo de zero indicam meses em que tende a ficar abaixo da tendência.
# - Exemplo: se em março o gráfico mostra +5000, significa que historicamente em março o BTC fica cerca de 5 mil USD acima da tendência média.

# In[21]:


from prophet.plot import plot_seasonality

# Plotar apenas a sazonalidade anual
fig_yearly = plot_seasonality(model, 'yearly')
plt.title("Sazonalidade Anual do Bitcoin (média por ano)")
plt.xlabel("Dias do ano")
plt.ylabel("Impacto no preço (USD)")
plt.show()


# ### Análise Exploratória Automatizada de Dados (EDA – Exploratory Data Analysis)

# In[ ]:


from ydata_profiling import ProfileReport

profile = ProfileReport(df, title="Relatório de Exploração de Dados (Cripto)", explorative=True)
profile.to_file("relatorio_cripto.html")

