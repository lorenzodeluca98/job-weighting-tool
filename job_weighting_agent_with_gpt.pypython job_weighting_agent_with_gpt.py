
matches = []
for idx in I[0]:
    matches.append({
        "title": titles[idx],
        "level": levels[idx],
        "description": descriptions[idx]
    })
    print(f"- {titles[idx]} (Level: {levels[idx]})")
    print(f"  ➤ JD: {descriptions[idx]}\n")
matches.append({
    "title": titles[idx],
    "level": levels[idx],
    "description": descriptions[idx]
})
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import openai

# 🔐 Inserisci la tua API Key qui
openai.api_key = "INSERISCI_LA_TUA_API_KEY"

# Dataset di esempio (puoi espanderlo)
titles = [
    "HR Manager", "Finance Analyst", "Marketing Director", "Logistics Supervisor",
    "IT Support Specialist", "Operations Manager", "Legal Counsel", 
    "Sales Representative", "Chief Marketing Officer", "Procurement Officer"
]

descriptions = [
    "Oversees HR processes, talent management, and employee relations.",
    "Supports budgeting and forecasting with analytical financial models.",
    "Leads marketing strategy across regional teams and digital channels.",
    "Manages warehouse operations, supervises team and logistics KPIs.",
    "Provides technical support, system troubleshooting, and maintenance.",
    "Leads production and logistics in a high-volume manufacturing site.",
    "Provides legal advice on contracts, compliance and risk management.",
    "Executes in-store sales and manages customer relationships.",
    "Defines global marketing vision, manages large international team.",
    "Handles supplier negotiation and procurement operations at plant level."
]

levels = [12, 13, 20, 11, 6, 24, 14, 4, 28, 12]

# Inizializza il modello di embedding
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(descriptions)

# Costruisce l'indice FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Input dell’utente
print("📩 Inserisci la nuova Job Description da valutare:")
new_jd = input("> ")

# Calcola embedding e cerca i ruoli più simili
new_embedding = model.encode([new_jd])
D, I = index.search(np.array(new_embedding), 3)

print("\n📊 Ruoli più simili trovati:")
matches = []
for idx in I[0]:
    matches.append({
    "title": titles[idx],
    "level": levels[idx],
    "description": descriptions[idx]
})


