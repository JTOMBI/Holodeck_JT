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

