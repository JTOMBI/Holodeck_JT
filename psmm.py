import paramiko
import time
import getpass
import subprocess
import mariadb
import re
from datetime import datetime
from module.ssh_mysql import ssh_login_mysql
from module.ssh_login_sudo import ssh_login_sudo
from module.ssh_mysql_vide_error import vider_error_db
from module.ssh_mysql_vide_error import vider_error_ftp
from module.ssh_mysql_vide_error import vider_error_www


def run_script(script_path):
    # Utilise subprocess pour lancer le script Python
    subprocess.run(["python3", script_path])


def choice_m():
    while True:
        output_choice = input("Que voulez vous:\n\n1 - Ecrire une commande sur le serveur\n2 - Ecrire des commandes sur le MySql\n3 - Enregistrer les erreurs de connexion\n4 - Vider la base de donnée erreur\nEnter choice here: ")
        conv_ma = int(output_choice)
        if conv_ma == 1:
            su_passw = getpass.getpass("mot de passe sudo: ")
            ssh_login_sudo(host="192.168.75.129", username="jtombi", ssh_priv="/home/py/.ssh/id_rsa", sudo_password=su_passw, command= input("commande :"))
            break
        elif conv_ma == 2:
            # The standard output stream is the screen so we don't need to redirect and just need to break the while loop.
            ssh_login_mysql(host="192.168.75.129", username="jtombi", ssh_priv="/home/py/.ssh/id_rsa")
            break
        elif conv_ma == 3:
            script_to_run = "/home/py/scrypt-python/module/ssh_mysql_error.py"
            run_script(script_to_run)
            break
        elif conv_ma == 4 :
            vider_error_db()
            break
        else :
            print("You entered an incorrect option, please try again.")

def choice_ftp():
    while True:
        output_choice = input("Que voulez vous:\n\n1 - Ecrire une commande sur le serveur\n2 - Enregistrer les erreurs de connexion\n3 - Vider la base de donnée erreur\nEnter choice here: ")
        conv_ma = int(output_choice)
        if conv_ma == 1:
            su_passw = getpass.getpass("mot de passe sudo: ")
            ssh_login_sudo(host="192.168.75.132", username="jtombi", ssh_priv="/home/py/.ssh/id_rsa", sudo_password=su_passw, command= input("commande :"))
            break
        elif conv_ma == 2:
            script_to_run = "/home/py/scrypt-python/module/ssh_ftp_error.py"
            run_script(script_to_run)
            break
        elif conv_ma == 3 :
            vider_error_ftp()
            break
        else :
            print("You entered an incorrect option, please try again.")

def choice_www():
    while True:
        output_choice = input("Que voulez vous:\n\n1 - Ecrire une commande sur le serveur\n2 - Enregistrer les erreurs de connexion\n3 - Vider la base de donnée erreur\nEnter choice here: ")
        conv_ma = int(output_choice)
        if conv_ma == 1:
            su_passw = getpass.getpass("mot de passe sudo: ")
            ssh_login_sudo(host="192.168.75.133", username="jtombi", ssh_priv="/home/py/.ssh/id_rsa", sudo_password=su_passw, command= input("commande :"))
            break
        elif conv_ma == 2:
            script_to_run = "/home/py/scrypt-python/module/ssh_web_error.py"
            run_script(script_to_run)
            break
        elif conv_ma == 3 :
            vider_error_www()
            break
        else :
            print("You entered an incorrect option, please try again.")

def choice_mail():
    while True:
        output_choice = input("Que voulez vous:\n\n1 - mail error login\n2 - mail system des serveurs\n3 - Google Group\nEnter choice here: ")
        conv_ma = int(output_choice)
        if conv_ma == 1:
            script_to_run = "/home/py/scrypt-python/module/ssh_serveur_mail.py"
            run_script(script_to_run)
            break

        elif conv_ma == 2:
            script_to_run = "/home/py/scrypt-python/module/ssh_system_mail.py"
            run_script(script_to_run)
            break

        elif conv_ma == 3:
            script_to_run = "/home/py/scrypt-python/module/info_google.py"
            run_script(script_to_run)
            break

while True:
        
        try:
            output_choice = input("Quelle serveur vous voullez vous connectez :\n\n1 - Binary-Beavers-Mariadb\n2 - Binary-Beavers-FTP\n3 - Binany-Beavers-Web\n4 - envoie mail/google\n5 - backup\nEnter choice here: ")
            conv_val = int(output_choice)
            if conv_val == 1:
                # We redirect the standard output stream to a file instead of the screen.
                    choice_m()
                    break
            elif conv_val == 2:
                # The standard output stream is the screen so we don't need to redirect and just need to break the while loop.
                    choice_ftp()                    
                    break

            elif conv_val == 3:
                # The standard output stream is the screen so we don't need to redirect and just need to break the while loop.
                    choice_www()
                    break
            elif conv_val == 4:
                 choice_mail()
                 break
            elif conv_val == 5:
                 script_to_run = "/home/py/scrypt-python/module/ssh_cron_backup.py"
                 run_script(script_to_run)
                 break
            else:
                print("You entered an incorrect option, please try again.")
        except:
            print("You entered an invalid option, please try again.")
