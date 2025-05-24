### I. Comment récupérer le code 
```bash
git clone https://github.com/surybang/Reporting_openpyxl.git
```

### II. Utilisez uv pour la configuration 

Si uv n'est pas installé sur votre poste : 

```bash
pip install uv
```
Vous pouvez ensuite vous synchroniser avec la commande : 

```bash
uv sync
```
Faites un nouvel environnement virtuel et activez le 

```bash
uv venv
source .venv/bin/activate (sur linux/macOS)
./.venv/Scripts/activate (sur Windows)
```

### III. Lancez populate.py 

Avec uv :
```bash
uv run populate.py
```

Avec python :
```bash
python populate.py
```
