import paramiko
import logging
import os
import psutil


class sftpClient:
  def __init__(self, remoteServerName, remoteSftpPath, userName, password):
    self.remoteSftpServer = remoteServerName
    self.remoteSftpServerPath = remoteSftpPath
    self.remoteEsvn2User = userName
    self.remoteEsvn2Pass = password
    self.connectionTimeOut = 5
 
  def getSftpClientSshConnection(self):
      try:
                ssh = paramiko.SSHClient()    
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.remoteSftpServer, username=self.remoteEsvn2User, password=self.remoteEsvn2Pass, timeout=self.connectionTimeOut)

      except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException) as error:
            logging.error(error)
            logging.error("failed to connect to sftp server")

      return ssh
 
  def pushl7MessagesToEsvn2(self, hl7PileOfMessages):
       
       client = self.getSftpClientSshConnection()
       sftp = client.open_sftp()
       localPathToHl7files = os.getcwd()

       for i in range(len(hl7PileOfMessages)):
          
          #pSegment = hl7PileOfMessages[i].PID
          #numeroDossier = pSegment.pid_3.pid_3_1

          #pvSegment = hl7PileOfMessages[i].PV1
          #numeroApplication = pvSegment.pv1_5
          pathToHl7FileInLocal = str(hl7PileOfMessages[i])
          pathToHl7FileInEsvn2 = self.remoteSftpServerPath + "/" + os.path.basename(os.path.normpath(str(hl7PileOfMessages[i])))

          #pathToHl7FileInLocal = str(localPathToHl7files) + "\\" + "hl7toEsvn2" + "\\" + str(numeroDossier.value) + "_" + str(numeroApplication.value) + ".hl7"
          #pathToHl7FileInEsvn2 = self.remoteSftpServerPath + "/" + str(numeroDossier.value) + "_" + str(numeroApplication.value) + ".hl7"

          try:
            sftp.put(pathToHl7FileInLocal, pathToHl7FileInEsvn2)
          except Exception as e:
            logging.error(e)
        
       #set connection free now they are available
       sftp.close()
       client.close()

           

      
      