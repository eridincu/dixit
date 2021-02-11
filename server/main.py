import time
import random
import socket
import json
import os
import threading
from os import listdir
from os.path import isfile, join

def find_my_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP = "127.0.0.1"
    try:
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP

user_count = 2 # PLEASE PROVIDE USER COUNT. THE GAME AUTOMATICALLY STARTS WHEN THIS COUNT IS REACHED.
SERVER_IP = find_my_local_ip()
MY_LOCAL_IP = ''
MY_NAME = os.uname().nodename
storyteller = ''
storyteller_image = ''
pool_images = dict()
description = ''
online_users = dict()
image_votes = dict()
turn_points = dict()
ready_users = []
deck = dict()


def listen_tcp():
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SERVER_IP, 12345))
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
                        if dic["TYPE"] == "STORYTELLER_IMAGE":
                            global storyteller_image
                            storyteller_image = dic["PAYLOAD"]
                            pool_images[dic["MY_IP"]] = dic["PAYLOAD"]
                            print("storyteller image arrived.", storyteller_image)
                        elif dic["TYPE"] == "DISCOVER":
                            if len(online_users) < 6:
                                online_users[dic["MY_IP"]] = dic["NAME"]
                        elif dic["TYPE"] == "CHOSEN_IMAGE":
                            pool_images[dic["MY_IP"]] = dic["PAYLOAD"]
                        elif dic["TYPE"] == "DESCRIPTION":
                            global description 
                            description = dic["PAYLOAD"]
                            print("description arrived.", description)
                        elif dic["TYPE"] == "IMAGE_VOTE":
                            image_votes[dic["MY_IP"]] = dic["PAYLOAD"]
                        elif dic["TYPE"] == "READY":
                            ready_users.append(dic["MY_IP"])
                        elif dic["TYPE"] == "GOODBYE":
                            del online_users[dic["MY_IP"]]
                            # send a goodbye message to server via TCP.
                            send_UDP("GOODBYE", dic["MY_IP"])
                        else:
                            pass
            except socket.timeout:
                pass

            s.close()

def get_packet(packet_type, payload=''):
    packet = {
        'NAME': MY_NAME,
        'MY_IP': MY_LOCAL_IP,
        'TYPE': packet_type,
        'PAYLOAD': payload,
    }

    return packet

def init_whole_deck():
    image_names = [f for f in listdir("../images/dixit_cards") if isfile(join("../images/dixit_cards", f))]

    for name in image_names:
        deck[name] = False
    print("LOG: images are imported:", deck)

def broadcast_storyteller(storyteller_):
    send_UDP("STORYTELLER", storyteller_)
    print("LOG: storyteller sent,", storyteller_)

def broadcast_description(storyteller_, description_):
    send_UDP("DESCRIPTION", online_users[storyteller_] + " says that:  '" + description_ + "'")
    print("LOG: Sent the description of", storyteller_, ":", description_)

def broadcast_pool_images():
    payload = ""
    imgs = list(pool_images.values())
    random.shuffle(imgs)
    for img in imgs:
        payload = payload + img + ","
    if len(payload) > 0:
        payload = payload[:-1]
    send_UDP("POOL_IMAGES", payload)
    print("LOG: pool images:", payload)

def broadcast_point_table():
    payload = ""
    for key in turn_points.keys():
        payload = payload + key + "," + str(turn_points[key]) + "_?_"
    if len(payload) > 0:
        payload = payload[:-3]
    send_UDP("POINT_TABLE", payload)
    print("LOG: point table:", payload)

def broadcast_user_image_pairs():
    payload = ""
    for key in pool_images.keys():
        payload = payload + key + "," + pool_images[key] + "_?_"
    if len(payload) > 0:
        payload = payload[:-3]
    send_UDP("USER_IMAGE_PAIRS", payload)
    print("LOG: user image pairs:", payload)


# not sure if needed
def broadcast_next_turn():
    payload = ""
    send_UDP("NEXT_TURN", payload)
    print("LOG: next turn is sent.")

def broadcast_online_users():
    payload = ""
    print("len: ", len(online_users))
    for key in online_users.keys():
        payload = payload + key + "," + online_users[key] + "_?_"
    if len(payload) > 0:
        # remove last 3 characters _?_
        payload = payload[:-3] 
    # send the packet including online users
    send_UDP("ONLINE_USERS", payload)
    print("LOG: online users are sent:", payload)

def send_image(dest_ip_, dest_port_):
    payload = ""
    found = False
    while not found:
        image_name = random.choice(list(deck.keys()))
        if not deck[image_name]:
            deck[image_name] = True
            payload = image_name 
            found = True
    send_TCP("DECK_IMG", payload, dest_ip_, dest_port_)
    print("LOG: deck img is sent to:", online_users[dest_ip_], "with the image:", payload)

