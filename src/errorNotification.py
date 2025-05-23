"""
Modules

"""

import smtplib
from email.mime.text import MIMEText


"""
Error Notification

"""

class errorNotification:

    def __init__(self, errorMessage, serverAddress, serverPort, senderAddress, senderPassword, recipientAddress):

        # Server info
        self.serverAddress = serverAddress
        self.serverPort = serverPort
                
        # Sender and recipient info
        self.sender = senderAddress
        self.password = senderPassword
        self.recipients = recipientAddress

        # Message
        self.subject = "Maze Error"
        self.errorMessage = errorMessage
        
    def sendEmail(self):
        message = MIMEText(self.errorMessage)
        message['Subject'] = self.subject
        message['From'] = self.sender
        message['To'] = ', '.join(self.recipients)
        with smtplib.SMTP_SSL(self.serverAddress, self.serverPort) as smtpServer:
           smtpServer.login(self.sender, self.password)
           smtpServer.sendmail(self.sender, self.recipients, message.as_string())
        

"""
Main Block

"""

if __name__ == "__main__":
    errorNotification = errorNotification.__init__()