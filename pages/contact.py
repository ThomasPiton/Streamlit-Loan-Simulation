import streamlit as st

st.title("Contactez-nous")

# Introduction
st.markdown("""
## Nous sommes à votre écoute

Vous avez une question concernant nos outils de simulation de prêt ?  
Besoin d’un accompagnement dans votre planification financière ?  
Notre équipe est disponible pour vous aider. Remplissez le formulaire ci-dessous, et nous vous répondrons par e-mail dans les plus brefs délais.
""")

# Engagement de réponse
st.info("""
**Notre engagement envers vous :**

Nous nous engageons à répondre à toutes les demandes sous 1 à 2 jours ouvrables.  
Chaque message est traité avec attention afin de vous fournir :

- Une réponse personnalisée et adaptée à votre situation
- Des informations claires, complètes et fiables
- Des ressources et documents utiles si nécessaire
- Une trace écrite de nos échanges pour vos références futures
""")

# Formulaire de contact
with st.form("contact_form"):
    col1, col2 = st.columns(2)

    with col1:
        nom = st.text_input("Nom complet*")
        email = st.text_input("Adresse e-mail*")

    with col2:
        telephone = st.text_input("Numéro de téléphone (facultatif)")
        sujet = st.text_input("Sujet*")

    message = st.text_area("Votre message ou question*", height=150)

    consentement = st.checkbox("J’accepte de recevoir une réponse par e-mail à ma demande")

    envoyer = st.form_submit_button("Envoyer la demande")

    if envoyer:
        if nom and email and sujet and message and consentement:
            st.success("Merci pour votre message ! Nous avons bien reçu votre demande et vous répondrons par e-mail sous peu.")

            # Pour l'exemple : afficher les données
            st.write("Détails du message (exemple de données envoyées) :")
            st.json({
                "nom": nom,
                "email": email,
                "téléphone": telephone,
                "sujet": sujet,
                "message": message
            })
        else:
            st.error("Veuillez remplir tous les champs obligatoires et accepter les conditions pour envoyer votre message.")

# Informations complémentaires
st.markdown("""
## Autres moyens de nous contacter

**Horaires d'ouverture :**  
Lundi à Vendredi : 9h00 - 17h00

**Téléphone :**  
(555) 123-4567

**E-mail :**  
support@simulateurpret.com
""")
