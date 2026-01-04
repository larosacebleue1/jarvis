# Guide d'Utilisation - Agent AMIKAL

## Introduction

L'**Agent AMIKAL** est un assistant intelligent autonome conçu pour vous aider à construire des outils informatiques et maintenir votre plateforme. Il fonctionne entièrement sur votre PC et n'agit que sur votre demande explicite.

## Caractéristiques principales

### Capacités de construction

L'agent peut créer automatiquement :

- **Sites web statiques** : HTML, CSS, JavaScript avec design moderne en mode sombre
- **Applications web dynamiques** : Avec base de données et authentification
- **APIs REST** : Utilisant FastAPI avec documentation automatique
- **Outils CLI** : Scripts en ligne de commande avec interface utilisateur riche
- **Applications mobiles** : React Native pour iOS et Android

### Capacités de maintenance

L'agent peut :

- **Analyser** vos projets existants pour comprendre leur structure
- **Diagnostiquer** les problèmes et identifier leurs causes
- **Réparer** automatiquement le code défectueux
- **Refactoriser** le code pour améliorer sa qualité
- **Créer des sauvegardes** automatiques avant toute modification

### Système d'apprentissage

L'agent possède une base de connaissances évolutive qui lui permet de :

- Sauvegarder les solutions aux problèmes rencontrés
- Mémoriser les patterns de conception utilisés
- Conserver l'historique de tous les projets créés
- Rechercher des solutions similaires pour de nouveaux problèmes

## Installation

### Prérequis

- Python 3.11 ou supérieur
- Accès à Internet (pour les appels au modèle LLM)
- Variable d'environnement `OPENAI_API_KEY` configurée

### Installation des dépendances

```bash
cd amikal-agent
pip install -r requirements.txt
```

### Configuration

Le fichier de configuration se trouve dans `config/config.yaml`. Vous pouvez personnaliser :

- Le modèle LLM utilisé (gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash)
- Les paramètres de sécurité
- Les répertoires autorisés pour les opérations
- Le niveau de journalisation

## Utilisation via CLI

### Commandes disponibles

#### 1. Construire un outil (`build`)

Crée un nouvel outil informatique à partir d'une description en langage naturel.

```bash
python3 amikal_agent_cli.py build "DESCRIPTION" [--output RÉPERTOIRE]
```

**Exemples :**

```bash
# Créer un site web de portfolio
python3 amikal_agent_cli.py build "Crée un site web pour présenter mon portfolio de développeur"

# Créer une API REST
python3 amikal_agent_cli.py build "Crée une API REST pour gérer une liste de tâches" --output ./mon-api

# Créer un outil CLI
python3 amikal_agent_cli.py build "Crée un outil en ligne de commande pour convertir des images"
```

#### 2. Réparer un projet (`fix`)

Répare un problème dans un projet existant.

```bash
python3 amikal_agent_cli.py fix CHEMIN_PROJET "DESCRIPTION_PROBLÈME"
```

**Exemples :**

```bash
# Réparer un problème d'authentification
python3 amikal_agent_cli.py fix ./mon-projet "L'authentification ne fonctionne pas"

# Corriger une erreur 404
python3 amikal_agent_cli.py fix ./mon-site "Erreur 404 sur la page contact"
```

#### 3. Analyser un projet (`analyze`)

Analyse la structure d'un projet et identifie les problèmes potentiels.

```bash
python3 amikal_agent_cli.py analyze CHEMIN_PROJET
```

**Exemple :**

```bash
python3 amikal_agent_cli.py analyze ./mon-projet
```

#### 4. Refactoriser du code (`refactor`)

Améliore la qualité d'un fichier de code.

```bash
python3 amikal_agent_cli.py refactor CHEMIN_FICHIER [--objective "OBJECTIF"]
```

**Exemples :**

```bash
# Refactoriser pour améliorer la qualité
python3 amikal_agent_cli.py refactor ./mon_script.py

# Refactoriser pour améliorer les performances
python3 amikal_agent_cli.py refactor ./app.js --objective "améliorer les performances"
```

#### 5. Poser une question (`ask`)

