# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QListView, QPlainTextEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backgroundImage = QtWidgets.QLabel(self.centralwidget)
        self.backgroundImage.setText("")
        pixmap = QtGui.QPixmap("../images/dixit-cover.jpg")
        self.backgroundImage.resize(pixmap.width(), pixmap.height())
        self.backgroundImage.setPixmap(pixmap)
        self.resize(self.backgroundImage.width(), self.backgroundImage.height())
        self.backgroundImage.setObjectName("backgroundImage")

        self.poolImagesList = QtWidgets.QListWidget(self.centralwidget)
        self.poolImagesList.setGeometry(QtCore.QRect(300, 150, 566, 160))
        self.poolImagesList.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.poolImagesList.setObjectName("poolImagesList")
        self.poolImagesList.setWindowTitle("pool images")
        self.poolImagesList.setViewMode(QListView.IconMode)
        self.poolImagesList.setIconSize(QtCore.QSize(128, 128))
        self.poolImagesList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.poolImagesList.setDragDropMode(QAbstractItemView.NoDragDrop) 

        self.deckImagesList = QtWidgets.QListWidget(self.centralwidget)
        self.deckImagesList.setGeometry(QtCore.QRect(200, 550, 566, 139))
        self.deckImagesList.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.deckImagesList.setObjectName("deckImagesList")
        self.deckImagesList.setWindowTitle("deck images")
        self.deckImagesList.setViewMode(QListView.IconMode)
        self.deckImagesList.setIconSize(QtCore.QSize(128, 128))
        self.deckImagesList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.deckImagesList.setDragDropMode(QAbstractItemView.NoDragDrop) 


        self.onlineUsers = QtWidgets.QTableWidget(0, 2, self.centralwidget)
        self.onlineUsers.setGeometry(QtCore.QRect(950, 500, 300, 200))
        self.onlineUsers.setSelectionMode(QAbstractItemView.NoSelection)
        self.onlineUsers.setStyleSheet("QTableWidget {background-color: transparent;}"
            "QTableWidget {border: 0;}"
            "QHeaderView::section {background-color: lightblue;}"
            "QHeaderView {background-color: transparent;}"
            "QTableCornerButton::section {background-color: transparent;}")
        self.onlineUsers.setShowGrid(False)
        self.onlineUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.onlineUsers.setObjectName("onlineUsers")
        self.onlineUsers.setWindowTitle("online users")
        self.onlineUsers.setHorizontalHeaderLabels(('Name', 'IP'))

        self.pointTable = QtWidgets.QTableWidget(0, 2, self.centralwidget)
        self.pointTable.setGeometry(QtCore.QRect(950, 50, 300, 200))
        self.pointTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.pointTable.setStyleSheet("QTableWidget {background-color: transparent;}"
            "QTableWidget {border: 0;}"
            "QHeaderView::section {background-color: lightblue;}"
            "QHeaderView {background-color: transparent;}"
            "QTableCornerButton::section {background-color: transparent;}")
        self.pointTable.setShowGrid(False)
        self.pointTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pointTable.setObjectName("pointTable")
        self.pointTable.setWindowTitle("point table")
        self.pointTable.setHorizontalHeaderLabels(('Name', 'Points'))

        self.descriptionBox = QPlainTextEdit(self.centralwidget)
        self.descriptionBox.setGeometry(400, 360, 400, 100)
        self.descriptionBox.setWindowTitle("desctip")
        
        self.descriptionBoxLabel = QtWidgets.QLabel(self.centralwidget)
        self.descriptionBoxLabel.setGeometry(300, 350, 100, 50)
        self.descriptionBoxLabel.setText("Description: ")
        self.descriptionBoxLabel.setFont(QtGui.QFont("default",10)) 

        self.messageToClient = QtWidgets.QLabel(self.centralwidget)
        self.messageToClient.setGeometry(400, 50, 400, 100)
        self.messageToClient.setFont(QtGui.QFont("default",11)) 

        self.descriptionDisplay = QtWidgets.QLabel(self.centralwidget)
        self.descriptionDisplay.setGeometry(400, 360, 400, 100)
        self.descriptionDisplay.setFont(QtGui.QFont("default",11)) 

        self.sendImageAndDesc = QtWidgets.QPushButton(self.centralwidget)
        self.sendImageAndDesc.setGeometry(QtCore.QRect(400, 500, 200, 50))
        self.sendImageAndDesc.setVisible(False)
        self.sendImageAndDesc.setText("send image and desc")

        self.displaySelectedImage = QtWidgets.QLabel(self.centralwidget)
        self.displaySelectedImage.setGeometry(QtCore.QRect(100, 250, 300, 500))
        self.displaySelectedImage.setVisible(False)


        self.sendImage = QtWidgets.QPushButton(self.centralwidget)
        self.sendImage.setGeometry(QtCore.QRect(400, 500, 200, 50))
        self.sendImage.setVisible(False)
        self.sendImage.setText("send image")

        self.sendVote = QtWidgets.QPushButton(self.centralwidget)
        self.sendVote.setGeometry(QtCore.QRect(900, 200, 100, 50))
        self.sendVote.setVisible(False)
        self.sendVote.setText("send vote")


        self.readyBox = QtWidgets.QCheckBox(self.centralwidget)
        self.readyBox.setGeometry(QtCore.QRect(1000, 460, 121, 20))
        self.readyBox.setObjectName("readyBox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.readyBox.setText(_translate("MainWindow", "I AM READY"))
