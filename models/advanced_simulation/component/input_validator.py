class InputValidator:
    def __init__(self, data):
        self.data = data
        self.warnings = []
        self.errors = []
        
    def validate(self):
        """Valide tous les inputs et retourne True si les données sont valides
        pour le calcul (même avec des warnings)"""
        validators = [
            self._validate_bien,
            self._validate_prets,
            self._validate_loyers,
            self._validate_travaux,
            self._validate_charges,
            self._validate_frais,
            self._validate_fisca,
            self._validate_croissance
        ]
        
        for validator in validators:
            validator()
        
        return len(self.errors) == 0
    
    def _validate_bien(self):
        bien = self.data.get("bien", {})
        
        # Vérification que le prix d'achat est positif
        if bien.get("prix_achat", 0) <= 0:
            self.errors.append("Le prix d'achat doit être positif")
            
        # Vérification que la surface est positive
        if bien.get("surface", 0) <= 0:
            self.warnings.append("La surface n'est pas renseignée ou est invalide")
            
    def _validate_prets(self):
        prets = self.data.get("prets", [])
        
        if not prets:
            self.warnings.append("Aucun prêt n'est défini. L'achat est-il au comptant?")
            return
            
        for i, pret in enumerate(prets):
            if pret.get("montant", 0) <= 0:
                self.errors.append(f"Le montant du prêt {i+1} doit être positif")
            
            if pret.get("taux", 0) < 0:
                self.errors.append(f"Le taux du prêt {i+1} ne peut pas être négatif")
                
            if pret.get("duree", 0) <= 0:
                self.errors.append(f"La durée du prêt {i+1} doit être positive")
    
    def _validate_loyers(self):
        loyers = self.data.get("loyers", {})
        
        if not loyers:
            self.warnings.append("Le loyer mensuel n'est pas défini ou est nul")
            return
        
        # Vérification du taux de vacance raisonnable
        taux_vacance = loyers.get("taux_vacance", 0)
        if taux_vacance > 30:
            self.warnings.append("Le taux de vacance semble très élevé (>30%)")
    
    def _validate_travaux(self):
        travaux = self.data.get("travaux")
        if not travaux:
            self.warnings.append("Les travaux n'ont pas été renseignés")
            
    def _validate_charges(self):
        charges = self.data.get("charges")
        if not charges:
            self.warnings.append("Les charges n'ont pas été renseignées")
            
    def _validate_frais(self):
        frais = self.data.get("frais")
        if not frais:
            self.warnings.append("Les frais n'ont pas été renseignés")
        
    def _validate_fisca(self):
        fisca = self.data.get("fisca")
        if not fisca:
            self.warnings.append("La fiscalité n'a pas été renseignée")
        
    def _validate_croissance(self):
        croissance = self.data.get("croissance")
        
        if not croissance:
            self.warnings.append("L'hypothèse d'inflation et de croissance n'ont pas été renseignées")
            return 
        
        # Vérification des hypothèses de croissance réalistes
        if croissance.get("croissance_loyer", 0) > 5:
            self.warnings.append("L'hypothèse de croissance des loyers semble élevée (>5%)")
            
        if croissance.get("inflation", 0) > 4:
            self.warnings.append("L'hypothèse d'inflation semble élevée (>4%)")
            
    def get_warnings(self):
        return self.warnings
        
    def get_errors(self):
        return self.errors