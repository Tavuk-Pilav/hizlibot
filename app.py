import os
import glob
import warnings  
import pandas as pd
import streamlit as st   
from streamlit_chat import message
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.connectors import PandasConnector
from streamlit_extras.colored_header import colored_header
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

warnings.filterwarnings('ignore')
os.environ['G_ENABLE_DIAGNOSTIC'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)

st.set_page_config(page_title="HızlıBot", page_icon=":rabbit2:")

# OpenAI API key and Chroma DB path
OPENAI_API_KEY = 'OPENAI_API_KEY'
CHROMA_PATH = "chroma"

# Chat Prompt Template
PROMPT_TEMPLATE = """
Soruyu yalnızca aşağıdaki bağlama dayanarak cevapla:

{context}

Yukarıdaki bağlama dayanarak soruyu cevapla: {question}
"""


# Initialize PandasAI and SmartDataframe
llm = OpenAI(api_token=OPENAI_API_KEY)

data = pd.read_csv('Data/harcama_gecmisi_ocak_subat_mart_nisan_final.csv')


field_descriptions = {
    'Yıl': 'Harcamanın yapıldığı yıl. (Örneğin: 2024)',
    'Ay': 'Harcamanın yapıldığı ay. (Örneğin: Ocak)',
    'Gün': 'Harcamanın yapıldığı gün. (Örneğin: 15)',
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
    'max_retries': 2}


connector = PandasConnector(
    {"original_df": data},
    field_descriptions=field_descriptions)


df = SmartDataframe(connector,
    description="Kişinin banka hesabından yaptığı harcama kayıtları",
    config=config
    )


def get_latest_chart_file():
    charts_dir = 'exports/charts/'
    list_of_files = glob.glob(os.path.join(charts_dir, '*.png'))
    if not list_of_files:
        return None
    
    latest_file = max(list_of_files, key=os.path.getctime)  
    return latest_file


def tr_promts(df, prompt):
    tr_promt = " Cevabı Türkçe olarak 1 kez döndür. Eğer grafik istiyorsam sadece 1 kez grafiği çiz."
    full_prompt = prompt + tr_promt
    response = df.chat(full_prompt)
    return response

# Function to handle user input starting with '/'
def handle_pandas_ai_query(query_text):
    if query_text.startswith('/'):
        # Process query using PandasAI
        response = tr_promts(df, query_text[1:])  # Remove the '/' and pass the rest as prompt
    else:
        # Handle regular queries using the default bot functionality
        response = generate_response(query_text)
    
    return response

def generate_response(query_text):
    # Handle regular queries as before
    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        return "Mesajınızı anlayamadım, size yardımcı olabilmemiz için 444 88 88 Telefon Bankacılığımızdan bize ulaşabilir ya da “Müşteri Temsilcisi“ yazarak canlı destek müşteri temsilcimizle görüşebilirsiniz."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    response_text = model.invoke(prompt)

    return response_text.content

# Streamlit UI setup
st.markdown("<h1 style='color: lightblue;'>HızlıBot 🐇</h1>", unsafe_allow_html=True)

# Custom CSS for the background and message colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    .user-message {
        background-color: #d4edda;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        margin-left: auto;
        color: black;
        width: fit-content;
        max-width: 80%;
    }
    .bot-message {
        background-color: #d1ecf1;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        color: black;
        width: fit-content;
        max-width: 80%;
    }
    .bot-message img {
    position: absolute;
    bottom: 10px;
    left: -60px; /* Resmin konuşma balonunun soluna çıkıntı yapmasını sağlamak için negatif bir değer kullanın */
    width: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state variables
if 'user_responses' not in st.session_state:
    st.session_state['user_responses'] = ["Merhaba"]
if 'bot_responses' not in st.session_state:
    st.session_state['bot_responses'] = ["Merhaba, ben akıl küpü chat asistanınız HızlıBot🐰 Size nasıl yardımcı olabilirim?"]

input_container = st.container()
response_container = st.container()

# Capture user input and display bot responses
user_input = st.text_input("Mesaj yazın: ", "", key="input")

with response_container:
    if user_input:
        response = handle_pandas_ai_query(user_input)
        st.session_state.user_responses.append(user_input)
        st.session_state.bot_responses.append(response)

    if st.session_state['bot_responses']:
        for i in range(len(st.session_state['bot_responses'])):
            st.markdown(f'<div class="user-message">{st.session_state["user_responses"][i]}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image("images/logo.png", width=50, use_column_width=True, clamp=True, output_format='auto')
            with col2:
                bot_response = st.session_state["bot_responses"][i]
                if ".png" in bot_response:
                    st.image(bot_response, use_column_width=True)
                else:
                    st.markdown(f'<div class="bot-message">{bot_response}</div>', unsafe_allow_html=True)


with input_container:
    display_input = user_input
