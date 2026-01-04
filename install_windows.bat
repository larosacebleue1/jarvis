@echo off
echo ========================================
echo   Installation de Jarvis pour Windows
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    echo.
    echo Téléchargez Python depuis: https://www.python.org/downloads/
    echo Assurez-vous de cocher "Add Python to PATH" pendant l'installation
    pause
    exit /b 1
)

echo [OK] Python est installé
python --version
echo.

REM Installer les dépendances
echo Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation des dépendances
    pause
    exit /b 1
)

echo.
echo [OK] Dépendances installées avec succès
echo.

REM Demander la clé API
echo ========================================
echo   Configuration de la clé API
echo ========================================
echo.
echo Vous avez besoin d'une clé API OpenAI pour utiliser Jarvis.
echo.
echo Si vous n'en avez pas encore:
echo 1. Allez sur https://platform.openai.com/
echo 2. Créez un compte
echo 3. Allez dans API Keys
echo 4. Créez une nouvelle clé
echo.
set /p API_KEY="Entrez votre clé API OpenAI (sk-...): "

if "%API_KEY%"=="" (
    echo [ERREUR] Clé API vide
    pause
    exit /b 1
)

REM Créer le fichier .env
echo OPENAI_API_KEY=%API_KEY% > .env
echo.
echo [OK] Clé API sauvegardée dans .env
echo.

REM Tester l'installation
echo ========================================
echo   Test de l'installation
echo ========================================
echo.
python jarvis_agent_cli.py info
if errorlevel 1 (
    echo [ERREUR] Le test a échoué
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation terminée avec succès !
echo ========================================
echo.
echo Pour utiliser Jarvis, tapez:
echo   python jarvis_agent_cli.py build "Votre commande"
echo.
echo Documentation:
echo   - INSTALLATION_RAPIDE.md
echo   - GUIDE_UTILISATION.md
echo   - GUIDE_WEBHOOK.md
echo.
pause
