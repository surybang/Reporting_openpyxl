import pandas as pd
import numpy as np

# 1) Paramètres
np.random.seed(42)
n_clients    = 25000
cutoff_prev  = pd.Timestamp("2025-01-01")   # date de coupure pour la période précédente

# 2) Type de client et DRC
type_clients  = np.random.choice(["PP", "PM"], n_clients)
drc_complets  = np.random.choice([True, False], n_clients, p=[0.8, 0.2])

# 3) Date d'adhésion entre 1980 et avril 2025
ts_start = pd.Timestamp("1980-01-01").value // 10**9
ts_end   = pd.Timestamp("2025-04-30").value // 10**9
date_adhesion = pd.to_datetime(
    np.random.randint(ts_start, ts_end, size=n_clients),
    unit="s"
)

# 4) Score courant
scores = np.random.choice(
    ["V", "O", "R", None],
    size=n_clients,
    p=[0.7, 0.2, 0.05, 0.05]
)

# 5) Identifiants d'agent pour tous
agents_pool = ["AUTO"] + [f"AGENT_{i}" for i in range(1, 11)]
# Par défaut AUTO sur toute la base
id_agent = np.full(n_clients, "AUTO", dtype=object)
# Pour les scorés R, on choisit aléatoirement AUTO ou AGENT_x
mask_r = (scores == "R")
id_agent[mask_r] = np.random.choice(agents_pool, mask_r.sum())

# 6) Détermination des « nouveaux » pour la période précédente
is_new = date_adhesion >= cutoff_prev

# 7) Génération du score de la période précédente
#    - None si nouveau
#    - Sinon tirage selon distribution réaliste
score_prev = np.full(n_clients, None, dtype=object)
p_prev = [0.6, 0.20, 0.15, 0.05]  # V, O, R, None
choices = ["V", "O", "R", None]
mask_old = ~is_new
score_prev[mask_old] = np.random.choice(choices, mask_old.sum(), p=p_prev)

# 8) Assemblage du DataFrame
df = pd.DataFrame({
    "client_id":      np.arange(1, n_clients+1),
    "type_client":    type_clients,
    "date_adhesion":  date_adhesion,
    "score":          scores,
    "score_prev":     score_prev,
    "id_agent":       id_agent,
    "drc_complet":    drc_complets
})

# 9) Sauvegarde
df.to_csv("data.csv", index=False)

# 10) Aperçu rapide
print(df.sample(5))
