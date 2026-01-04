"""
Module Fixer - Intervention sur l'environnement local pour réparer et maintenir du code.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class Fixer:
    """Module d'intervention sur l'environnement local."""
    
    def __init__(self, config, llm_client, knowledge_base, logger):
        """
        Initialise le module Fixer.
        
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
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyse un projet pour identifier sa structure et ses problèmes potentiels.
        
        Args:
            project_path: Chemin vers le projet
            
        Returns:
            Analyse du projet
        """
        self.logger.section(f"Analyse du projet : {project_path}")
        
        project_path = Path(project_path).resolve()
        
        if not project_path.exists():
            self.logger.error(f"Le projet n'existe pas : {project_path}")
            return {"success": False, "error": "Projet non trouvé"}
        
        # Vérifier les permissions
        if not self._is_directory_safe(project_path):
            self.logger.error(f"Accès non autorisé au répertoire : {project_path}")
            return {"success": False, "error": "Accès non autorisé"}
        
        analysis = {
            "success": True,
            "project_path": str(project_path),
            "project_type": self._detect_project_type(project_path),
            "files": self._list_project_files(project_path),
            "dependencies": self._detect_dependencies(project_path),
            "issues": []
        }
        
        self.logger.info(f"Type de projet détecté : {analysis['project_type']}")
        self.logger.info(f"Nombre de fichiers : {len(analysis['files'])}")
        
        return analysis
    
    def diagnose_issue(self, project_path: str, issue_description: str) -> Dict[str, Any]:
        """
        Diagnostique un problème dans un projet.
        
        Args:
            project_path: Chemin vers le projet
            issue_description: Description du problème
            
        Returns:
            Diagnostic du problème
        """
        self.logger.section(f"Diagnostic du problème")
        self.logger.info(f"Problème : {issue_description}")
        
        project_path = Path(project_path).resolve()
        
        # Analyser le projet
        analysis = self.analyze_project(str(project_path))
        if not analysis.get("success"):
            return analysis
        
        # Lire les fichiers pertinents
        relevant_files = self._get_relevant_files(project_path, issue_description)
        
        files_content = {}
        for file_path in relevant_files[:5]:  # Limiter à 5 fichiers
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) < 10000:  # Limiter la taille
                        files_content[str(file_path.relative_to(project_path))] = content
            except Exception as e:
                self.logger.warning(f"Impossible de lire {file_path}: {e}")
        
        # Utiliser le LLM pour diagnostiquer
        self.logger.action("Analyse du problème avec l'IA...")
        
        files_summary = "\n\n".join([
            f"Fichier: {path}\n```\n{content[:2000]}...\n```"
            for path, content in files_content.items()
        ])
        
        diagnostic_prompt = f"""Diagnostique le problème suivant dans ce projet {analysis['project_type']} :

Problème décrit : {issue_description}

Fichiers du projet :
{files_summary}

Identifie :
1. La cause probable du problème
2. Les fichiers concernés
3. Les étapes pour reproduire le problème
4. La solution recommandée
5. Les risques potentiels de la solution

