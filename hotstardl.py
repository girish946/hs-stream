import requests
import time
import json
import os

headers = {'User-Agent': 'custom user agent'}

vidId = raw_input("enter the video id ")

title = "http://account.hotstar.com/AVS/besc?action=GetAggregatedContentDetails&channel=PCTV&contentId={0}".format(vidId)

video_resp = requests.get(title, headers=headers)
video = json.loads(video_resp.content)

#print video
resultObj = video['resultObj']
contentInfo = resultObj['contentInfo'][0]
print type(contentInfo), len(contentInfo)

vid_title = contentInfo['contentTitle'].replace(" ", "-")
vid_episode = contentInfo['episodeNumber']
vid_ep_title = contentInfo['episodeTitle'].replace(" ", "-")
print vid_title, vid_episode, vid_ep_title

fileUrl = "http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=TABLET&id={0}&type=VOD".format(vidId)
remoteFile = requests.get(fileUrl, headers=headers)

remoteRespFile = json.loads(remoteFile.content)
#print remoteRespFile

resultObj = remoteRespFile['resultObj']
src = resultObj['src']

#print src

fileUrl = src.replace("https", "hlsvariant://https")

fileUrl = fileUrl.replace("2000,_STAR.","2000,3000,4500,_STAR.")

print fileUrl

localFile =  str(vid_title)+"-"+str(vid_episode)+"-"+str(vid_ep_title)+".mp4"
print localFile

quality = raw_input("enter the quality ")

choice = raw_input("Enter 'S' to Stream and 'D' to Download ")

if choice == "D":
    command = "livestreamer \"{0}\" \"{1}\" -o {2}".format(fileUrl, quality, localFile)
    os.system(command)
elif choice == "S":
    command = "livestreamer \"{0}\" \"{1}\" ".format(fileUrl, quality)
    os.system(command)
else:
    print "invalid command"

