import os
import warnings
import numpy as np  
import pandas as pd 
import seaborn as sns  
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.connectors import PandasConnector
import streamlit as st

st.set_page_config(page_title="Harcama Geçmişi Chatbot", page_icon=":money_with_wings:")

warnings.filterwarnings('ignore')
os.environ['G_ENABLE_DIAGNOSTIC'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)

openai_api_key = st.secrets["openai_api_key"]

llm = OpenAI(api_token=openai_api_key)

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

st.title("FibaBot")
st.write("Lütfen sormak istediğiniz soruyu aşağıya yazınız:")

user_input = st.text_input("Soru:")

if st.button("Gönder"):
    if user_input:
        response = tr_promts(df, user_input)
        st.write("Yanıt:")
        st.write(response)

        # If there is an image saved, display it
        chart_path = 'exports/charts'
        if os.path.exists(chart_path) and any(os.scandir(chart_path)):
            image_files = [f for f in os.scandir(chart_path) if f.is_file()]
            latest_image = max(image_files, key=lambda x: x.stat().st_mtime)
            st.image(latest_image.path)
    else:
        st.write("Lütfen bir soru giriniz.")
