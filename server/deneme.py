online_users = {
  "1st": "birinci",
  "2st": "iki",
  "3st": "üç",
  "4st": "döto",
  "5st": "beş",
}
storyteller = "1st"
storyteller_image = "resim1"


image_votes = {
  "2st": "resim1",
  "3st": "resim2",
  "4st": "resim5",
  "5st": "resim2",
}

pool_images = {
  "1st": "resim1",
  "2st": "resim2",
  "3st": "resim3",
  "4st": "resim4",
  "5st": "resim5",
}

turn_points = {}

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
        turn_points[user] = 0

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

print(turn_points)