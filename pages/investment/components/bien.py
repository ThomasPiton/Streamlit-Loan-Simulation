import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore
from pages.investment.components.config import STRATEGIES, TYPE_BIEN, ZONE_BIEN

class Bien(BaseSection):
    
    def render(self):
        with st.expander("1️⃣ Caractéristiques du Bien Immobilier – *Cliquez pour ouvrir*", expanded=False): 
            
            st.subheader("Informations sur le bien")
            
            type_bien = st.selectbox("Type de bien", TYPE_BIEN, key="type_bien")
            selected_strategy = st.selectbox("Choisissez une stratégie d’investissement immobilier :", list(STRATEGIES.keys()), key="strategie_invest")
            st.markdown(f"**Description :** {STRATEGIES[selected_strategy]}")
            prix_achat = st.number_input("Prix du bien (€)", min_value=0, value=100000, step=1, key=f"prix_achat")
            surface = st.number_input("Surface habitable (m²)", min_value=0.0, step=1.0, key="surface")
            surface_annexe = st.number_input("Surface annexe (balcon, cave, garage) (m²)", min_value=0.0, step=1.0, key="surface_annexe")
            nb_pieces = st.number_input("Nombre de pièces", min_value=0, step=1, key="nb_pieces")
            nb_chambres = st.number_input("Nombre de chambres", min_value=0, step=1, key="nb_chambres")
            annee_construction = st.number_input("Année de construction", min_value=1800, max_value=2100, step=1, key="annee_construction")
            etage = st.number_input("Étage", min_value=0, step=1, key="etage")
            ascenseur = st.checkbox("Ascenseur", key="ascenseur")
            etat_general = st.selectbox("État général du bien", ["Neuf", "Rénové", "Bon état", "Travaux à prévoir"], key="etat_general")
            date_travaux = st.date_input("Date prévue des travaux", key="date_travaux")
            dpe = st.selectbox("Classe énergétique (DPE)", ["A", "B", "C", "D", "E", "F", "G"], key="dpe")
            localisation = st.text_input("Localisation (ville, quartier, code postal)", key="localisation")
            zone_loyers = st.selectbox("Zone géographique (loyers réglementés)", ZONE_BIEN, key="zone_loyers")
            situation_locative = st.selectbox("Situation locative actuelle", ["Libre", "Loué", "Bail en cours", "Résidence principale"], key="situation_locative")
            meuble = st.selectbox("Meublé ou non meublé", ["Meublé", "Non meublé"], key="meuble")

            DataStore.set("bien", {
                "type_bien": type_bien,
                "strategy": selected_strategy,
                "prix_achat":prix_achat,
                "surface": surface,
                "surface_annexe": surface_annexe,
                "nb_pieces": nb_pieces,
                "nb_chambres": nb_chambres,
                "annee_construction": annee_construction,
                "etage": etage,
                "ascenseur": ascenseur,
                "etat_general": etat_general,
                "date_travaux": date_travaux,
                "dpe": dpe,
                "localisation": localisation,
                "zone_loyers": zone_loyers,
                "situation_locative": situation_locative,
                "meuble": meuble
            })