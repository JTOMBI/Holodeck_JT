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

            cp db.local db.atomit.local && sed -i -e 's/localhost/atomit.local/g' -e 's/127.0.0.1/192.168.56.100/g' db.atomit.local

ensuite vérifier le fichier

            nano /etc/bind/db.starfleet.lan

![image](https://github.com/user-attachments/assets/05d02b2a-ad5c-40cd-89bd-7064c8a1643e)

pour tester on tape la commande 

            nslookup atomit.local

il devrait afficher ceci

![image](https://github.com/user-attachments/assets/4f830bf7-0e69-435f-94c1-66800cc885eb)
