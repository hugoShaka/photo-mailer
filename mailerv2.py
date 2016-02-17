# -*- coding: utf-8 -*-

import getpass
import sys, os
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from lib.iptcinfo import IPTCInfo

class photo:
  """Une photo est une entit√"""
  def __init__(self,fileloc):
    self.location=fileloc
    info=IPTCInfo(path_to_image)
    mail=str(info.data['object name'])
    if mail=='':
      self.email=None
    else:
      self.email=mail
    self.sent=False
  def send(mailaccount):
    mail=mail(self.email,self.location,mailaccount)


class folder:
  """Repr√sente un dossier"""
  def __init__(self,pathtofolder):
    self.path=pathtofolder
    self.files=[]
  def scan():
    howmanyimport=0
    for root, dirs, files in os.walk(self.path):
      for file in files:
        if file.endswith(".jpg"):
          self.files.append(Photo(os.path.join(root, file)))
          howmanyimport+=1
    print(howmanyimport + "files were sucessfully imported")

class mailaccount:
  """Compte mail et parametres de connexion au serveur
"""

  def __init__(self):
    self.sender="Club Photo"
    self.port="587"
    self.smtp="smtp.rez-gif.supelec.fr"
    self.login="None"
    self.connected=False

  def credentials():
    self.login=input("Login")
    self.pwd=getpass.getpass("Mot de passe")

  def log():
    try:
      self.mailserver=smtplib.SMTP(self.smtp,self.port)
      self.mailserver.ehlo()
      self.mailserver.starttls()
      self.mailserver.ehlo()
      self.mailserver.login(self.login,self.pwd)
      self.connected=True
    except (socket.error) as err
      print("Socket error:.({0}): {1}".format(e.errno, e.strerror)
      self.connected=False

  def unlog()
    	self.mailserver.quit()
        self.connected=False

class mail:
  """Objet mail qui poss√®de les methodes pour etre envoye, recupere ses parametres d'un objet mailaccount"""
  def __init__(self,reciever,photo,mailaccount):
    self.msg=MIMEMultipart()
    self.msg['From'] = mailaccount.sender
    self.msg['To'] = reciever
    self.msg['Subject'] = mailaccount.subject
    self.msg.attach(MIMEText(message.create()))
    
    pj=open(photo, 'rb')
    self.msg.attach(MIMEApplication(pj.read(),Content_Disposition='attachement;filename="%s"' % os.path.basename(photo),Name=os.path.basename(photo)))
    pj.close()
  def send():
    if (mailaccount.connected):
      
class message:

  def __init__(self,text='Instert texte here'):
    self.text=text
    self.sign=''
  def create():
    return self.text+'\n-- \n'+self.sign

def main():
  print("Not yet")
