import streamlit as st
import pandas as pd
import pdfkit
import tempfile
import os

from models.advanced_simulation.component.data_store import DataStore
from models.advanced_simulation.component import *

with open("static/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titre principal
st.title("Analyse Projet d'Investissement Immobilier")

st.markdown("""
Bienvenue dans le simulateur d'investissement locatif.  
Vous pouvez ici renseigner toutes les dimensions de votre projet, des coûts initiaux à la fiscalité, en passant par les loyers, les prêts, les travaux, etc.  
À la fin, vous pouvez télécharger un récapitulatif **complet en CSV** ou **générer un rapport PDF**.
""")

st.divider()

# Composants dynamiques
Bien().render()
Marche().render()
Pret().render()
Loyer().render()
Charges().render()
Frais().render()
Fisca().render()
Croissance().render()
Travaux().render()

# Bouton de calcul
if st.button("Compute"):
    Result().render()


# # Espace de séparation
# st.markdown("---")

# # Données à exporter
# all_data = DataStore.get_all()
# df = pd.DataFrame([{**{"section": k}, **v} for k, v in all_data.items()])

# # 📤 Téléchargement CSV
# csv_data = df.to_csv(index=False).encode('utf-8')
# st.download_button(
#     label="📥 Télécharger le CSV",
#     data=csv_data,
#     file_name="analyse_investissement.csv",
#     mime="text/csv"
# )

# # 📄 Génération du PDF
# def generate_pdf_from_data(data: dict) -> str:
#     html = "<h1>Rapport d'Analyse d'Investissement</h1><br>"

#     for section, values in data.items():
#         html += f"<h2>{section}</h2><ul>"
#         for key, val in values.items():
#             html += f"<li><b>{key.replace('_', ' ').capitalize()} :</b> {val}</li>"
#         html += "</ul><hr>"

#     # Création temporaire
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#         pdfkit.from_string(html, tmp_file.name)
#         return tmp_file.name

# # Bouton pour créer et télécharger le PDF
# if st.button("📄 Générer un rapport PDF"):
#     pdf_path = generate_pdf_from_data(all_data)
#     with open(pdf_path, "rb") as f:
#         st.download_button(
#             label="📥 Télécharger le PDF",
#             data=f,
#             file_name="rapport_investissement.pdf",
#             mime="application/pdf"
#         )
#     os.remove(pdf_path)
