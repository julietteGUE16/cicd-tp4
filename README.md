# TP 4 – Reporting et Monitoring avec Allure, Prometheus et Grafana

## 🎯 Objectifs pédagogiques

À l'issue de ce TP, vous serez capable de :

1. **Générer des rapports HTML de tests** avec Allure
2. **Exporter des métriques de tests** vers Prometheus
3. **Visualiser les métriques** dans des dashboards Grafana
4. **Automatiser** la publication des rapports dans un pipeline CI/CD
5. **Monitorer** l'évolution des tests dans le temps

## 🔧 Pré-requis logiciels

### Logiciels requis
- **Python 3.11+** ([python.org](https://python.org))
- **Git** ([git-scm.com](https://git-scm.com))
- **Docker** et **Docker Compose** ([docker.com](https://docker.com)) - **REQUIS**
- **Node.js** et **npm** (pour Allure CLI) - **REQUIS**
  ```bash
  # Vérifier Node.js
  node --version  # Doit être >= 16
  npm --version
  ```

---

## Étape 1 – Configuration du projet et installation d'Allure

### 🎯 Objectif
Initialiser le projet et configurer Allure pour générer des rapports HTML de tests.

**Ce que vous allez faire :**
- Créer la structure du projet avec des tests pytest
- Installer Allure CLI via npm
- Configurer pytest pour exporter les résultats vers Allure
- Générer votre premier rapport HTML Allure

**Pourquoi :** Allure est un outil standard dans l'industrie pour générer des rapports de tests professionnels et visuellement attrayants.

### 🧩 Instructions

#### 1.1 clone le projet et creation de votre branche :

```bash
git checkout -b <votre_nom_prenom>
```

#### 1.2 Structure des dossiers

```
tp2-allure-monitoring/
├── src/
│   ├── __init__.py
│   └── calculator.py          # Application simple
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py     # Tests à exécuter
│   └── conftest.py            # Configuration pytest + Allure
├── monitoring/
│   └── prometheus_exporter.py # Exporteur Prometheus
├── scripts/
│   └── export_metrics.sh      # Script d'automatisation
├── reports/                    # Résultats Allure (JSON)
├── allure-report/              # Rapport HTML généré
├── prometheus/                 # Configuration Prometheus
│   └── prometheus.yml
├── grafana/                    # Configuration Grafana
│   └── datasources/
│       └── prometheus.yml
├── docker-compose.yml          # Stack Docker
├── requirements.txt
├── pytest.ini
├── conftest.py                 # Configuration globale
└── .gitignore
```

#### 1.3 Installation d'Allure CLI

**Sur macOS/Linux :**
```bash
npm install -g allure-commandline
allure --version
```

**Sur Windows :**
```bash
# Via Chocolatey
choco install allure-commandline

# Ou via Scoop
scoop install allure
```

#### 1.4 Créer les fichiers de base

**`requirements.txt` :**
```txt
pytest==7.4.3
allure-pytest==2.13.2
prometheus-client==0.19.0
requests==2.31.0
```

**`pytest.ini` :**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --alluredir=reports
    --tb=short
```

**`conftest.py` (à la racine) :**
```python
"""Configuration pytest et Allure"""
import sys
from pathlib import Path

# Ajouter src au PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))
```

#### 1.5 Application et les tests

Les fichiers suivants sont déja presents dans le projet :

**`src/calculator.py` :**

**`tests/test_calculator.py` :**

**`tests/test_calculator_advanced.py` :**

**`tests/test_calculator_integration.py` :**

**`tests/test_calculator_stress.py` :**

** Les fichiers de tests créent intentionnellement des tests qui échouent pour démontrer :
- Les rapports Allure avec échecs
- Les métriques Prometheus avec différents statuts
- Les dashboards Grafana avec des tendances variées
- Des durées de tests différentes (rapides vs lents)
- Différentes sévérités de tests

**Résumé des tests créés :**
- **Total : 41 tests**
- **Réussis : 36 tests** (88%)
- **Échouent : 5 tests** (12%) - tests intentionnellement en échec pour démonstration
- **Durées variées :** tests rapides (< 100ms) et lents (> 500ms)
- **Sévérités Allure :** CRITICAL, NORMAL, MINOR, BLOCKER, TRIVIAL
- **4 suites de tests :** Basic, Advanced, Integration, Stress

#### 1.6 Execution des tests

Installer les dépendances

```bash
# Installer les dépendances
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Exécuter les tests

```bash

# Exécuter TOUS les tests (environ 40 tests avec succès et échecs)
pytest tests/ -v

# Exécuter une suite spécifique
pytest tests/test_calculator.py -v           # Suite 1: Tests de base
pytest tests/test_calculator_advanced.py -v  # Suite 2: Tests avancés
pytest tests/test_calculator_integration.py -v  # Suite 3: Tests d'intégration
pytest tests/test_calculator_stress.py -v    # Suite 4: Tests de stress

# Exécuter uniquement les tests qui échouent (pour voir les erreurs)
pytest tests/ -v --lf

# Exécuter avec statistiques détaillées
pytest tests/ -v --tb=short
```

Générer le rapport Allure HTML (avec tous les tests)

```bash
# Générer le rapport Allure HTML (avec tous les tests)
pytest tests/ -v --alluredir=reports
allure generate reports --clean -o allure-report
```

# Ouvrir le rapport

```bash
# Ouvrir le rapport
allure open allure-report
```

### 🧪 Résultat attendu

✅ 41 tests exécutés (36 réussis, 5 échecs intentionnels)  
✅ Fichiers JSON Allure générés dans `reports/` pour tous les tests  
✅ Rapport HTML Allure généré dans `allure-report/` avec :
- Graphiques de statistiques (succès/échecs)
- Répartition par suite de tests (Basic, Advanced, Integration, Stress)
- Répartition par sévérité (CRITICAL, NORMAL, MINOR, BLOCKER, TRIVIAL)
- Durées des tests (rapides vs lents)
- Détails des erreurs pour les tests échoués
✅ Rapport ouvert dans le navigateur avec visualisations riches

**Ce que vous verrez dans Allure :**

- **Overview** : Environ 88% de réussite, 12% d'échecs
- **Graphs** : Distribution des durées, timeline des exécutions
- **Suites** : 4 suites différentes avec leurs statistiques
- **Behaviors** : Groupement par stories (Addition, Division, Performance, etc.)

---

## Étape 2 – Configuration Prometheus avec Docker

### 🎯 Objectif
Configurer Prometheus pour collecter et stocker les métriques de tests.

**Ce que vous allez faire :**
- Créer un exporter Prometheus qui expose les métriques de tests
- Configurer Prometheus pour scraper ces métriques
- Lancer Prometheus avec Docker Compose
- Visualiser les métriques dans l'interface Prometheus

**Pourquoi :** Prometheus est le standard de l'industrie pour le monitoring de métriques temporelles, permettant de tracer l'évolution des tests dans le temps.

### 🧩 Instructions

#### 2.1 Créer l'exporter Prometheus

**`monitoring/prometheus_exporter.py` :**
```python
"""
Exporteur Prometheus pour les métriques de tests
Expose les métriques via un endpoint HTTP que Prometheus peut scraper
"""

from prometheus_client import Counter, Gauge, Histogram, start_http_server
import time
import json
from pathlib import Path


# Métriques Prometheus
tests_total = Counter('tests_total', 'Total de tests exécutés', ['status', 'suite'])
tests_duration = Histogram('tests_duration_seconds', 'Durée des tests en secondes', ['suite'])
test_success_rate = Gauge('test_success_rate', 'Taux de succès des tests (0-100)', ['suite'])


class PrometheusExporter:
    """Exporte les métriques de tests vers Prometheus"""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.metrics_file = Path('reports')
    
    def start_server(self):
        """Démarre le serveur HTTP pour Prometheus"""
        start_http_server(self.port)
        print(f"✅ Serveur Prometheus démarré sur le port {self.port}")
        print(f"📍 Métriques disponibles: http://localhost:{self.port}/metrics")
    
    def update_metrics_from_allure(self):
        """Lit les résultats Allure et met à jour les métriques"""
        if not self.metrics_file.exists():
            print("⚠️  Aucun résultat Allure trouvé")
            return
        
        # Compter les tests par statut
        passed = 0
        failed = 0
        broken = 0
        skipped = 0
        
        # Parser les fichiers JSON Allure
        for result_file in self.metrics_file.glob('*-result.json'):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    
                status = data.get('status', 'unknown')
                suite = 'default'  # On pourrait extraire depuis les labels
                duration = data.get('stop', 0) - data.get('start', 0)
                
                # Incrémenter les compteurs
                if status == 'passed':
                    passed += 1
                    tests_total.labels(status='passed', suite=suite).inc()
                elif status == 'failed':
                    failed += 1
                    tests_total.labels(status='failed', suite=suite).inc()
                elif status == 'broken':
                    broken += 1
                    tests_total.labels(status='broken', suite=suite).inc()
                elif status == 'skipped':
                    skipped += 1
                    tests_total.labels(status='skipped', suite=suite).inc()
                
                # Enregistrer la durée
                if duration > 0:
                    tests_duration.labels(suite=suite).observe(duration / 1000.0)  # ms -> s
                    
            except Exception as e:
                print(f"⚠️  Erreur lecture {result_file}: {e}")
        
        # Calculer le taux de succès
        total = passed + failed + broken
        if total > 0:
            success_rate = (passed / total) * 100
            test_success_rate.labels(suite='all').set(success_rate)
        
        print(f"📊 Métriques mises à jour: {passed} passed, {failed} failed, {broken} broken, {skipped} skipped")


def main():
    """Point d'entrée principal"""
    exporter = PrometheusExporter(port=8000)
    exporter.start_server()
    
    # Mettre à jour les métriques toutes les 30 secondes
    while True:
        exporter.update_metrics_from_allure()
        time.sleep(30)


if __name__ == '__main__':
    main()
```

#### 2.2 Configuration Prometheus :

**`prometheus/prometheus.yml` :**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'test-metrics'
    static_configs:
      - targets: ['host.docker.internal:8000']
        labels:
          environment: 'testing'
          
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

#### 2.3 Docker Compose


**`docker-compose.yml` :**
```yaml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```

#### 2.4 Configuration Grafana datasource

**`grafana/datasources/prometheus.yml` :**
```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

#### 2.5 Démarrer Prometheus et Grafana

```bash
# MAINTENANT démarrer Prometheus et Grafana
docker-compose up -d

# Vérifier que les containers sont démarrés
docker-compose ps

# Vérifier les logs si problème
docker-compose logs prometheus
docker-compose logs grafana
```

Dans un autre terminal, démarrer l'exporter Python

```bash
# Dans un autre terminal, démarrer l'exporter Python
python monitoring/prometheus_exporter.py

# Accéder aux interfaces
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)

# Vérifier que Prometheus scrape les métriques
# Aller sur http://localhost:9090/targets // U ARE HERRRRRRREEEEEE
```

### 🧪 Résultat attendu

✅ Prometheus et Grafana démarrés avec Docker  
✅ Exporter Python accessible sur le port 8000  
✅ Prometheus scrape les métriques de tests  
✅ Métriques visibles dans l'interface Prometheus

---

## Étape 3 – Création de dashboards Grafana

### 🎯 Objectif
Créer des dashboards Grafana pour visualiser les métriques de tests.

**Ce que vous allez faire :**

- Vous connecter à Grafana
- Créer un dashboard avec des graphiques pour les métriques de tests
- Visualiser le taux de succès, le nombre de tests, les durées
- Configurer des alertes si nécessaire

**Pourquoi :** Les dashboards Grafana permettent de visualiser l'évolution des tests dans le temps et d'identifier rapidement les problèmes.

### 🧩 Instructions

#### 3.1 Accéder à Grafana

1. Ouvrez http://localhost:3000
2. Connectez-vous avec `admin` / `admin`
3. Changer le mot de passe si demandé (ou skip)

### 🧩 Instructions

#### 3.1 Accéder à Grafana

1. Ouvrez http://localhost:3000
2. Connectez-vous avec `admin` / `admin`
3. Changer le mot de passe si demandé (ou skip)

#### 3.2 Créer un dashboard

1. Cliquez sur **"Dashboards"** → **"New"** → **"New Dashboard"**
2. Cliquez sur **"Add visualization"**
3. Sélectionnez la datasource **"Prometheus"**


#### 3.3 Panneaux à créer

**Panneau 1 : Taux de succès des tests**
- **Query:** `test_success_rate{suite="all"}`
- **Visualization:** Stat (Gauge)
- **Title:** "Test Success Rate (%)"
- **Unit:** Percent (0-100)
- **Thresholds:**
  - Green: 90-100
  - Yellow: 70-90
  - Red: 0-70

**Panneau 2 : Nombre de tests par statut**
- **Query:** `tests_total`
- **Visualization:** Bar chart
- **Title:** "Tests by Status"
- **Legend:** `{{status}}`

**Panneau 3 : Durée totale des tests**
- **Query:** `sum(tests_duration_seconds)`
- **Visualization:** Time series
- **Title:** "Total Test Duration (seconds)"

**Panneau 4 : Évolution du taux de succès dans le temps**
- **Query:** `test_success_rate{suite="all"}`
- **Visualization:** Time series
- **Title:** "Success Rate Over Time"

#### 3.4 Sauvegarder le dashboard

1. Cliquez sur **"Save dashboard"**
2. Nommez-le "Test Metrics Dashboard"
3. Sauvegardez

#### 3.5 Exécuter les tests plusieurs fois pour générer de l'historique 

**Sur macOS/Linux :**
```bash
# Démarrer l'exporter Prometheus en arrière-plan (dans un terminal)
python monitoring/prometheus_exporter.py &

# Dans un autre terminal, exécuter les tests plusieurs fois
for i in {1..10}; do
  echo "=== Run $i de tests ==="
  pytest tests/ -v --alluredir=reports
  echo "Attente de 10 secondes avant le prochain run..."
  sleep 10
done

# L'exporter mettra à jour les métriques toutes les 30 secondes
# Les métriques devraient apparaître dans Grafana après quelques minutes
```

**Sur Windows (PowerShell) :**
```powershell
# Dans un terminal PowerShell, démarrer l'exporter en arrière-plan
Start-Job -ScriptBlock { python monitoring/prometheus_exporter.py }

# Dans un autre terminal PowerShell, exécuter les tests plusieurs fois
for ($i = 1; $i -le 10; $i++) {
  Write-Host "=== Run $i de tests ==="
  pytest tests/ -v --alluredir=reports
  Write-Host "Attente de 10 secondes avant le prochain run..."
  Start-Sleep -Seconds 10
}

# Pour arrêter le job en arrière-plan:
# Stop-Job -Name "Job1"; Remove-Job -Name "Job1"
```

**Résultat attendu :**
- Après plusieurs runs, vous verrez dans Grafana :
  - Une évolution du taux de succès dans le temps (~88%)
  - Des variations dans le nombre de tests passés/échoués
  - Des durées de tests variées (certains rapides, d'autres lents)
  - Des données historiques pour analyser les tendances

### 🧪 Résultat attendu

✅ Dashboard Grafana créé avec 4 panneaux  
✅ Métriques visibles et mises à jour en temps réel  
✅ Graphiques montrant l'évolution des tests

---

## Étape 4 – Intégration CI/CD avec GitHub Actions

### 🎯 Objectif
Automatiser la génération de rapports Allure dans le pipeline CI/CD et publier les résultats automatiquement.

**Ce que vous allez faire :**
- Créer un workflow GitHub Actions qui exécute les tests
- Générer automatiquement le rapport Allure HTML
- Publier le rapport comme artifact téléchargeable
- Ajouter des commentaires automatiques sur les Pull Requests

**Pourquoi :** L'automatisation CI/CD permet d'avoir des rapports à jour à chaque commit et de partager facilement les résultats avec l'équipe.

### 🧩 Instructions

"Ce que vous allez faire" : vous allez construire un pipeline CI/CD complet étape par étape qui intègre Allure pour générer et publier automatiquement les rapports de tests. Créez le fichier `.github/workflows/ci-monitoring.yml` en suivant les instructions ci-dessous.

#### 5.1 Structure de base du workflow

**Étape 1 : Définir le nom et les déclencheurs**

Ajoutez l'en-tête du workflow :
- `name:` : le nom du workflow (ex: "CI - Tests avec Allure et Monitoring")
- `on:` : quand le workflow doit s'exécuter (push, pull_request, schedule)

**Indices :**
- Le workflow doit s'exécuter sur les branches `main` et `develop` ou `nom_de_votre_branche`  lors d'un `push`
- Il doit aussi s'exécuter sur les `pull_request` vers `main`
- (Optionnel) Ajoutez un déclencheur `schedule` pour une exécution périodique (toutes les 6 heures par exemple)

**Vérification** : Votre structure doit ressembler à :
```yaml
name: CI - Tests avec Allure et Monitoring

on:
  push:
    branches: [ ??? ]  # Quelles branches ?
  pull_request:
    branches: [ ??? ]  # Vers quelle branche ?
```

---

#### 5.2 Définir le job et l'environnement

"Ce que vous allez faire" : créer le job principal avec l'environnement d'exécution.

**Étape 2 : Créer le job principal**

Ajoutez la section `jobs:` avec un job nommé `test-and-report`.

**Indices :**
- `runs-on: ubuntu-latest` : exécution sur Ubuntu
- Le nom du job peut être descriptif : "Tests + Allure Report"

**Vérification** : Vous devez avoir quelque chose comme :
```yaml
jobs:
  test-and-report:
    name: Tests + Allure Report
    runs-on: ???  # Quel OS ?
    
    steps:
      # Les étapes suivent ici...
```

---

#### 5.3 Étapes de configuration de base

**Étape 3 : Checkout et configuration Python**

"Ce que vous allez faire" : configurer l'environnement Python et installer les dépendances nécessaires.

Ajoutez les premières étapes du workflow :

1. **Checkout du code** : utilisez `actions/checkout@v4`
2. **Setup Python** : utilisez `actions/setup-python@v4` avec :
  - `python-version: '3.11'`
  - `cache: 'pip'` (pour accélérer les builds)
3. **Installation des dépendances** :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```


**Étape 4 : Installer Allure CLI**

"Ce que vous allez faire" : installer Allure CLI qui sera utilisé pour générer les rapports HTML.

Ajoutez une étape pour installer Allure CLI via npm :
- Installez Node.js avec `actions/setup-node@v4` (version 18 par exemple)
- Installez Allure CLI globalement : `npm install -g allure-commandline`
- Vérifiez l'installation : `allure --version`

---

#### 5.4 Exécution des tests

**Étape 5 : Exécuter les tests avec collecte Allure**

"Ce que vous allez faire" : exécuter tous les tests et collecter les résultats au format Allure.

Ajoutez une étape pour exécuter les tests :
- Commande : `pytest tests/ -v --alluredir=reports`
- Ajoutez `continue-on-error: true` pour que le workflow continue même si des tests échouent

**Question à réfléchir** : Pourquoi utilise-t-on `continue-on-error: true` ici ?

---

#### 5.5 Génération des rapports Allure

**Étape 6 : Générer le rapport HTML**

"Ce que vous allez faire" : transformer les données JSON Allure en un rapport HTML interactif.

Ajoutez une étape avec `if: always()` pour générer le rapport Allure :
- Commande : `allure generate reports --clean -o allure-report`
- Cette étape s'exécute même si les tests échouent grâce à `if: always()`

---

#### 5.6 Upload des artifacts

**Étape 7 : Publier les rapports**

"Ce que vous allez faire" : sauvegarder les rapports comme artifacts téléchargeables depuis GitHub.

Créez deux étapes pour uploader les rapports (avec `if: always()`) :

1. **Upload des résultats Allure (JSON)** :
  - Action : `actions/upload-artifact@v4`
  - `name: allure-results`
  - `path: reports/`
  - `retention-days: 30`

2. **Upload du rapport HTML Allure** :
  - Même action
  - `name: allure-html-report`
  - `path: allure-report/`
  - `retention-days: 30`

**Indice** : Consultez la [documentation upload-artifact](https://github.com/actions/upload-artifact) pour la syntaxe exacte.


#### 5.7 Après avoir créé votre workflow, validez-le :

```bash
# Pousser sur GitHub pour tester
git add .github/workflows/ci-monitoring.yml
git commit -m "feat: add CI/CD pipeline with Allure reporting"
git push
```

**Vérification sur GitHub :**
1. Allez dans l'onglet "Actions" de votre dépôt
2. Vous devriez voir votre workflow s'exécuter
3. Consultez les logs pour détecter d'éventuelles erreurs
4. Vérifiez que les tests s'exécutent et que les rapports Allure sont générés

---

### 🧪 Résultat attendu

✅ Workflow créé avec succès  
✅ Syntaxe YAML valide  
✅ Pipeline s'exécute sur push
✅ Tests exécutés automatiquement  
✅ Rapports Allure générés et uploadés comme artifacts  
✅ Rapport HTML téléchargeable depuis l'onglet Actions

---

### 🆘 En cas d'erreur

**Erreur de syntaxe YAML :**
- Vérifiez l'indentation (espaces, pas de tabs)
- Vérifiez que chaque clé est correctement fermée

**Allure CLI non installé :**
- Vérifiez que Node.js est bien installé dans le workflow
- Vérifiez les logs pour voir l'erreur d'installation

**Rapport Allure non généré :**
- Vérifiez que les tests ont bien été exécutés avec `--alluredir=reports`
- Vérifiez que le dossier `reports/` contient des fichiers JSON Allure

**Artifacts non uploadés :**
- Vérifiez que les chemins sont corrects (`reports/`, `allure-report/`)
- Vérifiez que `if: always()` est bien présent

**Action non trouvée :**
- Vérifiez les versions des actions (v4, v3, etc.)
- Consultez la documentation officielle de chaque action

---

#### 5.9 Créer le .gitignore

**`.gitignore` :**
```
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Allure
allure-report/
allure-results/
reports/*.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```


---

## 📚 Ressources complémentaires

- [Allure Documentation](https://docs.qameta.io/allure/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)

---

**🎉 Félicitations! Vous avez complété le TP2!**

Vous maîtrisez maintenant:
✅ La génération de rapports HTML avec Allure  
✅ L'export de métriques vers Prometheus  
✅ La visualisation dans Grafana  
✅ L'automatisation dans CI/CD
