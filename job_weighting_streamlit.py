import streamlit as st
import pandas as pd
import openai
import os

# Inserisci la tua OpenAI API Key
openai.api_key = "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"

st.set_page_config(page_title="AI Job Weighting Tool", layout="wide")
st.title("⚖️ AI Job Weighting")
st.markdown("Carica un file `.csv` con colonne **Job Title** e **Job Description**.")

uploaded_file = st.file_uploader(
    "Carica il file CSV", type=["csv"], key="file_upload"
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File caricato con successo.")
        st.dataframe(df)

        if "Job Title" not in df.columns or "Job Description" not in df.columns:
            st.error("❌ Il file deve contenere le colonne 'Job Title' e 'Job Description'.")
        else:
            if st.button("Esegui pesatura con AI"):
                weights = []

                for idx, row in df.iterrows():
                    prompt = f"""Sei un esperto di Compensation & Benefits. Ti verrà fornito un Job Title e una Job Description.

Valuta la pesatura del ruolo considerando la complessità, l'autonomia richiesta, il livello di responsabilità e il potenziale impatto sull’organizzazione.

Job Title: {row['Job Title']}
Job Description: {row['Job Description']}

Rispondi solo con un numero da 0 a 30."""

                    try:
                        response = openai.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0,
                        )
                        reply = response.choices[0].message.content.strip()
                        weight = int(''.join(filter(str.isdigit, reply)))
                    except Exception as e:
                        weight = 0
                        st.error(f"Errore alla riga {idx + 1}: {e}")

                    weights.append(weight)

                df["Job Weight (0-30)"] = weights
                st.success("✅ Pesatura completata.")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Scarica risultato CSV",
                    data=csv,
                    file_name="job_weighting_output.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")

