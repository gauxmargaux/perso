import streamlit as st
import pandas as pd
from datetime import date
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Connexion Google Sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.fromkey("AIzaSyC9YHhrnA665_TyJeio5lgWOUrR1FNOE8we")
client = gspread.authorize(creds)

# Ouvre le fichier
sheet = client.open("garde_robe").sheet1

# Lire en DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# # Modifier et sauvegarder
# # df.at[0, "nb_ports"] += 1  # exemple
# sheet.update([df.columns.values.tolist()] + df.values.tolist())

def format_label(i):
    row = df[df['id'] == i].iloc[0]
    return f"{row['type']} - {row['couleur']} (Ports: {row['nb_ports']})"


# FICHIER_CSV = "garde_robe.csv"

# # Charger les données
# if not os.path.exists(FICHIER_CSV):
#     st.error("Aucun fichier garde_robe.csv trouvé.")
#     st.stop()

# df = pd.read_csv(FICHIER_CSV)

st.title("📅 Marquer les vêtements portés aujourd'hui")

# Filtrer par catégorie (optionnel)
categorie = st.selectbox("Filtrer par type de vêtement", ["Tous"] + sorted(df["type"].unique()))
df_filtré = df if categorie == "Tous" else df[df["type"] == categorie]

# Liste à cocher
selection = st.multiselect(
    "Quels vêtements portes-tu aujourd'hui ?",
    options=df_filtré["id"],
    format_func=format_label
)

if st.button("✅ Enregistrer le port du jour"):
    today = date.today().isoformat()

    for item_id in selection:
        idx = df[df["id"] == item_id].index[0]
        df.at[idx, "nb_ports"] += 1
        df.at[idx, "date_dernier_port"] = today

    # df.to_csv(FICHIER_CSV, index=False)
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    st.success("Enregistré avec succès ✅")
