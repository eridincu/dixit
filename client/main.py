# SEND TCP:

# 1. selected image
# 2. storyteller sends description
# 3. non-storytellers vote image
# 4. goodbye

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QTableWidgetItem, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap

import json
import time
import sys
import mainWindow
import socket
import select

def find_my_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP = "127.0.0.1"
    try:
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP

ready = 0
MY_LOCAL_IP = find_my_local_ip()
PORT = 12345
MY_NAME = ''
online_users = {
    112.32: "fırat",
    1231.41: "faruk"
}
turn_points = {
    112.32: 4,
    1231.41: 1
}
deck_images = [
    "row-1-col-2",
    "row-6-col-5",
    "row-4-col-2",
    "row-2-col-3",
    "row-5-col-1",
    "row-5-col-2",
]
story_teller_ip = ''
point_table = {
    112.32: 12,
    1231.41: 15
} # {user_ip=point, ...}
pool_images = [
    "row-1-col-2",
    "row-6-col-5",
    "row-4-col-2",
    "row-2-col-3",
    "row-5-col-1",
    "row-5-col-2",
] # [image1,image2, ...]
description = ''
selected_pool_image = ''
selected_deck_image = ''


class DixitApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(DixitApp, self).__init__(parent)
        
        self.setupUi(self)

message = {
    "NAME": "",
    "MY_IP": "",
    "TYPE": "",
    "PAYLOAD": ""
    }

def get_packet(packet_type, payload=''):
    packet = {
        'NAME': MY_NAME,
        'MY_IP': MY_LOCAL_IP,
        'TYPE': packet_type,
        'PAYLOAD': payload,
    }

    return packet

def conv_to_bytes(message_):
    byte_message = (str(message_)+"\n").encode('utf-8')
    return byte_message

def sendDescription():
    desc = dixit.descriptionBox.toPlainText()
    if desc != '':
        send_TCP("DESCRIPTION", desc)
    else:
        print("please write description")

def displayDeckImages(upside):
    dixit.deckImagesList.clear()
    for imageName in deck_images:
        item = QListWidgetItem()
        item.setWhatsThis(imageName)
        icon = QIcon()
        pixmap = ''
        if upside:
            pixmap = QPixmap("../images/dixit_cards/"+imageName+".jpg")
        else:
            pixmap = QPixmap("../images/dixit-back.jpg")
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        item.setIcon(icon)
        dixit.deckImagesList.addItem(item)
    pass

def displayPoolImages(upside):
    dixit.poolImagesList.clear()
    for imageName in pool_images:
        item = QListWidgetItem()
        item.setWhatsThis(imageName)
        icon = QIcon()
        pixmap = ''
        if upside:
            item.setText("???")
            pixmap = QPixmap("../images/dixit_cards/"+imageName+".jpg")
        else:
            pixmap = QPixmap("../images/dixit-back.jpg")
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        item.setIcon(icon)
        dixit.poolImagesList.addItem(item)
    pass

def voteImage():
    if selected_pool_image != '':
        send_TCP("CHOSEN_IMAGE", selected_pool_image)
    else:
        print("please select an image") # print where????

def updatePointTable():
    for userID in turn_points.keys():
        point_table[userID] = point_table[userID] + turn_points[userID]
    displayPointTable()

def displayPointTable():
    for user in point_table.keys():
        rowPosition = dixit.pointTable.rowCount()

        dixit.pointTable.insertRow(rowPosition)

        dixit.pointTable.setItem(rowPosition , 0, QTableWidgetItem(online_users[user]))
        dixit.pointTable.setItem(rowPosition , 1, QTableWidgetItem(str(point_table[user])))
    dixit.pointTable.sortItems(1, QtCore.Qt.DescendingOrder)
    
    

