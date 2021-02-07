# SEND TCP:

# 1. selected image
# 2. storyteller sends description
# 3. non-storytellers vote image
# 4. goodbye

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
import sys

MY_LOCAL_IP = ""
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

def window():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setGeometry(500, 500, 500, 500)
    main_window.setWindowTitle("Dixit Game!")
    
    
    new_push_button = QPushButton("reset", main_window)
    new_push_button.setGeometry(150, 20, 80, 30)
    
    main_window.show()
    sys.exit(app.exec_())


def changeWindow(win):
    win.hide()

print("hello ")
window()
message = {
    "NAME": "",
    "MY_IP": "",
    "TYPE": "",
    "PAYLOAD": ""
    }

def get_packet(name, sender_ip, packet_type, payload=''):
    packet = {
        'NAME': name,
        'MY_IP': sender_ip,
        'TYPE': packet_type,
        'PAYLOAD': payload,
    }

    return packet

def conv_to_bytes(message_):
    byte_message = (str(message_)+"\n").encode('utf-8')
    return byte_message

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
                story_teller_ip = dic["PAYLOAD"]
            elif dic["TYPE"] == "POINT_TABLE":
                # point table format : user_ip1,point1_?_user_ip2,point2_?_...
                temp_point_table = dic["PAYLOAD"]
                temp_user_point_list = temp_point_table.split('_?_')
                for x in temp_user_point_list:
                    temp_user_info = x.split(',')
                    point_table[temp_user_info[0]] = temp_user_info[1]
            elif dic["TYPE"] == "POOL_IMAGES":
                # point table format : image1,image2,image3, ...
                pool_images.clear()
                temp_pool_images = dic["PAYLOAD"]
                pool_images_list = temp_pool_images.split(',')
                for x in pool_images_list:
                    pool_images.append(x)
            elif dic["TYPE"] == "DESCRIPTION":
                description = dic["PAYLOAD"]
            else:
                pass
        except socket.timeout:
            pass
        s.close()