import streamlit as st
import plotly.express as px

from pages.investment.displayer.display_base import DisplayBase

class DisplayResultBien(DisplayBase):
    
    def __init__(self):
        super().__init__()
        self.dtf = self.result["ComputeBien"]
        
    def render(self):
        st.subheader("🏡 Résultats du Bien Immobilier")
        st.dataframe(self.dtf)
        
class DisplayPrixEvolutionGraph(DisplayBase):

    def __init__(self):
        super().__init__()
        self.dtf = self.result["ComputeBien"]

    def render(self):
        st.subheader("📈 Évolution du Prix et du Prix/m²")
        fig = px.line(self.dtf, x="date", y=["prix", "prix_m2"], 
                      labels={"value": "Prix (€)", "variable": "Type"}, 
                      title="Prix du Bien et Prix au m²")
        st.plotly_chart(fig, use_container_width=True)
        
class DisplayTimeMetricsGraph(DisplayBase):

    def __init__(self):
        super().__init__()
        self.dtf = self.result["ComputeBien"]

    def render(self):
        st.subheader("⏳ Évolution temporelle (Années, Inflation, Growth)")
        fig = px.line(self.dtf, x="date", y=["annees_ecoulees", "periode_inflation", "periode_growth"],
                      labels={"value": "Valeur", "variable": "Metric"},
                      title="Évolution des Metrics Temporels")
        st.plotly_chart(fig, use_container_width=True)
       
class DisplayUpdateDatesGraph(DisplayBase):

    def __init__(self):
        super().__init__()
        self.dtf = self.result["ComputeBien"]

    def render(self):
        st.subheader("🛠 Dernières mises à jour Inflation et Croissance")
        fig = px.bar(self.dtf, x="date", 
                     y=["derniere_mise_a_jour_inflation", "derniere_mise_a_jour_growth"], 
                     barmode="group",
                     labels={"value": "Date de mise à jour", "variable": "Type"},
                     title="Dernières mises à jour")
        st.plotly_chart(fig, use_container_width=True)
        
class DisplayCorrectedPricesGraph(DisplayBase):

    def __init__(self):
        super().__init__()
        self.dtf = self.result["ComputeBien"]

    def render(self):
        st.subheader("🧮 Prix corrigés par inflation et croissance")
        fig = px.area(
            self.dtf, 
            x="date", 
            y=["prix_corrige_inflation", "prix_corrige_growth", "prix_corrige_total"],
            labels={"value": "Prix Corrigé (€)", "variable": "Type"},
            title="Prix Corrigés avec Inflation, Croissance et Total"
        )
        st.plotly_chart(fig, use_container_width=True)
        
class DisplayImpactOnPriceGraph(DisplayBase):

    def __init__(self):
        super().__init__()
        self.dtf = self.result["ComputeBien"]

    def render(self):
        st.subheader("💥 Impact sur le prix total et prix au m²")
        fig = px.bar(self.dtf, x="date", 
                     y=["impact_prix_total", "impact_prix_m2_total"], 
                     barmode="group",
                     labels={"value": "Impact (€)", "variable": "Type d'Impact"},
                     title="Impact du Prix Total et Prix au m²")
        st.plotly_chart(fig, use_container_width=True)