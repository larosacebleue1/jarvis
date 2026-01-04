"""
Module de déploiement pour l'Agent Jarvis.
Gère le déploiement de projets sur différentes plateformes.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import json


class Deployer:
    """Module de déploiement multi-plateforme."""
    
    def __init__(self, config, llm, kb, logger):
        """
        Initialise le module de déploiement.
        
        Args:
            config: Configuration de l'agent
            llm: Client LLM
            kb: Base de connaissances
            logger: Logger
        """
        self.config = config
        self.llm = llm
        self.kb = kb
        self.logger = logger
    
    def deploy(
        self,
        project_path: str,
        method: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Déploie un projet selon la méthode spécifiée.
        
        Args:
            project_path: Chemin vers le projet
            method: Méthode de déploiement (ssh, docker, cloud, ftp)
            config: Configuration de déploiement
            
        Returns:
            Résultat du déploiement
        """
        self.logger.section(f"Déploiement via {method}")
        
        if method == "ssh":
            return self.deploy_ssh(project_path, config)
        elif method == "docker":
            return self.deploy_docker(project_path, config)
        elif method == "cloud":
            return self.deploy_cloud(project_path, config)
        elif method == "ftp":
            return self.deploy_ftp(project_path, config)
        else:
            return {
                "success": False,
                "error": f"Méthode de déploiement '{method}' non supportée"
            }
    
    def deploy_ssh(
        self,
        project_path: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Déploie via SSH/SFTP.
        
        Args:
            project_path: Chemin vers le projet
            config: Configuration SSH (host, user, key_path, remote_path)
            
        Returns:
            Résultat du déploiement
        """
        self.logger.action("Déploiement SSH en cours...")
        
        try:
            host = config.get("host")
            user = config.get("user")
            key_path = config.get("key_path")
            remote_path = config.get("remote_path", "/var/www/html")
            port = config.get("port", 22)
            
            if not all([host, user]):
                return {
                    "success": False,
                    "error": "Configuration SSH incomplète (host et user requis)"
                }
            
            # Préparer la commande rsync
            ssh_cmd = f"ssh -p {port}"
            if key_path:
                ssh_cmd += f" -i {key_path}"
            
            rsync_cmd = [
                "rsync",
                "-avz",
                "--delete",
                "-e", ssh_cmd,
                f"{project_path}/",
                f"{user}@{host}:{remote_path}/"
            ]
            
            self.logger.info(f"Upload vers {user}@{host}:{remote_path}")
            
            # Exécuter rsync
            result = subprocess.run(
                rsync_cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Erreur rsync: {result.stderr}"
                }
            
            # Commandes post-déploiement (optionnel)
            post_commands = config.get("post_commands", [])
            if post_commands:
                self.logger.info("Exécution des commandes post-déploiement...")
                
                for cmd in post_commands:
                    ssh_exec = [
                        "ssh",
                        "-p", str(port),
                        f"{user}@{host}",
                        cmd
                    ]
                    
                    if key_path:
                        ssh_exec.insert(1, "-i")
                        ssh_exec.insert(2, key_path)
                    
                    subprocess.run(ssh_exec, timeout=60)
            
            self.logger.success("Déploiement SSH réussi !")
            
            return {
                "success": True,
                "method": "ssh",
                "host": host,
                "remote_path": remote_path,
                "url": config.get("url", f"http://{host}")
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout lors du déploiement SSH"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors du déploiement SSH: {str(e)}"
            }
    
    def deploy_docker(
        self,
        project_path: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Déploie via Docker.
        
        Args:
            project_path: Chemin vers le projet
            config: Configuration Docker (image_name, registry, host)
            
        Returns:
            Résultat du déploiement
        """
        self.logger.action("Déploiement Docker en cours...")
        
        try:
            image_name = config.get("image_name", "jarvis-app")
            registry = config.get("registry")
            tag = config.get("tag", "latest")
            
            project_path = Path(project_path)
            
            # Générer un Dockerfile si absent
            dockerfile_path = project_path / "Dockerfile"
            if not dockerfile_path.exists():
                self.logger.info("Génération du Dockerfile...")
                self._generate_dockerfile(project_path, config)
            
            # Build de l'image
            self.logger.info(f"Build de l'image {image_name}:{tag}...")
            
            build_cmd = [
                "docker", "build",
                "-t", f"{image_name}:{tag}",
                str(project_path)
            ]
            
            result = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Erreur build Docker: {result.stderr}"
                }
            
            # Push vers le registry (optionnel)
            if registry:
                full_image = f"{registry}/{image_name}:{tag}"
                
                self.logger.info(f"Tag de l'image: {full_image}")
                subprocess.run(
                    ["docker", "tag", f"{image_name}:{tag}", full_image],
                    timeout=60
                )
                
                self.logger.info(f"Push vers {registry}...")
                push_result = subprocess.run(
                    ["docker", "push", full_image],
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                
                if push_result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Erreur push Docker: {push_result.stderr}"
                    }
            
            # Déploiement sur un host distant (optionnel)
            host = config.get("host")
            if host:
                self.logger.info(f"Déploiement sur {host}...")
                self._deploy_docker_remote(config, image_name, tag)
            
            self.logger.success("Déploiement Docker réussi !")
            
            return {
                "success": True,
                "method": "docker",
                "image": f"{image_name}:{tag}",
                "registry": registry
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout lors du déploiement Docker"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors du déploiement Docker: {str(e)}"
            }
    
    def deploy_cloud(
        self,
        project_path: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Déploie sur une plateforme cloud.
        
        Args:
            project_path: Chemin vers le projet
            config: Configuration cloud (platform, api_key, project_name)
            
        Returns:
            Résultat du déploiement
        """
        self.logger.action("Déploiement Cloud en cours...")
        
        platform = config.get("platform", "vercel").lower()
        
        try:
            if platform == "vercel":
                return self._deploy_vercel(project_path, config)
            elif platform == "netlify":
                return self._deploy_netlify(project_path, config)
            elif platform == "heroku":
                return self._deploy_heroku(project_path, config)
            else:
                return {
                    "success": False,
                    "error": f"Plateforme '{platform}' non supportée"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors du déploiement cloud: {str(e)}"
            }
    
    def deploy_ftp(
        self,
        project_path: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Déploie via FTP/FTPS.
        
        Args:
            project_path: Chemin vers le projet
            config: Configuration FTP (host, user, password, remote_path)
            
        Returns:
            Résultat du déploiement
        """
        self.logger.action("Déploiement FTP en cours...")
        
        try:
            import ftplib
            
            host = config.get("host")
            user = config.get("user")
            password = config.get("password")
            remote_path = config.get("remote_path", "/")
            port = config.get("port", 21)
            use_tls = config.get("use_tls", False)
            
            if not all([host, user, password]):
                return {
                    "success": False,
                    "error": "Configuration FTP incomplète"
                }
            
            # Connexion FTP
            if use_tls:
                ftp = ftplib.FTP_TLS()
            else:
                ftp = ftplib.FTP()
            
            self.logger.info(f"Connexion à {host}:{port}...")
            ftp.connect(host, port)
            ftp.login(user, password)
            
            if use_tls:
                ftp.prot_p()
            
            # Changer vers le répertoire distant
            try:
                ftp.cwd(remote_path)
            except:
                self.logger.warning(f"Création du répertoire {remote_path}")
                ftp.mkd(remote_path)
                ftp.cwd(remote_path)
            
            # Upload des fichiers
            self.logger.info("Upload des fichiers...")
            uploaded_files = self._upload_directory_ftp(ftp, project_path, remote_path)
            
            ftp.quit()
            
            self.logger.success(f"Déploiement FTP réussi ! ({len(uploaded_files)} fichiers)")
            
            return {
                "success": True,
                "method": "ftp",
                "host": host,
                "remote_path": remote_path,
                "files_uploaded": len(uploaded_files)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors du déploiement FTP: {str(e)}"
            }
    
    def _generate_dockerfile(self, project_path: Path, config: Dict[str, Any]):
        """Génère un Dockerfile adapté au projet."""
        
        # Détecter le type de projet
        if (project_path / "package.json").exists():
            # Projet Node.js
            dockerfile_content = """FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
"""
        elif (project_path / "requirements.txt").exists():
            # Projet Python
            dockerfile_content = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
"""
        else:
            # Serveur web statique
            dockerfile_content = """FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
        
        dockerfile_path = project_path / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)
        self.logger.success("Dockerfile généré")
    
    def _deploy_docker_remote(self, config: Dict[str, Any], image_name: str, tag: str):
        """Déploie un container Docker sur un host distant."""
        
        host = config.get("host")
        user = config.get("user", "root")
        port_mapping = config.get("port_mapping", "80:80")
        container_name = config.get("container_name", image_name)
        
        # Commandes à exécuter sur le host distant
        commands = [
            f"docker pull {image_name}:{tag}",
            f"docker stop {container_name} || true",
            f"docker rm {container_name} || true",
            f"docker run -d --name {container_name} -p {port_mapping} {image_name}:{tag}"
        ]
        
        for cmd in commands:
            subprocess.run(
                ["ssh", f"{user}@{host}", cmd],
                timeout=120
            )
    
    def _deploy_vercel(self, project_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Déploie sur Vercel."""
        
        self.logger.info("Déploiement sur Vercel...")
        
        # Vérifier si vercel CLI est installé
        try:
            subprocess.run(["vercel", "--version"], capture_output=True, timeout=5)
        except:
            return {
                "success": False,
                "error": "Vercel CLI non installé. Installez avec: npm i -g vercel"
            }
        
        # Déployer
        result = subprocess.run(
            ["vercel", "--prod", "--yes"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            return {
                "success": False,
                "error": f"Erreur Vercel: {result.stderr}"
            }
        
        # Extraire l'URL de déploiement
        url = result.stdout.strip().split("\n")[-1]
        
        return {
            "success": True,
            "method": "cloud",
            "platform": "vercel",
            "url": url
        }
    
    def _deploy_netlify(self, project_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Déploie sur Netlify."""
        
        self.logger.info("Déploiement sur Netlify...")
        
        # Vérifier si netlify CLI est installé
        try:
            subprocess.run(["netlify", "--version"], capture_output=True, timeout=5)
        except:
            return {
                "success": False,
                "error": "Netlify CLI non installé. Installez avec: npm i -g netlify-cli"
            }
        
        # Déployer
        result = subprocess.run(
            ["netlify", "deploy", "--prod"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            return {
                "success": False,
                "error": f"Erreur Netlify: {result.stderr}"
            }
        
        return {
            "success": True,
            "method": "cloud",
            "platform": "netlify"
        }
    
    def _deploy_heroku(self, project_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Déploie sur Heroku."""
        
        self.logger.info("Déploiement sur Heroku...")
        
        app_name = config.get("app_name")
        
        # Vérifier si heroku CLI est installé
        try:
            subprocess.run(["heroku", "--version"], capture_output=True, timeout=5)
        except:
            return {
                "success": False,
                "error": "Heroku CLI non installé. Installez depuis: https://devcenter.heroku.com/articles/heroku-cli"
            }
        
        # Créer l'app si nécessaire
        if app_name:
            subprocess.run(
                ["heroku", "create", app_name],
                cwd=project_path,
                capture_output=True,
                timeout=60
            )
        
        # Déployer via git
        commands = [
            "git init",
            "heroku git:remote" + (f" -a {app_name}" if app_name else ""),
            "git add .",
            "git commit -m 'Deploy to Heroku'",
            "git push heroku master"
        ]
        
        for cmd in commands:
            result = subprocess.run(
                cmd.split(),
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0 and "git push" in cmd:
                return {
                    "success": False,
                    "error": f"Erreur Heroku: {result.stderr}"
                }
        
        return {
            "success": True,
            "method": "cloud",
            "platform": "heroku",
            "app_name": app_name
        }
    
    def _upload_directory_ftp(
        self,
        ftp,
        local_path: str,
        remote_path: str
    ) -> List[str]:
        """Upload récursif d'un répertoire via FTP."""
        
        uploaded = []
        local_path = Path(local_path)
        
        for item in local_path.rglob("*"):
            if item.is_file():
                # Calculer le chemin relatif
                rel_path = item.relative_to(local_path)
                remote_file = f"{remote_path}/{rel_path}".replace("\\", "/")
                
                # Créer les répertoires parents si nécessaire
                remote_dir = "/".join(remote_file.split("/")[:-1])
                self._ensure_ftp_directory(ftp, remote_dir)
                
                # Upload du fichier
                with open(item, "rb") as f:
                    ftp.storbinary(f"STOR {remote_file}", f)
                
                uploaded.append(str(rel_path))
                self.logger.info(f"  ✓ {rel_path}")
        
        return uploaded
    
    def _ensure_ftp_directory(self, ftp, path: str):
        """Crée un répertoire FTP s'il n'existe pas."""
        
        dirs = path.split("/")
        current = ""
        
        for d in dirs:
            if not d:
                continue
            
            current += f"/{d}"
            
            try:
                ftp.cwd(current)
            except:
                try:
                    ftp.mkd(current)
                except:
                    pass
