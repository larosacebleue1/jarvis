#!/usr/bin/env python3
"""
Script helper pour obtenir le cookie de session depuis le navigateur.
"""

import sys


def print_instructions():
    """Affiche les instructions pour obtenir le cookie de session."""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         Comment obtenir votre cookie de session                    ║
╚════════════════════════════════════════════════════════════════════╝

Pour que le webhook puisse s'authentifier auprès de l'API, vous devez
fournir votre cookie de session.

📱 MÉTHODE 1 : Depuis votre navigateur (Chrome/Edge/Firefox)
────────────────────────────────────────────────────────────────────

1. Ouvrez l'API Remote Control dans votre navigateur
   URL: https://votre-api.manus.space

2. Connectez-vous avec votre compte Manus

3. Ouvrez les outils de développement (F12)

4. Allez dans l'onglet "Application" (Chrome) ou "Stockage" (Firefox)

5. Dans la section "Cookies", trouvez le cookie nommé:
   → jarvis_session

6. Copiez la VALEUR du cookie (pas le nom)
   Exemple: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

7. Utilisez cette valeur avec le webhook:
   
   python3 jarvis_webhook.py \\
     --api-url https://votre-api.manus.space \\
     --session-cookie "VOTRE_COOKIE_ICI"


💻 MÉTHODE 2 : Depuis curl
────────────────────────────────────────────────────────────────────

1. Connectez-vous d'abord dans le navigateur

2. Utilisez curl avec l'option -c pour sauvegarder les cookies:
   
   curl -c cookies.txt https://votre-api.manus.space/api/trpc/auth.me

3. Lisez le fichier cookies.txt et cherchez jarvis_session


🔐 SÉCURITÉ
────────────────────────────────────────────────────────────────────

⚠️  IMPORTANT: Ce cookie donne accès à votre compte !
   • Ne le partagez JAMAIS
   • Ne le commitez JAMAIS dans Git
   • Stockez-le dans une variable d'environnement:
   
     export JARVIS_SESSION_COOKIE="votre_cookie"
     
     python3 jarvis_webhook.py \\
       --api-url https://votre-api.manus.space \\
       --session-cookie "$JARVIS_SESSION_COOKIE"


📝 EXEMPLE COMPLET
────────────────────────────────────────────────────────────────────

# 1. Définir les variables
export JARVIS_API_URL="https://3000-xxx.manus.computer"
export JARVIS_SESSION_COOKIE="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 2. Lancer le webhook
python3 jarvis_webhook.py \\
  --api-url "$JARVIS_API_URL" \\
  --session-cookie "$JARVIS_SESSION_COOKIE" \\
  --interval 5

# 3. Le webhook va maintenant:
#    • Vérifier les nouvelles commandes toutes les 5 secondes
#    • Exécuter automatiquement les commandes trouvées
#    • Mettre à jour le statut dans l'API


🔄 RENOUVELLEMENT
────────────────────────────────────────────────────────────────────

Les cookies de session expirent après un certain temps.
Si vous voyez des erreurs d'authentification:
  1. Reconnectez-vous dans le navigateur
  2. Récupérez le nouveau cookie
  3. Relancez le webhook avec le nouveau cookie

""")


if __name__ == "__main__":
    print_instructions()
