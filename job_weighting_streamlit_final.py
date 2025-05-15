
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import openai

# Carica le variabili di ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dropdown per selezionare industry e size
industry_options = [
    "Technology", "Healthcare", "Finance", "Manufacturing", "Retail",
    "Energy", "Telecommunications", "Education", "Transportation", "Consulting"
]

size_options = {
    "1-10": 1,
    "11-50": 2,
    "51-200": 3,
    "201-500": 4,
    "501-1,000": 5,
    "1,001-5,000": 6,
    "5,001-10,000": 7,
    "10,001+": 8
}

st.title("AI Job Weighting Tool con Affidabilità e Contesto")

industry = st.selectbox("Seleziona l'industry", industry_options)
size_label = st.selectbox("Seleziona la size dell'azienda", list(size_options.keys()))
size_value = size_options[size_label]

uploaded_file = st.file_uploader("Carica il file Excel con le Job Description", type=["xlsx"])

# Funzione per calcolare pesatura e affidabilità
def get_ai_weighting(jd_text, industry, size_value):
    prompt = f"""
Sei un esperto di HR e Compensation. Analizza la seguente Job Description e restituisci un punteggio da 0 a 30 che rappresenti la seniority e la complessità della posizione. Tieni conto del settore: '{industry}' e della dimensione aziendale (livello: {size_value}).

Job Description:
{jd_text}

Rispondi nel formato:
PUNTEGGIO: <valore numerico tra 0 e 30>
AFFIDABILITÀ: <valore percentuale>
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        text = response['choices'][0]['message']['content']
        score = ""
        reliability = ""

        for line in text.splitlines():
            if "PUNTEGGIO" in line.upper():
                score = int(''.join(filter(str.isdigit, line)))
            elif "AFFIDABILIT" in line.upper():
                reliability = ''.join(filter(lambda x: x.isdigit() or x == '.', line))
        return score, f"{reliability}%"
    except Exception as e:
        return "Errore", "N/A"

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "Job Description" not in df.columns:
        st.error("Il file deve contenere una colonna chiamata 'Job Description'")
    else:
        st.write("Anteprima dei dati caricati:")
        st.dataframe(df)

        if st.button("Esegui pesatura AI"):
            with st.spinner("Elaborazione in corso..."):
                weights = []
                reliabilities = []
                for jd in df['Job Description']:
                    score, reliability = get_ai_weighting(jd, industry, size_value)
                    weights.append(score)
                    reliabilities.append(reliability)

                df["AI Weighting"] = weights
                df["Affidabilità"] = reliabilities

            st.success("Pesatura completata!")
            st.dataframe(df)

            csv = df.to_csv(index=False)
            st.download_button(
                label="Scarica il file con le pesature",
                data=csv,
                file_name="job_weighting_output.csv",
                mime="text/csv"
            )

