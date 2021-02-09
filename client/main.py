
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
import threading

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
SERVER_IP = '192.168.1.39'
MY_LOCAL_IP = find_my_local_ip()
PORT = 12345
MY_NAME = 'client1'
online_users = dict()
turn_points = dict()
deck_images = []
story_teller_ip = ''
point_table = dict()
pool_images = dict()
description = ''
selected_pool_image = ''
selected_deck_image = ''
story_teller_image = ''


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
            pixmap = QPixmap("../images/dixit_cards/"+imageName)
        else:
            pixmap = QPixmap("../images/dixit-back.jpg")
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        item.setIcon(icon)
        dixit.deckImagesList.addItem(item)
    pass

def displayPoolImages(upside):
    dixit.poolImagesList.clear()
    for imageName in pool_images.keys():
        item = QListWidgetItem()
        item.setWhatsThis(imageName)
        icon = QIcon()
        pixmap = ''
        if upside:
            item.setText(pool_images[imageName])
            pixmap = QPixmap("../images/dixit_cards/"+imageName)
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
        if userID not in list(point_table.keys()):
            point_table[userID] = 0
        point_table[userID] = point_table[userID] + int(turn_points[userID])
    displayPointTable()

def displayPointTable():
    dixit.pointTable.clear()
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



def setupUi(isStoryteller, isVoteTime, isStorytellersTurn):
    displayPoolImages(isVoteTime)
    displayDeckImages(1)
    displayPointTable()
    dixit.poolImagesList.setVisible(True)
    dixit.deckImagesList.setVisible(True)
    dixit.pointTable.setVisible(True)
    dixit.messageToClient.setVisible(True)
    if isStoryteller:
        if isVoteTime:
            dixit.messageToClient.setText("Please wait for other players to vote.")
            dixit.sendImageAndDesc.setVisible(False)
            dixit.sendVote.setVisible(False)
            dixit.descriptionBox.setVisible(False)
            dixit.descriptionBoxLabel.setVisible(True)
            dixit.descriptionDisplay.setVisible(True)
        else:
            if isStorytellersTurn:
                dixit.messageToClient.setText("Please choose an image and write description for it.")
                dixit.sendVote.setVisible(False)
                dixit.sendImage.setVisible(False)
                dixit.sendImageAndDesc.setVisible(True)
                dixit.descriptionBox.setVisible(True)
                dixit.descriptionBoxLabel.setVisible(True)
                dixit.descriptionDisplay.setVisible(False)
            else:
                dixit.descriptionDisplay.setText(description)
                dixit.messageToClient.setText("Please wait for others to choose image.")
                dixit.sendVote.setVisible(False)
                dixit.sendImage.setVisible(False)
                dixit.sendImageAndDesc.setVisible(False)
                dixit.descriptionBox.setVisible(False)
                dixit.descriptionBoxLabel.setVisible(True)
                dixit.descriptionDisplay.setVisible(True)

    else:
        if isVoteTime:
            dixit.messageToClient.setText("Please vote for an image")
            dixit.sendImageAndDesc.setVisible(False)
            dixit.sendVote.setVisible(True)
            dixit.descriptionBoxLabel.setVisible(True)
            dixit.descriptionDisplay.setVisible(True)
            dixit.descriptionBox.setVisible(False)
        else:
            if isStorytellersTurn:
                dixit.messageToClient.setText("Please wait for the storyteller to choose an image.")
                dixit.sendVote.setVisible(False)
                dixit.sendImageAndDesc.setVisible(False)   
                dixit.descriptionBoxLabel.setVisible(False)
                dixit.descriptionDisplay.setVisible(False)    
                dixit.descriptionBox.setVisible(False)
            else:
                dixit.descriptionDisplay.setText(description)
                dixit.messageToClient.setText("Please choose an image according to the description.")
                dixit.sendVote.setVisible(False)
                dixit.sendImageAndDesc.setVisible(False)   
                dixit.descriptionBoxLabel.setVisible(True)
                dixit.descriptionDisplay.setVisible(True)    
                dixit.descriptionBox.setVisible(False)
                dixit.sendImage.setVisible(True)

        




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
                displayOnlineUsers()
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
                setupUi(story_teller_ip == MY_LOCAL_IP, 0, 1)

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
                temp_pool_images_list = temp_pool_images.split(',')
                for x in temp_pool_images_list:
                    if story_teller_ip == MY_LOCAL_IP and x == story_teller_image:
                        pool_images[x] = MY_NAME + "'s img"
                    else:
                        pool_images[x] = "???"
                setupUi(story_teller_ip == MY_LOCAL_IP, 1, 0)
            elif dic["TYPE"] == "DESCRIPTION":
                global description
                description = dic["PAYLOAD"]
                setupUi(MY_LOCAL_IP == story_teller_ip, 0, 0)
            elif dic["TYPE"] == "USER_IMAGE_PAIRS":
                pool_images.clear()
                temp_pool_images = dic["PAYLOAD"]
                temp_pool_images_list = temp_pool_images.split('_?_')
                for x in temp_pool_images_list:
                    temp_pool_image_info = x.split(",")
                    pool_images[temp_pool_image_info[0]] = temp_pool_image_info[1]
                setupUi(story_teller_ip == MY_LOCAL_IP, 1, 0)
            else:
                pass
        except socket.timeout:
            pass
        s.close()


