WEBSITES = [
    {
        "title": "Simulateur PTZ officiel",
        "url": "https://www.anil.org/outils/outils-de-calcul/votre-pret-a-taux-zero/",
        "desc": "Calculez votre PTZ et vérifiez votre éligibilité",
    },
    {
        "title": "Service-Public.fr",
        "url": "https://www.service-public.fr/particuliers/vosdroits/F10871",
        "desc": "Informations complètes sur le PTZ",
    },
    {
        "title": "Ministère de l'Économie",
        "url": "https://www.economie.gouv.fr/particuliers/PTZ-pret-taux-zero",
        "desc": "Textes officiels et dernières actualités PTZ",
    },
    {
        "title": "Zones géographiques",
        "url": "https://www.cohesion-territoires.gouv.fr/zones-geographiques-ptz",
        "desc": "Recherchez la zone de votre commune",
    },
    {
        "title": "Crédit Agricole PTZ",
        "url": "https://www.credit-agricole.fr/particulier/pret-immobilier/ptz.html",
        "desc": "Présentation du PTZ par le Crédit Agricole",
    },
    {
        "title": "CAF – Aides au logement",
        "url": "https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/acheter-louer-reparer/un-pret-pour-financer-votre-logement",
        "desc": "Prêts et aides complémentaires proposés par la CAF",
    },
    {
        "title": "Courtier Empruntis",
        "url": "https://www.empruntis.com/pret-immobilier/pret-a-taux-zero.php",
        "desc": "Guide et simulateur du PTZ avec un courtier",
    },
    {
        "title": "Simul’Aides ANAH",
        "url": "https://monprojet.anah.gouv.fr/",
        "desc": "Aides à la rénovation cumulables avec un PTZ",
    },
    {
        "title": "SeLoger – Financer son logement",
        "url": "https://edito.seloger.com/conseils-d-experts/financement/pret-taux-zero-article-39968.html",
        "desc": "Articles pratiques pour comprendre le PTZ",
    },
]

TRANCHES = ['Tranche 1', 'Tranche 2', 'Tranche 3', 'Tranche 4']

DICT_NATURE_BIEN = {
    "neuf_maison": "Maison individuelle neuve",
    "neuf_appartement": "Appartement neuf", 
    "ancien": "Logement ancien avec travaux (zones B2/C uniquement)"
}

NATURE_BIEN = ["neuf_maison", "neuf_appartement", "ancien"]

ZONE = ['A/A bis', 'B1', 'B2', 'C']

COEFFICIENT_FAMILIAL = {
    1:1.0,
    2:1.4,
    3:1.7,
    4:2.0,
    5:2.3,
    6:2.6,
    7:2.9,
    8:3.2
}

PLAFONDS_REVENUS = {
    1: {
        "A/A bis": 49_000,
        "B1": 34_500,
        "B2": 31_500,
        "C": 28_500
    },
    2: {
        "A/A bis": 73_500,
        "B1": 51_750,
        "B2": 47_250,
        "C": 42_750
    },
    3: {
        "A/A bis": 88_200,
        "B1": 62_100,
        "B2": 56_700,
        "C": 51_300
    },
    4: {
        "A/A bis": 102_900,
        "B1": 72_450,
        "B2": 66_150,
        "C": 59_850
    },
    5: {
        "A/A bis": 117_600,
        "B1": 82_800,
        "B2": 75_600,
        "C": 68_400
    },
    6: {
        "A/A bis": 132_300,
        "B1": 93_150,
        "B2": 85_050,
        "C": 76_950
    },
    7: {
        "A/A bis": 147_000,
        "B1": 103_500,
        "B2": 94_500,
        "C": 85_500
    },
    8: {
        "A/A bis": 161_700,
        "B1": 113_850,
        "B2": 103_950,
        "C": 94_050
    }
}

# Quotités différentes pour maisons individuelles neuves vs autres
QUOTITES = {
    1: {'neuf_maison': 30,'neuf_appartement': 50,'ancien': 50},
    2: {'neuf_maison': 20,'neuf_appartement': 40,'ancien': 40},
    3: {'neuf_maison': 20,'neuf_appartement': 40,'ancien': 40},
    4: {'neuf_maison': 10,'neuf_appartement': 20,'ancien': 20}
}

TRANCHES_RESSOURCES = {
    1: {"A/A bis": 25_000, "B1": 21_500, "B2": 18_000, "C": 15_000},
    2: {"A/A bis": 31_000, "B1": 26_000, "B2": 22_500, "C": 19_500},
    3: {"A/A bis": 37_000, "B1": 30_000, "B2": 27_000, "C": 24_000},
    4: {"A/A bis": 49_000, "B1": 34_500, "B2": 31_500, "C": 28_500},
}

PLAFOND_OPERATION = {
    1: {"A/A bis": 150_000, "B1": 135_000, "B2": 110_000, "C": 100_000},
    2: {"A/A bis": 225_000, "B1": 202_500, "B2": 165_000, "C": 150_000},
    3: {"A/A bis": 270_000, "B1": 243_000, "B2": 198_000, "C": 180_000},
    4: {"A/A bis": 315_000, "B1": 283_500, "B2": 231_000, "C": 210_000},
    5: {"A/A bis": 360_000, "B1": 324_000, "B2": 264_000, "C": 240_000}, 
}

# Barème de remboursement PTZ mis à jour
BAREME_REMBOURSEMENT = {
    1: {'capital_differe': 100, 'duree_periode1': 10, 'duree_periode2': 15},
    2: {'capital_differe': 100, 'duree_periode1': 8, 'duree_periode2': 12},
    3: {'capital_differe': 100, 'duree_periode1': 2, 'duree_periode2': 13},
    4: {'capital_differe': 0, 'duree_periode1': 10, 'duree_periode2': 0}
}




# Données de référence PTZ (basées sur les barèmes officiels)
# PLAFONDS_REVENUS = {
#     'A': [37000, 51800, 62900, 74000, 85100, 96200, 107300, 118400],
#     'A bis': [30000, 42000, 51000, 60000, 69000, 78000, 87000, 96000],
#     'B1': [30000, 42000, 51000, 60000, 69000, 78000, 87000, 96000],
#     'B2': [27000, 37800, 45900, 54000, 62100, 70200, 78300, 86400],
#     'C': [24000, 33600, 40800, 48000, 55200, 62400, 69600, 76800]
# }

MONTANTS_MAX_PTZ = {
    'A': {'neuf_maison': 150_000, 'neuf_appartement': 150_000, 'ancien': 0},
    'A bis': {'neuf_maison': 135_000, 'neuf_appartement': 135_000, 'ancien': 0},
    'B1': {'neuf_maison': 110_000, 'neuf_appartement': 110_000, 'ancien': 0},
    'B2': {'neuf_maison': 100_000, 'neuf_appartement': 100_000, 'ancien': 100_000},
    'C': {'neuf_maison': 100_000, 'neuf_appartement': 100_000, 'ancien': 100_000}
}














remboursement_PTZ = {
    "Tranche 1": {"Capital différé": 1, "Période 1": 10, "Période 2": 15},
    "Tranche 2": {"Capital différé": 1, "Période 1": 8,  "Période 2": 12},
    "Tranche 3": {"Capital différé": 1, "Période 1": 2,  "Période 2": 13},
    "Tranche 4": {"Capital différé": 0,   "Période 1": 10, "Période 2": None},
}
