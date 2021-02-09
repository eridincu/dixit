# Dixit

## Contributors
- Fırat Bulut
- Hasan Demirkıran
- Mehmet Erdinç Oğuz

## About Game

### Game Description
Dixit is a game in which using a deck of cards illustrated with dreamlike images, players select cards that match a title suggested by the "storyteller", and attempt to guess which card the "storyteller" selected. Game can be played with 4-6 players.

### Scoring

[![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Dixit_points.jpg/220px-Dixit_points.jpg)](https://en.wikipedia.org/wiki/File:Dixit_points.jpg)

Scoring according to Dixit revised rules

The original rules were revised after publication.[[2]](https://en.wikipedia.org/wiki/Dixit_(card_game)#cite_note-2)

**If all players find the storyteller's card**

-   Storyteller: 0 points
-   Other players: 2 points

**If no players find the storyteller's card**

-   Storyteller: 0 points
-   Other players: 2 points (+1 bonus point per vote for his/her card)

**If at least 1 player, but not all players have found the storyteller's card**

-   Storyteller: 3 points
-   Players who found the card: 3 points (+1 bonus point per vote for his/her card)
-   Other players: 0 points (+1 bonus point per vote for his/her card)
    -   In the original rules, players who did not find the storyteller's card were ineligible for bonus points. In the revised rules, the other players receive +1 bonus point per vote for his/her card.

In the original rules, the winner is the first player to reach 30 points. In the revised rules, the winner is the player with the most points when the last card is drawn.

## Implementation Details

### Challenges

There were a few challenges during the implementation on our side.


- Workload Balancing:
  - We peer-programmed most of the code due to the remote situation, and because of the current situation in our university, all members weren't be available all the time. However, all team members gave their full effort to finish the project and peer-programming helped everyone to contribute to the project equally.
- Network: 
  - We decided to have server-based gameplay and handle game logic such as the point calculation, assigning the storyteller and giving players a deck of cards etc. in the hosting server. Using this design, the server knows all the information about the state of the game and informs players about them when necessary. The communication of common information(such as the images on the table, round points earned in each turn by each user etc.) between server and players about game is made using UDP packets to decrease the latency and for the sake of simplicity; whereas each player receives their decks in TCP packets since that information shouldn't be public. Users don't need to communicate any information with each other during the game since the server informs players about the state of the game; therefore, users only communicate with the server using TCP packets. By centralizing the game logic in one place, the game logic is consistent. 
  - Another challenge was to distribute cards among the players. We decided to have users keeping all the pictures in their local storage instead of sharing images among all the players each round, because that way the game will use less network traffic and the game can flow faster. Instead of sharing images, the server shares the names of the images with the players. 
  - We were planning to deploy the server using a cloud service; and therefore hardcoded the SERVER_IP value in the client code. However, we didn’t deploy the code to a cloud server hence the clients need to hardcode the SERVER_IP in the client directory __main.py__ file when they run the server, with the IP of the computer hosting server program.
- UI: 
   - We didn't have any prior knowledge about the Python GUI implementation. We found PyQt as a solution since each member of the team had some experience with that. We didn't manage to create the most artistic UI with our PyQt knowledge, but it served our purpose of creating a tabletop game quite well without causing any performance issues.


## Run the Game

The game requires at least 5 computers connected to the same network since we designed the program to work locally. One of the computers will be the server computer, whereas the others will be the clients playing the game. Server computers should be started to initialize the game and other computers can connect afterwards.
### Requirements
Before the start, please run the following command in the main directory:
> pip3 install -r requirements.txt

to install all the requirements for the game. You can also use ___pip___ instead of pip3.
> NOTE: If you run the game on _"Ubuntu"_ and receive an error related to not finding __xbc module__,  run the following command:  ___sudo apt-get install libxcb-xinerama0___

### Run the Game
There are two services in the main directory, which are __server__ and __client__. One computer should run the __main.py__ file in the __server__ directory and rest of the players should run the __main.py__ in the client directory with the following command after moving to the related directory:
> python3 main.py

After that, clients need to set the variable _SERVERIP_ in the code in __main.py__ file to the IP address of the PC which hosts the server program(main.py in server directory). Afterwards, enjoy the game!

## References
https://en.wikipedia.org/wiki/Dixit_(card_game)#:~:text=Using%20a%20deck%20of%20cards,game%20was%20introduced%20in%202008.


