import requests
padlet_name = "singapore_itinerary"
padlet_username = "gallery"
myheader = {
    "Content-type": "application/json",
    "App-Id": "227cf1602fd752e8b4396068c61bb11e47141a3ef8a42fcbbcd01739823c137e",
    'Accept': '*/*'
}

padlets = requests.get(
      f'https://padlet.com/api/0.9/public_padlets?username={padlet_username}',
      headers=myheader,
      ).json()
for mypadlet in padlets["data"]:
    if mypadlet["name"] == padlet_name:
        mypadlet_id = mypadlet["id"]
        print("yes")
    else:
       print( {
                "body": "404 error, padlet not found",
                "padlet_name": padlet_name,
                "padlet_username": padlet_username
            })
