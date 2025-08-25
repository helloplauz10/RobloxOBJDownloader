import requests
import sys
import os

# https://devforum.roblox.com/t/roblox-cdn-how-to-work-out-the-hash/2731447
def getCDNURL(hash): # adjusted to getting the first 38 chars due to the "30DAY-" string
    i = 31
    for char in hash[:38]:
        i ^= ord(char)  # i ^= int(char, 16) also works
    return f"https://t{i%8}.rbxcdn.com/{hash}"

def downloadFile(url, output):
    with requests.get(url, stream=True) as req:
        with open(output, "wb") as f:
            for chunk in req.iter_content(chunk_size=2048):
                f.write(chunk)

username = sys.argv[1]
outputDir = sys.argv[2]

os.makedirs(outputDir, exist_ok = False)

userId = requests.post(f"https://users.roblox.com/v1/usernames/users", json = {
    "usernames": [username],
    "excludeBannedUsers": True
}).json()["data"][0]["id"]
print(f"User ID is {userId}")

avatarUrl = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-3d?userId={userId}").json()["imageUrl"]
print(f"Avatar properties url is {avatarUrl}")
avatarProperties = requests.get(avatarUrl).json()
objUrl = getCDNURL(avatarProperties["obj"])
mtlUrl = getCDNURL(avatarProperties["mtl"])
textureUrls = [getCDNURL(i) for i in avatarProperties["textures"]]
print(f"OBJ Url is {objUrl}")
print(f"Material Url is {mtlUrl}")
print(f"Texture urls are: {textureUrls}")

print("Downloading OBJ File")
downloadFile(objUrl, os.path.join(outputDir, f"{username}.obj"))
print("Downloading Material File")
downloadFile(mtlUrl, os.path.join(outputDir, f"{username}.mtl"))

count = 0
for texture in textureUrls:
    count += 1
    print(f"Downloading texture url {texture}")
    downloadFile(texture, os.path.join(outputDir, f"{username}{count}Tex.png"))

print("Done!")