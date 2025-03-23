
import time
import streamlit as st

def compteur_temps():
    start_time = time.time()
    espace = st.empty()  # Crée un espace réservé pour l'affichage
    while True:
        elapsed_time = int(time.time() - start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        espace.write(f"Temps écoulé : {minutes:02d}:{seconds:02d}")
        time.sleep(1)

compteur_temps()