Pose une question technique à l'agent.

```bash
python3 amikal_agent_cli.py ask "QUESTION"
```

**Exemples :**

```bash
python3 amikal_agent_cli.py ask "Comment créer une API REST en Python ?"
python3 amikal_agent_cli.py ask "Quelle est la différence entre GET et POST ?"
```

#### 6. Apprendre une connaissance (`learn`)

Enseigne une nouvelle connaissance à l'agent.

```bash
python3 amikal_agent_cli.py learn "CONTENU" [--type TYPE] [--tags TAG1 TAG2 ...]
```

**Exemples :**

```bash
# Apprendre une solution
python3 amikal_agent_cli.py learn "Problème: Erreur CORS\nSolution: Ajouter les headers CORS dans FastAPI"

# Apprendre un pattern
python3 amikal_agent_cli.py learn "Pattern de singleton en Python" --type pattern --tags python design-pattern
```

#### 7. Informations sur l'agent (`info`)

Affiche les informations et capacités de l'agent.

```bash
python3 amikal_agent_cli.py info
```

## Utilisation via API Python

Vous pouvez également utiliser l'agent directement dans vos scripts Python :

```python
from src.core.agent import AmikalAgent

# Initialiser l'agent
agent = AmikalAgent()

# Construire un outil
result = agent.build(
    "Crée un site web pour mon restaurant",
    output_dir="./mon-restaurant"
)

# Réparer un projet
result = agent.fix(
    "./mon-projet",
    "Le formulaire de contact ne fonctionne pas"
)

# Analyser un projet
analysis = agent.analyze("./mon-projet")

# Refactoriser un fichier
result = agent.refactor(
    "./mon_script.py",
    objective="améliorer la lisibilité"
)

# Poser une question
answer = agent.ask("Comment déployer une application FastAPI ?")

# Apprendre une connaissance
knowledge_id = agent.learn(
    "Problème: Timeout de connexion\nSolution: Augmenter le timeout dans les settings",
    content_type="solution",
    tags=["network", "timeout"]
)
```

## Exemples d'utilisation

### Exemple 1 : Créer un site web de présentation

```bash
python3 amikal_agent_cli.py build "Crée un site web moderne en mode sombre avec des couleurs vives pour présenter AMIKAL, mon assistant IA personnel. Le site doit avoir une page d'accueil, une section fonctionnalités, et un formulaire de contact."
```

L'agent va :
1. Analyser votre demande
2. Générer le HTML, CSS et JavaScript
3. Créer un site responsive avec design moderne
4. Sauvegarder le projet dans un répertoire
5. Créer un README avec les instructions

### Exemple 2 : Créer une API pour gérer des utilisateurs

```bash
python3 amikal_agent_cli.py build "Crée une API REST avec FastAPI pour gérer des utilisateurs. L'API doit permettre de créer, lire, modifier et supprimer des utilisateurs. Chaque utilisateur a un nom, un email et un rôle." --output ./api-utilisateurs
```

L'agent va créer :
- Un fichier `main.py` avec tous les endpoints
- Les modèles Pydantic pour la validation
- Un fichier `requirements.txt`
- Un README avec les instructions de lancement

### Exemple 3 : Réparer un problème dans votre plateforme AMIKAL

```bash
python3 amikal_agent_cli.py fix ./amikal-platform "Le système d'authentification ne vérifie pas correctement les tokens JWT"
```

L'agent va :
1. Créer une sauvegarde de votre projet
2. Analyser le code pour identifier le problème
3. Diagnostiquer la cause
4. Proposer et appliquer une correction
5. Sauvegarder la solution dans sa base de connaissances

### Exemple 4 : Apprendre à l'agent comment gérer un problème spécifique

```bash
python3 amikal_agent_cli.py learn "Problème: L'agent AMIKAL ne répond pas aux commandes vocales\nSolution: Vérifier que le microphone est activé et que les permissions sont accordées. Redémarrer le service d'écoute vocale." --tags amikal vocal troubleshooting
```

La prochaine fois que vous aurez un problème similaire, l'agent pourra retrouver cette solution.

