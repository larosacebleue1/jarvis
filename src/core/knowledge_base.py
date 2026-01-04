"""
Module de gestion de la base de connaissances de l'agent AMIKAL.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings


class KnowledgeBase:
    """Gestionnaire de la base de connaissances."""
    
    def __init__(self, config, llm_client):
        """
        Initialise la base de connaissances.
        
        Args:
            config: Instance de Config
            llm_client: Instance de LLMClient pour les embeddings
        """
        self.config = config
        self.llm_client = llm_client
        self.base_path = config.get_knowledge_base_path()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Initialisation de ChromaDB si activé
        self.vector_db_enabled = config.knowledge_base.vector_db_enabled
        if self.vector_db_enabled:
            self._init_vector_db()
    
    def _init_vector_db(self):
        """Initialise la base de données vectorielle ChromaDB."""
        db_path = self.base_path / "chroma_db"
        db_path.mkdir(parents=True, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Collection pour les templates
        self.templates_collection = self.chroma_client.get_or_create_collection(
            name="templates",
            metadata={"description": "Templates de code réutilisables"}
        )
        
        # Collection pour les patterns
        self.patterns_collection = self.chroma_client.get_or_create_collection(
            name="patterns",
            metadata={"description": "Patterns de conception appris"}
        )
        
        # Collection pour les solutions
        self.solutions_collection = self.chroma_client.get_or_create_collection(
            name="solutions",
            metadata={"description": "Solutions à des problèmes spécifiques"}
        )
    
    def save_template(self, name: str, description: str, code: str, 
                     language: str, tags: List[str] = None) -> str:
        """
        Sauvegarde un template de code.
        
        Args:
            name: Nom du template
            description: Description du template
            code: Code du template
            language: Langage de programmation
            tags: Tags pour la recherche
            
        Returns:
            ID du template sauvegardé
        """
        template_id = f"template_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Sauvegarde dans le système de fichiers
        template_dir = self.base_path / "templates" / language
        template_dir.mkdir(parents=True, exist_ok=True)
        
        template_data = {
            "id": template_id,
            "name": name,
            "description": description,
            "code": code,
            "language": language,
            "tags": tags or [],
            "created_at": datetime.now().isoformat()
        }
        
        template_file = template_dir / f"{name}.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)
        
        # Sauvegarde du code dans un fichier séparé
        code_file = template_dir / f"{name}.{self._get_file_extension(language)}"
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Indexation dans ChromaDB si activé
        if self.vector_db_enabled:
            self.templates_collection.add(
                documents=[f"{name}: {description}\n\n{code}"],
                metadatas=[{
                    "name": name,
                    "language": language,
                    "tags": ",".join(tags or [])
                }],
                ids=[template_id]
            )
        
        return template_id
    
    def search_templates(self, query: str, language: Optional[str] = None, 
                        limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recherche des templates par similarité sémantique.
        
        Args:
            query: Requête de recherche
            language: Filtrer par langage (optionnel)
            limit: Nombre maximum de résultats
            
        Returns:
            Liste de templates correspondants
        """
        if not self.vector_db_enabled:
            return self._search_templates_filesystem(query, language, limit)
        
        # Recherche dans ChromaDB
        where_filter = {"language": language} if language else None
        
        results = self.templates_collection.query(
            query_texts=[query],
            n_results=limit,
            where=where_filter
        )
        
        templates = []
        if results['ids'] and results['ids'][0]:
            for i, template_id in enumerate(results['ids'][0]):
                metadata = results['metadatas'][0][i]
                templates.append({
                    "id": template_id,
                    "name": metadata.get("name"),
                    "language": metadata.get("language"),
                    "tags": metadata.get("tags", "").split(",") if metadata.get("tags") else [],
                    "score": results['distances'][0][i] if 'distances' in results else None
                })
        
        return templates
    
    def _search_templates_filesystem(self, query: str, language: Optional[str] = None,
                                    limit: int = 5) -> List[Dict[str, Any]]:
        """Recherche de templates dans le système de fichiers (fallback)."""
        templates_dir = self.base_path / "templates"
        if not templates_dir.exists():
            return []
        
        templates = []
        
        # Parcourir les répertoires de langages
        for lang_dir in templates_dir.iterdir():
            if not lang_dir.is_dir():
                continue
            
            if language and lang_dir.name != language:
                continue
            
            # Lire les fichiers JSON
            for template_file in lang_dir.glob("*.json"):
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        templates.append(template_data)
                except Exception:
                    continue
        
        # Filtrage simple par mots-clés
        query_lower = query.lower()
        filtered_templates = [
            t for t in templates
            if query_lower in t.get("name", "").lower() or
               query_lower in t.get("description", "").lower() or
               any(query_lower in tag.lower() for tag in t.get("tags", []))
        ]
        
        return filtered_templates[:limit]
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un template par son ID.
        
        Args:
            template_id: ID du template
            
        Returns:
            Données du template ou None
        """
        templates_dir = self.base_path / "templates"
        
        # Rechercher dans tous les répertoires de langages
        for lang_dir in templates_dir.iterdir():
            if not lang_dir.is_dir():
                continue
            
            for template_file in lang_dir.glob("*.json"):
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        if template_data.get("id") == template_id:
                            return template_data
                except Exception:
                    continue
        
        return None
    
    def save_solution(self, problem: str, solution: str, context: str = "",
                     tags: List[str] = None) -> str:
        """
        Sauvegarde une solution à un problème.
        
        Args:
            problem: Description du problème
            solution: Solution apportée
            context: Contexte additionnel
            tags: Tags pour la recherche
            
        Returns:
            ID de la solution sauvegardée
        """
        solution_id = f"solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Sauvegarde dans le système de fichiers
        solutions_dir = self.base_path / "solutions"
        solutions_dir.mkdir(parents=True, exist_ok=True)
        
        solution_data = {
            "id": solution_id,
            "problem": problem,
            "solution": solution,
            "context": context,
            "tags": tags or [],
            "created_at": datetime.now().isoformat()
        }
        
        solution_file = solutions_dir / f"{solution_id}.json"
        with open(solution_file, 'w', encoding='utf-8') as f:
            json.dump(solution_data, f, indent=2, ensure_ascii=False)
        
        # Indexation dans ChromaDB si activé
        if self.vector_db_enabled:
            self.solutions_collection.add(
                documents=[f"Problème: {problem}\n\nSolution: {solution}\n\nContexte: {context}"],
                metadatas=[{
                    "tags": ",".join(tags or [])
                }],
                ids=[solution_id]
            )
        
        return solution_id
    
    def search_solutions(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recherche des solutions similaires.
        
        Args:
            query: Requête de recherche
            limit: Nombre maximum de résultats
            
        Returns:
            Liste de solutions correspondantes
        """
        if not self.vector_db_enabled:
            return []
        
        results = self.solutions_collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        solutions = []
        if results['ids'] and results['ids'][0]:
            for i, solution_id in enumerate(results['ids'][0]):
                solution_data = self.get_solution(solution_id)
                if solution_data:
                    solution_data['score'] = results['distances'][0][i] if 'distances' in results else None
                    solutions.append(solution_data)
        
        return solutions
    
    def get_solution(self, solution_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère une solution par son ID.
        
        Args:
            solution_id: ID de la solution
            
        Returns:
            Données de la solution ou None
        """
        solution_file = self.base_path / "solutions" / f"{solution_id}.json"
        
        if not solution_file.exists():
            return None
        
        try:
            with open(solution_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def save_project_history(self, project_name: str, description: str,
                            files: Dict[str, str], metadata: Dict[str, Any] = None) -> str:
        """
        Sauvegarde l'historique d'un projet.
        
        Args:
            project_name: Nom du projet
            description: Description du projet
            files: Dictionnaire {chemin: contenu} des fichiers du projet
            metadata: Métadonnées additionnelles
            
        Returns:
            ID de l'historique sauvegardé
        """
        history_id = f"project_{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Sauvegarde dans le système de fichiers
        history_dir = self.base_path / "projects_history" / project_name
        history_dir.mkdir(parents=True, exist_ok=True)
        
        history_data = {
            "id": history_id,
            "project_name": project_name,
            "description": description,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
        
        history_file = history_dir / f"{history_id}.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        # Sauvegarde des fichiers
        files_dir = history_dir / history_id
        files_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path, content in files.items():
            file_full_path = files_dir / file_path
            file_full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return history_id
    
    def _get_file_extension(self, language: str) -> str:
        """Retourne l'extension de fichier pour un langage."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "html": "html",
            "css": "css",
            "java": "java",
            "cpp": "cpp",
            "c": "c",
            "go": "go",
            "rust": "rs",
            "ruby": "rb",
            "php": "php",
            "swift": "swift",
            "kotlin": "kt"
        }
        return extensions.get(language.lower(), "txt")
