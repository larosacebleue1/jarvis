#!/bin/bash
# Script d'installation de l'Agent Jarvis

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  Installation de Jarvis                    ║"
echo "║           Agent intelligent pour le projet AMIKAL          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier Python
echo "🔍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION détecté"

# Vérifier la version minimale
REQUIRED_VERSION="3.11"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "⚠️  Python 3.11+ est recommandé (vous avez $PYTHON_VERSION)"
fi

# Vérifier pip
echo ""
echo "🔍 Vérification de pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi
echo "✓ pip3 détecté"

# Vérifier la variable d'environnement OPENAI_API_KEY
echo ""
echo "🔍 Vérification de la clé API OpenAI..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Variable OPENAI_API_KEY non définie"
    echo "   Pour définir la clé API :"
    echo "   export OPENAI_API_KEY='votre-clé-api'"
    echo ""
    read -p "Voulez-vous continuer sans clé API ? (o/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
else
    echo "✓ Clé API OpenAI configurée"
fi

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances..."
if sudo pip3 install -q -r requirements.txt 2>&1 | grep -v "Requirement already satisfied"; then
    echo "✓ Dépendances installées"
else
    echo "⚠️  Certaines dépendances étaient déjà installées"
fi

# Créer les répertoires nécessaires
echo ""
echo "📁 Création des répertoires..."
mkdir -p logs
mkdir -p projects
mkdir -p knowledge_base/{templates,patterns,solutions,documentation,projects_history}
echo "✓ Répertoires créés"

# Rendre les scripts exécutables
echo ""
echo "🔧 Configuration des permissions..."
chmod +x jarvis_agent_cli.py
chmod +x test_agent.py
echo "✓ Permissions configurées"

# Créer un alias (optionnel)
echo ""
read -p "Voulez-vous créer un alias 'jarvis' pour faciliter l'utilisation ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    JARVIS_PATH="$(pwd)/jarvis_agent_cli.py"
    
    # Déterminer le fichier de configuration du shell
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    # Ajouter l'alias
    if ! grep -q "alias jarvis=" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# Alias pour l'Agent Jarvis" >> "$SHELL_RC"
        echo "alias jarvis='python3 $JARVIS_PATH'" >> "$SHELL_RC"
        echo "✓ Alias 'jarvis' ajouté à $SHELL_RC"
        echo "  Rechargez votre shell avec : source $SHELL_RC"
    else
        echo "✓ Alias 'jarvis' déjà configuré"
    fi
fi

# Test rapide
echo ""
echo "🧪 Test de l'installation..."
if python3 -c "from src.core.agent import JarvisAgent; print('OK')" 2>/dev/null | grep -q "OK"; then
    echo "✓ Test réussi"
else
    echo "⚠️  Erreur lors du test. Vérifiez les logs pour plus de détails."
fi

# Résumé
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Installation terminée avec succès !            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Pour commencer :"
echo "   python3 jarvis_agent_cli.py info"
echo ""
echo "💡 Exemples d'utilisation :"
echo "   python3 jarvis_agent_cli.py build \"Crée un site web\""
echo "   python3 jarvis_agent_cli.py ask \"Comment créer une API ?\""
echo ""
echo "📖 Documentation complète :"
echo "   cat README.md"
echo "   cat GUIDE_UTILISATION.md"
echo ""
echo "🎉 Jarvis est prêt à vous assister !"
echo ""
