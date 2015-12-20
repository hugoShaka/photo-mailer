# -*- coding: utf-8 -*-

#Author : Shaka
#Date: 14-12-16
#
#
#

#################################################
#                  CONSIGNES
#################################################
#Toujours laisser le dossier entier
#Indiquer le mail dans le titre de la photo sur lightroom
#Tout exporter dans un dossier
#Entrer le chemin du dossier dans le champ os.walk() de la fonction scanfolder
#Lancer le script



import getpass
import smtplib
import sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from iptcinfo import IPTCInfo


def log():
  user= getpass.getuser('Entrez votre mail')
  pwd = getpass.gestpass('Entrez le mor de passe')
  mailserver = smtplib.SMTP('smtp.rez-gif.supelec.fr', 587)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.ehlo()
  mailserver.login(user, pwd)
  return (mailserver,True)

def unlog(mailserver):
  mailserver.quit()
  return (mailserver,False)


def lookandsend():
  pics=scanfolder() #On récupère le contenu du dossier courant
  (mailserver,logged)=log()
  if logged==False:
    print('Erreur : Non connecté au SMTP \n Arret du programme')
  else:
    for photo in pics: #Pour toutes les photos
      dest=getmail(photo) #On prend l'email du mec
      if dest=='None':
        print('no')
      else:
        sendemail(photo,dest,mailserver) #On lui envoie un mail
    unlog(mailserver) #On se déconnecte du serveur mail
    print('Fait')

def sendemail(photo, dest, mailserver):
  global message #le message du mail
  # On cree le mail
  msg = MIMEMultipart()
  msg['From'] = 'photoscv@larez.fr' #De qui ?
  msg['To'] = dest #Pour qui?
  msg['Subject'] = 'Photo individuelle prise sur notre stand' #Le sujet du mail
  msg.attach(MIMEText(message)) # On met le texte dans le mail

  #La partie photo
  pj = open(photo, 'rb') #On ouvre le fichier
  msg.attach(MIMEApplication(pj.read(),Content_Disposition='attachment; filename="%s"' % os.path.basename(photo),Name=os.path.basename(photo)))
  pj.close() #On le ferme
#  msg.attach(img) # On met la photo dans le mail


  #La partie où l'on envoie le mail
  mailserver.sendmail('photoscv@larez.fr', dest, msg.as_string())
  #mailserve.quit()

def scanfolder():
  pics=[]
  import os
  for root, dirs, files in os.walk("/media/removable/UUI/standcv"): #On parcours le dossier courant
    for file in files:
        if file.endswith(".jpg"): #Si on a une image
             print(os.path.join(root, file))
             pics.append(os.path.join(root, file)) #On prend son chemin
  return pics
  
def getmail(path_to_image):
  info=IPTCInfo(path_to_image)
  if str(info.data['object name'])=='':
    return None
  else:
    return str(info.data['object name'])



message='Bonjour, \n desole pour le doublon, le script mail est encore en developpement et a mal joint les images (sauf pour thunderbird). \n Vous trouverez ci-joint votre photo individuelle prise sur notre stand. \n Ces photos sont larges pour pouvoir etre recadrees a votre guise. \n \n \n \nClub Photo Supelec \nPour des photos de CV propres et professionnelles, avec des mails plus qualis.'

lookandsend()
