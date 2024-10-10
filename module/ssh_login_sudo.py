import paramiko
import time

def ssh_login_sudo(host, username, ssh_priv, sudo_password, command):
    # Initialiser le client SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    
    

    try:
        # Utilisation d'une clé privée (recommandé) :1
        mypkey = paramiko.RSAKey.from_private_key_file(ssh_priv)
        # Connexion au serveur distant
        client.connect(host, username=username, pkey=mypkey)
        print(f"Connexion réussie à {host} en tant que {username}")

        # Exécution de la commande en tant que superutilisateur (sudo)
        ssh_command = f"sudo -S -p '' {command}"
        

        # Ouvrir le canal pour l'exécution de la commande
        stdin, stdout, stderr = client.exec_command(ssh_command)

        # Fournir le mot de passe sudo
        stdin.write(sudo_password + "\n")
        stdin.flush()

        # Attendre quelques instants pour permettre à la commande de s'exécuter
        time.sleep(1)

        # Lire la sortie et les erreurs
        output = stdout.read().decode()
        error = stderr.read().decode()

        # Afficher les résultats
        if output:
            print("Sortie de la commande :")
            print(output)
        if error:
            print("Erreurs (si présentes) :")
            print(error)

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermer la connexion SSH
        client.close()

#ssh_login_sudo(host="192.168.75.129", username="jtombi", ssh_priv="C:/Users/J-TOMBI/Documents/Code/Script python/SSH/module/id_rsa", sudo_password="salakae", command= input("commande :"))
