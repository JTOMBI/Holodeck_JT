import paramiko
import mariadb
import sys
import getpass

def ssh_login_mysql(host, username, ssh_priv):
    # Connexion SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn = None  # Initialisation de la variable

    try:
        # Utilisation d'une clé privée (recommandé) :1
        mypkey = paramiko.RSAKey.from_private_key_file(ssh_priv)
        # Connexion au serveur distant
        client.connect(host, username=username, pkey=mypkey)
        print(f"Connexion SSH réussie à {host} en tant que {username}")

        # Connexion à la base de données MariaDB
        conn = mariadb.connect(user="jtombi", host="192.168.75.129",password=getpass.getpass("mot de passe mysql: "), port=3306, database="bb_sql")
        print("Connexion à la base de données MariaDB réussie")

        # Exécutez vos opérations sur la base de données ici (par exemple, SELECT, INSERT, UPDATE, etc.)
 # Boucle pour exécuter des commandes SQL
        while True:
            command = input("Entrez votre commande SQL (ou 'exit' pour quitter) : ")
            if command.lower() == 'exit':
                break

            cursor = conn.cursor()
            try:
                cursor.execute(command)
                if command.strip().lower().startswith("select"):
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                else:
                    conn.commit()
                    print(f"Commande exécutée avec succès : {command}")
            except mariadb.Error as e:
                print(f"Erreur lors de l'exécution de la commande : {e}")
            finally:
                cursor.close()

    except paramiko.SSHException as ssh_e:
        print(f"Erreur SSH : {ssh_e}")
    except mariadb.Error as db_e:
        print(f"Erreur de base de données : {db_e}")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        sys.exit(1)

    finally:
        # Fermez les connexions
        if conn:
            conn.close()
        client.close()