Retourne ta réponse au format JSON avec les clés suivantes :
- cause: cause probable
- affected_files: liste des fichiers concernés
- reproduction_steps: étapes pour reproduire
- solution: solution recommandée
- risks: risques potentiels
- confidence: niveau de confiance (low, medium, high)"""
        
        response = self.llm.answer_question(diagnostic_prompt)
        
        # Parser la réponse JSON
        import json
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                diagnostic = json.loads(json_str)
                diagnostic["success"] = True
                self.logger.success("Diagnostic terminé")
                return diagnostic
            else:
                return {"success": False, "error": "Impossible de parser le diagnostic"}
        except json.JSONDecodeError:
            return {"success": False, "error": "Erreur de parsing du diagnostic"}
    
    def fix_issue(self, project_path: str, issue_description: str, 
                  auto_backup: bool = True) -> Dict[str, Any]:
        """
        Répare un problème dans un projet.
        
        Args:
            project_path: Chemin vers le projet
            issue_description: Description du problème
            auto_backup: Créer une sauvegarde automatique
            
        Returns:
            Résultat de la réparation
        """
        self.logger.section(f"Réparation du problème")
        
        project_path = Path(project_path).resolve()
        
        # Créer une sauvegarde si demandé
        if auto_backup and self.config.security.backup_before_modification:
            backup_path = self._create_backup(project_path)
            self.logger.success(f"Sauvegarde créée : {backup_path}")
        
        # Diagnostiquer le problème
        diagnostic = self.diagnose_issue(str(project_path), issue_description)
        
        if not diagnostic.get("success"):
            self.logger.error("Impossible de diagnostiquer le problème")
            return diagnostic
        
        self.logger.info(f"Cause identifiée : {diagnostic.get('cause', 'Inconnue')}")
        self.logger.info(f"Confiance : {diagnostic.get('confidence', 'unknown')}")
        
        # Obtenir les fichiers à modifier
        affected_files = diagnostic.get("affected_files", [])
        
        if not affected_files:
            self.logger.warning("Aucun fichier à modifier identifié")
            return {
                "success": False,
                "error": "Aucun fichier à modifier",
                "diagnostic": diagnostic
            }
        
        # Réparer chaque fichier
        fixed_files = []
        for file_rel_path in affected_files:
            file_path = project_path / file_rel_path
            
            if not file_path.exists():
                self.logger.warning(f"Fichier non trouvé : {file_path}")
                continue
            
            self.logger.action(f"Réparation de {file_rel_path}...")
            
            try:
                # Lire le contenu actuel
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # Générer le code corrigé
                fixed_content = self.llm.fix_code(
                    code=original_content,
                    error_message=issue_description,
                    language=self._detect_language(file_path)
                )
                
                # Nettoyer le code
                fixed_content = self._clean_code(fixed_content)
                
                # Écrire le fichier corrigé
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_files.append(file_rel_path)
                self.logger.success(f"✓ {file_rel_path} réparé")
                
            except Exception as e:
                self.logger.error(f"Erreur lors de la réparation de {file_rel_path}: {e}")
        
        if not fixed_files:
            self.logger.error("Aucun fichier n'a pu être réparé")
            return {
                "success": False,
                "error": "Échec de la réparation",
                "diagnostic": diagnostic
            }
        
        # Sauvegarder la solution dans la base de connaissances
        self.kb.save_solution(
            problem=issue_description,
            solution=f"Fichiers modifiés : {', '.join(fixed_files)}\n\nSolution : {diagnostic.get('solution', 'N/A')}",
            context=f"Projet : {project_path}\nType : {self._detect_project_type(project_path)}",
            tags=[self._detect_project_type(project_path), "fix"]
        )
        
        self.logger.success(f"Réparation terminée ! {len(fixed_files)} fichier(s) modifié(s)")
        
        return {
            "success": True,
            "fixed_files": fixed_files,
            "diagnostic": diagnostic,
            "backup_path": backup_path if auto_backup else None
        }
    
    def refactor_code(self, file_path: str, objective: str = "améliorer la qualité") -> Dict[str, Any]:
        """
        Refactorise un fichier de code.
        
        Args:
            file_path: Chemin vers le fichier
            objective: Objectif du refactoring
            
        Returns:
            Résultat du refactoring
        """
        self.logger.section(f"Refactoring : {file_path}")
        
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            return {"success": False, "error": "Fichier non trouvé"}
        
        if not self._is_directory_safe(file_path.parent):
            return {"success": False, "error": "Accès non autorisé"}
        
        # Créer une sauvegarde
        if self.config.security.backup_before_modification:
            backup_path = self._create_file_backup(file_path)
            self.logger.success(f"Sauvegarde créée : {backup_path}")
        
        # Lire le contenu
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            return {"success": False, "error": f"Impossible de lire le fichier : {e}"}
        
        # Refactoriser
        self.logger.action(f"Refactoring pour {objective}...")
        
        language = self._detect_language(file_path)
        refactored_content = self.llm.refactor_code(
            code=original_content,
            language=language,
            objective=objective
        )
        
        refactored_content = self._clean_code(refactored_content)
        
        # Écrire le fichier refactorisé
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(refactored_content)
            
            self.logger.success("Refactoring terminé !")
            
            return {
                "success": True,
                "file_path": str(file_path),
                "backup_path": backup_path if self.config.security.backup_before_modification else None
            }
        except Exception as e:
            return {"success": False, "error": f"Impossible d'écrire le fichier : {e}"}
    
    def _is_directory_safe(self, directory: Path) -> bool:
        """Vérifie si un répertoire est autorisé."""
        return self.config.is_directory_allowed(str(directory))
    
    def _detect_project_type(self, project_path: Path) -> str:
        """Détecte le type de projet."""
        if (project_path / "package.json").exists():
            return "nodejs"
        elif (project_path / "requirements.txt").exists() or (project_path / "setup.py").exists():
            return "python"
        elif (project_path / "pom.xml").exists():
            return "java"
        elif (project_path / "Cargo.toml").exists():
            return "rust"
        elif (project_path / "go.mod").exists():
            return "go"
        elif any((project_path / f).exists() for f in ["index.html", "index.htm"]):
            return "web_static"
        else:
            return "unknown"
    
    def _list_project_files(self, project_path: Path, max_files: int = 100) -> List[str]:
        """Liste les fichiers d'un projet."""
        files = []
        
        # Extensions à ignorer
        ignore_extensions = {'.pyc', '.pyo', '.so', '.dll', '.dylib', '.exe', '.o', '.a'}
        ignore_dirs = {'node_modules', '__pycache__', '.git', '.venv', 'venv', 'dist', 'build'}
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                # Ignorer certains fichiers
                if file_path.suffix in ignore_extensions:
                    continue
                if any(ignored in file_path.parts for ignored in ignore_dirs):
                    continue
                
                files.append(str(file_path.relative_to(project_path)))
                
                if len(files) >= max_files:
                    break
        
        return files
    
    def _detect_dependencies(self, project_path: Path) -> Dict[str, List[str]]:
        """Détecte les dépendances d'un projet."""
        dependencies = {}
        
        # Python
        req_file = project_path / "requirements.txt"
        if req_file.exists():
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    dependencies["python"] = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception:
                pass
        
        # Node.js
        package_file = project_path / "package.json"
        if package_file.exists():
            try:
                import json
                with open(package_file, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    dependencies["nodejs"] = list(package_data.get("dependencies", {}).keys())
            except Exception:
                pass
        
        return dependencies
    
    def _get_relevant_files(self, project_path: Path, issue_description: str) -> List[Path]:
        """Identifie les fichiers pertinents pour un problème."""
        # Pour l'instant, retourner les fichiers principaux
        relevant = []
        
        # Fichiers Python
        for py_file in project_path.rglob('*.py'):
            if '__pycache__' not in py_file.parts and 'venv' not in py_file.parts:
                relevant.append(py_file)
        
        # Fichiers JavaScript/TypeScript
        for js_file in project_path.rglob('*.js'):
            if 'node_modules' not in js_file.parts:
                relevant.append(js_file)
        
        for ts_file in project_path.rglob('*.ts'):
            if 'node_modules' not in ts_file.parts:
                relevant.append(ts_file)
        
        # Fichiers HTML/CSS
        for html_file in project_path.rglob('*.html'):
            relevant.append(html_file)
        
        return relevant[:10]  # Limiter à 10 fichiers
    
    def _detect_language(self, file_path: Path) -> str:
        """Détecte le langage d'un fichier."""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php'
        }
        return extension_map.get(file_path.suffix, 'text')
    
    def _create_backup(self, project_path: Path) -> str:
        """Crée une sauvegarde d'un projet."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{project_path.name}_backup_{timestamp}"
        backup_path = project_path.parent / backup_name
        
        shutil.copytree(project_path, backup_path, ignore=shutil.ignore_patterns(
            'node_modules', '__pycache__', '.git', 'venv', '.venv', 'dist', 'build'
        ))
        
        return str(backup_path)
    
    def _create_file_backup(self, file_path: Path) -> str:
        """Crée une sauvegarde d'un fichier."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.parent / f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        shutil.copy2(file_path, backup_path)
        return str(backup_path)
    
    def _clean_code(self, code: str) -> str:
        """Nettoie le code généré."""
        # Enlever les balises markdown
        if "```" in code:
            parts = code.split("```")
            if len(parts) >= 3:
                code = parts[1]
                if "\n" in code:
                    lines = code.split("\n")
                    if lines[0].strip() in ['python', 'javascript', 'typescript', 'html', 'css', 'java']:
                        code = "\n".join(lines[1:])
        
        return code.strip()
