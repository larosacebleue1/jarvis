#!/usr/bin/env python3
"""
Script de test pour l'Agent AMIKAL.
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.agent import AmikalAgent


def test_initialization():
    """Test l'initialisation de l'agent."""
    print("=" * 60)
    print("Test 1: Initialisation de l'agent")
    print("=" * 60)
    
    try:
        agent = AmikalAgent()
        print("✓ Agent initialisé avec succès")
        print(f"  - Modèle LLM: {agent.config.llm.model}")
        print(f"  - Module Builder: {'Activé' if agent.builder else 'Désactivé'}")
        print(f"  - Module Fixer: {'Activé' if agent.fixer else 'Désactivé'}")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de l'initialisation: {e}")
        return False


def test_build_request_analysis():
    """Test l'analyse d'une demande de construction."""
    print("\n" + "=" * 60)
    print("Test 2: Analyse d'une demande de construction")
    print("=" * 60)
    
    try:
        agent = AmikalAgent()
        request = "Crée un site web pour présenter mon portfolio de développeur"
        
        print(f"Demande: {request}")
        analysis = agent.builder.analyze_request(request)
        
        print("✓ Analyse réussie")
        print(f"  - Type d'outil: {analysis.get('tool_type', 'N/A')}")
        print(f"  - Nom du projet: {analysis.get('project_name', 'N/A')}")
        print(f"  - Complexité: {analysis.get('complexity', 'N/A')}")
        print(f"  - Fonctionnalités: {', '.join(analysis.get('features', []))[:100]}...")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ask_question():
    """Test la fonctionnalité de question."""
    print("\n" + "=" * 60)
    print("Test 3: Poser une question à l'agent")
    print("=" * 60)
    
    try:
        agent = AmikalAgent()
        question = "Qu'est-ce qu'une API REST ?"
        
        print(f"Question: {question}")
        answer = agent.ask(question)
        
        print("✓ Réponse reçue")
        print(f"  Réponse (extrait): {answer[:200]}...")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de la question: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_base():
    """Test la base de connaissances."""
    print("\n" + "=" * 60)
    print("Test 4: Base de connaissances")
    print("=" * 60)
    
    try:
        agent = AmikalAgent()
        
        # Sauvegarder une solution
        solution_id = agent.kb.save_solution(
            problem="Test de connexion à la base de données",
            solution="Vérifier les credentials et la connectivité réseau",
            tags=["database", "test"]
        )
        
        print(f"✓ Solution sauvegardée: {solution_id}")
        
        # Rechercher la solution
        results = agent.kb.search_solutions("problème de base de données", limit=1)
        
        if results:
            print(f"✓ Solution retrouvée: {results[0].get('id', 'N/A')}")
        else:
            print("⚠ Aucune solution trouvée (normal si vector DB désactivé)")
        
        return True
    except Exception as e:
        print(f"✗ Erreur avec la base de connaissances: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_build_simple_website():
    """Test la construction d'un site web simple."""
    print("\n" + "=" * 60)
    print("Test 5: Construction d'un site web simple")
    print("=" * 60)
    
    try:
        agent = AmikalAgent()
        
        output_dir = "/home/ubuntu/amikal-agent/test_output/test_site"
        
        print("Construction en cours...")
        result = agent.build(
            "Crée un site web simple avec une page d'accueil",
            output_dir=output_dir
        )
        
        if result.get("success"):
            print("✓ Site web construit avec succès")
            print(f"  - Projet: {result.get('project_name', 'N/A')}")
            print(f"  - Répertoire: {result.get('output_dir', 'N/A')}")
            print(f"  - Fichiers: {', '.join(result.get('files', []))}")
            return True
        else:
            print(f"✗ Échec de la construction: {result.get('error', 'Erreur inconnue')}")
            return False
    except Exception as e:
        print(f"✗ Erreur lors de la construction: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Exécute tous les tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "TESTS DE L'AGENT AMIKAL" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        test_initialization,
        test_build_request_analysis,
        test_ask_question,
        test_knowledge_base,
        test_build_simple_website
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ Erreur inattendue dans {test.__name__}: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests réussis: {passed}/{total}")
    
    if passed == total:
        print("✓ Tous les tests sont passés avec succès!")
    else:
        print(f"⚠ {total - passed} test(s) ont échoué")
    
    print()


if __name__ == "__main__":
    main()
