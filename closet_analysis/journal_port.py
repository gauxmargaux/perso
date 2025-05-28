import streamlit as st
import pandas as pd
from datetime import date
import os

FICHIER_CSV = "garde_robe.csv"

# Charger les données
if not os.path.exists(FICHIER_CSV):
    st.error("Aucun fichier garde_robe.csv trouvé.")
    st.stop()

df = pd.read_csv(FICHIER_CSV)

st.title("📅 Marquer les vêtements portés aujourd'hui")

# Filtrer par catégorie (optionnel)
categorie = st.selectbox("Filtrer par type de vêtement", ["Tous"] + sorted(df["type"].unique()))
df_filtré = df if categorie == "Tous" else df[df["type"] == categorie]

# Liste à cocher
selection = st.multiselect(
    "Quels vêtements portes-tu aujourd'hui ?",
    options=df_filtré["id"],
    format_func=lambda i: f"{df[df['id'] == i]['type'].values[0]} - {df[df['id'] == i]['couleur'].values[0]}"
)

if st.button("✅ Enregistrer le port du jour"):
    today = date.today().isoformat()

    for item_id in selection:
        idx = dperof[df["id"] == item_id].index[0]
        df.at[idx, "nb_ports"] += 1
        df.at[idx, "date_dernier_port"] = today

    df.to_csv(FICHIER_CSV, index=False)
    st.success("Enregistré avec succès ✅")
