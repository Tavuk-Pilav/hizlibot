# Hızlı Bot 🐇

This application was developed as part of the Fintern Future Talent Hackathon. It's a RAG-LLM-GenAI based chatbot designed to answer questions on customers' minds. You send your question and the chatbot generates the most appropriate answer from vectordb or analyzes data from PandasAI.

## Technologies Used

- [LangChain](https://python.langchain.com/v0.2/docs/introduction/) - LangChain version: 0.2.5
- [PandasAI](https://docs.pandas-ai.com/intro) - PandasAI version: 2.1.1 
- [Streamlit](https://docs.streamlit.io/) - Streamlit version: 1.29.0

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
- Set up your .env file:

```bash
cd <project-directory>
```
- Installing the necessary libraries:
```bash
pip install -r requirements.txt
```

### Run

- Launch the Streamlit app in terminal:
```bash
streamlit run app.py
```
---