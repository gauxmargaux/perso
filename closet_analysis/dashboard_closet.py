import streamlit as st
import pandas as pd
import os
import plotly.express as px
from PIL import Image

FICHIER_CSV = "garde_robe.csv"
DOSSIER_PHOTOS = "photos"

st.title("📊 Analyse de la garde-robe")

df = pd.read_csv(FICHIER_CSV)

# 📊 Statistiques
st.metric("Total vêtements", len(df))
# st.metric("Total ports", df["nb_ports"].sum())

# # 📈 Graphiques
# st.subheader("Nombre de ports par type")
# fig = px.bar(df, x="type", y="nb_ports", color="couleur", barmode="group")
# st.plotly_chart(fig)

# 🖼️ Galerie
st.subheader("Galerie des vêtements")

for _, row in df.iterrows():
    with st.expander(f"{row['type']} - {row['couleur']} ({row['marque']})"):
        cols = st.columns([1, 2])
        if row["photo"] and os.path.exists(os.path.join(DOSSIER_PHOTOS, row["photo"])):
            image = Image.open(os.path.join(DOSSIER_PHOTOS, row["photo"]))
            cols[0].image(image, width=150)
        else:
            cols[0].text("📸 Aucune photo")

        cols[1].markdown(f"""
        - **Type :** {row['type']}
        - **Couleur :** {row['couleur']}
        - **Marque :** {row['marque']}
        - **Année :** {row['année_achat']}
        - **Ports :** {row['nb_ports']}
        - **Dernier port :** {row['date_dernier_port']}
        - **Notes :** {row['notes']}
        """)
