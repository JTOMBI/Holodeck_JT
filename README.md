# Holodeck

1 - Installation de Debian 11 sur VMware Workstation 17

1.1 - Installation de l'image iso

Prérequis : Iso Debian 11 (https://www.debian.org/distrib/netinst)
            
VMware Workstation 17

Lancer VMware au demarrage cliquez "create a new virtuel machine"

![image](https://github.com/user-attachments/assets/8e06bc4d-65a4-4798-bfe8-9edea37e17b2)

Puis, laisser cocher "typical"

![image](https://github.com/user-attachments/assets/822b65be-aca9-4156-8b5a-638ac196b568)

Chercher dans votre ordinateur l'iso de debian 11

![image](https://github.com/user-attachments/assets/74f9f7e5-5893-4883-88d0-73841dda1cf1)

ecrivez le nom et choisissez la localisation de la VM sur votre PC

![image](https://github.com/user-attachments/assets/4f607d67-f555-4e0d-9716-8b4e3b09201c)

Choisissez le nombre de Go qu'aura votre VM 

![image](https://github.com/user-attachments/assets/74fbb8e7-9052-4139-98c0-840eb62b568f)

vous avez la liste de ce que contient votre VM et cliquez sur "Custom Hardawe"

![image](https://github.com/user-attachments/assets/a797ccbf-157c-4e63-a2b1-4795a1de3524)

Sur l'Hardawe cliquez sur "add" en bas a guauche puis ajouter un dexieme carte réseau en cliquant sur "Network adaptateur"

![image](https://github.com/user-attachments/assets/e7fba58e-76f4-4f8d-aac2-25bfe4273e82)

sur le 2e carte réseau on va le mettre a un LAN, cocher "LAN segmnet" puis ajouter un nouveau lan sur le bouton "LAN Segment"

![image](https://github.com/user-attachments/assets/d616d3aa-a3d7-4e3e-b370-4ade5a4b7d1c)

1.2 - Installer Debian 11

maintenant que c'est on peut maintenant demarrée la machine pour installé debian cliquer sur le bouton démarré

![image](https://github.com/user-attachments/assets/40f8e8eb-0b80-40d7-a3db-c431fc58bbb3)

cliquez sur install pour pouvoir installer debian sans interface graphique

![image](https://github.com/user-attachments/assets/b0aa7444-9a2f-4744-962d-3fac4977930c)

configuré jusqu'a avoir la configuration réseau car comme on a 2 carte réseau il va nous demander de choisir l'interface principal pour l'installation, choisissez la carte WAN

![image](https://github.com/user-attachments/assets/287349c3-ff39-46f3-9d7d-b7c581665f2b)

Continuer les configuration comme le nom d'utilisateur, mot de passe, disque, ect

Dans "Configurer l'outil de gestion des paquets" choisissez par default deb.debian.org

![image](https://github.com/user-attachments/assets/04eb9442-e974-4cf7-b013-0e1e0258a1c8)

décocher "environnement de bureau debian" et "GNOME"

![image](https://github.com/user-attachments/assets/c37d6844-fe61-4d64-97b7-1fe8fa4e72b2)

et enfin il faut mettre oui pour mettre grub au démarrage

2 - Configuration réseau

pour passer en mode administrateur au demarrage le nom d'utlisateur vous mettez root et le mdp inscirt lors de l'installation ou on tape la commande

            su -

Pour configurer l'addresse ip et la passerelle par default il faut tappez

            nano /etc/network/interfaces

a l'interrieur on configure le 2e carte réseau en ajoutant a la fin du fichier

            allow-hitplug ens34
            iface ens34 inet static
                        address 10.100.255.1/24

enregistrer puis reboot apres faite la commmande suivante pour verifier les interface réseaux

            ip a 

3 - Mise en place du serveur DHCP

tout d'abord il faut installer le dhcp en tappant

            apt install isc-dhcp-server -y

Ensuite, nous devons préciser sur quel interface du serveur, le “démon” (le “service”) va écouter et donc attendre les requêtes des clients, nous on va utiliser ens34 puisse que c'est l'interface LAN. Modifiez le fichier nécessaire avec la commande suivante

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

tout d'abort il faut configurer certain fichier avant d'installer le DNS, pour commencer tappez les commandes suivantes

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

ensuite créé le fichier de définition de notre zone DNS. Nous allons nous baser sur la conf par défaut db.localhost qui contient la configuration minimal pour une zone dns

            cp db.local db.starfleet.lan && sed -i -e 's/localhost/starfleet.lan/g' -e 's/127.0.0.1/10.100.255.1/g' starfleet.lan

ensuite vérifier le fichier

            nano /etc/bind/db.starfleet.lan

![image](https://github.com/user-attachments/assets/05d02b2a-ad5c-40cd-89bd-7064c8a1643e)

pour tester on tape la commande 

            nslookup atomit.local

il devrait afficher ceci

![image](https://github.com/user-attachments/assets/4f830bf7-0e69-435f-94c1-66800cc885eb)

4.2 - probleme resolv.conf

après avoir modifier le fichier resolv .conf le fichier écrase et reécrit a chaque démarrage a cause du dhcp du WAN pour éviter ce probleme on va désactiver le DHCP et mettre le réseau WAN en static pour ce faire il faut aller dans VMware edit et "Virtual network éditor"

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


enfin testé dabort avec le réseau internet en mettant a jour debian avec apt-get update et après un nslookup pour le dns local et pour etre sur redémaré pour voir si le fichier resolv.conf change

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


9 - FTPS

![image](https://github.com/user-attachments/assets/8d94a477-7b57-4224-bb35-edb7faf488ac)

Installer PHP7.4 et 8.3 et les faire

9 - LDAP et LAM

![image](https://github.com/user-attachments/assets/b4bc6583-1417-46f0-bff7-5b89258fd40b)
