# -*- coding: utf-8 -*-

import getpass
import sys, os
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from iptcinfo import IPTCInfo
import logging

logging.basicConfig(filename='error.log')

class photo:
  """A photo can be sent, it also contains the recipient's email address"""
  def __init__(self,fileloc):
    self.location=fileloc
    try:
      self.info=IPTCInfo(self.location)
      self.addr=str(self.info.data['object name'])
      self.IPTCred=True
    except Exception:
      print(fileloc+" No valid IPTC tags found.")
      self.IPTCred=False

  def generateEmail(self,mailaccount,message):
    if self.addr=='':
      self.email=None
      print("Warning no valid email address for : "+self.location)
    else:
      self.email=mail(self.addr,self.location,mailaccount,message)
    self.sent=False

  def send(self):
    if self.sent:
      print('Warning :Re-sending the email')
    self.email.send()
    self.sent=True

class folder:
  """Contains the path to the photos. Can be scanned to get the photos and can be used to mass edit/send the mails/the photos"""
  def __init__(self,pathtofolder):
    self.path=pathtofolder
    self.files=[]
  def scan(self):
    howManyImport=0
    for root, dirs, files in os.walk(self.path):
      for file in files:
        if file.endswith(".jpg"):
          importedPhoto=photo(os.path.join(root, file))
          if importedPhoto.IPTCred:
            self.files.append(importedPhoto)
            howManyImport+=1
    print(str(howManyImport) + " files were sucessfully imported")
  def generateEmails(self,mailaccount,message):
    for pic in self.files:
      pic.generateEmail(mailaccount,message)



class mailaccount:
  """Compte mail et parametres de connexion au serveur
"""

  def __init__(self):
    self.sender="Club Photo"
    self.port="587"
    self.smtp="smtp.rez-gif.supelec.fr"
    self.login="None"
    self.connected=False

  def credentials(self):
    self.login=raw_input("Login : ")
    self.pwd=getpass.getpass("Mot de passe : \n")

  def showMailSettings(self):
    print("\n--------------------\n MailServer Settings \n--------------------\n")
    print("sender : "+self.sender+"\nsmtp server : "+self.smtp+"\nport : "+self.port+"\nlogin : ")
    if not self.connected:
      print("Status : not connected")
    else:
      print("Status : connected as : "+self.login)

  def editMailSettings(self):
    self.sender=raw_input("sender ?")
    self.smtp=raw_input("server ?")
    self.port=raw_input("port?")

  def log(self):
    try:
      self.mailserver=smtplib.SMTP(self.smtp,self.port)
      self.mailserver.ehlo()
      self.mailserver.starttls()
      self.mailserver.ehlo()
      self.mailserver.login(self.login,self.pwd)
      self.connected=True
    except (socket.error) as err:
      print("Socket error:.({0}): {1}".format(e.errno, e.strerror))
      self.connected=False

  def unlog(self):
    self.mailserver.quit()
    self.connected=False

class mail:
  """Objet mail qui possède les methodes pour etre envoye, recupere ses parametres d'un objet mailaccount"""
  def __init__(self,reciever,photo,mailaccount,message):
    if reciever==None:
      print("\n /!\ Email not created due to invalid email address")
    else:
      self.msg=MIMEMultipart()
      self.msg['From'] = mailaccount.sender
      self.msg['To'] = reciever
      self.msg['Subject'] = message.subject
      self.msg.attach(MIMEText(message.generate()))
    
      pj=open(photo, 'rb')
      self.msg.attach(MIMEApplication(pj.read(),Content_Disposition='attachement;filename="%s"' % os.path.basename(photo),Name=os.path.basename(photo)))
      pj.close()
      print("Mail to : "+reciever+" successfully generated")

  def send(self):
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
    self.subject='Your photo'
  def generate(self):
    return self.text+'\n-- \n'+self.sign

def main():
  print("Not yet")
  mailacc=mailaccount()
  mailacc.showMailSettings()
  if (raw_input("\nEdit mail server settings ? (y/N)")=='y'):
    mailacc.editMailSettings()
  print("Please enter your credentials")
  mailacc.credentials()
  print("Testing the settings")
  mailacc.log()
  if mailacc.connected:
    print("\nSuccessfully logged    :) \n")
  else:
    print("Exiting")
  pathto=raw_input("Choose your folder")
  currentFolder=folder('/home/shaka/Downloads/photos/')
  currentFolder.scan()
  currentMessage=message()
  currentMessage.text=raw_input("enter the email's body text")
  currentFolder.generateEmails(mailacc,currentMessage)

main()
