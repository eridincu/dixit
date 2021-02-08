# Listen TCP:

# 1. receive selected image from everyone
# 2. storyteller sends description
# 3. non-storytellers vote image
# 4. receive goodbye

# Send TCP:

# 1. send image X6 to everyone.
# 2. send 1 image at the begining of each round to everyone.

# Send UDP:

# 1. send online users.
# 2. send left users.
# 3. send who storyteller is
# 4. send description
# 5. send pool images
# 6. send end of round info:
#   a. points
#   b. who picked which image
#   c. storyteller's image
#   d. next storyteller?
# 7. start of new round message

import time

storyteller = ''
storyteller_image = ''
pool_images = {}
description = ''
online_users = {}
image_votes = {}
turn_points = {}

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
                        if dic["TYPE"] == "STORYTELLER_IMAGE":
                            storyteller_image = {dic["MY_IP"]: dic["PAYLOAD"]}
                            pool_images[dic["MY_IP"]] = dic["PAYLOAD"]
                        elif dic["TYPE"] == "CHOSEN_IMAGE":
                            pool_images[dic["MY_IP"]] = dic["PAYLOAD"]
                        elif dic["TYPE"] == "DESCRIPTION":
                            description = dic["PAYLOAD"]
                        elif dic["TYPE"] == "IMAGE_VOTE":
                            image_votes[dic["MY_IP"]] = dic["PAYLOAD"]
                        elif dic["TYPE"] == "GOODBYE":
                            del online_users(dic["MY_IP"])
                        else:
                            pass
            except socket.timeout:
                pass

            s.close()


# deck init / herkese 6 image gönder
for storyteller in user_list:
    storyteller_image = ''
    description = ''
    pool_images.clear()
    # start of round.
    # send UDP / tell who storyteller is to everyone.
    print(storyteller)
    time.sleep(5)
    
    # wait for storyteller's image and description.
    while storyteller_image == '' or description == '': # description and image arrive at the same time.
        time.sleep(0.2)
        pass # if server waits more than 30 sec, storyteller duty passes on to the next client.
    pool_images[storyteller] = storyteller_image

    # send udp / send the description, wait for chosen images from other clients
    while len(pool_images) != len(online_users):
        time.sleep(0.2)
        pass

    # send udp / send pool images to clients in shuffled order.
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

    # send udp / send point table.
    # end of turn.
    # herkese 1 image gönder


    # non-storytellers whose images are selected by someone get 1 point.




        