## Structure du projet

```
amikal-agent/
├── config/
│   └── config.yaml              # Configuration de l'agent
├── knowledge_base/              # Base de connaissances
│   ├── templates/               # Templates de code
│   ├── patterns/                # Patterns de conception
│   ├── solutions/               # Solutions aux problèmes
│   ├── documentation/           # Documentation
│   └── projects_history/        # Historique des projets
├── logs/
│   └── amikal-agent.log        # Journaux d'activité
├── src/
│   ├── core/                    # Modules principaux
│   │   ├── agent.py            # Orchestrateur principal
│   │   ├── config.py           # Gestion de la configuration
│   │   ├── logger.py           # Système de journalisation
│   │   ├── llm.py              # Client LLM
│   │   └── knowledge_base.py   # Base de connaissances
│   └── modules/                 # Modules fonctionnels
│       ├── builder.py          # Construction d'outils
│       └── fixer.py            # Réparation et maintenance
├── tests/                       # Tests
├── amikal_agent_cli.py         # Interface CLI
├── test_agent.py               # Script de test
├── requirements.txt            # Dépendances Python
└── README.md                   # Documentation

```

## Sécurité et confidentialité

### Contrôles de sécurité

- **Exécution locale** : Tout le code s'exécute sur votre PC
- **Activation manuelle** : L'agent n'agit que sur demande explicite
- **Répertoires autorisés** : Seuls certains répertoires peuvent être modifiés (configurables)
- **Sauvegardes automatiques** : Avant toute modification de code
- **Journalisation complète** : Toutes les actions sont tracées

### Configuration des répertoires autorisés

Par défaut, l'agent ne peut modifier que les répertoires spécifiés dans `config/config.yaml` :

```yaml
security:
  allowed_directories:
    - "/home/ubuntu/amikal-agent"
    - "/home/ubuntu/projects"
```

Pour autoriser d'autres répertoires, ajoutez-les à cette liste.

## Dépannage

### L'agent ne démarre pas

Vérifiez que :
- Python 3.11+ est installé : `python3 --version`
- Les dépendances sont installées : `pip install -r requirements.txt`
- La variable `OPENAI_API_KEY` est définie

### L'agent ne peut pas modifier un fichier

Vérifiez que le répertoire est dans la liste des répertoires autorisés dans `config/config.yaml`.

### Les réponses sont lentes

Vous pouvez changer le modèle LLM dans `config/config.yaml` pour un modèle plus rapide :

```yaml
llm:
  model: "gpt-4.1-nano"  # Plus rapide que gpt-4.1-mini
```

### La base de connaissances ne fonctionne pas

Si vous rencontrez des problèmes avec ChromaDB, vous pouvez désactiver la recherche vectorielle :

```yaml
knowledge_base:
  vector_db_enabled: false
```

## Personnalisation

### Changer le modèle LLM

Éditez `config/config.yaml` :

```yaml
llm:
  model: "gemini-2.5-flash"  # ou gpt-4.1-mini, gpt-4.1-nano
  temperature: 0.7
  max_tokens: 4000
```

### Ajuster le niveau de journalisation

```yaml
logging:
  level: "DEBUG"  # DEBUG, INFO, WARNING, ERROR
```

### Désactiver un module

```yaml
modules:
  builder: true
  fixer: false  # Désactive le module de réparation
  learner: true
```

## Évolution future

L'agent est conçu pour évoluer. Vous pouvez facilement :

- Ajouter de nouveaux types d'outils dans le module Builder
- Créer de nouveaux modules pour d'autres fonctionnalités
- Enrichir la base de connaissances avec vos propres templates
- Intégrer d'autres modèles LLM

## Support

Pour toute question ou problème :

1. Consultez les logs : `logs/amikal-agent.log`
2. Exécutez les tests : `python3 test_agent.py`
3. Posez une question à l'agent : `python3 amikal_agent_cli.py ask "VOTRE QUESTION"`

## Licence

Agent AMIKAL - Développé pour le projet AMIKAL

---

**Version** : 1.0.0  
**Date** : 2026-01-04
