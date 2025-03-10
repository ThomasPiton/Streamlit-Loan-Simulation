# Streamlit-Loan-Simulation
Application coded with Streamlit to simulate loan


# useful links
https://blog.streamlit.io/data-analysis-with-mito-a-powerful-spreadsheet-in-streamlit/


# 1. Paramètres d’entrée - Ces données permettront d'ajuster les simulations :

Montant du prêt (€)
Durée du prêt (mois/années)
Taux d’intérêt nominal (%)
Type de taux (fixe, variable, progressif)
Taux d'assurance (%)
Différé de remboursement (oui/non, durée en mois)
Frais de dossier (€ ou %)
Apport personnel (€)

# 2. Calculs de base: Ces valeurs clés découlent des paramètres d’entrée :

Mensualité hors assurance (€)
Mensualité avec assurance (€)
Coût total du crédit (intérêts + assurance + frais)
Coût total des intérêts (€)
Coût total de l’assurance (€)
Montant total remboursé (€)
TAEG (Taux Annuel Effectif Global) (%)

# 3. Table d’amortissement détaillée

Une ligne par mois/année avec :
Numéro de l’échéance
Capital restant dû (€)
Part d’intérêt payée (€)
Part de capital remboursée (€)
Montant assurance (€)
Mensualité totale (€)

# 4. Indicateurs avancés : Si tu veux une analyse plus poussée :

Effort de remboursement (mensualité / revenu disponible)
Ratio d’endettement avant et après crédit (%)
Montant total des intérêts en cas de remboursement anticipé à une date donnée (€)
Montant des pénalités en cas de remboursement anticipé (€)
Comparaison coût du crédit avec et sans différé (€)

# 5. Simulations & scénarios : Tu peux tester l’impact des variations sur :

Un remboursement anticipé à différentes dates
Un changement de taux d’intérêt si variable
Un scénario de rachat de crédit
Une augmentation des revenus et impact sur l’effort de remboursement
L’impact d’un remboursement partiel exceptionnel