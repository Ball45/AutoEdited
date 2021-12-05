from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

self.process = QProcess()
self.connect(self.process, SIGNAL("readyReadStdout()"), self.readOutput)
self.connect(self.process, SIGNAL("readyReadStderr()"), self.readErrors)
tarsourcepath="sudo tar xvpf "+ self.path1
self.process.setArguments(QStringList.split(" ",tarsourcepath))
self.process.start()



def readOutput(self):

    self.textBrowser2.append(QString(self.process.readStdout()))
    if self.process.isRunning()==False:
        self.textBrowser2.append("n Completed Successfully")




def readErrors(self):
    self.textBrowser2.append("error: " + QString(self.process.readLineStderr()))