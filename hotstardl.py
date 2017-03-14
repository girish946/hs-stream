import requests
import time
import json
import os
from clint.textui import prompt
import const
from lib import err, info


def main():
    video_id = prompt.query("Enter the video ID: ")
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

    file_url = src.replace("https", "hlsvariant://https")
    file_url = file_url.replace("2000,_STAR.", "2000,3000,4500,_STAR.")

    if (vid_title):
        localFile = str(vid_title)
    if (vid_episode):
        localFile += "_" + str(vid_episode)
    if (vid_ep_title):
        localFile += "_" + str(vid_ep_title)
    localFile += ".mp4"

    info("Downloading with filename: {0}".format(localFile))
    video_options = "1080p (best), 180p (worst), 234p, 360p, 404p, 720p, 900p"
    quality = prompt.query("Enter quality {0}: ".format(video_options))

    choice = prompt.query("Enter 'S' to Stream and 'D' to Download ")

    command = "livestreamer \"{0}\" \"{1}\" ".format(file_url, quality)
    if choice == "D" or choice == 'd':
        command += "-o {0}".format(localFile)
    elif choice == "S" or choice == 's':
        info("Streaming ...")
    else:
        err("Invalid command")
        return

    info("Starting system command : {0}".format(command))
    os.system(command)

if __name__ == "__main__":
    main()