def listen_tcp():
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((MY_LOCAL_IP, PORT))
            s.settimeout(5)
            try:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        stri = data.decode('utf-8').rstrip()
                        dic = eval(stri)
                        if dic["TYPE"] == "DECK_IMG":
                            deck_images.append(dic["PAYLOAD"])
                        elif dic["TYPE"] == "DECK_INIT":
                            # image format : image1,image2,...
                            temp_deck = dic["PAYLOAD"]
                            deck_image = temp_deck.split(',')
                            for x in deck_image:
                                deck_images.append(x)
                        else:
                            pass
            except socket.timeout:
                pass

            s.close()



def setupUi(isStoryteller, isVoteTime):
    displayPoolImages(isVoteTime)
    displayDeckImages(1)
    displayPointTable()
    dixit.poolImagesList.setVisible(True)
    dixit.deckImagesList.setVisible(True)
    dixit.pointTable.setVisible(True)
    dixit.messageToClient.setVisible(True)
    dixit.descriptionBox.setVisible(isStoryteller)
    dixit.descriptionBoxLabel.setVisible(isStoryteller)
    if isStoryteller:
        dixit.messageToClient.setText("Please select an image and give description")
    else:
        dixit.messageToClient.setText("Please wait for storyteller.")
    if isStoryteller and not isVoteTime:
        dixit.sendImageAndDesc.setText("send image & desc")
        dixit.sendVote.setVisible(False)
        dixit.sendImageAndDesc.setVisible(True)
    elif isStoryteller and isVoteTime:
        dixit.sendImageAndDesc.setVisible(False)
        dixit.sendVote.setVisible(True)




def listen_udp():
    while(True):
        #print("in broadcast")
        port_ = 12345
        bufferSize = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(5)
        try:
            s.bind(('', port_))
            #print("in broadcast")
            s.setblocking(0)

            result = select.select([s], [], [])
            msg = result[0][0].recv(bufferSize)
            stri = msg.decode('utf-8').rstrip()
            dic = eval(stri)
            if dic["TYPE"] == "ONLINE_USERS":
                # user list format : user_ip1,user_name1_?_user_ip2,user_name2_?_...
                temp_user_list = dic["PAYLOAD"]
                temp_user_info_list = temp_user_list.split('_?_')
                for x in temp_user_info_list:
                    temp_user_info = x.split(',')
                    online_users[temp_user_info[0]] = temp_user_info[1]
            elif dic["TYPE"] == "USER_LEFT":
                # user left format : user_ip
                left_user_ip = dic["PAYLOAD"]
                del online_users[left_user_ip]
            elif dic["TYPE"] == "STORYTELLER":
                # story teller fomat : story_teller_ip
                # start of a new round
                story_teller_ip = dic["PAYLOAD"]
                # display images with qt
                # display the storyteller's name with qt
                if story_teller_ip == MY_LOCAL_IP:
                    setupUi(1, 0)
                    image_, description_ = chooseImage()  # returns name and description of the image.
                    send_TCP("STORYTELLER_IMAGE", image_)
                    send_TCP("DESCRIPTION", description_)
                else:
                    setupUi(0, 0)
                    # do nothing
                    pass

            elif dic["TYPE"] == "POINT_TABLE":
                # point table format : user_ip1,point1_?_user_ip2,point2_?_...
                temp_point_table = dic["PAYLOAD"]
                temp_user_point_list = temp_point_table.split('_?_')
                for x in temp_user_point_list:
                    temp_user_info = x.split(',')
                    turn_points[temp_user_info[0]] = temp_user_info[1]
                updatePointTable()
            elif dic["TYPE"] == "POOL_IMAGES":
                # point table format : image1,image2,image3, ...
                pool_images.clear()
                temp_pool_images = dic["PAYLOAD"]
                pool_images_list = temp_pool_images.split(',')
                for x in pool_images_list:
                    pool_images.append(x)
                if story_teller_ip != MY_LOCAL_IP:
                    voted_image = voteImage()
                    send_TCP("IMAGE_VOTE", voted_image)
            elif dic["TYPE"] == "DESCRIPTION":
                description = dic["PAYLOAD"]
                dixit.descriptionBox.setPlainText(description)
                if story_teller_ip != MY_LOCAL_IP:
                    image_ = chooseImage()
                    send_TCP("CHOSEN_IMAGE", image_)
                else:
                    # do nothing
                    pass
            else:
                pass
        except socket.timeout:
            pass
        s.close()


