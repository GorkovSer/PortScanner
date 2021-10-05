from PyQt5 import QtCore, QtGui, QtWidgets
from netaddr import valid_ipv4
import socket,threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(370, 436)
        MainWindow.setMinimumSize(QtCore.QSize(370, 436))
        MainWindow.setMaximumSize(QtCore.QSize(370, 436))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 380, 331, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.portScan)

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 30, 141, 151))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setAcceptRichText(False)

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 210, 141, 151))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setAcceptRichText(False)

        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(190, 30, 160, 331))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setAcceptRichText(False)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 190, 161, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 161, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(190, 10, 161, 16))
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 370, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PortScaner"))
        self.pushButton.setText(_translate("MainWindow", "Начать проверку"))
        self.label.setText(_translate("MainWindow", "Список портов"))
        self.label_2.setText(_translate("MainWindow", "Список IP"))
        self.label_3.setText(_translate("MainWindow", "Отчет"))
    
    def portScan(self):
        textTargets = self.textEdit.toPlainText()
        textPorts = self.textEdit_2.toPlainText()

        ports = textPorts.split(" ")
        targets = textTargets.split(" ")
        
        if Ui_MainWindow.ipCheck(self,targets) or Ui_MainWindow.portCheck(self,ports) == False: # проверка данных
            return

        def streamPortScan(port,targets):  # Создаём функцию сканирования портов

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаём сокет
            s.settimeout(0.5)   # таймаут

            try:
                connection = s.connect((str(targets), int(port)))  # коннект к хосту

                print('Port: ' + str(port) + " is open.")   # пишем что порт открыт
                self.textEdit_3.append('Port: ' + str(port) + " is open.")

                connection.close()   
            except:
                # заглушка, отсутствиt соединениq
                pass   #
          
        for eleme in targets:
            for element in ports:   # Перебор в цикле портов
                t = threading.Thread(target=streamPortScan, kwargs={'port': element,'targets': eleme })  # Создаём поток
                t.start()   # Запуск потока


    def ipCheck(self, ip):
            for element in ip: # проверка ip
                if valid_ipv4(element) == False:
                    self.textEdit_3.append("Ошибка в написании ip")
                    return False

    def portCheck(self, ports):
        for element in ports:# проверка порта
            portChars = set('0123456789')

            try:
                if int(element) > 65535:
                    self.textEdit_3.append("Ошибка в написании портов")
                    return False

                if any((c in portChars) for c in element):
                    pass
                else:
                    self.textEdit_3.append("Ошибка в написании портов")
                    return False     
            except:
                self.textEdit_3.append("Ошибка в написании портов")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
