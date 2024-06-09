import os
import openai
import warnings
import numpy as np  
import pandas as pd 
import seaborn as sns  
from pandasai import Agent
from pandasai.llm import OpenAI
import matplotlib.pyplot as plt  
from pandasai import SmartDataframe
from pandasai.connectors import BaseConnector
from pandasai.connectors import PandasConnector

warnings.filterwarnings('ignore')
os.environ['G_ENABLE_DIAGNOSTIC'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)


llm = OpenAI(api_token="Your OpenAI API Key")

data = pd.read_csv('Data/harcama_gecmisi_ocak_subat.csv')


field_descriptions = {
    'Tarih': 'Harcamanın yapıldığı tarih. (Örneğin: 2024-01-15)',
    'İşlem Türü': 'Harcamanın türü. Bu, harcamanın hangi kategoriye girdiğini belirtir. (Örneğin: Alışveriş, Fatura Ödemesi, ATM Çekimi, Restoran, Ulaşım)',
    'Tutar': 'Harcamanın parasal değeri. (Örneğin: 150.75)',
    'Harcama Kategorisi': 'Harcamanın yapıldığı genel kategori. (Örneğin: Market, Elektrik, Su, İnternet, ATM, Restoran, Ulaşım)',
    'Açıklama': 'Harcama hakkında daha spesifik bilgi veren açıklama. Genellikle mağaza adı veya fatura türü gibi detaylar içerir. (Örneğin: Migros, Kebapçı, Otobüs)',
}


config = {
    'llm': llm,
    'save_charts': True,
    'save_charts_path': 'exports/charts',
    'open_charts': False,
    'max_retries': 1}


connector = PandasConnector(
    {"original_df": data},
    field_descriptions=field_descriptions)


df = SmartDataframe(connector,
    description="Kişinin banka hesabından yaptığı harcama kayıtları",
    config=config
    )


def tr_promts(df, prompt):
    tr_promt = " Cevabı Türkçe olarak 1 kez döndür. Eğer grafik istiyorsam sadece 1 kez grafiği çiz."
    full_prompt = prompt + tr_promt
    response = df.chat(full_prompt)
    return response


user_input = input("Size nasıl yardımcı olabilirim: ")


response = tr_promts(df, user_input)
print(response)