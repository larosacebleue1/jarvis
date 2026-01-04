# Agent Jarvis

**Agent Jarvis** est un assistant intelligent autonome conçu pour vous aider à construire des outils informatiques et maintenir votre plateforme AMIKAL. Il fonctionne entièrement sur votre PC et n'agit que sur votre demande explicite.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-Projet_AMIKAL-orange)

## 🚀 Capacités principales

### Construction d'outils

- **Sites web** : Statiques et dynamiques avec design moderne en mode sombre
- **APIs REST** : Avec FastAPI et documentation automatique
- **Outils CLI** : Scripts en ligne de commande avec interface riche
- **Applications mobiles** : React Native pour iOS et Android

### Maintenance et réparation

- **Analyse** de projets existants
- **Diagnostic** automatique des problèmes
- **Réparation** de code défectueux
- **Refactoring** pour améliorer la qualité
- **Sauvegardes** automatiques avant modification

### Apprentissage continu

- Base de connaissances évolutive
- Mémorisation des solutions
- Historique des projets
- Recherche sémantique

## 📦 Installation

### Prérequis

- Python 3.11 ou supérieur
- Variable d'environnement `OPENAI_API_KEY` configurée

### Installation rapide

```bash
cd jarvis-agent
pip install -r requirements.txt
```

## 🎯 Utilisation rapide

### Construire un site web

```bash
python3 jarvis_agent_cli.py build "Crée un site web pour présenter mon portfolio"
```

### Réparer un projet

```bash
python3 jarvis_agent_cli.py fix ./mon-projet "L'authentification ne fonctionne pas"
```

### Analyser un projet

```bash
python3 jarvis_agent_cli.py analyze ./mon-projet
```

### Poser une question

```bash
python3 jarvis_agent_cli.py ask "Comment créer une API REST en Python ?"
```

### Apprendre une nouvelle connaissance

```bash
python3 jarvis_agent_cli.py learn "Problème: Erreur CORS\nSolution: Ajouter les headers CORS"
```

## 📚 Documentation complète

Consultez le [Guide d'Utilisation](GUIDE_UTILISATION.md) pour une documentation complète incluant :

- Toutes les commandes disponibles
- Exemples détaillés d'utilisation
- Configuration avancée
- Dépannage
- API Python

## 🏗️ Structure du projet

```
jarvis-agent/
├── config/                  # Configuration
├── knowledge_base/          # Base de connaissances
├── logs/                    # Journaux d'activité
├── src/
│   ├── core/               # Modules principaux
│   │   ├── agent.py       # Orchestrateur
│   │   ├── llm.py         # Client LLM
│   │   └── knowledge_base.py
│   └── modules/            # Modules fonctionnels
│       ├── builder.py     # Construction
│       └── fixer.py       # Réparation
├── jarvis_agent_cli.py    # Interface CLI
└── test_agent.py          # Tests
```

## 🔒 Sécurité

- ✅ Exécution locale uniquement
- ✅ Activation manuelle requise
- ✅ Répertoires autorisés configurables
- ✅ Sauvegardes automatiques
- ✅ Journalisation complète

## 🧪 Tests

Exécutez les tests pour vérifier que tout fonctionne :

```bash
python3 test_agent.py
```

## ⚙️ Configuration

Le fichier `config/config.yaml` permet de personnaliser :

- Le modèle LLM (gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash)
- Les paramètres de sécurité
- Les répertoires autorisés
- Le niveau de journalisation

## 🤖 Utilisation via API Python

```python
from src.core.agent import JarvisAgent

# Initialiser l'agent
agent = JarvisAgent()

# Construire un outil
result = agent.build("Crée un site web pour mon restaurant")

# Réparer un projet
result = agent.fix("./mon-projet", "Le formulaire ne fonctionne pas")

# Poser une question
answer = agent.ask("Comment déployer une application FastAPI ?")
```

## 📝 Exemples

### Créer un site web de présentation

```bash
python3 jarvis_agent_cli.py build "Crée un site web moderne en mode sombre avec des couleurs vives pour présenter AMIKAL, mon assistant IA personnel"
```

### Créer une API REST

```bash
python3 jarvis_agent_cli.py build "Crée une API REST avec FastAPI pour gérer des utilisateurs" --output ./api-utilisateurs
```

### Réparer la plateforme AMIKAL

```bash
python3 jarvis_agent_cli.py fix ./amikal-platform "Le système d'authentification ne vérifie pas correctement les tokens JWT"
```

## 🎨 Personnalisation

Jarvis est conçu pour évoluer avec vos besoins :

- Ajoutez de nouveaux types d'outils
- Créez vos propres modules
- Enrichissez la base de connaissances
- Intégrez d'autres modèles LLM

## 🆘 Dépannage

### L'agent ne démarre pas

```bash
# Vérifier Python
python3 --version

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problèmes de permissions

Vérifiez les répertoires autorisés dans `config/config.yaml`

### Réponses lentes

Changez le modèle pour un plus rapide dans la configuration :

```yaml
llm:
  model: "gpt-4.1-nano"
```

## 📊 Commandes disponibles

| Commande | Description |
|----------|-------------|
| `build` | Construit un nouvel outil |
| `fix` | Répare un projet existant |
| `analyze` | Analyse un projet |
| `refactor` | Refactorise du code |
| `ask` | Pose une question |
| `learn` | Apprend une connaissance |
| `info` | Affiche les informations |

## 🌟 Fonctionnalités avancées

- **Recherche sémantique** dans la base de connaissances
- **Génération de code** optimisée par IA
- **Diagnostic intelligent** des problèmes
- **Apprentissage automatique** des patterns
- **Historique complet** des projets

## 📖 Ressources

- [Guide d'Utilisation](GUIDE_UTILISATION.md) - Documentation complète
- [Architecture](amikal_agent_architecture.md) - Détails techniques
- Logs : `logs/jarvis-agent.log`

## 🔄 Mises à jour

Pour mettre à jour les dépendances :

```bash
pip install -r requirements.txt --upgrade
```

## 💡 Conseils d'utilisation

1. **Soyez précis** dans vos demandes pour de meilleurs résultats
2. **Utilisez la base de connaissances** pour mémoriser vos solutions
3. **Vérifiez les logs** en cas de problème
4. **Testez les projets générés** avant déploiement
5. **Créez des sauvegardes** régulières

## 🎯 Cas d'usage

- Construction rapide de prototypes
- Maintenance de la plateforme AMIKAL
- Apprentissage de nouvelles technologies
- Automatisation de tâches répétitives
- Documentation de solutions

## 🚧 Développement futur

- Interface web pour une utilisation plus intuitive
- Support de plus de langages et frameworks
- Intégration avec Git pour le versioning
- Déploiement automatique
- Tests automatiques des projets générés

## 👨‍💻 Développé pour

**Projet AMIKAL** - Assistant IA personnel

---

**Version** : 1.0.0  
**Date** : 2026-01-04  
**Nom** : Jarvis

Pour toute question, consultez le guide d'utilisation ou posez une question à Jarvis directement !

```bash
python3 jarvis_agent_cli.py ask "Comment puis-je t'utiliser efficacement ?"
```
