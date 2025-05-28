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

# Modifier et sauvegarder
df.at[0, "nb_ports"] += 1  # exemple
sheet.update([df.columns.values.tolist()] + df.values.tolist())
