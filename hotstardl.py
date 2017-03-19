import sys
import requests
import time
import json
import os
import const
import argparse
from clint.textui import prompt
from lib import err, info

def getVideoId(url):
    if "hotstar.com/" in url:
        video_id = url.split("/")[-1]
        if len(video_id) == 10  and int(video_id):
            return video_id
        else:
            return
    elif len(url) == 10 and int(url):
        return url
    else:
        return
        


def getVideoFileUrl(video_id):
    title_url = const.BASEURL.format(video_id)
    video_resp = requests.get(title_url, headers=const.HEADERS)
    if video_resp.status_code != requests.codes.ok:
        err("Failed to get URL")
        return
    result = video_resp.json()
    content_info = result['resultObj']['contentInfo'][0]
    # Video Details
    vid_title = content_info['contentTitle'].replace(" ", "-")
    vid_episode = content_info['episodeNumber']
    vid_ep_title = content_info['episodeTitle'].replace(" ", "-")

    info("You are downloading \"{0}\"".format(vid_title))

    # Downloading actual content now
    file_url = const.CDNURL.format(video_id)
    cdn_resp = requests.get(file_url, headers=const.HEADERS)
    if cdn_resp.status_code != requests.codes.ok:
        err("Failed to get info about content")
        return
    cdn_content = cdn_resp.json()['resultObj']
    src = cdn_content['src']

    file_url = src.replace("http", "hlsvariant://http")
    file_url = file_url.replace("2000,_STAR.", "2000,3000,4500,_STAR.")
    info(file_url)
    
    if (vid_title):
        localFile = str(vid_title)
    if (vid_episode):
        localFile += "_" + str(vid_episode)
    if (vid_ep_title):
        localFile += "_" + str(vid_ep_title)
    localFile += ".mp4"
    localFile = localFile.replace("'", '-')
    localFile = localFile.replace('"', '-')
    localFile = localFile.replace('(', '-')
    localFile = localFile.replace(')', '-')
    return file_url, localFile
    

def main(video_id=None, quality=None, saveOrStream='D'):

    if not video_id:
        idstr = prompt.query("Enter the video ID: ")
        video_id = getVideoId(idstr)
        if not video_id:
            err('invalid video id entered')
            return
    try:
        file_url, localFile = getVideoFileUrl(video_id)
    
        info("Downloading with filename: {0}".format(localFile))
    
        if not quality:
            video_options = "1080p (best), 180p (worst), 234p, 360p, 404p, 720p, 900p"
            quality = prompt.query("Enter quality {0}: ".format(video_options))
        
        if not saveOrStream:
            choice = prompt.query("Enter 'S' to Stream and 'D' to Download ")
        else:
            choice = saveOrStream    

        command = "livestreamer \"{0}\" \"{1}\" ".format(file_url, quality)
        if choice == "D" or choice == 'd':
            command += "-o \"{0}\"".format(localFile)
        elif choice == "S" or choice == 's':
            info("Streaming ...")
        else:
            err("Invalid command")
            return

        info("Starting system command : {0}".format(command))
        os.system(command)
    except Exception as e:
        err(str(e))
        
if __name__ == "__main__":
    if len(sys.argv) <2:
        main()
    else:
        parser = argparse.ArgumentParser(description='tool to stream and \
        download Hotstar videos')

        parser.add_argument('-u', '--url', default=None, help='video url or id')
        parser.add_argument('-q','--quality',  default=None,
                            help='video quality. 1080p (best), 180p (worst),\
                             234p, 360p, 404p, 720p, 900p')
        parser.add_argument('-c', '--choice',  default=None,
                            help="'D' for downloading 'S' for streaming")

        args = parser.parse_args()
        if args.url:
            video_id = getVideoId(args.url)
        else:
            video_id = None
        main(video_id=video_id, quality=args.quality, saveOrStream=args.choice)
