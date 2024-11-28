import os
import paramiko
import logging
from datetime import datetime

# Configurations
BACKUP_DIR = os.getenv('BACKUP_DIR', '~/backup')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'bb_sql')
DATABASE_USER = os.getenv('DATABASE_USER', 'jtombi')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'votre_mot_de_passe')
REMOTE_HOST = os.getenv('REMOTE_HOST', '192.168.75.129')
REMOTE_USER = os.getenv('REMOTE_USER', 'jtombi')
PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH', '/home/py/.ssh/id_rsa')
NUMBER_OF_BACKUPS_TO_KEEP = int(os.getenv('NUMBER_OF_BACKUPS_TO_KEEP', 7))
SUDO_PASSWORD = os.getenv('SUDO_PASSWORD', 'votre_mot_de_passe')  # Mot de passe sudo

# Configurer la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'{BACKUP_DIR}/db_backup_{timestamp}.sql'
    dump_command = f'sudo mysqldump -u {DATABASE_USER} -p{DATABASE_PASSWORD} {DATABASE_NAME} > {backup_file}'

    try:
        key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(REMOTE_HOST, username=REMOTE_USER, pkey=key)

        stdin, stdout, stderr = client.exec_command(dump_command, get_pty=True)
        stdin.write(SUDO_PASSWORD + '\n')
        stdin.flush()
        errors = stderr.read().decode('utf-8')
        if errors:
            logging.error(f"Erreur lors de l'exécution de la commande sur le serveur distant : {errors}")
        else:
            logging.info(f"Sauvegarde réussie : {backup_file}")

        client.close()
        return backup_file
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde de la base de données : {e}")
        return None

def clean_old_backups_remote():
    try:
        key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(REMOTE_HOST, username=REMOTE_USER, pkey=key)

        list_backups_cmd = f'ls -1t {BACKUP_DIR}/db_backup_*.sql'
        stdin, stdout, stderr = client.exec_command(list_backups_cmd)
        backup_files = stdout.read().decode().splitlines()
        logging.info(f"Nombre total de sauvegardes trouvées : {len(backup_files)}")

        if len(backup_files) > NUMBER_OF_BACKUPS_TO_KEEP:
            backups_to_delete = backup_files[NUMBER_OF_BACKUPS_TO_KEEP:]
            for backup in backups_to_delete:
                delete_cmd = f'sudo rm {backup}'
                stdin, stdout, stderr = client.exec_command(delete_cmd, get_pty=True)
                stdin.write(SUDO_PASSWORD + '\n')
                stdin.flush()
                errors = stderr.read().decode('utf-8')
                if errors:
                    logging.error(f"Erreur lors de la suppression de {backup} : {errors}")
                else:
                    logging.info(f"Suppression de la sauvegarde : {backup}")
        else:
            logging.info("Aucune sauvegarde à supprimer.")

        client.close()
    except Exception as e:
        logging.error(f"Erreur lors de la suppression des anciennes sauvegardes : {e}")

if __name__ == '__main__':
    backup_database()
    clean_old_backups_remote()

