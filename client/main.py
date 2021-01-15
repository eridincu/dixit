# SEND TCP:

# 1. selected image
# 2. storyteller sends description
# 3. non-storytellers vote image
# 4. goodbye

message = {
    "NAME": username, 
    "MY_IP": own_ip, 
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
                            # TO DO
                            pass
                        elif dic["TYPE"] == "DECK_INIT":
							# TO DO
							pass
                        else:
                            # TO dO
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
            if dic["TYPE"] == "DISCOVER":
                # TO DO
                pass
            elif dic["TYPE"] == "GOODBYE":
                # TO DO
                pass
            elif dic["TYPE"] == "STORYTELLER":
                # TO DO
                pass
            elif dic["TYPE"] == "POINTS":
                # TO DO
                pass
            elif dic["TYPE"] == "POOL_IMAGES":
				# TO DO
				pass
			elif dic["TYPE"] == "DESCRIPTION":
				# TO DO
				pass
            #print("in broadcast")
        except socket.timeout:
            pass
        s.close()