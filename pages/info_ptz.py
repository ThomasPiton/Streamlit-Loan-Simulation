import streamlit as st
from models.pret_zero.config import *


# En-tête principal
st.title("Guide du Prêt à Taux Zéro (PTZ)")

# Description générale
st.markdown("""
Le Prêt à Taux Zéro (PTZ) est un prêt immobilier réglementé, <strong>sans intérêts</strong>, destiné à faciliter 
l'accession à la propriété pour les primo-accédants. Ce dispositif gouvernemental permet de financer une partie 
de votre achat immobilier sans payer d'intérêts.
""", unsafe_allow_html=True)

# Section Définitions - Organisation en colonnes
st.header("Termes clés")

# Colonnes pour une meilleure organisation
# Colonnes pour une meilleure organisation
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px;">Zones géographiques</h4>
    <p style="margin-bottom: 15px;">
        <strong>Définition :</strong> Classification des communes en zones A bis, A, B1, B2 et C selon la tension du marché immobilier.
    </p>
    <p style="color: #b0bec5; font-size: 14px; margin-bottom: 0;">
        <strong>Exemple :</strong> Paris = Zone A bis (marché tendu), Lyon = Zone A, Nantes = Zone B1, Limoges = Zone B2, commune rurale = Zone C.
    </p>
</div>
""", unsafe_allow_html=True)

# Quotité
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px;">Quotité</h4>
    <p style="margin-bottom: 15px;">
        <strong>Définition :</strong> Pourcentage du coût total de l'opération immobilière que peut financer le PTZ.
    </p>
    <p style="color: #b0bec5; font-size: 14px; margin-bottom: 0;">
        <strong>Exemple :</strong> Pour un logement neuf en zone B2, la quotité est de 20%. 
        Si votre projet coûte 200 000€, le PTZ maximum sera de 40 000€ (20% × 200 000€).
    </p>
</div>
""", unsafe_allow_html=True)

# Plafond de revenus
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px;">Plafond de revenus</h4>
    <p style="margin-bottom: 15px;">
        <strong>Définition :</strong> Limite de revenus à ne pas dépasser pour être éligible au PTZ, 
        déterminée selon la zone géographique et la composition du foyer.
    </p>
    <p style="color: #b0bec5; font-size: 14px; margin-bottom: 0;">
        <strong>Exemple :</strong> Pour un couple avec 1 enfant en zone B1, le plafond est de 74 000€. 
        Leurs revenus n-2 ne doivent pas dépasser cette somme.
    </p>
</div>
""", unsafe_allow_html=True)

# Capital différé
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px;">Capital différé</h4>
    <p style="margin-bottom: 15px;">
        <strong>Définition :</strong> Période pendant laquelle vous ne remboursez pas le capital du PTZ, 
        seulement l'assurance éventuelle. Cette période dépend de vos revenus.
    </p>
    <p style="color: #b0bec5; font-size: 14px; margin-bottom: 0;">
        <strong>Exemple :</strong> Si vos revenus sont faibles, vous pouvez avoir 15 ans de différé, 
        puis rembourser le capital sur 10 ans (durée totale : 25 ans).
    </p>
</div>
""", unsafe_allow_html=True)

# Coefficient familial
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px;">Coefficient familial</h4>
    <p style="margin-bottom: 15px;">
        <strong>Définition :</strong> Multiplicateur appliqué aux plafonds de base selon le nombre 
        de personnes dans le foyer fiscal.
    </p>
    <p style="color: #b0bec5; font-size: 14px; margin-bottom: 0;">
        <strong>Exemple :</strong> Coefficient de 1 pour 1 personne, 1,4 pour 2 personnes, 
        1,7 pour 3 personnes, etc. Plus le foyer est grand, plus les plafonds sont élevés.
    </p>
</div>
""", unsafe_allow_html=True)

# Revenus considérés
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px;">Revenus considérés</h4>
    <p style="margin-bottom: 15px;">
        <strong>Définition :</strong> Revenus fiscaux de référence de l'année n-2 de tous les 
        occupants du logement (même non-emprunteurs).
    </p>
    <p style="color: #b0bec5; font-size: 14px; margin-bottom: 0;">
        <strong>Exemple :</strong> En 2025, on considère les revenus de 2023. Si vous achetez en couple, 
        on additionne vos deux revenus fiscaux de référence de 2023.
    </p>
</div>
""", unsafe_allow_html=True)

# Zones géographiques (en doublon avec premier, mais harmonisé)
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px;">Zones géographiques</h4>
    <p style="margin-bottom: 15px;">
        <strong>Définition :</strong> Classification des communes en zones A bis, A, B1, B2 et C 
        selon la tension du marché immobilier.
    </p>
    <p style="color: #b0bec5; font-size: 14px; margin-bottom: 0;">
        <strong>Exemple :</strong> Paris = Zone A bis (marché tendu), Lyon = Zone A, 
        Nantes = Zone B1, Limoges = Zone B2, commune rurale = Zone C.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Section Informations pratiques