def send_TCP(type_, payload_):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((MY_LOCAL_IP, PORT))
            packet = get_packet(type_, payload_)
            packet_bytes = json.dumps((packet)).encode('utf-8')
            s.send(packet_bytes)
            print("ME: "+ payload_)
            s.close()
    except ConnectionRefusedError:
        print("unexpected offline client detected")



app = QApplication(sys.argv)
dixit = DixitApp()

def descriptionChanged():
    description = dixit.descriptionBox.toPlainText()
    print(description)

def poolImageSelectionChanged():
    selected_pool_image = dixit.poolImagesList.selectedItems()[0].whatsThis()
    print(selected_pool_image)

def deckImageSelectionChanged():
    selected_deck_image = dixit.deckImagesList.selectedItems()[0].whatsThis()
    print(selected_deck_image)
    print(description)



def changeReady():
    ready = dixit.readyBox.isChecked()
    dixit.readyBox.setDisabled(True)
    if ready:
        setupUi(1, 0)
        # send_TCP("READY", "1")
    else:
        # send_TCP("READY", "0")
        pass

def sendVotedImage():
    if len(dixit.poolImagesList.selectedItems()) != 0:
        selected_pool_image_ = dixit.poolImagesList.selectedItems()[0].whatsThis()
    else:
        selected_pool_image_ = ''
    if selected_pool_image_ != '':
        dixit.messageToClient.setText("You voted!")
        send_TCP("IMAGE_VOTE", selected_pool_image_)
        dixit.sendVote.setDisabled(True)
    else:
        dixit.messageToClient.setText("Please vote for a picture...")

def sendImageAndDescription():
    description_ = dixit.descriptionBox.toPlainText()
    if len(dixit.deckImagesList.selectedItems()) != 0:
        selected_deck_image_ = dixit.deckImagesList.selectedItems()[0].whatsThis()
    else:
        selected_deck_image_ = ''
    print("deck image", selected_deck_image_ )
    print("des", description_)
    if selected_deck_image_ != '' and description_ != '':
        dixit.messageToClient.setText("image and description sent, please wait for other users to send their images.")
        send_TCP("STORYTELLER_IMAGE", selected_deck_image_)
        send_TCP("DESCRIPTION", description_)
    else: 
        dixit.messageToClient.setText("PLEASE SELECT AN IMAGE AND WRITE A DESCRIPTION FOR IT!")


def main():

    dixit.deckImagesList.itemSelectionChanged.connect(deckImageSelectionChanged)
    dixit.poolImagesList.itemSelectionChanged.connect(poolImageSelectionChanged)
    dixit.descriptionBox.textChanged.connect(descriptionChanged)
    dixit.readyBox.toggled.connect(changeReady)
    dixit.sendImageAndDesc.clicked.connect(sendImageAndDescription)
    dixit.sendVote.clicked.connect(sendVotedImage)

    for user in online_users.keys():
        rowPosition = dixit.onlineUsers.rowCount()

        dixit.onlineUsers.insertRow(rowPosition)

        dixit.onlineUsers.setItem(rowPosition , 0, QTableWidgetItem(online_users[user]))
        dixit.onlineUsers.setItem(rowPosition , 1, QTableWidgetItem(str(user)))

    dixit.poolImagesList.setVisible(False)
    dixit.deckImagesList.setVisible(False)
    dixit.pointTable.setVisible(False)
    dixit.descriptionBox.setVisible(False)
    dixit.descriptionBoxLabel.setVisible(False)

    

    # Optional, resize window to image size

    dixit.show()
    app.exec_()
    

main()

