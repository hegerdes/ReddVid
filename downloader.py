import subprocess
import json
import uuid
import os
import requests
from bs4 import BeautifulSoup
import helper.constants as const


if not os.path.exists(const.tmp_path):
    os.makedirs(const.tmp_path)

headers = {'User-Agent':'Mozilla/5.0'}

def getAVurl(url: str) -> tuple[str]:
    response = requests.get(url,headers = headers)

    post_id = url[url.find('comments/') + 9:]
    post_id = f"t3_{post_id[:post_id.find('/')]}"

    if(response.status_code == 200):
        soup = BeautifulSoup(response.text,'lxml')
        required_js = soup.find('script',id='data')

        json_data = json.loads(required_js.text.replace('window.___r = ','')[:-1])
        title = json_data['posts']['models'][post_id]['title']
        title = title.replace(' ','_')
        dash_url = json_data['posts']['models'][post_id]['media']['dashUrl']
        height  = json_data['posts']['models'][post_id]['media']['height']
        dash_url = dash_url[:int(dash_url.find('DASH')) + 4]

        # the dash URL is the main URL we need to search for
        # height is used to find the best quality of video available
        video_url = f'{dash_url}_{height}.mp4'
        audio_url = f'{dash_url}_audio.mp4'
        return(video_url, audio_url)
    else:
        raise LookupError('Unable to find video url')


def downloadAV(video_url: str, audio_url: str) -> tuple[str]:
    v_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, video_url)) + '.mp4'
    a_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, audio_url)) + '.mp3'
    with open(const.tmp_path + v_id,'wb') as file:
        print('Downloading Video...',end='',flush = True)
        response = requests.get(video_url,headers=headers)
        if(response.status_code == 200):
            file.write(response.content)
            print('\rVideo Downloaded...!')
        else:
            print('\rVideo Download Failed..!')

    with open(const.tmp_path + a_id,'wb') as file:
        print('Downloading Audio...',end = '',flush = True)
        response = requests.get(audio_url,headers=headers)
        if(response.status_code == 200):
            file.write(response.content)
            print('\rAudio Downloaded...!')
        else:
            print('\rAudio Download Failed..!')
            a_id = 'none'

    return (v_id,a_id)

def combineAV(video_path: str, audio_path: str):
    # Handle no audio clips
    if (audio_path == 'none'):
        return const.tmp_path + video_path
    # Create new UID and merge video and audio with ffmpeg
    av_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, video_path + audio_path)) + '.mp4'
    subprocess.call(['ffmpeg','-y','-i',const.tmp_path + video_path,'-i',const.tmp_path + audio_path,'-map','0:v','-map','1:a','-c:v','copy',const.tmp_path + av_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return const.tmp_path + av_id