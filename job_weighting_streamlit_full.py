import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import openai
import random

# Carica chiave API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dropdown iniziali
st.title("AI Job Weighting")

size = st.selectbox("Seleziona la dimensione dell'azienda (LinkedIn)", [
    "1-10", "11-50", "51-200", "201-500", "501-1.000", "1.001-5.000", "5.001-10.000", "10.001+"
])

industry = st.selectbox("Seleziona l'industry", [
    "Technology", "Finance", "Healthcare", "Retail", "Education", "Manufacturing",
    "Consulting", "Energy", "Telecommunications", "Transportation", "Hospitality",
    "Legal", "Entertainment", "Real Estate", "Pharma", "Automotive", "Public Sector", "Other"
])

# Funzione per calcolare la pesatura
def get_ai_weighting(jd_text, size, industry):
    prompt = f"""
    Sei un esperto di HR e Compensation. Assegna un punteggio da 0 a 30 alla seguente Job Description in base alla complessità del ruolo, alla dimensione aziendale ("{size}") e al settore ("{industry}").
    Job Description:
    {jd_text}
    Rispondi solo con il numero.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return int(response['choices'][0]['message']['content'].strip())
    except Exception as e:
        return f"Errore: {e}"

# Funzione per suggerire Job Title
def get_job_titles(jd_text, size, industry):
    prompt = f"""
    Sei un esperto di HR. Sulla base della seguente Job Description, della dimensione aziendale ("{size}") e del settore ("{industry}"), suggerisci il Job Title più adatto. Fornisci anche 2 alternative.
    
    Job Description:
    {jd_text}
    
    Rispondi in questo formato:
    - Job Title Principale: ...
    - Alternativa 1: ...
    - Alternativa 2: ...
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Errore: {e}"

# Funzione per affidabilità (mock)
def estimate_confidence():
    return f"{random.randint(70, 95)}%"  # In futuro collegare a DB per migliorare

# Caricamento file Excel
uploaded_file = st.file_uploader("Carica il file Excel con le Job Description", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "Job Description" not in df.columns:
        st.error("Il file deve contenere una colonna chiamata 'Job Description'")
    else:
        st.write("Anteprima dei dati caricati:")
        st.dataframe(df)

        if st.button("Avvia Analisi AI"):
            with st.spinner("Elaborazione in corso..."):
                df['AI Weighting'] = df['Job Description'].apply(lambda jd: get_ai_weighting(jd, size, industry))
                df['Job Title Suggerito'] = df['Job Description'].apply(lambda jd: get_job_titles(jd, size, industry))
                df['Affidabilità'] = df['Job Description'].apply(lambda _: estimate_confidence())

            st.success("Analisi completata!")
            st.dataframe(df)

            csv = df.to_csv(index=False)
            st.download_button(
                label="Scarica il file analizzato",
                data=csv,
                file_name="job_analysis_output.csv",
                mime="text/csv"
            )

