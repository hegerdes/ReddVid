import subprocess
import json
import uuid
import os
import logging
import requests
import helper.constants as const

headers = {'User-Agent':'Mozilla/5.0'}
if not os.path.exists(const.tmp_path):
    os.makedirs(const.tmp_path)

def getAVurl(url: str) -> tuple[str]:
    response = requests.get(url + '.json',headers = headers)

    if(response.status_code == 200):
        data = response.json()[0]['data']
        mainPost = data['children'][0]

        title = mainPost['data']['title'].strip().replace(' ','_')
        media = mainPost['data']['media']['reddit_video']
        vidURL = media['fallback_url']
        audURL = None
        if(media['has_audio']):
            audURL = vidURL.rsplit('/', 1)[0] + '/DASH_audio.mp4'
        logging.info('For url {} found media {} {}'.format(url, vidURL ,audURL))

        return (vidURL, audURL)
    else:
        raise LookupError('Unable to find video url')

def downloadAV(video_url: str, audio_url: str = None) -> tuple[str]:
    a_id = v_id = None
    v_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, video_url)) + '.mp4'
    with open(const.tmp_path + v_id,'wb') as file:
        print('Downloading Video...',end='',flush = True)
        response = requests.get(video_url,headers=headers)
        if(response.status_code == 200):
            file.write(response.content)
            print('\rVideo Downloaded...!')
        else:
            print('\rVideo Download Failed..!')

    if(audio_url):
        a_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, audio_url)) + '.mp3'
        with open(const.tmp_path + a_id,'wb') as file:
            print('Downloading Audio...',end = '',flush = True)
            response = requests.get(audio_url,headers=headers)
            if(response.status_code == 200):
                file.write(response.content)
                print('\rAudio Downloaded...!')
            else:
                print('\rAudio Download Failed..!')
                a_id = 'none'
    return (v_id, a_id)

def combineAV(video_path: str, audio_path: str):
    # Handle no audio clips
    if (audio_path == 'none'):
        return const.tmp_path + video_path
    # Create new UID and merge video and audio with ffmpeg
    av_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, video_path + audio_path)) + '.mp4'
    subprocess.call(['ffmpeg','-y','-i',const.tmp_path + video_path,'-i',const.tmp_path + audio_path,'-map','0:v','-map','1:a','-c:v','copy',const.tmp_path + av_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return const.tmp_path + av_id
