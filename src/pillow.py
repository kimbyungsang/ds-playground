import requests
from PIL import Image
import hashlib

url = 'https://cdn.trixoli.com/hokkaido-feature.png'
r = requests.get(url, stream=True).raw

img = Image.open(r)
img.show()
img.save('src.png')

BUF_SIZE = 1024
with open('src.png', 'rb') as sf, open('dst.png', 'rb') as df:
    while True:
        data = sf.read(BUF_SIZE)
        if not data:
            break
        df.write(data)

sha_src = hashlib.sha256()
sha_dst = hashlib.sha256()

with open('src.png', 'rb') as sf, open('dst.png', 'rb') as df:
    sha_src.update(sf.read())
    sha_dst.update(df.read())

print("src.png's hash is {}".format(sha_src))
print(f"dst.png's hash is {sha_dst}")
