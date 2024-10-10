import mariadb
import paramiko
import re
from datetime import datetime
from io import BytesIO
import getpass

def read_log_file_via_ssh_www(ssh_client, remote_file_path, sudo_password):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(f'sudo cat {remote_file_path}', get_pty=True)
        stdin.write(f'{sudo_password}\n')
        stdin.flush()
        log_content = stdout.read().decode()
        print("Fichier lu depuis le serveur via SSH")
        return log_content
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier depuis le serveur via SSH : {e}")
        return None

def parse_log_content_www(log_content):
    tentatives_acces = []
    try:
        for line in log_content.splitlines():
            #print(f"Analyzing line: {line}")  # Impression pour débogage
            # Pour les erreurs d'authentification HTTP
            match_http = re.search(r"\[(.*?)\] \[auth_basic:error\] \[pid \d+:tid \d+] \[client ([\d\.]+):\d+\] AH01618: user ([^ ]+) not found: /", line)
            if match_http:
                timestamp_str = match_http.group(1)
                timestamp = datetime.strptime(timestamp_str, "%a %b %d %H:%M:%S.%f %Y")
                ip_address = match_http.group(2)
                username = match_http.group(3)
                tentatives_acces.append((username, ip_address, timestamp))
                #print(f"HTTP Auth Error: {username}, {ip_address}, {timestamp}")
            #else:
                #print("No match found for HTTP auth error")  # Impression pour débogage
    except Exception as e:
        print(f"Erreur lors de l'analyse du contenu du fichier de log : {e}")
    return tentatives_acces



def store_access_attempts_www(tentatives_acces):
    try:
        conn = mariadb.connect(
            user="jtombi",
            password=getpass.getpass("mot de passe mysql: "),
            host="192.168.75.129",
            port=3306,  # Port spécifié ici
            database="bb_sql"
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_www (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                ip_address VARCHAR(255),
                timestamp DATETIME
            )
        """)

        for attempt in tentatives_acces:
            print(f"Insertion : {attempt}")  # Impression pour débogage
            cursor.execute("""
                INSERT INTO error_www (username, ip_address, timestamp)
                VALUES (%s, %s, %s)
            """, attempt)

        conn.commit()
        print("Tentatives d'accès enregistrées avec succès !")

    except mariadb.Error as e:
        print(f"Erreur lors de l'enregistrement des tentatives d'accès : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":

    remote_file_path = "/var/log/apache2/error.log"
    sudo_password = getpass.getpass("mot de passe sudo: ")

    hote_ssh = "192.168.75.133"
    utilisateur_ssh = "jtombi"
    chemin_cle_privee = "/home/py/.ssh/id_rsa"  # Utilisation de la chaîne brute

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hote_ssh, username=utilisateur_ssh, key_filename=chemin_cle_privee)

    log_content = read_log_file_via_ssh_www(ssh_client, remote_file_path, sudo_password)
    if log_content:
        tentatives_acces = parse_log_content_www(log_content)
        store_access_attempts_www(tentatives_acces)

    ssh_client.close()
