import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from connection import get_engine
st.set_page_config(page_title='Currency Analytics',layout='wide')
st.title('Анализ курсов валют')
engine=get_engine()
pairs_df=pd.read_sql(
    "select distinct base_currency,quote_currency from exchange_rate_daily order by base_currency,quote_currency",engine
)
pair_options=[f"{row.base_currency}/{row.quote_currency}" for row in pairs_df.itertuples()]
choice=st.selectbox('Выберите валютную пару',pair_options)
base,quote=choice.split('/')

features_df=pd.read_sql(
    'select date,rate,rolling_avg_7d from rate_features where base_currency=%(base)s and quote_currency=%(quote)s',
    engine,params={'base':base,'quote':quote}
)
st.subheader(f"Динамика курса{choice}")
st.line_chart(features_df.set_index('date')[['rate','rolling_avg_7d']])

std_df=pd.read_sql(
    'select distinct date,rate,rolling_std_7d from rate_features where base_currency=%(base)s and quote_currency=%(quote)s',
    engine,params={'base':base,'quote':quote}
)
st.subheader(f"Волатильность (rolling_std_7d)")
st.line_chart(std_df.set_index('date')['rolling_std_7d'])

rates_df=pd.read_sql(
    'select date,actual_rate,predicted_rate,naive_prediction from rate_predictions where base_currency=%(base)s and quote_currency=%(quote)s',
    engine,params={'base':base,'quote':quote}
)
st.subheader('Сравнение прогноза с фактическим значением')
st.line_chart(rates_df.set_index('date')[['actual_rate','predicted_rate','naive_prediction']])

metrics_df=pd.read_sql(
'select base_currency,quote_currency, '
    'avg(abs(actual_rate-naive_prediction)) as naive_mae, '
    'avg(abs(actual_rate-predicted_rate)) as model_mae '
    'from rate_predictions group by base_currency,quote_currency',engine
)
metrics_df['improvement_%']=(metrics_df['naive_mae']-metrics_df['model_mae'])/metrics_df['naive_mae']*100
st.subheader('Сравнение модели с наивным бейзлайном')
st.dataframe(metrics_df.style.format({'naive_mae':'{:.4f}','model_mae':'{:.4f}','improvement_%':'{:.2f}%'}))

pivot_df=pd.read_sql(
    "select date,base_currency || '/' || quote_currency as pair, rate from exchange_rate_daily",engine
).pivot(index='date',columns='pair',values='rate')
corr=pivot_df.corr()
fig_corr=go.Figure(data=go.Heatmap(z=corr.values,x=corr.columns,y=corr.columns,colorscale='RdBu',zmid=0))
st.plotly_chart(fig_corr,use_container_width=True)