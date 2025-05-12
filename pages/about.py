import streamlit as st

st.title("À propos de notre plateforme")

# Introduction
st.markdown("""
## Votre partenaire en simulation financière

Bienvenue sur notre application de simulation de prêts.  
Notre objectif est simple : **vous aider à mieux comprendre et anticiper vos engagements financiers** grâce à des outils simples, intuitifs et fiables.
""")

# Mission
st.header("🎯 Notre mission")
st.markdown("""
Nous mettons à votre disposition des outils de simulation qui vous permettent de :

- Visualiser vos mensualités en fonction de votre prêt
- Comparer différentes options de financement
- Prendre des décisions éclairées, en toute autonomie
- Gagner du temps lors de vos démarches financières

Notre approche repose sur la **transparence**, la **précision** des calculs, et une **expérience utilisateur fluide**.
""")

# Valeurs
st.header("💡 Nos valeurs")
st.markdown("""
- **Simplicité** : Des outils accessibles à tous, sans jargon technique
- **Fiabilité** : Des calculs basés sur des formules financières standards
- **Confidentialité** : Aucune donnée personnelle n’est partagée ou stockée sans votre consentement
- **Disponibilité** : Une équipe à votre écoute pour toute question ou besoin d'assistance
""")

# Équipe ou contact
st.header("👥 Une équipe dédiée")
st.markdown("""
Derrière cette plateforme se trouve une équipe de passionnés de finance et de technologie, unis par la volonté de rendre la gestion financière plus simple et plus claire pour tous.

Si vous souhaitez en savoir plus, **n'hésitez pas à nous contacter** via la [page de contact](pages/contact.py).
""")

st.success("Merci de votre confiance.")
