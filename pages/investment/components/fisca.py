import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore

class Fisca(BaseSection):
    
    def render(self):
        with st.expander("7️⃣ Fiscalité et Considérations Fiscales – *Cliquez pour ouvrir*", expanded=False):
            
            st.subheader("Hypothèses Fiscales et de Taxation")
            st.divider()
            st.markdown("### À l’Achat")
            regime_fiscal = st.selectbox("Régime fiscal", ["Nue-propriété", "LMNP", "LMP", "SCI IS", "SCI IR"], key="regime_fiscal")
            tva_recuperable = st.checkbox("TVA récupérable", key="tva_recuperable")
            frais_notaire_deductibles = st.checkbox("Frais de notaire déductibles", key="frais_notaire_deductibles")
            frais_agence_deductibles = st.number_input("Frais d’agence déductibles (€)", min_value=0, value=0, step=500, key="frais_agence_deductibles")
            droits_enregistrement = st.number_input("Droits d’enregistrement (€)", min_value=0, value=0, step=500, key="droits_enregistrement")

            st.markdown("### Pendant la Détention")
            imposition_loyers = st.selectbox("Imposition des loyers", ["Micro-foncier", "Réel IR", "IS"], key="imposition_loyers")
            abattement_loyers = st.number_input("Abattement forfaitaire sur loyers (%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0, key="abattement_loyers")
            amortissements_possibles = st.number_input("Amortissements annuels estimés (€)", min_value=0, value=0, step=100, key="amortissements_possibles")
            charges_deductibles = st.number_input("Charges déductibles annuelles (€)", min_value=0, value=1000, step=100, key="charges_deductibles")
            deficit_imputable = st.checkbox("Déficit imputable sur revenus globaux", key="deficit_imputable")
            csg_crds = st.number_input("CSG-CRDS (%)", min_value=0.0, max_value=20.0, value=17.2, step=0.1, key="csg_crds")
            duree_detention = st.number_input("Durée de détention prévue (années)", min_value=0, value=10, step=1, key="duree_detention")

            st.markdown("### À la Revente")
            regime_plus_value = st.selectbox("Régime d’imposition sur la plus-value", ["IR particulier", "IS"], key="regime_plus_value")
            abattement_plus_value = st.number_input("Abattement estimé sur plus-value (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key="abattement_plus_value")
            base_plus_value = st.number_input("Base imposable de la plus-value (€)", min_value=0, value=0, step=1000, key="base_plus_value")
            taux_plus_value = st.number_input("Taux d’imposition sur la plus-value (%)", min_value=0.0, max_value=50.0, value=19.0, step=0.1, key="taux_plus_value")
            surtaxe_possible = st.checkbox("Surtaxe sur plus-value (si >50k€)", key="surtaxe_possible")
            reevaluation_sci_is = st.checkbox("Réévaluation à la sortie (SCI IS)", key="reevaluation_sci_is")
            
        DataStore.set("fisca", {
            # À l’achat
            "regime_fiscal": regime_fiscal,
            "tva_recuperable": tva_recuperable,
            "frais_notaire_deductibles": frais_notaire_deductibles,
            "frais_agence_deductibles": frais_agence_deductibles,
            "droits_enregistrement": droits_enregistrement,
            # Pendant
            "imposition_loyers": imposition_loyers,
            "abattement_loyers": abattement_loyers,
            "amortissements_possibles": amortissements_possibles,
            "charges_deductibles": charges_deductibles,
            "deficit_imputable": deficit_imputable,
            "csg_crds": csg_crds,
            "duree_detention": duree_detention,
            # À la revente
            "regime_plus_value": regime_plus_value,
            "abattement_plus_value": abattement_plus_value,
            "base_plus_value": base_plus_value,
            "taux_plus_value": taux_plus_value,
            "surtaxe_possible": surtaxe_possible,
            "reevaluation_sci_is": reevaluation_sci_is
        })