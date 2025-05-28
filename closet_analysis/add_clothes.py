import streamlit as st
import pandas as pd
import os
import shutil
from datetime import date
from PIL import Image

# Config
FICHIER_CSV = "garde_robe.csv"
DOSSIER_PHOTOS = "photos"
os.makedirs(DOSSIER_PHOTOS, exist_ok=True)

COLONNES = [
    "id", "type", "couleur", "marque", "année_achat",
    "nb_ports", "date_dernier_port", "notes", "photo"
]

# Charger ou créer le fichier
if os.path.exists(FICHIER_CSV):
    df = pd.read_csv(FICHIER_CSV)
else:
    df = pd.DataFrame(columns=COLONNES)

st.title("👕 Ajouter un vêtement à la garde-robe")

with st.form("form_ajout"):
    title= st.text_input('Nom')
    type_ = st.selectbox("Type", ["T-shirt", "Chemise","Pantalon", "Short","Pull", "Robe", "Chaussures", "Veste", "Jupe","Gilet", "Combinaison","Chapeau", "Autre"])
    subtype = st.selectbox('Sous-type',["T-shirt manche longues", "T-shirt manches courtes","Débardeur","T-shirt bustier", "Robe longue", "Robe courte", 'Jupe longue','Jupe courte','Combi longue','Combi courte', "Chemise trad", "Chemisier", "Sous pull", "Pull", "Sweatshirt", "Doudoune","Manteau long","Manteau court","Bombers","Veste costume", "Veste cuir"])
    Sport =st.checkbox('Pour le sport')
    saison=st.selectbox("Saison", ['Toutes saison', 'Eté', "Hiver"])
    couleur = st.text_input("Couleur")
    marque = st.text_input("Marque")
    annee = st.number_input("Année d'achat", 2000, date.today().year)
    type_achat = st.selectbox("Type d'achat ", ["Neuf", "Seconde Main", "Offert", "Fabriqué"])
    # nb_ports = st.number_input("Nombre de fois porté", 0)
    # dernier_port = st.date_input("Date du dernier port", value=date.today())
    notes = st.text_area("Notes")
    photo = st.file_uploader("Photo (JPEG/PNG)", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Ajouter")

if submit:
    new_id = int(df["id"].max() + 1) if not df.empty else 1
    photo_filename = ""

    if photo is not None:
        ext = os.path.splitext(photo.name)[1]
        photo_filename = f"{new_id}{ext}"
        with open(os.path.join(DOSSIER_PHOTOS, photo_filename), "wb") as f:
            f.write(photo.read())

    nouvelle_ligne = {
        "id": new_id,
        "type": type_,
        "couleur": couleur,
        "marque": marque,
        "année_achat": int(annee),
        # "nb_ports": int(nb_ports),
        # "date_dernier_port": str(dernier_port),
        "notes": notes,
        "photo": photo_filename
    }

    df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    df.to_csv(FICHIER_CSV, index=False)

    st.success("✅ Vêtement ajouté avec succès")
