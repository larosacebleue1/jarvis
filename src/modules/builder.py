"""
Module Builder - Construction d'outils informatiques.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader


class Builder:
    """Module de construction d'outils informatiques."""
    
    def __init__(self, config, llm_client, knowledge_base, logger):
        """
        Initialise le module Builder.
        
        Args:
            config: Instance de Config
            llm_client: Instance de LLMClient
            knowledge_base: Instance de KnowledgeBase
            logger: Instance de Logger
        """
        self.config = config
        self.llm = llm_client
        self.kb = knowledge_base
        self.logger = logger
        
        # Répertoire des templates
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Environnement Jinja2
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=False
        )
    
    def analyze_request(self, request: str) -> Dict[str, Any]:
        """
        Analyse une demande de construction.
        
        Args:
            request: Demande de l'utilisateur
            
        Returns:
            Analyse de la demande
        """
        self.logger.action("Analyse de la demande...")
        
        # Utiliser le LLM pour analyser la demande
        analysis_prompt = f"""Analyse cette demande de construction d'outil informatique :

"{request}"

Identifie :
1. Le type d'outil demandé (site web statique, application web dynamique, API, script CLI, application mobile, autre)
2. Les fonctionnalités principales requises
3. Les technologies suggérées
4. Le niveau de complexité (simple, moyen, complexe)
5. Les questions à poser à l'utilisateur pour clarifier les besoins

Retourne ta réponse au format JSON avec les clés suivantes :
- tool_type: type d'outil
- features: liste des fonctionnalités
- technologies: liste des technologies suggérées
- complexity: niveau de complexité
- questions: liste des questions à poser (peut être vide si tout est clair)
- project_name: suggestion de nom de projet (format snake_case)"""
        
        response = self.llm.answer_question(analysis_prompt)
        
        # Parser la réponse JSON
        import json
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                analysis = json.loads(json_str)
                self.logger.success("Analyse terminée")
                return analysis
            else:
                self.logger.warning("Impossible de parser l'analyse, utilisation de valeurs par défaut")
                return {
                    "tool_type": "unknown",
                    "features": [],
                    "technologies": [],
                    "complexity": "medium",
                    "questions": [],
                    "project_name": "nouveau_projet"
                }
        except json.JSONDecodeError:
            self.logger.warning("Erreur de parsing JSON, utilisation de valeurs par défaut")
            return {
                "tool_type": "unknown",
                "features": [],
                "technologies": [],
                "complexity": "medium",
                "questions": [],
                "project_name": "nouveau_projet"
            }
    
    def build_website_static(self, project_name: str, description: str,
                           features: List[str], output_dir: str) -> Dict[str, Any]:
        """
        Construit un site web statique.
        
        Args:
            project_name: Nom du projet
            description: Description du site
            features: Fonctionnalités demandées
            output_dir: Répertoire de sortie
            
        Returns:
            Résultat de la construction
        """
        self.logger.section(f"Construction du site web statique : {project_name}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Générer le HTML
        self.logger.action("Génération du HTML...")
        html_prompt = f"""Crée un site web HTML5 complet et moderne pour :

Nom du projet : {project_name}
Description : {description}
Fonctionnalités : {', '.join(features)}

Le site doit :
- Être responsive (mobile-first)
- Utiliser un design moderne et élégant en mode sombre avec des couleurs vives
- Inclure une navigation claire
- Avoir une structure sémantique HTML5
- Être prêt à l'emploi

Retourne uniquement le code HTML complet."""
        
        html_content = self.llm.generate_code(html_prompt, "html")
        
        # Nettoyer le code (enlever les balises markdown si présentes)
        html_content = self._clean_code(html_content, "html")
        
        # Sauvegarder le fichier HTML
        html_file = output_path / "index.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.success(f"HTML généré : {html_file}")
        
        # Générer le CSS
        self.logger.action("Génération du CSS...")
        css_prompt = f"""Crée un fichier CSS moderne pour le site web "{project_name}".

Le design doit :
- Utiliser un mode sombre avec des couleurs vives et chatoyantes
- Être responsive avec des media queries
- Utiliser des animations subtiles
- Avoir une typographie moderne
- Inclure des transitions fluides

Retourne uniquement le code CSS."""
        
        css_content = self.llm.generate_code(css_prompt, "css")
        css_content = self._clean_code(css_content, "css")
        
        # Sauvegarder le fichier CSS
        css_file = output_path / "style.css"
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        self.logger.success(f"CSS généré : {css_file}")
        
        # Générer le JavaScript si nécessaire
        if any(keyword in ' '.join(features).lower() for keyword in ['interactif', 'dynamique', 'animation']):
            self.logger.action("Génération du JavaScript...")
            js_prompt = f"""Crée un fichier JavaScript pour ajouter de l'interactivité au site "{project_name}".

Fonctionnalités : {', '.join(features)}

Le JavaScript doit :
- Être moderne (ES6+)
- Gérer les interactions utilisateur
- Ajouter des animations fluides
- Être bien commenté

Retourne uniquement le code JavaScript."""
            
            js_content = self.llm.generate_code(js_prompt, "javascript")
            js_content = self._clean_code(js_content, "javascript")
            
            js_file = output_path / "script.js"
            with open(js_file, 'w', encoding='utf-8') as f:
                f.write(js_content)
            
            self.logger.success(f"JavaScript généré : {js_file}")
        
        # Créer un README
        readme_content = f"""# {project_name}

{description}

## Fonctionnalités

{chr(10).join(f'- {feature}' for feature in features)}

## Installation

Ouvrez simplement le fichier `index.html` dans votre navigateur web.

## Structure du projet

```
{project_name}/
├── index.html      # Page principale
├── style.css       # Styles CSS
└── script.js       # Scripts JavaScript (si applicable)
```

## Généré par

Agent AMIKAL - {self._get_timestamp()}
"""
        
        readme_file = output_path / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.logger.success("Site web statique créé avec succès!")
        
        # Sauvegarder dans l'historique
        files = {
            "index.html": html_content,
            "style.css": css_content,
            "README.md": readme_content
        }
        
        if (output_path / "script.js").exists():
            with open(output_path / "script.js", 'r', encoding='utf-8') as f:
                files["script.js"] = f.read()
        
        self.kb.save_project_history(
            project_name=project_name,
            description=description,
            files=files,
            metadata={
                "type": "website_static",
                "features": features
            }
        )
        
        return {
            "success": True,
            "project_name": project_name,
            "output_dir": str(output_path),
            "files": list(files.keys())
        }
    
    def build_api_rest(self, project_name: str, description: str,
                      endpoints: List[Dict[str, str]], output_dir: str) -> Dict[str, Any]:
        """
        Construit une API REST avec FastAPI.
        
        Args:
            project_name: Nom du projet
            description: Description de l'API
            endpoints: Liste des endpoints à créer
            output_dir: Répertoire de sortie
            
        Returns:
            Résultat de la construction
        """
        self.logger.section(f"Construction de l'API REST : {project_name}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Générer le code de l'API
        self.logger.action("Génération du code API...")
        
        endpoints_description = "\n".join([
            f"- {ep.get('method', 'GET')} {ep.get('path', '/')}: {ep.get('description', '')}"
            for ep in endpoints
        ])
        
        api_prompt = f"""Crée une API REST complète avec FastAPI pour :

Nom du projet : {project_name}
Description : {description}

Endpoints à implémenter :
{endpoints_description}

L'API doit :
- Utiliser FastAPI
- Inclure la validation des données avec Pydantic
- Avoir une documentation automatique (Swagger)
- Gérer les erreurs correctement
- Utiliser des modèles de données clairs
- Être bien structurée et commentée

Retourne uniquement le code Python complet pour main.py."""
        
        api_content = self.llm.generate_code(api_prompt, "python")
        api_content = self._clean_code(api_content, "python")
        
        # Sauvegarder le fichier principal
        main_file = output_path / "main.py"
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(api_content)
        
        self.logger.success(f"API générée : {main_file}")
        
        # Créer requirements.txt
        requirements_content = """fastapi>=0.109.0
uvicorn>=0.27.0
pydantic>=2.0.0
python-dotenv>=1.0.0
"""
        
        requirements_file = output_path / "requirements.txt"
        with open(requirements_file, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        
        # Créer un README
        readme_content = f"""# {project_name}

{description}

## Endpoints

{endpoints_description}

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn main:app --reload
```

L'API sera accessible sur http://localhost:8000

Documentation interactive : http://localhost:8000/docs

## Généré par

Agent AMIKAL - {self._get_timestamp()}
"""
        
        readme_file = output_path / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.logger.success("API REST créée avec succès!")
        
        # Sauvegarder dans l'historique
        self.kb.save_project_history(
            project_name=project_name,
            description=description,
            files={
                "main.py": api_content,
                "requirements.txt": requirements_content,
                "README.md": readme_content
            },
            metadata={
                "type": "api_rest",
                "endpoints": endpoints
            }
        )
        
        return {
            "success": True,
            "project_name": project_name,
            "output_dir": str(output_path),
            "files": ["main.py", "requirements.txt", "README.md"]
        }
    
    def build_cli_tool(self, project_name: str, description: str,
                      commands: List[Dict[str, str]], output_dir: str) -> Dict[str, Any]:
        """
        Construit un outil CLI en Python.
        
        Args:
            project_name: Nom du projet
            description: Description de l'outil
            commands: Liste des commandes à créer
            output_dir: Répertoire de sortie
            
        Returns:
            Résultat de la construction
        """
        self.logger.section(f"Construction de l'outil CLI : {project_name}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Générer le code CLI
        self.logger.action("Génération du code CLI...")
        
        commands_description = "\n".join([
            f"- {cmd.get('name', 'command')}: {cmd.get('description', '')}"
            for cmd in commands
        ])
        
        cli_prompt = f"""Crée un outil CLI complet en Python avec Click pour :

Nom du projet : {project_name}
Description : {description}

Commandes à implémenter :
{commands_description}

L'outil doit :
- Utiliser Click pour la CLI
- Avoir une aide claire pour chaque commande
- Gérer les erreurs correctement
- Utiliser Rich pour un affichage amélioré
- Être bien structuré et commenté

Retourne uniquement le code Python complet."""
        
        cli_content = self.llm.generate_code(cli_prompt, "python")
        cli_content = self._clean_code(cli_content, "python")
        
        # Sauvegarder le fichier principal
        main_file = output_path / f"{project_name}.py"
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(cli_content)
        
        # Rendre le fichier exécutable
        os.chmod(main_file, 0o755)
        
        self.logger.success(f"CLI générée : {main_file}")
        
        # Créer requirements.txt
        requirements_content = """click>=8.1.0
rich>=13.0.0
"""
        
        requirements_file = output_path / "requirements.txt"
        with open(requirements_file, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        
        # Créer un README
        readme_content = f"""# {project_name}

{description}

## Commandes

{commands_description}

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python {project_name}.py --help
```

## Généré par

Agent AMIKAL - {self._get_timestamp()}
"""
        
        readme_file = output_path / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.logger.success("Outil CLI créé avec succès!")
        
        # Sauvegarder dans l'historique
        self.kb.save_project_history(
            project_name=project_name,
            description=description,
            files={
                f"{project_name}.py": cli_content,
                "requirements.txt": requirements_content,
                "README.md": readme_content
            },
            metadata={
                "type": "cli_tool",
                "commands": commands
            }
        )
        
        return {
            "success": True,
            "project_name": project_name,
            "output_dir": str(output_path),
            "files": [f"{project_name}.py", "requirements.txt", "README.md"]
        }
    
    def _clean_code(self, code: str, language: str) -> str:
        """
        Nettoie le code généré (enlève les balises markdown).
        
        Args:
            code: Code à nettoyer
            language: Langage du code
            
        Returns:
            Code nettoyé
        """
        # Enlever les balises markdown de code
        if f"```{language}" in code:
            code = code.split(f"```{language}")[1]
            code = code.split("```")[0]
        elif "```" in code:
            code = code.split("```")[1]
            if "\n" in code:
                code = "\n".join(code.split("\n")[1:])
            code = code.split("```")[0]
        
        return code.strip()
    
    def _get_timestamp(self) -> str:
        """Retourne un timestamp formaté."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
