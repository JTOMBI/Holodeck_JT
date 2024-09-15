# Holodeck

1 - Installation de Debian 11 sur VMware Workstation 17

1.1 - Installation de l'image iso

Prérequis : Iso Debian 11 (https://www.debian.org/distrib/netinst)
            
VMware Workstation 17

Lancer VMware au demarrage, cliquez sur "create a new virtuel machine"

![image](https://github.com/user-attachments/assets/8e06bc4d-65a4-4798-bfe8-9edea37e17b2)

Puis, laisser cocher "typical"

![image](https://github.com/user-attachments/assets/822b65be-aca9-4156-8b5a-638ac196b568)

Cherchez dans votre ordinateur l'iso de debian 11

![image](https://github.com/user-attachments/assets/74f9f7e5-5893-4883-88d0-73841dda1cf1)

ecrivez le nom et choisissez la localisation de la VM sur votre PC

![image](https://github.com/user-attachments/assets/4f607d67-f555-4e0d-9716-8b4e3b09201c)

Choisissez le nombre de Go qu'aura votre VM 

![image](https://github.com/user-attachments/assets/74fbb8e7-9052-4139-98c0-840eb62b568f)

vous avez la liste de ce que contient votre VM et cliquez sur "Custom Hardawe"

![image](https://github.com/user-attachments/assets/a797ccbf-157c-4e63-a2b1-4795a1de3524)

Sur l'Hardawe cliquez sur "add" en bas à guauche, puis ajouter une deuxieme carte réseau en cliquant sur "Network adaptateur"

![image](https://github.com/user-attachments/assets/e7fba58e-76f4-4f8d-aac2-25bfe4273e82)

sur la 2e carte réseau, on va le mettre a un LAN, cocher "LAN segmnet" puis ajouter un nouveau lan sur le bouton "LAN Segment"

![image](https://github.com/user-attachments/assets/d616d3aa-a3d7-4e3e-b370-4ade5a4b7d1c)

1.2 - Installer Debian 11

maintenant que c'est fait, on peut maintenant demarrer la machine pour installer debian cliquer sur le bouton démarrer

![image](https://github.com/user-attachments/assets/40f8e8eb-0b80-40d7-a3db-c431fc58bbb3)

cliquez sur "install" pour pouvoir installer debian sans interface graphique

![image](https://github.com/user-attachments/assets/b0aa7444-9a2f-4744-962d-3fac4977930c)

configuré jusqu'a avoir la configuration réseau car comme on a 2 carte réseau, il va nous demander de choisir l'interface principale pour l'installation, choisissez la carte WAN

![image](https://github.com/user-attachments/assets/287349c3-ff39-46f3-9d7d-b7c581665f2b)

Continuer les configurations comme le nom d'utilisateur, mot de passe, disque, ect

Dans "Configurer l'outil de gestion des paquets" choisissez par default deb.debian.org

![image](https://github.com/user-attachments/assets/04eb9442-e974-4cf7-b013-0e1e0258a1c8)

décocher "environnement de bureau debian" et "GNOME"

![image](https://github.com/user-attachments/assets/c37d6844-fe61-4d64-97b7-1fe8fa4e72b2)

et enfin il faut mettre oui pour mettre grub au démarrage

2 - Configuration réseau

pour passer en mode administrateur au demarrage, le nom d'utilisateur vous mettez root et le mdp inscrit lors de l'installation ou on tape la commande

            su -

Pour configurer l'adresse ip et la passerelle par default, il faut tapper

            nano /etc/network/interfaces

à l'interrieur, on configure la 2e carte réseau en ajoutant à la fin du fichier

            allow-hitplug ens34
            iface ens34 inet static
                        address 10.100.255.1/24

enregistrer, puis reboot apres avoir fait la commande suivante pour verifier les interfaces réseaux

            ip a 

3 - Mise en place du serveur DHCP

tout d'abord, il faut installer le dhcp en tapant

            apt install isc-dhcp-server -y

Ensuite, nous devons préciser sur quelle interface du serveur, le “démon” (le “service”) va écouter et donc attendre les requêtes des clients, nous on va utiliser ens34 puisque que c'est l'interface LAN. Modifiez le fichier nécessaire avec la commande suivante

            nano /etc/default/isc-dhcp-server

![image](https://github.com/user-attachments/assets/980b5293-30bb-41b6-9740-83f3e2774883)

Ensuite, il faut éditer le fichier dhcpd.conf pour configurer le service DHCP

            nano /etc/dhcp/dhcpd.conf

décommenter la ligne "authoritative"

![image](https://github.com/user-attachments/assets/f5e4db6e-afb9-4e5e-91ab-1c6885cded91)

            # Etendue LAN
            subnet 10.100.255.0 netmask 255.255.255.0 {
            #option routers ;
            range 10.100.255.10 10.100.255.10;
            }

redémarrer et verifier si le service dhcp fonctionne bien

            service isc-dhcp-server restart
            sudo systemctl status isc-dhcp-server

4- mise en place du serveur DNS
4.1 - installation et configuration du DNS

tout d'abort, il faut configurer certains fichiers avant d'installer le DNS, pour commencer tappez les commandes suivantes

            nano /etc/hosts
écrivez la ligne suivante

![image](https://github.com/user-attachments/assets/9b077695-6c54-40ce-b8f8-8387a0fd0a73)

            nano /etc/hostname

mettez le nom de la machine "holodesk"

            nano /etc/resolv.conf

![image](https://github.com/user-attachments/assets/de7b2473-eca2-4ac2-b8ab-fca09eb29e7b)

apres avoir configurer les fichier précedent il faut installer le packet Bind9 pour le DNS

            apt-get install bind9 -y

une fois installé configurer le fichier suivant

            nano /etc/bind/named.conf.local

![image](https://github.com/user-attachments/assets/01aee809-67aa-4cc7-bd07-c70cb1bc0679)

ensuite, crée le fichier de définition de notre zone DNS. Nous allons nous baser sur la conf par défaut db.localhost qui contient la configuration minimale pour une zone dns

            cp db.local db.starfleet.lan && sed -i -e 's/localhost/starfleet.lan/g' -e 's/127.0.0.1/10.100.255.1/g' starfleet.lan

ensuite vérifier le fichier

            nano /etc/bind/db.starfleet.lan

![image](https://github.com/user-attachments/assets/05d02b2a-ad5c-40cd-89bd-7064c8a1643e)

pour tester on tape la commande 

            nslookup atomit.local

il devrait afficher ceci

![image](https://github.com/user-attachments/assets/4f830bf7-0e69-435f-94c1-66800cc885eb)

4.2 - probleme resolv.conf

après avoir modifié le fichier resolv .conf le fichier écrase et réécrit a chaque démarrage a cause du dhcp du WAN. pour éviter ce probleme, on va désactiver le DHCP et mettre le réseau WAN en static. pour le faire, il faut aller dans VMware edit et "Virtual network éditor"

![image](https://github.com/user-attachments/assets/d75f132d-7060-4810-9d51-739f7b914de3)

une fois dans la page vitual network soyez en mode administrateur pour modifier le network

![image](https://github.com/user-attachments/assets/85458c73-a17d-475c-b5cd-2dc93b3df382)

cliquez sur le NAT

![image](https://github.com/user-attachments/assets/aee65707-1995-4267-842b-584b6b9f20e6)

et désactiver le DHCP

![image](https://github.com/user-attachments/assets/d37bfaf2-8708-4c79-8b9f-5234c1449348)

puis dans Debian 11 retourné dans vos interface en écrivant 

            nano /etc/network/interfaces

puis mettre un # sur la ligne qui contient du DHCP sur l'interface ens33 pouis on va le mettre en static

            allow-hitplug ens33
            #iface ens33 inet dhcp
            iface ens33 inet static
                        address 192.168.75.25/24
                        gateway 192.168.75.2

redémaré et modifié le fichier resolv.conf en rajoutant le serveur dns local

            nano /etc/resolv.conf
            
![image](https://github.com/user-attachments/assets/41a21662-aa3f-47ae-9225-248dadda6ae0)


enfin testé d'abord avec le réseau internet en mettant a jour debian avec apt-get update et après un nslookup pour le dns local et pour etre sur redémarré pour voir si le fichier resolv.conf change

4.3 modification du serveur DHCP local

Nous allons rajouté l'ip du serveur DNS afin que les client puisse ce connecté au serveur DNS local

allez dans le fichier

            nano /etc/dhcp/dhcpd.conf

on rajoute la ligne qui permet de donner au client l'ip

            option domain-name-servers 10.100.255.1;

![image](https://github.com/user-attachments/assets/d6c627e6-5fc6-4856-9d5b-d6283ee730de)

5 - Mise en place de Mariadb

installer mariadb

            sudo apt-get install mariadb-server -y

Démarrez le service MariaDB

            systemctl start mariadb

Activez le service MariaDB pour démarrer au redémarrage du système

            systemctl enable mariadb

MariaDB fournit un script de sécurité pour sécuriser la base de données. Exécutez-le et répondez à toutes les questions de sécurité comme indiqué

            mysql_secure_installation

Au départ, il n'y a pas de mot de passe pour root. Appuyez sur Enter

Appuyez Y pour passer à l’authentification

Appuyez Y pour modifier le mot de passe root

puis appuyer sur Y jusqu'a la fin 

Connectez-vous au shell MariaDB et entrez votre mot de passe root MariaDB

            mysql -u root -p

Vérifiez la version de MariaDB pour vérifier l'installation

Cela devrait renvoyer quelque chose comme ceci :

            MariaDB [(none)]> SELECT @@version

             +---------------------------+
             | @@version                 |
             +---------------------------+
             | 10.5.12-MariaDB-0+deb11u1 |
             +---------------------------+
             1 row in set (0.000 sec)

Quitter le shell MariaDB

            MariaDB [(none)]> exit

6 - mettre en place le service web avec Nginx

installez Nginx

            sudo apt install nginx

avant de configuré Nginx on va allez dans le DNS pour ajouté les nom des 2 site qu'on va ajouté, allez dans le fichier de configuration

            nano /etc/bind/db.starfleet.lan

rajouté les deux site (nom des sites www7 et www8)

![image](https://github.com/user-attachments/assets/18c8ef15-e867-4a6f-9b01-9cbe1bb8cea1)

on peut testé avec les nom des site sur un navigateur web

Maintenant nous  pouvons commencer la configuration qui se fera en quatre étapes. D’abord la création des répertoires qui va contenir les pages de nos sites ensuite la création des pages et la configuration des block  server pour chaque site au niveau de nginx et enfin faire les tests

            mdkir -p /var/www/starfleet.lan/www7
            mdkir -p /var/www/starfleet.lan/www8

nous allons copier le fichier de configuration par défault dans un fichier que nous allons créer pour chacun des site 

            cp /etc/nginx/sites-available/default /etc/nginx/sites-available/www7
            cp /etc/nginx/sites-available/default /etc/nginx/sites-available/www8

ensuite on modifie le fichier qu'on vient de copier

            nano /etc/nginx/site-available/www7
            
tout d'abord il faut retirer le "default_server" (et commenté l'ip v6 si vous ne l'utilisé pas) du port 80

![image](https://github.com/user-attachments/assets/f24c719d-5863-461f-b504-dba397698ccd)

puis en bas sur root mettez le chemin qu'on a créer au debut pour contenir le site

![image](https://github.com/user-attachments/assets/219a6988-d5a8-4169-b546-57b7a7d3f310)

enfin dans le "server_name" mettez le nom de domaine du premier site

![image](https://github.com/user-attachments/assets/235adb88-0a49-4b89-aefe-0f492d7434fd)

vous avez fini de configurer le premier (www7) site il faut le faire pour le second (www8)

ensuite on va faire un lien des configuation qui va de /etc/nginx/site-available à /etc/nginx/site-enable pour les 2 fichier de configuration d'abord il faut ce placer dans le fichier site-enable

            cd /etc/nginx/sites-enable

après créer les lien

            ln -s /etc/nginx/sites-available/www7 www7
            ln -s /etc/nginx/sites-available/www8 www8
            
on va supprimé les fichier par défaut de site-enable et site-available sinon il va y avoir une erreur

            rm /etc/nginx/sites-available/default
            rm /etc/nginx/sites-enable/default

enfin pour vérifier si il n'y pas d'érreur tappez la commande 

            nginx -t

si tout est bon reload nginx

            systemctl reload nginx

tester maintenant dans un navigateur web si les 2 site fonctionne

7. Mise en place du service SFTP

Installez le paquet openssh-server

            apt install openssh-server

L'utilisateur Nginx sous Debian 11 étant par défaut www-data , vous avez attribué celui-ci et son groupe associé aux dossiers et fichiers de starfleet lors de l'installation du CMS.

Les scripts PHP de Dotclear ont ainsi hérité des droits d'accès en écriture leur permettant de mettre à jour localement le contenu de /var/www/starfleet.lan/.

Rappel des permissions utilisées par starfleet :
- Dossiers = 755
soit propriétaire u drwx, groupe g r-x, autres o r-x

- Fichiers = 644
soit propriétaire u rw-, groupe g r--, autres o r--

Les écritures effectuées depuis un client SFTP ne doivent pas modifier cette configuration au risque de voir starfleet ne plus pouvoir se mettre à jour.

Une technique pour éviter cela consiste à créer un dossier miroir du dossier Web de starfleet

Création du dossier miroir

            cd /home
            mkdir -p admin/sites-web/starfleet

Créez ensuite son groupe sftp-groupe

            addgroup sftp-groupe 

et son utilisateur admin que vous lierez à sftp-groupe

            useradd -d /home/admin/sites-web/starfleet -g sftp-groupe admin

Enfin, appliquez ces permissions sur le dossier miroir

            chown admin:sftp-groupe /home/admin/sites-web/starfleet
            chmod 755 /home/admin/sites-web/starfleet

et terminez en créant un MDP pour l'utilisateur admin

            passwd admin

 Utilisation de bindfs pour remplir le miroir

             apt install bindfs

Pour remplir automatiquement le miroir, éditez fstab

            nano /etc/fstab

et ajoutez les 2 lignes suivantes à la fin du fichier

            # Montage automatique du dossier miroir de Dotclear 

            bindfs#/var/www/starfleet.lan /home/admin/sites-web/starfleet fuse force-user=admin,force-group=sftp-groupe,create-for-user=www-data,create-for-group=www-data,create-with-perms=ud=rwx:god=rx:uf=rw:gof=r,chgrp-ignore,chown-ignore,chmod-ignore 0 0

Redémarrez afin de traiter la Cde bindfs du fichier fstab

            reboot   

et vérifiez ensuite le contenu du dossier miroir

            ls -l /home/admin/sites-web/starfleet 
            ls -l /var/www/starfleet.lan

Editez le fichier de configuration du démon SSH

            nano /etc/ssh/sshd_config

Commentez les 2 lignes suivantes

            X11Forwarding yes
            Subsystem          sftp          /usr/lib/openssh/sftp-server

et ajoutez en fin de fichier ce groupe de lignes

            # Configuration sshd de l'hôte srvdmz
            Subsystem     sftp     internal-sftp
            Port 384                                                                   
            PermitRootLogin no                                         
            Match User admin
            ChrootDirectory  /home/admin/sites-web
            X11Forwarding no
            AllowTcpForwarding no
            ForceCommand internal-sftp -u 022

Vérifiez afin que le ChrootDirectory (limite dossier racine) fonctionne que le propriétaire des dossiers admin et sites-web soit bien l'utilisateur root

            ls -l /home
            ls -l /home/admin

Redémarrez le serveur SSH

            systemctl restart ssh
            systemctl status ssh 

Testez ensuite une connexion locale 

            sftp -o Port=384 admin@starfleet.lan
8 - SSL

Pour sécuriser notre serveur en activant le protocole HTTPS et installer un certificat, nous
allons tout d'abord, installez OpenSSL en utilisant la commande suivante

            apt install openssl

Ensuite, générez un certificat auto-signé avec la commande suivante

            sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/starfleet.lan.key -out                         /etc/ssl/certs/starfleet.lan.crt

ajouter le SSL dans le fichiers situer dans etc/nginx/site-available et écouté les port 443 au lieu de 80

![image](https://github.com/user-attachments/assets/cbebd356-bf73-4543-9fc9-bc3731186af2)


9 - Installer PHP7.4 et 8.3 et les faire cohabiter

Tout d'abord, les paquets de services requis sont installés

            apt install lsb-release apt-transport-https ca-certificates wget gnupg -y

Ajoutez le référentiel Sury pour la dernière version PHP sur le système

            wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
            echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list

Mettez à jour les listes de packages comme suit

            apt update

Installez maintenant PHP 8.3/7.4 et PHP-FPM avec les modules PHP les plus importants

            apt install php8.3 php8.3-fpm php8.3-{cli,mysql,imap,intl,apcu,cgi,bz2,zip,mbstring,gd,curl,xml,common,opcache,imagick} -y

            apt install php7.4 php7.4-fpm php7.4-{cli,mysql,imap,intl,apcu,cgi,bz2,zip,mbstring,gd,curl,xml,common,opcache,imagick} -y

Mettez à jour les packages comme suit

            apt update && apt upgrade -y

Pour éviter les conflit entre les 2 version de php on va modifier le fichier de php 8.3 dans 

      nano /etc/php/8.3/fpm/pool.d/www.conf

dans le fichier on modifie la ligne listen pour qu'il ecoute php8.3 avec l'adresse ip et le port du serveur Holodesk (il va écouter dans le port 2000)

            listen = 10.100.255.1:2000
            
quittez et enregistrez puis démarrez les 2 php

            systemctl start php8.2-fpm
            systemctl start php7.4-fpm

10 - site utilisant 2 version de php différant

tout d'abord allez dans le l'index.html de www7

            cd /var/www/starfleet.lan/www7/
            nano index.html

Supprimer tout pour remplacer par

            <?php
            phpinfo(); 
            ?>
ensuite renommez le fichier index.html par index.php

            mv index.html index.php

faite la meme opération pour www8

ensuite allez dans le fichier site-available de www7

            nano /etc/nginx/sites-available/www7

rajouter dans le fichier la localisation de php7.4 et ajouter index.php dans index

![image](https://github.com/user-attachments/assets/a498510f-1436-456d-b443-ecbc05bc1b7b)

faite parreille pour www8 en mettant dans fastcgi_pass l'addresse ip et le port qu'on a mit dans le fichier www.conf de php8.3

![image](https://github.com/user-attachments/assets/68e64b7e-1183-40c0-b271-4f89c3480b26)

verifier si il y a des erreur avec la commande 

            nginx -t

puis redemarrer nginx

            systemctl restart nginx

tester sur un navigateur web si www7 nous montre php7.4 et si www8 nous montre php8.3

11 - Mise en place OPENLDAP et LAM (LDAP Account Manager)

Exécutez la commande suivante pour installer le serveur OpenLDAP et les utilitaires de ligne de commande client à partir du référentiel de packages Debian 11

            apt install slapd ldap-utils

Il vous sera demandé de définir un mot de passe pour l'entrée administrateur dans l'annuaire LDAP.

![image](https://github.com/user-attachments/assets/d5054e95-d8af-4764-bd1b-ead6b928f701)

Le processus d'installation installe le package sans aucune configuration. Pour que notre serveur OpenLDAP fonctionne correctement, nous devons effectuer une configuration post-installation de base. Exécutez la commande suivante pour démarrer l'assistant de configuration

            dpkg-reconfigure slapd

Omettre la configuration du serveur LDAP : NON

![image](https://github.com/user-attachments/assets/a2cd0a28-c242-4b50-8128-3da63d701a17)

Nom de domaine DNS : saisissez votre nom de domaine

![image](https://github.com/user-attachments/assets/577dcb67-36b3-4e95-b54b-1f9e5026b02d)

Nom de l'organisation : saisissez le nom de votre organisation comme LinuxBabe

![image](https://github.com/user-attachments/assets/400befb0-e8eb-49bd-a642-602e929d5334)

Mot de passe administrateur : Entrez le même mot de passe défini lors de l'installation

![image](https://github.com/user-attachments/assets/2cb1073a-5e18-4cce-83e5-6591abdcfa68)

Voulez-vous que la base de données soit supprimée lorsque slapd est purgé ? Non

![image](https://github.com/user-attachments/assets/2b87f0ec-976c-443e-8bf9-7e337f90c04c)

Déplacer l'ancienne base de données ? Oui

![image](https://github.com/user-attachments/assets/36c41ad0-7a7d-4e87-a354-8afaabd98113)

/etc/ldap/ldap.confest le fichier de configuration de tous les clients OpenLDAP. Ouvrez ce fichier

            nano /etc/ldap/ldap.conf

Nous devons spécifier deux paramètres : le DN de base et l' URI de notre serveur OpenLDAP. Copiez et collez le texte suivant à la fin du fichier. Remplacez your-domainet comselon le cas

            BASE dc=starfleet,dc= lan
            URI ldap://localhost

Enregistrez et fermez le fichier puis Maintenant que le serveur OpenLDAP est en cours d'exécution et que la configuration du client est terminée, exécutez la commande suivante pour établir des connexions de test au serveur

            ldapsearch-x
            
Résultat : 0. Le succès indique que le serveur OpenLDAP fonctionne. Si vous obtenez la ligne suivante, cela signifie qu'il ne fonctionne pas


résultat : 32 Aucun objet de ce type

LDAP Account Manager est un programme Web de gestion de serveur OpenLDAP. Les utilitaires de ligne de commande peuvent être utilisés pour gérer notre serveur OpenLDAP, mais pour ceux qui souhaitent une interface facile à utiliser, vous pouvez installer LDAP Account Manager

            apt install ldap-account-manager

créez un hôte virtuel pour le gestionnaire de comptes LDAP

            nano /etc/nginx/sites-available/openldap.conf

voicie ce qui se trouve dans le fichier

![image](https://github.com/user-attachments/assets/3246f9c8-4f34-4147-87ee-784577040e05)

puis on fait un lien vers le sites-enable

            cd /etc/nginx/sites-enable/
            ln -s /etc/nginx/sites-available/openldap.conf

ensuite on ajoute le nom de domaine openldap.starfleet.lan allez dans le fichier

            nano /etc/bind/db.starfleet.lan

ajouter la ligne 

            openldap IN A 10.100.255.1

Enregistrez et fermez le fichier. Ensuite, envoyez les configurations Nginx

            sudo nginx -t

puis redemarrer nginx et bind

            systemctl restart nginx bind

ensuite par default ldap a comme utilisateur "Manager" et comme mot de passe inconnu donc pour modifier l'utilisateur et le mot de passe il faut allez dans le fichier

            nano /usr/share/ldap-account-manager/config/lam.conf

changer les ligne

            Admins: cn=admin,dc=starfleet,dc=lan
            Passwd: "mot de passe"
            types: suffix_user: ou=People,dc=starfleet,dc=lan
            types: suffix_group: ou=People,dc=starfleet,dc=lan

enregistrer et quittez puis verrifier sur un navigateur web si sa fonctionne et vous connectez

12 - Mise en place de PhpMyAdmin

phpMyAdmin n'est pas inclus dans le dépôt de logiciels Debian 11, vous devrez donc télécharger manuellement le logiciel. Accédez à la page de téléchargement de phpMyAdmin pour vérifier la dernière version stable. Exécutez ensuite la commande suivante pour le télécharger

            wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.tar.gz

Extraire le fichier téléchargé

            tar xvf phpMyAdmin-5.2.1-all-languages.tar.gz

Déplacer le phpMyAdmin-5.2.1-all-languagesvers /usr/share/le répertoire

            mv phpMyAdmin-5.2.1-all-languages /usr/share/phpmyadmin

Créez un sous-répertoire avec la commande suivante

            mkdir -p /var/lib/phpmyadmin/tmp

Faites de l'utilisateur du serveur Web www-datale propriétaire de ce répertoire

            chown -R www-data:www-data /var/lib/phpmyadmin

Faire une copie dans le fichier/usr/share/phpmyadmin/config.inc.php

            cp /usr/share/phpmyadmin/config.sample.inc.php /usr/share/phpMyAdmin/config.inc.php

Installez et utilisez le programme pwgen pour générer une chaîne aléatoire,

            apt install pwgen

Générer un mot de passe aléatoire

            pwgen -s 32 1

Modifiez le /usr/share/phpmyadmin/config.inc.php

            nano /usr/share/phpmyadmin/config.inc.php

Saisissez une chaîne de 32 caractères aléatoires entre guillemets simples

![image](https://github.com/user-attachments/assets/4381a0b6-6f9f-476d-988b-618367da9daf)

Ensuite, supprimez le commentaire de cette section du /usr/share/phpmyadmin/config.inc.phpfichier et elle ressemblera à ceci

![image](https://github.com/user-attachments/assets/d617239d-b40c-466a-a2ee-d87c052719f7)

Ajoutez la ligne suivante au bas du fichier

            $cfg['TempDir'] = '/var/lib/phpmyadmin/tmp';

Enfin, enregistrez et quittez le fichier

Créez la base de données et les tables de stockage de configuration en exécutant la commande suivante

            mariadb < /usr/share/phpmyadmin/sql/create_tables.sql

Ouvrez l'invite MariaDB

            mariadb

Créez l'utilisateur pma et accordez-lui les autorisations appropriées et remplacez les textes par votre mot de passe préféré

            GRANT SELECT, INSERT, UPDATE, DELETE ON phpmyadmin.* TO 'pma'@'localhost' IDENTIFIED BY 'password';
            GRANT ALL PRIVILEGES ON phpmyadmin.* TO 'pma'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;
            GRANT ALL PRIVILEGES ON *.* TO 'pma'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;
            flush privileges;
            exit;

créez un hôte virtuel pour le gestionnaire de comptes LDAP

            nano /etc/nginx/sites-available/phpmyadmin.conf

voicie ce qui se trouve dans le fichier

![image](https://github.com/user-attachments/assets/a53b6248-ab13-4075-bbc2-7c082a61ef02)

puis on fait un lien vers le sites-enable

            cd /etc/nginx/sites-enable/
            ln -s /etc/nginx/sites-available/phpmyadmin.conf

ensuite on ajoute le nom de domaine openldap.starfleet.lan allez dans le fichier

            nano /etc/bind/db.starfleet.lan

ajouter la ligne 

            php IN A 10.100.255.1

Enregistrez et fermez le fichier. Ensuite, envoyez les configurations Nginx

            sudo nginx -t

puis redemarrer nginx et bind

            systemctl restart nginx bind9

verrifier sur un navigateur web si sa fonctionne et vous connectez

13 - Mise en place de Zabbix

Installer le référentiel Zabbix

            wget https://repo.zabbix.com/zabbix/6.4/debian/pool/main/z/zabbix-release/zabbix-release_6.4-1+debian11_all.deb
            dpkg -i zabbix-release_6.4-1+debian11_all.deb
            apt update
Installer le serveur, le frontend et l'agent Zabbix

            apt install zabbix-server-mysql zabbix-frontend-php zabbix-nginx-conf zabbix-sql-scripts zabbix-agent

Créer la base de données initiale

            mysql -uroot -p
            create database zabbix character set utf8mb4 collate utf8mb4_bin;
            create user zabbix@localhost identified by 'password';
            grant all privileges on zabbix.* to zabbix@localhost;
            set global log_bin_trust_function_creators = 1;
            quit;

Sur l'hôte du serveur Zabbix, importez le schéma et les données initiaux. Vous serez invité à saisir votre mot de passe nouvellement créé

            zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix

Désactivez l'option log_bin_trust_function_creators après l'importation du schéma de base de données

            mysql -uroot -p
            set global log_bin_trust_function_creators = 0;
            quit;

Modifier le fichier /etc/zabbix/zabbix_server.conf

            DBPassword=password

Modifiez le fichier /etc/zabbix/nginx.conf, supprimez les commentaires et définissez les directives « listen » et « server_name ».

            listen 443;
            server_name admin.starfleet.lan;

Modifier aussi le chemin php

            fastcgi_pass 10.100.255.1:2000

et ajouter le SSL

![image](https://github.com/user-attachments/assets/75fd0739-7d85-43a9-988b-f1937940961a)
 
ensuite il faut suprimer dans le fpm de php8.3 zabbix.conf car il peut y avoir des conflit php

            rm /etc/php/8.3/fpm/pool.d/zabbix.conf

ensuite on ajoute le nom de domaine openldap.starfleet.lan allez dans le fichier

            nano /etc/bind/db.starfleet.lan

ajouter la ligne 

            php IN A 10.100.255.1

Enregistrez et fermez le fichier puis démarrez les processus du serveur et de l'agent Zabbix et faites-les démarrer au démarrage du système

            systemctl restart zabbix-server zabbix-agent nginx php8.3-fpm bind9
            systemctl enable zabbix-server zabbix-agent nginx php8.3-fpm bind9

Ouvrir la page Web de l'interface utilisateur de Zabbix puis connectez vous

Maintenant on va istaller l'agent zabbix pour le client donc pour le client on tape 

            apt-get install wget
            wget https://repo.zabbix.com/zabbix/6.4/debian/pool/main/z/zabbix-release/zabbix-release_6.4-1+debian11_all.deb
            dpkg -i zabbix-release_6.4-1+debian11_all.deb
            apt update

Installer l'agent Zabbix

            apt install zabbix-agent

Démarrez le processus de l'agent Zabbix et faites-le démarrer au démarrage du système

            systemctl restart zabbix-agent
            systemctl enable zabbix-agent

modifier le fichier client de l'agent zabbix

            nano /etc/zabbix/zabbix_agentd.conf

modifier les ligne suivant

            Server=10.100.255.1
            ServerActive=10.100.255.1
            Hostname=vm-client-1

enregistrer et quittez puis allez sur le site de zabbix server pour ajouter un hote connectez vous puis allez sur Surveillance / Hotes

![image](https://github.com/user-attachments/assets/7f2a7ccb-7715-443f-afb1-4f6b5f96c015)

Cliquez en haut a droite "Créer un hote"

créer le nouveau hote

![image](https://github.com/user-attachments/assets/698a7040-fcff-4a1c-ba5a-781da10777f6)

attendez jusqu'a que "ZBX" passe en vert 

![image](https://github.com/user-attachments/assets/9db9e89e-60b2-464a-aa1d-b5aba4d15662)

le client est maintenant reconnue par le serveur

14 - FTPS

installez vsftpd

            apt install vsftpd

modifiez le fichier de vsftpd

            nano /etc/vsftpd.conf

![image](https://github.com/user-attachments/assets/03158a83-74e7-46a2-a29b-252bada72745)

pour le ssl on ajoute aussi dans le meme fichier

![image](https://github.com/user-attachments/assets/6cd674d6-390d-4cc7-ae61-d4628c3808cc)

et pour le fichier chroot qui sera rediriger vers le site web on ajoute en fin du meme fichier

![image](https://github.com/user-attachments/assets/4eee4aff-e0f0-4041-a7b6-3f26332a2de6)

Ainsi on a déterminé que nous souhaitons que le propriétaire des fichiers uploadés  soit www-data.

On a également spécifié le chemin de configuration des utilisateurs FTP user_config_dir=/etc/vsftpd

Notez au passage, que pour des raisons de sécurité, il convient de modifier le port d’écoute par défaut du serveur FTP (21) par un autre (ici 21988).Cela évite, en effet, que le serveur se fasse bêtement scanner et/ou attaquer en force brute sur le port 21.

Autre point important dans cette configuration, nous utilisons le mode ‘passif‘. Le mode passif est recommandé dans le cas où un pare-feu (firewall) filtre votre réseau. L’avantage de ce mode est que votre serveur FTP n’initialise aucune connexion FTP.

Il convient de créer le dossier /etc/vsftpd comme précédemment spécifié

            mkdir /etc/vsftpd

Via la commande adduser, il faut créer en amont, l’utilisateur UNIX ‘client‘ (et donc l’utilisateur FTP)

            adduser client

Enfin, il reste a spécifier dans le fichier de l’utilisateur le chemin ou se trouve votre CMS (exemple : /var/www/starfleet.lan) :

            nano /etc/vsftpd/client
            local_root=/var/www/starfleet.lan

Pour terminer, il faut redémarrer le serveur Vsftpd afin que la nouvelle configuration soit prise en compte

            service vsftpd restart

sur le client lancer filezila, allez sur fichier puis gestionnaire de site et configurer le nouveau site

![image](https://github.com/user-attachments/assets/4b17aabb-7556-4153-9a6a-e01994e41a59)

ecrivez votre mot de passe et normalement filezila vous montre le certificat ssl du server puis vous aurez access au fichier web

![image](https://github.com/user-attachments/assets/8d94a477-7b57-4224-bb35-edb7faf488ac)

![image](https://github.com/user-attachments/assets/e271245e-2cff-42fa-9587-7a01e6948b13)

15 - FireWall avec UFW

L'installation de ufw

            apt-get install ufw

Avant de commencer, ufw ne se démarre pas par défaut pour ne pas vous enfermer dehors. Avant de l'activer on va commencer par gérer les politiques d'accès par défaut.

            ufw default deny incoming
            ufw default allow outgoing

maintenant on va ajouté les regles avant d'activer le FireWall

Notre serveur contient du https, DNS, DHCP, SSH (sftp)

            ufw allow https
            ufw allow bootps comment 'Allow 67/UDP'
            ufw allow bootps comment 'Allow 68/UDP'
            ufw allow bootps comment 'Allow DNS_53/UDP'
            ufw allow bootps comment 'Allow DNS_53/TCP'
            ufw allow dns
            ufw allow ssh
            ufw allow 384/tcp
            
serveur ftps

            ufw allow 40000:50000/tcp
            ufw allow 20/tcp
            ufw allow 21/tcp
            ufw allow 21988/tcp
            ufw allow 990/tcp

Serveur Zabbix serveur et agent
            
            ufw allow 10051/tcp
            ufw allow 10051/udp
            ufw allow 10050/tcp
            ufw allow 10050/tcp

pour activez le FireWall tappez

            ufw enable

pour verifiez tappez

            ufw status