st.header("Informations pratiques")

# Tabs pour organiser l'information
tab1, tab2, tab3 = st.tabs(["🎯 Conditions d'éligibilité", "📋 Documents nécessaires", "⚠️ Points importants"])

with tab1:
    st.markdown("""
    ### Qui peut bénéficier du PTZ ?
    
    **Conditions principales :**
    - Être **primo-accédant** (ne pas avoir été propriétaire de sa résidence principale au cours des 2 dernières années)
    - Respecter les **plafonds de revenus** selon la zone et la composition du foyer
    - Le logement doit être votre **résidence principale**
    - Acheter un logement **neuf** ou **ancien avec travaux** (sous conditions)
    
    **Cas particuliers dispensés de la condition de primo-accession :**
    - Personnes handicapées (titulaires carte d'invalidité)
    - Victimes de catastrophes naturelles ou technologiques
    - Personnes dont le logement a été rendu inhabitable
    """)

with tab2:
    st.markdown("""
    ### Documents à préparer pour votre demande
    
    **Documents revenus :**
    - Avis d'imposition n-2 de tous les occupants
    - Justificatifs de revenus actuels (3 derniers bulletins de salaire)
    
    **Documents projet :**
    - Compromis de vente ou contrat de réservation
    - Descriptif détaillé du logement et des travaux (si applicable)
    - Justificatifs des autres financements
    
    **Documents personnels :**
    - Pièces d'identité de tous les emprunteurs
    - Justificatifs domicile
    - Situation familiale (livret de famille, PACS, etc.)
    """)

with tab3:
    st.markdown("""
    ### Points de vigilance
    
    **⚠️ Le PTZ ne peut pas financer 100% de votre achat**
    - Il doit être complété par un prêt principal et/ou un apport personnel
    - Minimum 10% d'apport personnel généralement requis par les banques
    
    **⚠️ Vérifiez votre zone géographique**
    - La zone détermine les plafonds de revenus ET les quotités
    - Une erreur de zone peut invalider votre éligibilité
    
    **⚠️ Respectez les délais**
    - Le PTZ doit être utilisé dans les 4 ans suivant l'émission de l'offre
    - Les travaux (si applicable) doivent être réalisés dans les 2 ans après l'achat
    """)

st.markdown("---")

# Comment connaître sa zone
st.subheader("Comment connaître la zone de votre logement ?")
st.markdown("""
<style>
.interactive-box {
    background: linear-gradient(135deg, #11141c 0%, #131720 50%, #161a24 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #FFFFFF;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.interactive-box:hover {
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.05);
    transform: scale(1.01);
    border-left: 5px solid #FFFFFF;
}
</style>

<div class="interactive-box">
    <p style="margin-bottom: 15px;">
        La zone géographique de votre logement est <strong style='color:#ffffff;'>déterminante</strong> pour :
    </p>
    <ul style="margin-bottom: 15px; padding-left: 20px;">
        <li>Les plafonds de ressources à respecter</li>
        <li>Les montants maximum du PTZ</li>
        <li>Les quotités applicables</li>
    </ul>
    <p style="margin-bottom: 0;">
        Vous pouvez vérifier la zone de votre commune sur les sites officiels référencés ci-dessous.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sites gouvernementaux utiles - Version améliorée
st.subheader("🔗 Sites officiels pour plus d'informations")

# Organisation en grille 2x2 pour plus de lisibilité
col1, col2, col3 = st.columns(3)

columns = [col1, col2, col3]

for i, info in enumerate(WEBSITES):
    col = columns[i % 3]
    with col:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #0e1117 0%, #0f121a 50%, #11131c 100%);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                margin-bottom: 20px;
                transition: transform 0.3s ease;
            ">
                <h4 style="margin-bottom: 15px; color: white;">
                    <a href="{info['url']}" target="_blank" style="text-decoration: none; color: white;">
                        {info['title']}
                    </a>
                </h4>
                <p style="font-size: 14px; color: #f1f3f5; margin-bottom: 0; line-height: 1.4;">
                    {info['desc']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("---")

# Disclaimer
st.warning("""
**⚠️ Disclaimer :** Les calculs et données utilisées dans ce simulateur sont basés sur les informations 
mises à jour au 02/04/2025 disponibles sur le site https://www.economie.gouv.fr/particuliers/PTZ-pret-taux-zero.

Les résultats sont donnés **à titre indicatif** et ne constituent pas un engagement de financement. 
Pour une étude personnalisée de votre dossier, consultez un conseiller bancaire ou un professionnel de l'ADIL.

**Dernière mise à jour des barèmes :** Avril 2025
""")
