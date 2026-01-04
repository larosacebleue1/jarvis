# Guide de Démarrage Rapide - Jarvis

Bienvenue ! Ce guide vous permettra de démarrer avec **Jarvis** en quelques minutes.

## ⚡ Installation en 3 étapes

### 1. Cloner ou télécharger Jarvis

Si vous lisez ceci, vous avez déjà Jarvis sur votre PC ! 🎉

### 2. Configurer la clé API

Jarvis utilise OpenAI pour son intelligence. Configurez votre clé API :

```bash
export OPENAI_API_KEY='votre-clé-api-ici'
```

Pour rendre cette configuration permanente, ajoutez cette ligne à votre `~/.bashrc` ou `~/.zshrc`.

### 3. Installer les dépendances

```bash
cd jarvis-agent
./install.sh
```

Ou manuellement :

```bash
pip install -r requirements.txt
```

## 🚀 Premiers pas

### Vérifier que Jarvis fonctionne

```bash
python3 jarvis_agent_cli.py info
```

Vous devriez voir les informations sur Jarvis et ses capacités.

### Votre premier projet : un site web

```bash
python3 jarvis_agent_cli.py build "Crée un site web simple avec une page d'accueil"
```

Jarvis va :
1. Analyser votre demande
2. Générer le HTML, CSS et JavaScript
3. Créer un projet complet dans `projects/`

### Poser votre première question

```bash
python3 jarvis_agent_cli.py ask "Qu'est-ce qu'une API REST ?"
```

Jarvis vous donnera une explication claire et détaillée.

## 📝 Commandes essentielles

### Construction (`build`)

Créer un nouvel outil :

```bash
# Site web
python3 jarvis_agent_cli.py build "Crée un site web pour mon restaurant"

# API REST
python3 jarvis_agent_cli.py build "Crée une API pour gérer des tâches"

# Outil CLI
python3 jarvis_agent_cli.py build "Crée un outil pour convertir des images"
```

### Réparation (`fix`)

Réparer un projet existant :

```bash
python3 jarvis_agent_cli.py fix ./mon-projet "Le formulaire de contact ne fonctionne pas"
```

### Analyse (`analyze`)

Analyser un projet :

```bash
python3 jarvis_agent_cli.py analyze ./mon-projet
```

### Questions (`ask`)

Poser des questions techniques :

```bash
python3 jarvis_agent_cli.py ask "Comment déployer une application Python ?"
```

### Apprentissage (`learn`)

Enseigner quelque chose à Jarvis :

```bash
python3 jarvis_agent_cli.py learn "Problème: Erreur 404\nSolution: Vérifier les routes"
```

## 💡 Exemples pratiques

### Exemple 1 : Site web de portfolio

```bash
python3 jarvis_agent_cli.py build "Crée un site web moderne en mode sombre pour présenter mon portfolio de développeur. Inclus une section projets, une page à propos et un formulaire de contact."
```

Résultat : Un site web complet dans `projects/portfolio_developpeur/`

### Exemple 2 : API de gestion d'utilisateurs

```bash
python3 jarvis_agent_cli.py build "Crée une API REST avec FastAPI pour gérer des utilisateurs. Endpoints : créer, lire, modifier, supprimer des utilisateurs." --output ./mon-api
```

Résultat : Une API complète dans `./mon-api/`

### Exemple 3 : Réparer un bug

```bash
# D'abord, analyser le projet
python3 jarvis_agent_cli.py analyze ./mon-site-web

# Ensuite, réparer le problème
python3 jarvis_agent_cli.py fix ./mon-site-web "La page de contact affiche une erreur 500"
```

Résultat : Jarvis diagnostique et répare le problème, avec sauvegarde automatique

## 🎯 Conseils pour de meilleurs résultats

### Soyez précis dans vos demandes

❌ Mauvais : "Crée un site"  
✅ Bon : "Crée un site web moderne en mode sombre pour présenter mon restaurant italien, avec un menu, une galerie photos et un formulaire de réservation"

### Utilisez la base de connaissances

Après avoir résolu un problème, apprenez-le à Jarvis :

```bash
python3 jarvis_agent_cli.py learn "Problème: L'API ne répond pas\nSolution: Vérifier que le serveur est démarré et que le port est correct"
```

La prochaine fois, Jarvis se souviendra de cette solution !

### Vérifiez les projets générés

Jarvis génère du code de qualité, mais testez toujours avant de déployer :

```bash
cd projects/mon-nouveau-projet
cat README.md  # Lire les instructions
```

## 🔧 Configuration

### Changer le modèle LLM

Éditez `config/config.yaml` :

```yaml
llm:
  model: "gpt-4.1-nano"  # Plus rapide
  # ou "gpt-4.1-mini"    # Plus précis
  # ou "gemini-2.5-flash" # Alternative
```

### Autoriser d'autres répertoires

Par défaut, Jarvis ne peut modifier que certains répertoires. Pour en ajouter :

```yaml
security:
  allowed_directories:
    - "/home/ubuntu/jarvis-agent"
    - "/home/ubuntu/projects"
    - "/home/ubuntu/mon-autre-projet"  # Ajoutez ici
```

## 🆘 Problèmes courants

### "Module not found"

```bash
pip install -r requirements.txt
```

### "Permission denied"

```bash
chmod +x jarvis_agent_cli.py
```

### "OPENAI_API_KEY not set"

```bash
export OPENAI_API_KEY='votre-clé-api'
```

### Jarvis est lent

Changez le modèle pour un plus rapide dans `config/config.yaml` :

```yaml
llm:
  model: "gpt-4.1-nano"
```

## 📚 Aller plus loin

### Documentation complète

- **README.md** : Vue d'ensemble et fonctionnalités
- **GUIDE_UTILISATION.md** : Guide complet avec tous les détails
- **jarvis_agent_architecture.md** : Architecture technique

### Tester Jarvis

```bash
python3 test_agent.py
```

### Consulter les logs

```bash
tail -f logs/jarvis-agent.log
```

### Utiliser Jarvis dans vos scripts Python

```python
from src.core.agent import JarvisAgent

agent = JarvisAgent()

# Construire un projet
result = agent.build("Crée un site web")

# Poser une question
answer = agent.ask("Comment fonctionne FastAPI ?")

# Réparer un projet
result = agent.fix("./mon-projet", "Bug dans le formulaire")
```

## 🎓 Cas d'usage

### Pour les développeurs

- Prototypage rapide d'idées
- Génération de boilerplate
- Refactoring de code legacy
- Documentation automatique

### Pour l'apprentissage

- Poser des questions techniques
- Comprendre des concepts
- Voir des exemples de code
- Apprendre de nouvelles technologies

### Pour la maintenance

- Diagnostiquer des bugs
- Réparer du code
- Mettre à jour des dépendances
- Optimiser les performances

## 🌟 Prochaines étapes

1. **Créez votre premier projet** avec `build`
2. **Posez des questions** pour apprendre
3. **Enseignez à Jarvis** vos solutions avec `learn`
4. **Explorez la documentation** pour découvrir toutes les fonctionnalités

## 💬 Besoin d'aide ?

Demandez directement à Jarvis :

```bash
python3 jarvis_agent_cli.py ask "Comment puis-je utiliser Jarvis efficacement ?"
```

---

**Vous êtes prêt !** 🚀

Jarvis est là pour vous assister dans tous vos projets informatiques. N'hésitez pas à expérimenter et à explorer ses capacités.

```bash
python3 jarvis_agent_cli.py build "Crée quelque chose d'incroyable"
```

Bonne création ! 🎉
