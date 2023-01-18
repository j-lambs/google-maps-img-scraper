import re
import requests

# constant vars
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}
maxPX = '2000'

link = 'https://www.google.com/maps/contrib/114598947622868520820'

# http request page
r = requests.get(url=link, headers=headers)
pageHTML = r.text

# find all image links on google map page
imgList = re.findall('\"(https://lh5\.googleusercontent\.com.*?)\"', pageHTML)

# fix links from http request
newImgList = []
toRemove = r'\\u003d'
for imgs in imgList:
    imgs = imgs.replace(toRemove, '=') # replace '\\u003d' with '='
    imgs = imgs.strip('\\')            # remove trailing backslash
    
    imgs = re.sub('=w[^-]*', f'=w{maxPX}', imgs) # resize width to max px
    imgs = re.sub('-h[^-]*', f'-h{maxPX}', imgs)  # reszie height to max px
    newImgList.append(imgs)

for imgs in newImgList:
    print(imgs)

for i in range(len(newImgList)):
    img_data = requests.get(newImgList[i]).content
    with open(f'{i}.jpg', 'wb') as handler:
        handler.write(img_data)