def send_TCP(type_, payload_):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((SERVER_IP, PORT))
            packet = get_packet(type_, payload_)
            packet_bytes = json.dumps((packet)).encode('utf-8')
            s.send(packet_bytes)
            print("ME: "+ payload_)
            s.close()
    except ConnectionRefusedError:
        print("unexpected offline client detected")

send_TCP("DISCOVER", "")

app = QApplication(sys.argv)
dixit = DixitApp()

listen_TCP_thread = threading.Thread(target=listen_tcp, name='tcp-thread', daemon=True)
listen_UDP_thread = threading.Thread(target=listen_udp, name='udp-thread', daemon=True)

listen_TCP_thread.start()
listen_UDP_thread.start()

def descriptionChanged():
    description = dixit.descriptionBox.toPlainText()
    print(description)

def poolImageSelectionChanged():
    selected_pool_image = dixit.poolImagesList.selectedItems()[0].whatsThis()
    print(selected_pool_image)

def deckImageSelectionChanged():
    selected_deck_image = dixit.deckImagesList.selectedItems()[0].whatsThis()
    print(selected_deck_image)



def changeReady():
    ready = dixit.readyBox.isChecked()
    dixit.readyBox.setDisabled(True)
    send_TCP("READY", "")

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
        story_teller_image = selected_deck_image_        
        send_TCP("STORYTELLER_IMAGE", selected_deck_image_)
        time.sleep(0.2)
        send_TCP("DESCRIPTION", description_)
        setupUi(1, 0, 0)
        deck_images.remove(selected_deck_image_)
        pool_images[selected_deck_image_] = "MY_IMAGE"
        displayDeckImages(1)
        displayPoolImages(1)

def sendImage():
    if len(dixit.deckImagesList.selectedItems()) != 0:
        selected_deck_image_ = dixit.deckImagesList.selectedItems()[0].whatsThis()
    else:
        selected_deck_image_ = ''
    print("deck image", selected_deck_image_ )
    if selected_deck_image_ != '':
        send_TCP("STORYTELLER_IMAGE", selected_deck_image_)
        dixit.messageToClient.setText("Please wait for other players to choose their image")
        dixit.sendImage.setDisabled(True)
        deck_images.remove(selected_deck_image_)
        pool_images[selected_deck_image_] = "MY_IMAGE"
        displayDeckImages(1)
        displayPoolImages(1)

    else: 
        dixit.messageToClient.setText("PLEASE SELECT AN IMAGE AND WRITE A DESCRIPTION!")

def displayOnlineUsers():
    dixit.onlineUsers.setRowCount(0)
    for user in online_users.keys():
        rowPosition = dixit.onlineUsers.rowCount()

        dixit.onlineUsers.insertRow(rowPosition)

        dixit.onlineUsers.setItem(rowPosition , 0, QTableWidgetItem(online_users[user]))
        dixit.onlineUsers.setItem(rowPosition , 1, QTableWidgetItem(str(user)))

def main():

    # dixit.deckImagesList.itemSelectionChanged.connect(deckImageSelectionChanged)
    dixit.poolImagesList.itemSelectionChanged.connect(poolImageSelectionChanged)
    dixit.descriptionBox.textChanged.connect(descriptionChanged)
    dixit.readyBox.toggled.connect(changeReady)
    dixit.sendImageAndDesc.clicked.connect(sendImageAndDescription)
    dixit.sendVote.clicked.connect(sendVotedImage)
    dixit.sendImage.clicked.connect(sendImage)

    dixit.onlineUsers.setVisible(True)

    displayOnlineUsers()
    dixit.poolImagesList.setVisible(False)
    dixit.deckImagesList.setVisible(False)
    dixit.pointTable.setVisible(False)
    dixit.descriptionBox.setVisible(False)
    dixit.descriptionBoxLabel.setVisible(False)
    dixit.descriptionDisplay.setVisible(False)

    # Optional, resize window to image size

    dixit.show()
    app.exec_()
    

main()



