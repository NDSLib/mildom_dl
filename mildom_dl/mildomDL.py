import ffmpeg
import json
# from ffmpy import FFmpeg
import tempfile
import urllib.request
from urllib.parse import urlparse
from tqdm import tqdm
import os
from dataclasses import dataclass
import re
import shutil

# https://www.mildom.com/playback/10738086?v_id=10738086-1598025891

VIDEO_CONTENT_BASE_URL = "https://cloudac.mildom.com/nonolive/videocontent/playback/getPlaybackDetail?v_id="

class MildomDL():
    def __init__(self,url):
        self.url = url
        if not self.isMildomURL(url):
            raise Exception("A URL other than Mildom has been detected.")

        self.isLive = False

        info = self.info()
        self.user_id = info.user_id
        self.video_id = info.video_id

    def isMildomURL(self,url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == "www.mildom.com":
             return True
        return False


    def info(self):
        if self.isLive:
            pass
        else:
            try:
                useridS = re.search(r"playback/", self.url).span()[1]
            except AttributeError:
                self.isLive = True
            #aida = re.search(r"\?v_id=", self.url).span()
            #useridE = aida[0]
            #videoidS = aida[1]
            #user_id = self.url[useridS:useridE]
            #video_id = self.url[videoidS::]
            #if video_id[-1] == "/":
            #    video_id = video_id[:-1]

            #video_content_url = VIDEO_CONTENT_BASE_URL + video_id

            #response = urllib.request.urlopen(video_content_url)
            #json_str = response.read().decode()
            #jsondata = json.loads(json_str)

            itms = self.url.split("/")
            if itms[-1] == "":
                itms.pop(-1)
            video_id = itms[-1]
            user_id  = itms[-2]

            

            return VideoData(user_id=user_id,video_id=video_id)

    # FIXME
    def get_title(self):
        return "video"

    def getm3u8(self):
     # https://d3ooprpqd2179o.cloudfront.net/vod/jp/10738086/10738086-1598025891/transcode/raw/10738086-1598025891-0_raw.m3u8
     # https://d3ooprpqd2179o.cloudfront.net/vod/jp/10658167/10658167-1599743721/transcode/raw/10658167-1599743721-0_raw.m3u8
        try:
            base_m3u8_url = "https://d3ooprpqd2179o.cloudfront.net/vod/jp/{user_id}/{video_id}/transcode/raw/{video_id}-0_raw.m3u8"
            url = base_m3u8_url.format(user_id=self.user_id,video_id=self.video_id)
            with urllib.request.urlopen(url) as response:
                print("m3u8 getted")
                return response.read().decode()
        except urllib.request.HTTPError as e:
            print("NOMAL LINK ERROR",e)
            base_m3u8_url = "https://d3ooprpqd2179o.cloudfront.net/vod/jp/{user_id}/{video_id}/origin/raw/{video_id}_raw.m3u8"
            url = base_m3u8_url.format(user_id=self.user_id,video_id=self.video_id)
            with urllib.request.urlopen(url) as response:
                return response.read().decode()
        except Exception as e:
            print(e)
            exit()
            


    def download(self,path="aaaj:.mp4",start=0,end=None):
        if os.path.isfile(path):
            raise Exception("The file already exists.,ファイルが既に存在します。")

        if self.isLive:
            print("live動画は対応していません。")
            return
        else:
            self.__archive_download(path)

        if isAllVideo:
            #shutil.move(download_filename,path)
            return
        else:
            cut_lasttime = end - start
            ffmpeg.input(download_filename).output(path,t=cut_lasttime,ss=0).run(capture_stdout=False, capture_stderr=False)
        print("Done!")

    def __live_download(self):
        pass

    def __archive_download(self, path):
        url = f"http://cloudac.mildom.com/nonolive/videocontent/playback/getPlaybackDetail?v_id={self.video_id}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
        v_url = body["body"]["playback"]["source_part_url"][0]["url"]

        urllib.request.urlretrieve(v_url, path)


        

    def _videocut(video,last):
        pass


@dataclass
class VideoData:
    user_id:str
    video_id:str




#mdl = MildomDL(url="url")
#mdl.download(path="./test.mp4")
#mdl.download(path="./test.mp4",start=0,end=30)
