# -*- coding: utf-8 -*-

import getpass
import smtplib
import sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from lib.iptcinfo import IPTCInfo


def log():
  global user, smtp, port
  pwd = getpass.getpass('Entrez le mot de passe')
  mailserver = smtplib.SMTP(smtp, port)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.ehlo()
  mailserver.login(user, pwd)
  return (mailserver,True)

def unlog(mailserver):
  mailserver.quit()
  return (mailserver,False)


def lookandsend():
  global pics
#  pics=scanfolder() #On récupère le contenu du dossier courant
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
  global message, subject, sender #le message du mail
  # On cree le mail
  msg = MIMEMultipart()
  msg['From'] = sender #De qui ?
  msg['To'] = dest #Pour qui?
  msg['Subject'] = subject #Le sujet du mail
  msg.attach(MIMEText(message)) # On met le texte dans le mail

  #La partie photo
  pj = open(photo, 'rb') #On ouvre le fichier
  msg.attach(MIMEApplication(pj.read(),Content_Disposition='attachment; filename="%s"' % os.path.basename(photo),Name=os.path.basename(photo)))
  pj.close() #On le ferme
#  msg.attach(img) # On met la photo dans le mail


  #La partie où l'on envoie le mail
  mailserver.sendmail(sender, dest, msg.as_string())
  #mailserve.quit()

def scanfolder():
  global folder, pics
  pics=[]
  import os
  for root, dirs, files in os.walk(folder): #On parcours le dossier courant
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
def init():
  global message, subject, sender, smtp, port, login, folder, lg
  print('Initialisation...')
  message='Bonjour, \n desole pour le doublon, le script mail est encore en developpement et a mal joint les images (sauf pour thunderbird). \n Vous trouverez ci-joint votre photo individuelle prise sur notre stand. \n Ces photos sont larges pour pouvoir etre recadrees a votre guise. \n \n \n \nClub Photo Supelec \nPour des photos de CV propres et professionnelles, avec des mails plus qualis.'
  subject='Votre photo sur le stand'
  sender='photocv@larez.fr'
  smtp='smtp.rez-gif.supelec.fr'
  port ='587'
  login='hugo.hervieux'
  folder='./'
  lg=raw_input('Language ? en=English fr=French')


def main():
  global lg
  if lg=fr:
    print('\nMenu : \n')
    print('Que voulez-vous faire ?\n'
          '1.Choisir le dossier\n'
          '2.Choisir le message\n'
          '3.Choisir le serveur mail\n'
          '4.Choisir une identité \n'
          '5.Scanner les fichiers pour avoir les mails\n'
          '6.Verifier la validité des mails\n'
          '7.Editer un ou plusieurs mails\n'
          'go.Envoyer le mail')
  else:
    print('\nMenu :\n')
    print('What do you want to do ?\n'
          '1.Choose the folder\n'
          '2.Choose the message\n'
          '3.Choose the mail server\n'
          '4.Choose an identity\n'
          '5.Parse the files to get emails\n'
          '6.Check emails\n'
          '7.Edit an email address\n'
          'go.Send mails')
  choice=raw_input()
  if choice=='1':
    setfolder()
  elif choice=='2':
    setmessage()
  elif choice=='3':
    setsrv()
  elif choice=='4':
    setuser()
  elif choice=='5':
    checkmails()
  elif choice=='6':
    editmails()
  elif choice=='go':
    lookandsend()

def setfolder():
  global folder,lg
  if lg==fr:
    print("Dossier actuel :",folder)
    if raw_input('Changer ? (y/N')=='y'
      folder=raw_input('Nouveau chemin')
      print('Fait')
  else:
    print("Actual fodler :",folder)
    if raw_input('Change ? (y/N')=='y'
      folder=raw_input('New path')
      print('Done')

def setmessage():
  global message, subject, lg
  if lg==fr:
    print("Object actuel : ",subject,"\nMessage actuel : ",message)
    if raw_input('Changer ? (y/N')=='y'
      subject=raw_input('Nouvel objet')
      message=raw_input('Nouveau message')
      print('Fait')
  else:
    print("Actual subject", subject,"\nActual message :",message)
    if raw_input('Change ? (y/N')=='y'
      subject=raw_input('New subject')
      message=raw_input('New message')
      print('Done')

def setsrv():
  global smtp, port, lg
  if lg==fr:
    print("Serveur smtp actuel : ",smtp," port : ",port)
    if raw_input('Changer ? (y/N')=='y'
      smtp=raw_input('Nouveau serveur smtp')
      port=raw_input('Nouveau port')
      print('Fait')
  else:
    print("Actual smtp server :",smtp," port : ",port)
    if raw_input('Change ? (y/N')=='y'
      smtp=raw_input('New smtp server')
      port=raw_input('New port')
      print('Done')

def setuser():
  global login, sender ,lg
  if lg==fr:
    print("Login actuel :",login,'Expediteur actuel', sender)
    if raw_input('Changer ? (y/N')=='y'
      login=raw_input('Nouveau login mail')
      sender=raw_input('Nouvel expediteur')
      print('Fait')
  else:
    print("Actual login :",login, "Actual sender", sender)
    if raw_input('Change ? (y/N')=='y'
      login=raw_input('New login')
      sender=raw_input('New sender')
      print('Done')

def checkmails():
  print('not yet')



lookandsend()
