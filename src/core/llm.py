"""
Module de gestion des interactions avec les modèles LLM.
"""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI


class LLMClient:
    """Client pour interagir avec les modèles LLM."""
    
    def __init__(self, config):
        """
        Initialise le client LLM.
        
        Args:
            config: Instance de Config contenant la configuration LLM
        """
        self.config = config
        self.provider = config.llm.provider
        self.model = config.llm.model
        self.temperature = config.llm.temperature
        self.max_tokens = config.llm.max_tokens
        
        # Initialisation du client OpenAI
        # Les variables d'environnement OPENAI_API_KEY et base_url sont déjà configurées
        self.client = OpenAI()
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: Optional[float] = None,
             max_tokens: Optional[int] = None) -> str:
        """
        Envoie une requête de chat au modèle LLM.
        
        Args:
            messages: Liste de messages au format OpenAI
            temperature: Température pour la génération (optionnel)
            max_tokens: Nombre maximum de tokens (optionnel)
            
        Returns:
            Réponse du modèle
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temp,
            max_tokens=tokens
        )
        
        return response.choices[0].message.content
    
    def generate_code(self, prompt: str, language: str = "python") -> str:
        """
        Génère du code à partir d'un prompt.
        
        Args:
            prompt: Description de ce que le code doit faire
            language: Langage de programmation cible
            
        Returns:
            Code généré
        """
        system_message = f"""Tu es un expert en développement {language}.
Génère du code propre, bien structuré et commenté.
Suis les meilleures pratiques et conventions du langage.
Retourne uniquement le code, sans explications supplémentaires."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages)
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyse du code pour détecter des problèmes.
        
        Args:
            code: Code à analyser
            language: Langage de programmation
            
        Returns:
            Dictionnaire contenant l'analyse
        """
        system_message = f"""Tu es un expert en analyse de code {language}.
Analyse le code fourni et identifie :
1. Les erreurs potentielles
2. Les problèmes de performance
3. Les violations des meilleures pratiques
4. Les suggestions d'amélioration

Retourne ta réponse au format JSON avec les clés suivantes :
- errors: liste des erreurs
- warnings: liste des avertissements
- suggestions: liste des suggestions d'amélioration
- severity: niveau de gravité global (low, medium, high)"""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Code à analyser :\n\n```{language}\n{code}\n```"}
        ]
        
        response = self.chat(messages)
        
        # Tenter de parser la réponse JSON
        import json
        try:
            # Extraire le JSON de la réponse si elle contient du texte supplémentaire
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {"raw_response": response}
        except json.JSONDecodeError:
            return {"raw_response": response}
    
    def fix_code(self, code: str, error_message: str, language: str = "python") -> str:
        """
        Répare du code en fonction d'un message d'erreur.
        
        Args:
            code: Code à réparer
            error_message: Message d'erreur
            language: Langage de programmation
            
        Returns:
            Code corrigé
        """
        system_message = f"""Tu es un expert en débogage {language}.
Analyse le code et l'erreur fournis, puis génère une version corrigée du code.
Retourne uniquement le code corrigé, sans explications supplémentaires."""
        
        user_message = f"""Code avec erreur :
```{language}
{code}
```

Erreur rencontrée :
```
{error_message}
```

Corrige ce code."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        return self.chat(messages)
    
    def explain_code(self, code: str, language: str = "python") -> str:
        """
        Explique ce que fait un code.
        
        Args:
            code: Code à expliquer
            language: Langage de programmation
            
        Returns:
            Explication du code
        """
        system_message = f"""Tu es un expert en {language}.
Explique clairement ce que fait le code fourni, en français.
Structure ton explication de manière pédagogique."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Explique ce code :\n\n```{language}\n{code}\n```"}
        ]
        
        return self.chat(messages)
    
    def generate_documentation(self, code: str, language: str = "python") -> str:
        """
        Génère de la documentation pour du code.
        
        Args:
            code: Code à documenter
            language: Langage de programmation
            
        Returns:
            Documentation générée
        """
        system_message = f"""Tu es un expert en documentation technique {language}.
Génère une documentation complète pour le code fourni, incluant :
- Description générale
- Paramètres et types
- Valeurs de retour
- Exemples d'utilisation
- Notes importantes

Utilise le format de documentation standard pour {language}."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Documente ce code :\n\n```{language}\n{code}\n```"}
        ]
        
        return self.chat(messages)
    
    def refactor_code(self, code: str, language: str = "python", 
                     objective: str = "améliorer la lisibilité et la maintenabilité") -> str:
        """
        Refactorise du code selon un objectif.
        
        Args:
            code: Code à refactoriser
            language: Langage de programmation
            objective: Objectif du refactoring
            
        Returns:
            Code refactorisé
        """
        system_message = f"""Tu es un expert en refactoring {language}.
Refactorise le code fourni pour {objective}.
Conserve la fonctionnalité exacte du code original.
Retourne uniquement le code refactorisé."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Code à refactoriser :\n\n```{language}\n{code}\n```"}
        ]
        
        return self.chat(messages)
    
    def answer_question(self, question: str, context: Optional[str] = None) -> str:
        """
        Répond à une question, éventuellement avec un contexte.
        
        Args:
            question: Question à répondre
            context: Contexte additionnel (optionnel)
            
        Returns:
            Réponse à la question
        """
        system_message = """Tu es un assistant expert en développement informatique.
Réponds de manière claire, précise et structurée en français.
Si tu n'es pas sûr d'une information, indique-le clairement."""
        
        user_message = question
        if context:
            user_message = f"Contexte :\n{context}\n\nQuestion :\n{question}"
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        return self.chat(messages)
