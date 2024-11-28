import mariadb
import getpass

def vider_error_db():
    try:
        conn = mariadb.connect(
            user="jtombi",
            password=getpass.getpass("mot de passe mysql: "),
            host="192.168.75.129",
            port=3306,  # Port spécifié ici
            database="bb_sql"
        )
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE error_mariadb")
        conn.commit()
        print("Table error_mariadb vidée avec succès !")

    except mariadb.Error as e:
        print(f"Erreur lors du vidage de la table error_mariadb : {e}")
    finally:
        if conn:
            conn.close()


def vider_error_ftp():
    try:
        conn = mariadb.connect(
            user="jtombi",
            password=getpass.getpass("mot de passe mysql: "),
            host="192.168.75.129",
            port=3306,  # Port spécifié ici
            database="bb_sql"
        )
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE error_sftp")
        conn.commit()
        print("Table error_sftp vidée avec succès !")

    except mariadb.Error as e:
        print(f"Erreur lors du vidage de la table error_sftp : {e}")
    finally:
        if conn:
            conn.close()


def vider_error_www():
    try:
        conn = mariadb.connect(
            user="jtombi",
            password=getpass.getpass("mot de passe mysql: "),
            host="192.168.75.129",
            port=3306,  # Port spécifié ici
            database="bb_sql"
        )
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE error_www")
        conn.commit()
        print("Table error_www vidée avec succès !")

    except mariadb.Error as e:
        print(f"Erreur lors du vidage de la table error_sftp : {e}")
    finally:
        if conn:
            conn.close()
