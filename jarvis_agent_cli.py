#!/usr/bin/env python3
"""
Interface CLI pour l'Agent Jarvis.
"""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.core.agent import JarvisAgent


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Agent Jarvis - Assistant intelligent pour la construction et la maintenance d'outils informatiques.
    
    L'agent peut :
    - Construire des sites web, APIs, outils CLI et plus
    - Réparer et maintenir du code existant
    - Apprendre de nouvelles compétences
    - Répondre à vos questions techniques
    """
    pass


@cli.command()
@click.argument('request', type=str)
@click.option('--output', '-o', type=str, help='Répertoire de sortie pour le projet')
def build(request, output):
    """
    Construit un outil informatique à partir d'une description.
    
    Exemples :
    
    \b
    jarvis-agent build "Crée un site web pour présenter mon portfolio"
    jarvis-agent build "Crée une API REST pour gérer des utilisateurs" -o ./mon-api
    jarvis-agent build "Crée un outil CLI pour convertir des images"
    """
    console.print(Panel.fit(
        f"[bold cyan]Construction d'un outil[/bold cyan]\n\n{request}",
        border_style="cyan"
    ))
    
    try:
        agent = JarvisAgent()
        result = agent.build(request, output_dir=output)
        
        if result.get("success"):
            console.print("\n[bold green]✓ Construction réussie ![/bold green]\n")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Propriété", style="cyan")
            table.add_column("Valeur", style="white")
            
            table.add_row("Projet", result.get("project_name", "N/A"))
            table.add_row("Répertoire", result.get("output_dir", "N/A"))
            table.add_row("Fichiers créés", ", ".join(result.get("files", [])))
            
            console.print(table)
            
            console.print(f"\n[bold]Pour tester votre projet :[/bold]")
            console.print(f"  cd {result.get('output_dir')}")
            console.print(f"  Consultez le README.md pour les instructions\n")
        else:
            console.print(f"\n[bold red]✗ Erreur :[/bold red] {result.get('error', 'Erreur inconnue')}\n")
    
    except Exception as e:
        console.print(f"\n[bold red]✗ Erreur inattendue :[/bold red] {e}\n")


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.argument('issue', type=str)
def fix(project_path, issue):
    """
    Répare un problème dans un projet existant.
    
    Exemples :
    
    \b
    jarvis-agent fix ./mon-projet "L'authentification ne fonctionne pas"
    jarvis-agent fix ./mon-site "Erreur 404 sur la page contact"
    """
    console.print(Panel.fit(
        f"[bold cyan]Réparation d'un projet[/bold cyan]\n\nProjet : {project_path}\nProblème : {issue}",
        border_style="cyan"
    ))
    
    try:
        agent = JarvisAgent()
        result = agent.fix(project_path, issue)
        
        if result.get("success"):
            console.print("\n[bold green]✓ Réparation réussie ![/bold green]\n")
            
            diagnostic = result.get("diagnostic", {})
            
            console.print("[bold]Diagnostic :[/bold]")
            console.print(f"  Cause : {diagnostic.get('cause', 'N/A')}")
            console.print(f"  Confiance : {diagnostic.get('confidence', 'N/A')}")
            
            console.print(f"\n[bold]Fichiers modifiés :[/bold]")
            for file in result.get("fixed_files", []):
                console.print(f"  ✓ {file}")
            
            if result.get("backup_path"):
                console.print(f"\n[bold]Sauvegarde créée :[/bold] {result.get('backup_path')}\n")
        else:
            console.print(f"\n[bold red]✗ Erreur :[/bold red] {result.get('error', 'Erreur inconnue')}\n")
    
    except Exception as e:
        console.print(f"\n[bold red]✗ Erreur inattendue :[/bold red] {e}\n")


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
def analyze(project_path):
    """
    Analyse un projet pour identifier sa structure et ses problèmes potentiels.
    
    Exemple :
    
    \b
    jarvis-agent analyze ./mon-projet
    """
    console.print(Panel.fit(
        f"[bold cyan]Analyse du projet[/bold cyan]\n\n{project_path}",
        border_style="cyan"
    ))
    
    try:
        agent = JarvisAgent()
        result = agent.analyze(project_path)
        
        if result.get("success"):
            console.print("\n[bold green]✓ Analyse terminée ![/bold green]\n")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Propriété", style="cyan")
            table.add_column("Valeur", style="white")
            
            table.add_row("Type de projet", result.get("project_type", "N/A"))
            table.add_row("Nombre de fichiers", str(len(result.get("files", []))))
            
            dependencies = result.get("dependencies", {})
            if dependencies:
                for lang, deps in dependencies.items():
                    table.add_row(f"Dépendances {lang}", str(len(deps)))
            
            console.print(table)
            
            if result.get("files"):
                console.print("\n[bold]Fichiers principaux :[/bold]")
                for file in result.get("files", [])[:10]:
                    console.print(f"  • {file}")
                
                if len(result.get("files", [])) > 10:
                    console.print(f"  ... et {len(result.get('files', [])) - 10} autres fichiers\n")
        else:
            console.print(f"\n[bold red]✗ Erreur :[/bold red] {result.get('error', 'Erreur inconnue')}\n")
    
    except Exception as e:
        console.print(f"\n[bold red]✗ Erreur inattendue :[/bold red] {e}\n")


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--objective', '-obj', type=str, default="améliorer la qualité", 
              help='Objectif du refactoring')
def refactor(file_path, objective):
    """
    Refactorise un fichier de code.
    
    Exemples :
    
    \b
    jarvis-agent refactor ./mon_script.py
    jarvis-agent refactor ./app.js --objective "améliorer les performances"
    """
    console.print(Panel.fit(
        f"[bold cyan]Refactoring[/bold cyan]\n\nFichier : {file_path}\nObjectif : {objective}",
        border_style="cyan"
    ))
    
    try:
        agent = JarvisAgent()
        result = agent.refactor(file_path, objective)
        
        if result.get("success"):
            console.print("\n[bold green]✓ Refactoring réussi ![/bold green]\n")
            console.print(f"Fichier modifié : {result.get('file_path')}")
            
            if result.get("backup_path"):
                console.print(f"Sauvegarde créée : {result.get('backup_path')}\n")
        else:
            console.print(f"\n[bold red]✗ Erreur :[/bold red] {result.get('error', 'Erreur inconnue')}\n")
    
    except Exception as e:
        console.print(f"\n[bold red]✗ Erreur inattendue :[/bold red] {e}\n")


@cli.command()
@click.argument('question', type=str)
def ask(question):
    """
    Pose une question à l'agent.
    
    Exemples :
    
    \b
    jarvis-agent ask "Comment créer une API REST en Python ?"
    jarvis-agent ask "Quelle est la différence entre GET et POST ?"
    """
    console.print(Panel.fit(
        f"[bold cyan]Question[/bold cyan]\n\n{question}",
        border_style="cyan"
    ))
    
    try:
        agent = JarvisAgent()
        answer = agent.ask(question)
        
        console.print("\n[bold green]Réponse :[/bold green]\n")
        console.print(Panel(answer, border_style="green"))
    
    except Exception as e:
        console.print(f"\n[bold red]✗ Erreur inattendue :[/bold red] {e}\n")


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--method', '-m', type=click.Choice(['ssh', 'docker', 'cloud', 'ftp']), 
              default='ssh', help='Méthode de déploiement')
@click.option('--config', '-c', type=str, help='Configuration JSON pour le déploiement')
def deploy(project_path, method, config):
    """
    Déploie un projet sur un serveur.
    
    Exemples :
    
    \b
    jarvis-agent deploy ./mon-site --method ssh --config '{"host":"example.com","user":"root"}'
    jarvis-agent deploy ./mon-app --method docker --config '{"image_name":"mon-app"}'
    jarvis-agent deploy ./mon-site --method cloud --config '{"platform":"vercel"}'
    jarvis-agent deploy ./mon-site --method ftp --config '{"host":"ftp.example.com","user":"user","password":"pass"}'
    """
    console.print(Panel.fit(
        f"[bold cyan]Déploiement d'un projet[/bold cyan]\n\nProjet : {project_path}\nMéthode : {method}",
        border_style="cyan"
    ))
    
    try:
        import json
        
        agent = JarvisAgent()
        
        # Parser la configuration
        deploy_config = {}
        if config:
            try:
                deploy_config = json.loads(config)
            except json.JSONDecodeError:
                console.print("[bold red]✗ Erreur :[/bold red] Configuration JSON invalide\n")
                return
        
        result = agent.deploy(project_path, method, deploy_config)
        
        if result.get("success"):
            console.print("\n[bold green]✓ Déploiement réussi ![/bold green]\n")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Propriété", style="cyan")
            table.add_column("Valeur", style="white")
            
            table.add_row("Méthode", result.get("method", "N/A"))
            
            if result.get("url"):
                table.add_row("URL", result.get("url"))
            if result.get("host"):
                table.add_row("Serveur", result.get("host"))
            if result.get("platform"):
                table.add_row("Plateforme", result.get("platform"))
            
            console.print(table)
            console.print("")
        else:
            console.print(f"\n[bold red]✗ Erreur :[/bold red] {result.get('error', 'Erreur inconnue')}\n")
    
    except Exception as e:
        console.print(f"\n[bold red]✗ Erreur inattendue :[/bold red] {e}\n")


@cli.command()
@click.argument('content', type=str)
@click.option('--type', '-t', type=click.Choice(['solution', 'template', 'pattern']), 
              default='solution', help='Type de connaissance')
@click.option('--tags', '-tag', multiple=True, help='Tags pour la recherche')
def learn(content, type, tags):
    """
    Apprend une nouvelle connaissance à l'agent.
    
    Exemples :
    
    \b
    jarvis-agent learn "Problème: Erreur CORS\nSolution: Ajouter les headers CORS"
    jarvis-agent learn "Pattern de singleton en Python" --type pattern --tags python design-pattern
    """
    console.print(Panel.fit(
        f"[bold cyan]Apprentissage[/bold cyan]\n\nType : {type}\nTags : {', '.join(tags) if tags else 'Aucun'}",
        border_style="cyan"
    ))
    
    try:
        agent = JarvisAgent()
        knowledge_id = agent.learn(content, content_type=type, tags=list(tags) if tags else None)
        
        console.print(f"\n[bold green]✓ Connaissance sauvegardée ![/bold green]")
        console.print(f"ID : {knowledge_id}\n")
    
    except Exception as e:
        console.print(f"\n[bold red]✗ Erreur inattendue :[/bold red] {e}\n")


@cli.command()
def info():
    """
    Affiche les informations sur l'agent.
    """
    console.print(Panel.fit(
        """[bold cyan]Agent Jarvis[/bold cyan]
        
[bold]Version :[/bold] 1.0.0

[bold]Capacités :[/bold]
  • Construction de sites web (statiques et dynamiques)
  • Création d'APIs REST
  • Développement d'outils CLI
  • Réparation et maintenance de code
  • Refactoring de code
  • Apprentissage de nouvelles compétences
  • Réponses aux questions techniques

[bold]Modules activés :[/bold]
  ✓ Builder - Construction d'outils
  ✓ Fixer - Réparation et maintenance
  ✓ Learner - Apprentissage

[bold]Configuration :[/bold]
  Fichier : config/config.yaml
  Base de connaissances : knowledge_base/
  Logs : logs/jarvis-agent.log

[bold]Pour plus d'aide :[/bold]
  jarvis-agent --help
  jarvis-agent <commande> --help
""",
        border_style="cyan"
    ))


if __name__ == '__main__':
    cli()
