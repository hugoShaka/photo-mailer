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
  """A photo can be sent, it also contains the recipient's email address"""
  def __init__(self,fileloc,mailaccount,message):
    self.location=fileloc
    self.info=IPTCInfo(path_to_image)
    self.addr=str(self.info.data['object name'])
    if self.addr=='':
      self.email=None
    else:
      self.email=mail(self.addr,self.location,mailaccount,message)
    self.sent=False
  def send()
    if self.sent:
      print('Warning :Re-sending the email')
    self.email.send()
    self.sent=True

class folder:
  """Représente un dossier"""
  def __init__(self,pathtofolder):
    self.path=pathtofolder
    self.files=[]
  def scan():
    howmanyimport=0
    for root, dirs, files in os.walk(self.path):
      for file in files:
        if file.endswith(".jpg"):
          self.files.append(photo(os.path.join(root, file)))
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

  def showMailSettings():
    print("sender : "+self.sender+"\nsmtp server : "+self.smtp+"\nport : "+self.port+"\nlogin : ")
    if not self.connected:
      print("Not connected")
    else:
      print("Connected as : "+self.login)

  def editMailSettings():
    self.sender=input("sender ?")
    self.smtp=input("server ?")
    self.port=input("port?")

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
  """Objet mail qui possède les methodes pour etre envoye, recupere ses parametres d'un objet mailaccount"""
  def __init__(self,reciever,photo,mailaccount,message):
    self.msg=MIMEMultipart()
    self.msg['From'] = mailaccount.sender
    self.msg['To'] = reciever
    self.msg['Subject'] = mailaccount.subject
    self.msg.attach(MIMEText(message.create()))
    
    pj=open(photo, 'rb')
    self.msg.attach(MIMEApplication(pj.read(),Content_Disposition='attachement;filename="%s"' % os.path.basename(photo),Name=os.path.basename(photo)))
    pj.close()

  def send():
    """Send the mail object"""
    if (mailaccount.connected):
      mailaccount.mailserver.sendmail(mailaccount.sender, self.msg['To'], self.msg.as_string())
    else :
      mailaccount.log()
      mailaccount.mailserver.sendmail(mailaccount.sender, self.msg['To'], self.msg.as_string())
      
class message:
    """A class to manage the e-mail text"""
  def __init__(self,text='No text'):
    self.text=text
    self.sign=''
  def create():
    return self.text+'\n-- \n'+self.sign

def main():
  print("Not yet")
  mailacc=mailaccount()
  mailacc.showMailSettings()
  if (input("Edit mail server settings ? (y/N)")=='y')
    mailacc.edit():
  print("Please enter your credentials")
  mailacc.credentials()
  print("Testing the settings")
  mailacc.log()
  if mailacc.conncted
    print("Successfully logged :) ")
  else:
    print("Exiting")
    break
  pathto=input("Choose yout folder")
  location=folder(pathto)
  
