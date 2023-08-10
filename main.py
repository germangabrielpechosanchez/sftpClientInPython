
import messageHeaders
import sftpClient
import glob, os
import base64

pileOfhl7Messages = []

def pathToHl7Message(pathToHl7FolderFiles):
    
    for hl7FileName in os.listdir(pathToHl7FolderFiles):
        if os.path.isfile(os.path.join(pathToHl7FolderFiles, hl7FileName)):
            pathToFileInFolder = pathToHl7FolderFiles + "\\" + str(hl7FileName)
            pileOfhl7Messages.append(pathToFileInFolder)
    return pileOfhl7Messages

def main():
    localPathToApp = os.getcwd()
    #pathToHl7files = localPathToApp + "\\" + "HL7Nephro"
    pathToHl7files = localPathToApp + "\\" + "HL7WinVision"
    pathToHl7Message(pathToHl7files)

    mySftpClient = sftpClient.sftpClient(messageHeaders.esvn2Sname, messageHeaders.esvn2Spath, messageHeaders.esvn2Suser, messageHeaders.esvn2Spass)
    mySftpClient.pushl7MessagesToEsvn2(pathToHl7Message(pathToHl7files))

if __name__ == "__main__":
    main()