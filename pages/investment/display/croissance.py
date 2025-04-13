import streamlit as st
from pages.investment.display.base_section import BaseSection

class Croissance(BaseSection):

    def render(self):
        with st.expander("Hypothèses de Croissance Économique et d'Inflation", expanded=False):
            st.subheader("Hypothèses de Croissance et d'Inflation")

            # Activation du contrôle de la croissance et inflation
            active_growth = st.checkbox("Activer / Désactiver la gestion de la Croissance et Inflation", key="active_growth")
            if active_growth:
                st.success("**Activée**") 
            else: 
                st.warning("**Désactivée**")

            # Taux de Croissance Économique Annuel
            st.markdown("### Taux de Croissance Économique Annuel (%)")
            st.markdown("Ce taux représente la croissance attendue de l'économie sur une année. Il est utilisé pour estimer la hausse des revenus, des prix et des autres éléments économiques.")
            taux_croissance_annuel = st.number_input("Taux de Croissance Économique Annuel (%)", 
                                                    min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_annuel")

            # Taux d'Inflation Annuel
            st.markdown("### Taux d'Inflation Annuel (%)")
            st.markdown("L'inflation représente l'augmentation générale des prix dans l'économie, ce qui affecte les coûts des biens et services sur une période donnée.")
            taux_inflation = st.number_input("Taux d'Inflation Annuel (%)", 
                                            min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_inflation")

            # Taux d'Augmentation Annuel des Loyers
            st.markdown("### Taux d'Augmentation Annuel des Loyers (%)")
            st.markdown("Ce taux indique la hausse moyenne des loyers sur une année, en fonction de l'inflation et des conditions économiques du marché immobilier.")
            taux_augmentation_loyer = st.number_input("Taux d'Augmentation Annuel des Loyers (%)", 
                                                    min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_augmentation_loyer")
            
            # Croissance du Prix au M²
            st.markdown("### Croissance du Prix au M² (%)")
            st.markdown("Indique l'augmentation estimée du prix du mètre carré dans la région concernée. Cela peut refléter l'appréciation du bien immobilier dans un marché en croissance.")
            taux_croissance_prix_m2 = st.number_input("Croissance du Prix au M² (%)", 
                                                    min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_prix_m2")

            # Croissance des Charges de Copropriété
            st.markdown("### Croissance des Charges de Copropriété (%)")
            st.markdown("Ce taux représente l'augmentation des charges annuelles de copropriété (syndic, entretien, etc.). Ces charges peuvent être impactées par l'inflation ou les décisions de la copropriété.")
            taux_croissance_charges_copro = st.number_input("Croissance des Charges de Copropriété (%)", 
                                                            min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_charges_copro")

            # Croissance de la Taxe Foncière
            st.markdown("### Croissance de la Taxe Foncière (%)")
            st.markdown("Cette taxe locale peut augmenter au fil du temps, généralement en lien avec les ajustements fiscaux locaux ou l'inflation générale.")
            taux_croissance_taxe_fonciere = st.number_input("Croissance de la Taxe Foncière (%)", 
                                                            min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_taxe_fonciere")

            # Croissance des Frais d'Entretien
            st.markdown("### Croissance des Frais d'Entretien (%)")
            st.markdown("Estime l'augmentation des coûts d'entretien de la propriété (réparations, maintenance, nettoyage, etc.), en fonction des tendances économiques.")
            taux_croissance_entretien = st.number_input("Croissance des Frais d'Entretien (%)", 
                                                        min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_entretien")

            # Croissance du Coût de l'Assurance PNO
            st.markdown("### Croissance du Coût de l'Assurance PNO (%)")
            st.markdown("Représente l'augmentation du coût de l'assurance propriétaire non occupant (PNO), souvent en fonction de l'inflation et des risques associés à la propriété.")
            taux_croissance_assurance_pno = st.number_input("Croissance du Coût de l'Assurance PNO (%)", 
                                                            min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_assurance_pno")

            # Croissance du Coût de l'Assurance Emprunteur
            st.markdown("### Croissance du Coût de l'Assurance Emprunteur (%)")
            st.markdown("Si l'assurance emprunteur est révisée périodiquement, ce taux indique l'augmentation attendue de cette assurance, souvent liée à des facteurs comme l'âge ou l'état de santé.")
            taux_croissance_assurance_emprunteur = st.number_input("Croissance du Coût de l'Assurance Emprunteur (%)", 
                                                                min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_assurance_emprunteur")

            # Croissance des Travaux
            st.markdown("### Croissance des Coûts des Travaux (%)")
            st.markdown("L'inflation dans le secteur de la construction peut entraîner une hausse des coûts des travaux futurs (réparations, rénovations, etc.).")
            taux_croissance_cout_travaux = st.number_input("Croissance des Coûts des Travaux (%)", 
                                                        min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_cout_travaux")

            # Taux d'Actualisation
            st.markdown("### Taux d'Actualisation (%)")
            st.markdown("Le taux d'actualisation est utilisé pour déterminer la valeur actuelle des flux futurs. Il est souvent égal à l'inflation plus une prime de rendement.")
            taux_actualisation = st.number_input("Taux d'Actualisation (%)", 
                                                min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_actualisation")

            # Croissance des Revenus Personnels
            st.markdown("### Croissance des Revenus Personnels (%)")
            st.markdown("Estime l'évolution annuelle de tes revenus personnels (salaires, dividendes, etc.), ce qui peut affecter ta capacité d'épargne et ta situation fiscale.")
            taux_croissance_revenus = st.number_input("Croissance des Revenus Personnels (%)", 
                                                    min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_revenus")