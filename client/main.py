# SEND TCP:

# 1. selected image
# 2. storyteller sends description
# 3. non-storytellers vote image
# 4. goodbye

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap

import sys
import mainWindow

SERVER_IP = ''
PORT = ''
MY_LOCAL_IP = ''
MY_NAME = ''
user_list = {}
deck_list = []
story_teller_ip = ''
point_table = {} # {user_ip=point, ...}
pool_images = [] # [image1,image2, ...]
description = ''


def find_my_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP = "127.0.0.1"
    try:
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP

class DixitApp(QtWidgets.QMainWindow, mainWindow.Ui_mainWindow):
    def __init__(self, parent=None):
        super(DixitApp, self).__init__(parent)
    
        pixmap = QPixmap('row-1-col-1.jpg')    
        mainWindow.Ui_mainWindow.dixitCoverImage.setPixmap(pixmap)


        self.setupUi(self)

def main():
    app = QApplication(sys.argv)
    dixit = DixitApp()

    label = QLabel("self", dixit)
    pixmap = QPixmap('row-1-col-1.jpg')
    label.setPixmap(pixmap)

    # Optional, resize window to image size

    dixit.show()
    app.exec_()

if __name__ == '__main__':
    main()

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

def getDescription():

    pass

def chooseImage():
    
    pass

def displayImage():

    pass

def voteImage():

    pass

def updatePointTable():

    pass

def listen_tcp():
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
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
                            deck_list.append(dic["PAYLOAD"])
                        elif dic["TYPE"] == "DECK_INIT":
                            # image format : image1,image2,...
                            temp_deck = dic["PAYLOAD"]
                            deck_image = temp_deck.split(',')
                            for x in deck_image:
                                deck_list.append(x)
                        else:
                            pass
            except socket.timeout:
                pass

            s.close()


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
                    user_list[temp_user_info[0]] = temp_user_info[1]
            elif dic["TYPE"] == "USER_LEFT":
                # user left format : user_ip
                left_user_ip = dic["PAYLOAD"]
                del user_list[left_user_ip]
            elif dic["TYPE"] == "STORYTELLER":
                # story teller fomat : story_teller_ip
                # start of a new round
                story_teller_ip = dic["PAYLOAD"]
                # display images with qt
                # display the storyteller's name with qt
                if story_teller_ip == MY_LOCAL_IP:
                    image_, description_ = chooseImage()  # returns name and description of the image.
                    send_TCP("STORYTELLER_IMAGE", image_)
                    send_TCP("DESCRIPTION", description_)
                else:
                    # do nothing
                    pass

            elif dic["TYPE"] == "POINT_TABLE":
                # point table format : user_ip1,point1_?_user_ip2,point2_?_...
                temp_point_table = dic["PAYLOAD"]
                temp_user_point_list = temp_point_table.split('_?_')
                for x in temp_user_point_list:
                    temp_user_info = x.split(',')
                    point_table[temp_user_info[0]] = temp_user_info[1]
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
            s.connect((SERVER_IP, PORT))
            packet = get_packet(type_, payload_)
            packet_bytes = json.dumps((packet)).encode('utf-8')
            s.send(packet_bytes)
            print("ME: "+ messagePayload)
            s.close()
    except ConnectionRefusedError:
        print("unexpected offline client detected")