def send_init_deck(dest_ip_, dest_port_):
    count = 0
    payload = ""
    while count != 6:
        image_name = random.choice(list(deck.keys()))
        if not deck[image_name]:
            deck[image_name] = True
            count = count + 1
            payload = payload + image_name + ","

    payload = payload[:-1]
    send_TCP("DECK_INIT", payload, dest_ip_, dest_port_)
    print("LOG: deck init is sent to:", online_users[dest_ip_], "with the deck:", payload)


def send_UDP(type_, payload_):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', 0))
            s.settimeout(5) # ???
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
            packet = get_packet(type_, payload_)
            packet_bytes = json.dumps((packet)).encode('utf-8')
            s.sendto(packet_bytes, ('<broadcast>', 12345))
            print("ME(UDP): "+ payload_)
            s.close()
    except ConnectionRefusedError:
        print("unexpected offline client detected")

def send_TCP(type_, payload_, dest_ip_, dest_port_):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5) # ???
            s.connect((dest_ip_, dest_port_))
            packet = get_packet(type_, payload_)
            packet_bytes = json.dumps((packet)).encode('utf-8')
            s.send(packet_bytes)
            print("ME(TCP): "+ payload_)
            s.close()
    except ConnectionRefusedError:
        print("unexpected offline client detected")

listen_TCP_thread = threading.Thread(target=listen_tcp, name='tcp-thread', daemon=True)

listen_TCP_thread.start()

# GAME LOGIC
while len(online_users) < user_count:
    time.sleep(2)
    broadcast_online_users()

while len(online_users) != len(ready_users):
    print("ready users: ", ready_users, "online_users: ", online_users)
    time.sleep(2)

# everything is set, start the rounds
broadcast_next_turn()
# create the deck from the card directory
init_whole_deck()

user_list = list(online_users.keys())
# send the deck to all users
for user in user_list:
    send_init_deck(user, 12345)

i = -1
# deck init / herkese 6 image gönder -- DONE
while True:
    # choose player
    i = (i + 1) % len(user_list)
    storyteller = user_list[i]

    pool_images.clear()
    # start of round.
    # send UDP / tell who storyteller is to everyone. -- DONE
    broadcast_storyteller(storyteller)
    time.sleep(5)
    
    # wait for storyteller's image and description.
    start = time.time()
    user_timeout = False
    while storyteller_image == '' or description == '': # description and image arrive at the same time.
        print("image: ", storyteller_image, "  desc: ", description)
        time.sleep(1)
        print("desc and image not yet arrived.")
        if time.time() - start > 30:
            # if server waits more than 30 sec, storyteller duty passes on to the next client. --  DONE
            # broadcast_next_turn() # ???
            user_timeout = True
            break
    # move to next user
    if user_timeout:
        continue

    pool_images[storyteller] = storyteller_image

    # send udp / send the description, wait for chosen images from other clients
    broadcast_description(storyteller, description)

    while len(pool_images) != len(online_users):
        time.sleep(0.2)
        pass

    # send udp / send pool images to clients in shuffled order.
    broadcast_pool_images()

    while len(image_votes) != len(online_users)-1:
        time.sleep(0.2)
        pass

    # calculate points.
    right_voters = []
    for voter in image_votes.keys():
        if image_votes[voter] == storyteller_image:
            right_voters.append(voter)

    if len(right_voters) == len(online_users)-1:
        for user in right_voters:
            turn_points[user] = 2
        turn_points[storyteller] = 0

    elif len(right_voters) == 0:
        for user in online_users.keys():
            turn_points[user] = 2
        turn_points[storyteller] = 0

    else:
        for user in online_users:
            if user in right_voters:
                turn_points[user] = 3
            else:
                turn_points[user] = 0
        turn_points[storyteller] = 3

    for voter in image_votes.keys():
        if image_votes[voter] != storyteller_image:
            for image_owner in pool_images.keys():
                if pool_images[image_owner] == image_votes[voter]:
                    turn_points[image_owner] = turn_points[image_owner] + 1

    # send udp / send point table. --  DONE
    broadcast_point_table()
    broadcast_user_image_pairs()
    time.sleep(1)
    # end of turn. --  DONE
    broadcast_next_turn()
    description = ''
    storyteller_image = ''
    image_votes = dict()
    pool_images = dict()
    time.sleep(3)
    # herkese 1 image gönder -- DONE
    for user in user_list:
        send_image(user, 12345)

    # non-storytellers whose images are selected by someone get 1 point.




        
