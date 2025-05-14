import streamlit as st
import pandas as pd
import openai
import os

# Inserisci la tua API Key
openai.api_key = "INSERISCI_LA_TUA_API_KEY"

def get_job_weighting(title, description):
    prompt = f"""Sei un esperto di HR e compensation. Assegna un punteggio da 0 a 30 a questo ruolo in base alla descrizione, considerando che più è strategico, complesso e ad alto impatto, più alta sarà la valutazione.

Job title: {title}
Job description: {description}

Rispondi solo con un numero da 0 a 30."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        result = response.choices[0].message["content"].strip()
        return int(result)
    except Exception as e:
        return f"Errore: {e}"

st.title("AI Job Weighting Tool")

uploaded_file = st.file_uploader("Carica un file Excel o CSV con Job Title e Job Description", type=["xlsx", "csv"], key="job_upload")

if uploaded_file is not None:
    file_ext = os.path.splitext(uploaded_file.name)[1]

    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Formato file non supportato. Carica un file .csv o .xlsx")
        st.stop()

    if "Job Title" not in df.columns or "Job Description" not in df.columns:
        st.error("Il file deve contenere le colonne 'Job Title' e 'Job Description'")
    else:
        with st.spinner("Calcolo dei punteggi in corso..."):
            df["Weighting"] = df.apply(lambda row: get_job_weighting(row["Job Title"], row["Job Description"]), axis=1)

        st.success("Calcolo completato!")
        st.dataframe(df)

        output_excel = df.to_excel(index=False)

        st.download_button(
            label="📥 Scarica Excel con pesature",
            data=output_excel,
            file_name="job_weighting_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
