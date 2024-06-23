# HızlıBot🐇

This application was developed as part of the Fintern Future Talent Hackathon. It's a RAG-LLM-GenAI based chatbot designed to answer questions on customers' minds. You send your question and the chatbot generates the most appropriate answer from vectordb or analyzes data from PandasAI.

## Technologies Used

- [LangChain](https://python.langchain.com/v0.2/docs/introduction/) - LangChain version: 0.2.5
- [PandasAI](https://docs.pandas-ai.com/intro) - PandasAI version: 2.1.1 
- [Streamlit](https://docs.streamlit.io/) - Streamlit version: 1.36.0

---

## Requirements

### Environment

Ensure that your Python version is set to `3.10.12` (pip version is `24.0`):

```bash
python --version
```
- Setting up Virtualenv:

```bash
pip install virtualenv
```
- Creating a Virtual Environment:
```bash
virtualenv venv
```
- Activating the Virtual Environment:
```bash
source venv/bin/activate
```
- Installing the necessary libraries:
```bash
pip install -r requirements.txt
```

### Configuration

- Set up your .env file:
- Set up your .streamlit/secrets.toml file:
- Set up your app.py file:

```bash
cd <project-directory>
```

```bash
- Create the .env file and add your OPENAI_API_KEY:

    OPENAI_API_KEY='key' # .env file
    openai_api_key='Your OpenAI API Key' # secrets.toml
    OPENAI_API_KEY = 'OPENAI_API_KEY' # app.py 
```
### Create VectorDB

```bash
python3 create_database.py
```

### Run

- Launch the Streamlit app in terminal:
```bash
streamlit run app.py
```
---

https://github.com/Future-Talent-Hackathon/chatbot/assets/88631980/551d957a-b3a4-488f-ba05-abf0b5812f22
