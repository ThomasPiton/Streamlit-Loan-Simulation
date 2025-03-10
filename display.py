import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as mtick

class LoanVisualizer:
    """Classe améliorée pour visualiser les résultats d'un prêt."""
    
    def __init__(self, loan):
        """
        Initialise le visualiseur.
        
        Args:
            loan (Loan): Instance de la classe Loan à visualiser
        """
        self.loan = loan
        self.schedule = loan.generate_amortization_schedule()
        self.summary = loan.calculate_loan_summary()
        
        # Configuration du style pour tous les graphiques
        plt.style.use('seaborn-v0_8-whitegrid')
        self.colors = {
            'principal': '#4CAF50',  # Vert
            'interet': '#F44336',    # Rouge
            'assurance': '#2196F3',  # Bleu
            'frais': '#FFC107',      # Jaune
            'total': '#673AB7',      # Violet
            'background': '#f9f9f9'
        }
        
    def prepare_streamlit_data(self):
        """
        Prépare les données pour les graphiques Streamlit.
        
        Returns:
            dict: Dictionnaire contenant les dataframes pour Streamlit
        """
        # DataFrame pour l'évolution du capital restant dû
        capital_df = self.schedule[['Mois', 'Capital restant dû']].copy()
        capital_df['Capital initial'] = self.loan.montant
        
        # DataFrame pour la répartition mensuelle des paiements
        payment_df = self.schedule[['Mois', 'Principal', 'Intérêts', 'Assurance']].copy()
        
        # DataFrame pour l'évolution des intérêts vs principal
        cumulative_df = self.schedule[['Mois', 'Principal', 'Intérêts', 'Assurance']].copy()
        cumulative_df['Cumul Principal'] = cumulative_df['Principal'].cumsum()
        cumulative_df['Cumul Intérêts'] = cumulative_df['Intérêts'].cumsum()
        cumulative_df['Cumul Assurance'] = cumulative_df['Assurance'].cumsum()
        
        # Ajout d'une colonne pour l'année
        self.schedule['Année'] = (self.schedule['Mois'] - 1) // 12 + 1
        
        # Agrégation par année pour certains graphiques
        yearly_df = self.schedule.groupby('Année').agg({
            'Principal': 'sum',
            'Intérêts': 'sum',
            'Assurance': 'sum'
        }).reset_index()
        
        # DataFrame pour le ratio d'amortissement
        ratio_df = self.schedule[['Mois']].copy()
        ratio_df['Ratio capital'] = self.schedule['Principal'] / self.schedule['Mensualité totale'] * 100
        ratio_df['Ratio intérêts'] = self.schedule['Intérêts'] / self.schedule['Mensualité totale'] * 100
        ratio_df['Ratio assurance'] = self.schedule['Assurance'] / self.schedule['Mensualité totale'] * 100
        
        return {
            'capital_df': capital_df,
            'payment_df': payment_df,
            'cumulative_df': cumulative_df,
            'yearly_df': yearly_df,
            'ratio_df': ratio_df,
            'full_schedule': self.schedule
        }
    
    def plot_capital_vs_interest(self):
        """
        Génère un graphique montrant la répartition entre le capital et les intérêts.
        
        Returns:
            fig: Figure matplotlib
        """
        # Données pour le graphique
        capital = self.summary["Montant emprunté"]
        interest = self.summary["Total intérêts"]
        insurance = self.summary["Total assurance"]
        fees = self.summary["Frais initiaux"]
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=self.colors['background'])
        labels = ['Capital', 'Intérêts', 'Assurance', 'Frais']
        values = [capital, interest, insurance, fees]
        colors = [self.colors['principal'], self.colors['interet'], 
                 self.colors['assurance'], self.colors['frais']]
        
        # Création du graphique à barres avec des barres plus jolies
        bars = ax.bar(labels, values, color=colors, width=0.6, 
                     edgecolor='white', linewidth=1.5)
        
        # Ajout d'un titre et des labels avec une meilleure typographie
        ax.set_title('Répartition du coût total du prêt', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Montant (€)', fontsize=12, fontweight='bold')
        
        # Amélioration de l'apparence
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        
        # Formatage des ticks de l'axe y avec des séparateurs de milliers
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}".replace(',', ' ')))
        
        # Ajout des valeurs au-dessus des barres avec un meilleur formatage
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01 * max(values),
                   f'{height:,.2f} €'.replace(',', ' '),
                   ha='center', va='bottom', fontsize=11)
        
        # Ajout du total
        total = sum(values)
        ax.text(0.5, 0.9, f'Total : {total:,.2f} €'.replace(',', ' '), 
               transform=ax.transAxes, ha='center', 
               fontsize=14, fontweight='bold',
               bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
        
        # Ajout des pourcentages dans les barres
        for i, bar in enumerate(bars):
            height = bar.get_height()
            percentage = height / total * 100
            if percentage > 5:  # Afficher seulement si assez de place
                ax.text(bar.get_x() + bar.get_width()/2., height/2,
                       f'{percentage:.1f}%',
                       ha='center', va='center', fontsize=11, fontweight='bold',
                       color='white')
        
        fig.tight_layout()
        return fig
    
    def plot_amortization_curve(self):
        """
        Génère une courbe d'amortissement améliorée.
        
        Returns:
            fig: Figure matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['background'])
        
        # Calcul du pourcentage remboursé pour l'ombrage
        self.schedule['Pourcentage remboursé'] = (1 - self.schedule['Capital restant dû'] / self.loan.montant) * 100
        
        # Création de la courbe principale avec une ligne plus épaisse et un joli dégradé
        line = ax.plot(self.schedule['Mois'], self.schedule['Capital restant dû'], 
                 color=self.colors['principal'], linewidth=3, label='Capital restant dû')
        
        # Ajout d'une zone ombrée sous la courbe
        ax.fill_between(self.schedule['Mois'], self.schedule['Capital restant dû'], 
                       alpha=0.3, color=self.colors['principal'])
        
        # Ajouter une ligne pour le capital initial
        ax.axhline(y=self.loan.montant, color=self.colors['interet'], linestyle='--', 
                   linewidth=1.5, label='Capital initial')
        
        # Amélioration de l'apparence
        ax.set_title('Évolution du capital restant dû', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montant (€)', fontsize=12, fontweight='bold')
        
        # Formatage des ticks de l'axe y avec des séparateurs de milliers
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}".replace(',', ' ')))
        
        # Ajout d'une grille légère en arrière-plan
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Personnalisation des spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        
        # Ajout d'un axe secondaire pour le pourcentage remboursé
        ax2 = ax.twinx()
        ax2.plot(self.schedule['Mois'], self.schedule['Pourcentage remboursé'], 
                 color=self.colors['total'], linestyle='-.', linewidth=2, 
                 label='Pourcentage remboursé')
        ax2.set_ylabel('Pourcentage remboursé (%)', fontsize=12, fontweight='bold', color=self.colors['total'])
        ax2.tick_params(axis='y', colors=self.colors['total'])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_linewidth(0.5)
        ax2.spines['right'].set_color(self.colors['total'])
        
        # Formatage des ticks de l'axe secondaire
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
        
        # Légende combinée
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, 
                 framealpha=0.9, facecolor='white')
        
        # Annotation du point à mi-remboursement
        halfway_idx = np.argmin(np.abs(self.schedule['Capital restant dû'] - self.loan.montant/2))
        halfway_month = self.schedule.iloc[halfway_idx]['Mois']
        halfway_capital = self.schedule.iloc[halfway_idx]['Capital restant dû']
        
        ax.annotate(f'Mi-remboursement: Mois {int(halfway_month)}',
                   xy=(halfway_month, halfway_capital),
                   xytext=(halfway_month + 10, halfway_capital + self.loan.montant * 0.2),
                   arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                   fontsize=10, ha='center')
        
        fig.tight_layout()
        return fig
    
    def plot_payment_breakdown(self):
        """
        Génère un graphique amélioré montrant la répartition des paiements mensuels.
        
        Returns:
            fig: Figure matplotlib
        """
        # Sélection de mois représentatifs pour une meilleure lisibilité
        if self.loan.duree_mois > 60:  # Pour les prêts longs, on prend des étapes plus espacées
            step = self.loan.duree_mois // 10
            sample_months = [1]
            
            if self.loan.differe_mois > 0:
                sample_months.append(self.loan.differe_mois)
                sample_months.append(self.loan.differe_mois + 1)
            
            sample_months.extend(list(range(step, self.loan.duree_mois + 1, step)))
            if self.loan.duree_mois not in sample_months:
                sample_months.append(self.loan.duree_mois)
        else:
            # Pour les prêts courts, on prend plus de points
            sample_months = [1]
            if self.loan.differe_mois > 0:
                sample_months.append(self.loan.differe_mois)
                sample_months.append(self.loan.differe_mois + 1)
            
            sample_months.extend([
                self.loan.duree_mois // 5,
                2 * self.loan.duree_mois // 5,
                3 * self.loan.duree_mois // 5,
                4 * self.loan.duree_mois // 5,
                self.loan.duree_mois
            ])
        
        sample_months = sorted(list(set(sample_months)))
        
        filtered_schedule = self.schedule[self.schedule['Mois'].isin(sample_months)]
        
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['background'])
        
        # Création du graphique empilé
        bottom = np.zeros(len(filtered_schedule))
        
        # Empilement par partie avec des couleurs améliorées
        for column, color, label in zip(
            ['Principal', 'Intérêts', 'Assurance'], 
            [self.colors['principal'], self.colors['interet'], self.colors['assurance']],
            ['Capital', 'Intérêts', 'Assurance']
        ):
            values = filtered_schedule[column].values
            ax.bar(filtered_schedule['Mois'], values, bottom=bottom, 
                   label=label, color=color, width=0.7, 
                   edgecolor='white', linewidth=0.8)
            bottom += values
        
        # Amélioration du titre et des labels
        ax.set_title('Évolution de la composition des mensualités', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montant (€)', fontsize=12, fontweight='bold')
        
        # Personnalisation des spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        
        # Amélioration des ticks
        ax.set_xticks(filtered_schedule['Mois'])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}".replace(',', ' ')))
        
        # Légende améliorée
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                 fancybox=True, shadow=True, ncol=3, fontsize=11)
        
        # Ajout des valeurs totales au-dessus des barres
        for i, (_, row) in enumerate(filtered_schedule.iterrows()):
            ax.text(row['Mois'], row['Mensualité totale'] + 5, 
                    f'{row["Mensualité totale"]:.0f} €', 
                    ha='center', va='bottom', fontsize=9, fontweight='bold',
                    bbox=dict(facecolor='white', edgecolor='gray', alpha=0.7, 
                             boxstyle='round,pad=0.2'))
            
            # Ajout des années sur l'axe x pour les prêts longs
            if self.loan.duree_mois > 60:
                year = (row['Mois'] - 1) // 12 + 1
                ax.text(row['Mois'], -max(filtered_schedule['Mensualité totale']) * 0.05, 
                       f'An {year}', ha='center', rotation=45, fontsize=8)
        
        fig.tight_layout(rect=[0, 0.05, 1, 0.95])
        return fig
    
    def plot_pie_chart_costs(self):
        """
        Génère un graphique en camembert montrant la répartition des coûts.
        
        Returns:
            fig: Figure matplotlib
        """
        # Données pour le graphique
        capital = self.summary["Montant emprunté"]
        interest = self.summary["Total intérêts"]
        insurance = self.summary["Total assurance"]
        fees = self.summary["Frais initiaux"]
        
        # Création d'une figure avec deux sous-graphiques côte à côte
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=self.colors['background'])
        
        # Premier graphique: répartition des coûts (sans le capital)
        cost_labels = ['Intérêts', 'Assurance', 'Frais initiaux']
        cost_values = [interest, insurance, fees]
        cost_colors = [self.colors['interet'], self.colors['assurance'], self.colors['frais']]
        
        # Filtrer les valeurs nulles
        non_zero_indices = [i for i, v in enumerate(cost_values) if v > 0]
        cost_labels = [cost_labels[i] for i in non_zero_indices]
        cost_values = [cost_values[i] for i in non_zero_indices]
        cost_colors = [cost_colors[i] for i in non_zero_indices]
        
        # Créer le camembert des coûts
        wedges1, texts1, autotexts1 = ax1.pie(
            cost_values, 
            labels=None, 
            autopct='%1.1f%%',
            colors=cost_colors,
            wedgeprops=dict(width=0.5, edgecolor='w', linewidth=1),
            startangle=90,
            pctdistance=0.85
        )
        
        # Créer un cercle blanc au centre pour faire un donut
        centre_circle = plt.Circle((0, 0), 0.3, fc='white')
        ax1.add_patch(centre_circle)
        
        # Personnaliser les textes du pourcentage
        for autotext in autotexts1:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        # Ajouter un titre au premier graphique
        ax1.set_title('Répartition des coûts du crédit', fontsize=14, fontweight='bold', pad=20)
        
        # Ajouter une légende
        ax1.legend(
            wedges1, 
            [f"{l} : {v:,.2f} €".replace(',', ' ') for l, v in zip(cost_labels, cost_values)],
            loc="center",
            bbox_to_anchor=(0.5, -0.1),
            fontsize=10,
            frameon=True,
            fancybox=True,
            shadow=True
        )
        
        # Deuxième graphique: capital vs coûts totaux
        total_cost = sum(cost_values)
        total_labels = ['Capital', 'Coûts du crédit']
        total_values = [capital, total_cost]
        total_colors = [self.colors['principal'], self.colors['total']]
        
        wedges2, texts2, autotexts2 = ax2.pie(
            total_values, 
            labels=None, 
            autopct='%1.1f%%',
            colors=total_colors,
            wedgeprops=dict(width=0.5, edgecolor='w', linewidth=1),
            startangle=90,
            pctdistance=0.85
        )
        
        # Créer un cercle blanc au centre pour faire un donut
        centre_circle = plt.Circle((0, 0), 0.3, fc='white')
        ax2.add_patch(centre_circle)
        
        # Personnaliser les textes du pourcentage
        for autotext in autotexts2:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        # Ajouter un titre au deuxième graphique
        ax2.set_title('Capital vs Coût total', fontsize=14, fontweight='bold', pad=20)
        
        # Ajouter une légende
        ax2.legend(
            wedges2, 
            [f"{l} : {v:,.2f} €".replace(',', ' ') for l, v in zip(total_labels, total_values)],
            loc="center",
            bbox_to_anchor=(0.5, -0.1),
            fontsize=10,
            frameon=True,
            fancybox=True,
            shadow=True
        )
        
        # Ajouter une annotation avec le coût en pourcentage du capital
        cost_percentage = (total_cost / capital) * 100
        ax2.text(0, -1.3, f"Coût total: {cost_percentage:.2f}% du capital emprunté", 
                ha='center', fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
        
        plt.tight_layout()
        return fig
    
    def plot_cumulative_costs(self):
        """
        Génère un graphique montrant l'évolution cumulée des différents coûts.
        
        Returns:
            fig: Figure matplotlib
        """
        # Calcul des coûts cumulés
        self.schedule['Cumul Principal'] = self.schedule['Principal'].cumsum()
        self.schedule['Cumul Intérêts'] = self.schedule['Intérêts'].cumsum()
        self.schedule['Cumul Assurance'] = self.schedule['Assurance'].cumsum()
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['background'])
        
        # Tracé des courbes cumulatives
        ax.plot(self.schedule['Mois'], self.schedule['Cumul Principal'], 
               color=self.colors['principal'], linewidth=2.5, label='Capital remboursé')
        ax.plot(self.schedule['Mois'], self.schedule['Cumul Intérêts'], 
               color=self.colors['interet'], linewidth=2.5, label='Intérêts payés')
        
        # Ajout de la courbe d'assurance si non nulle
        if self.loan.assurance_taux:
            ax.plot(self.schedule['Mois'], self.schedule['Cumul Assurance'], 
                   color=self.colors['assurance'], linewidth=2.5, label='Assurance payée')
        
        # Personnalisation du graphique
        ax.set_title('Évolution cumulée des paiements', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montant cumulé (€)', fontsize=12, fontweight='bold')
        
        # Amélioration de l'apparence
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        
        # Ajout d'une grille légère
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Formatage des ticks de l'axe y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}".replace(',', ' ')))
        
        # Amélioration de la légende
        ax.legend(loc='upper left', frameon=True, framealpha=0.9, 
                 facecolor='white', edgecolor='lightgray', fontsize=10)
        
        # Annotation du point de croisement principal/intérêts
        try:
            # Trouver le point où le capital remboursé dépasse les intérêts payés
            crossover_idx = np.argmax(self.schedule['Cumul Principal'] > self.schedule['Cumul Intérêts'])
            if crossover_idx > 0:
                crossover_month = self.schedule.iloc[crossover_idx]['Mois']
                crossover_value = self.schedule.iloc[crossover_idx]['Cumul Principal']
                
                ax.annotate('Point où le capital remboursé\ndépasse les intérêts payés',
                           xy=(crossover_month, crossover_value),
                           xytext=(crossover_month + 5, crossover_value * 1.2),
                           arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=7),
                           fontsize=9, ha='center')
        except:
            # Si pas de croisement ou erreur, on ne met pas d'annotation
            pass
        
        # Ajout du total remboursé à la fin
        final_month = self.schedule.iloc[-1]['Mois']
        final_principal = self.schedule.iloc[-1]['Cumul Principal']
        final_interest = self.schedule.iloc[-1]['Cumul Intérêts']
        final_insurance = self.schedule.iloc[-1]['Cumul Assurance']
        total_paid = final_principal + final_interest + final_insurance
        
        ax.text(final_month * 0.95, total_paid * 0.9,
               f"Total remboursé: {total_paid:,.2f} €".replace(',', ' '),
               fontsize=11, fontweight='bold',
               bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
        
        fig.tight_layout()
        return fig
    
    def plot_payment_distribution_heatmap(self):
        """
        Génère une heatmap montrant la distribution des paiements par année.
        
        Returns:
            fig: Figure matplotlib
        """
        # Ne procéder que si le prêt dure au moins 2 ans
        if self.loan.duree_mois < 24:
            return None
        
        # Préparation des données par année
        yearly_data = self.schedule.copy()
        yearly_data['Année'] = (yearly_data['Mois'] - 1) // 12 + 1
        yearly_data['Mois dans année'] = ((yearly_data['Mois'] - 1) % 12) + 1
        
        # Pivoter les données pour obtenir une matrice (années x mois)
        pivot_data = yearly_data.pivot_table(
            index='Année', 
            columns='Mois dans année',
            values=['Principal', 'Intérêts', 'Assurance']
        )
        
        # Calculer la répartition en pourcentage
        total_monthly = yearly_data.groupby(['Année', 'Mois dans année'])['Mensualité totale'].first().reset_index()
        total_monthly_pivot = total_monthly.pivot(index='Année', columns='Mois dans année', values='Mensualité totale')
        
        # Calculer les ratios pour chaque composant
        principal_ratio = pivot_data['Principal'] / total_monthly_pivot * 100
        interest_ratio = pivot_data['Intérêts'] / total_monthly_pivot * 100
        
        # Création d'une colormap personnalisée
        cmap = LinearSegmentedColormap.from_list(
            'custom_cmap', 
            [(0, '#f8d7da'), (0.5, '#fff3cd'), (1, '#d1e7dd')]
        )
        
        # Choisir quelle matrice visualiser (pourcentage du capital dans la mensualité)
        heatmap_data = principal_ratio
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['background'])
        
        # Création de la heatmap
        im = ax.imshow(heatmap_data, cmap=cmap, aspect='auto')
        
        # Ajout d'une barre de couleur
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('% du capital dans la mensualité', rotation=270, labelpad=20, fontsize=10)
        
        # Configuration des ticks
        ax.set_xticks(np.arange(heatmap_data.shape[1]))
        ax.set_yticks(np.arange(heatmap_data.shape[0]))
        ax.set_xticklabels([f'Mois {i}' for i in range(1, 13)])
        ax.set_yticklabels([f'Année {i}' for i in range(1, len(heatmap_data) + 1)])
        
        # Rotation des labels de l'axe x
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Ajout des valeurs dans les cellules
        for i in range(heatmap_data.shape[0]):
            for j in range(heatmap_data.shape[1]):
                if not np.isnan(heatmap_data.iloc[i, j]):
                    text_color = 'black' if heatmap_data.iloc[i, j] > 50 else 'black'
                    ax.text(j, i, f"{heatmap_data.iloc[i, j]:.1f}%",
                           ha="center", va="center", color=text_color, fontsize=8)
        
        # Titre et ajustements
        ax.set_title('Évolution de la composition des mensualités par année', fontsize=14, fontweight='bold', pad=20)
        fig.tight_layout()
        
        return fig