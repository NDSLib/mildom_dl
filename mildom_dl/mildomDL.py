import ffmpeg
import json
import animation
# from ffmpy import FFmpeg
import tempfile
import urllib.request
import requests
from urllib.parse import urlparse
from tqdm import tqdm
import os
from dataclasses import dataclass
import re
import shutil
from time import sleep

import logging
import coloredlogs

formatter = "[%(asctime)s] [%(levelname)8s]: %(message)s (%(filename)s:%(lineno)s)"
Logger = logging.getLogger()
coloredlogs.install(level='DEBUG', logger=Logger, fmt=formatter)
Logger.debug('Logger loaded')


class MildomDL:
    def __init__(self, url):
        self.url = url
        if not self.is_mildom_url(url):
            raise Exception("A URL other than Mildom has been detected.")

        self.isLive = False

        info = self.info()
        self.user_id = info.user_id
        self.video_id = info.video_id

        Logger.info("video_id: " + self.video_id)
        Logger.info("user_id : " + self.user_id)

    def is_mildom_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == "www.mildom.com":
            return True
        return False

    def info(self):
        video_id = ""
        user_id = ""
        try:
            # uID_vID_index = re.search(r"playback/", self.url).span()[1]
            # sep_url = self.url.replace("/", "")
            # uID_vID_l = sep_url[uID_vID_index:].split("?v_id=")
            # video_id = uID_vID_l[1]
            # user_id = uID_vID_l[0]
            uID_vID_index = re.search(r"playback/", self.url).span()[1]
            uID_vID_l = self.url[uID_vID_index:].split("/")
            video_id = uID_vID_l[1]
            user_id = uID_vID_l[0]
        except AttributeError:
            self.isLive = True
            uID_vID_index = re.search(r"mildom.com/", self.url).span()[1]
            user_id = self.url[uID_vID_index:].replace("/", "")

            # itms = self.url.split("/")
            # if itms[-1] == "":
            #     itms.pop(-1)
            # video_id = itms[-1]
            # user_id = itms[-2]

        return VideoData(user_id=user_id, video_id=video_id)

    # FIXME
    def get_title(self):
        return "video"

    def download(self, path="aaaj:.mp4", start=0, end=None, override=False):
        if override:
            os.remove(path)
        else:
            if os.path.isfile(path):
                # raise Exception("The file already exists.,ファイルが既に存在します。")
                print("The file already exists.,ファイルが既に存在します。")
                sleep(0.01)  # Loggerとかぶる
                yn = input("override? [y/N] >")
                if yn == "y":
                    os.remove(path)
                else:
                    exit()

        if end is None and start == 0:
            isAllVideo = True

        if self.isLive:
            self.__live_download(path)
        else:
            self.__archive_download(path)

        if isAllVideo:
            # shutil.move(download_filename,path)
            return
        else:
            cut_lasttime = end - start
            ffmpeg.input(download_filename).output(path, t=cut_lasttime, ss=0).run(capture_stdout=False,
                                                                                   capture_stderr=False)
        print("Done!")

    @animation.wait(("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"), text="Downloading  ", speed=0.1)
    def __live_download(self, path, quality="raw"):
        url = "https://cloudac.mildom.com/nonolive/gappserv/live/enterstudio?" \
              "__cluster=aws_japan&__platform=web&__la=ja&__user_id=0&__pcv=v2.8.44&timestamp=&sfr=pc&accessToken=" \
              f"&user_id={self.user_id}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
        try:
            anchor_live = body['body']['playback']["author_info"]['anchor_live']
            if anchor_live != 11:
                raise Exception("This user is not live　now. このユーザは現在ライブ中ではありません。")
        except KeyError:
            pass

        datas = body["body"]["realtime_playback_info"]["video_link"]
        datas_quality = [d['definition'] for d in datas]
        try:
            data_quality_index = datas_quality.index(quality)
        except ValueError:
            raise Exception(f"品質{quality} が見つかりませんでした。({', '.join(datas_quality)}) の中から選んでください。")
        #  === LIVE m3u8 URL ===
        m3u8URL = datas[data_quality_index].get("url")
        tmp_dir = tempfile.TemporaryDirectory()
        tmp_dir_name = tmp_dir.name
        try:
            (ffmpeg
             .input(m3u8URL)
             .output(tmp_dir_name + f"/test.mp4", preset='fast', movflags="frag_keyframe+empty_moov", c="copy",
                     **{"bsf:a": "aac_adtstoasc"}, pix_fmt='yuv420p', loglevel="quiet")
             .run()
             )
        except KeyboardInterrupt:
            print("ctrl + C pressed")
            # FIXME: moovが欠けてるため、全部再生できない(VLCではいけた。) https://qiita.com/kichiki/items/c6ad1cda80c00810928d
        except Exception as e:
            print(e)
        Logger.info(f"moving {tmp_dir_name}/{path} to {path}")
        (ffmpeg
         .input(tmp_dir_name + f"/test.mp4")
         .output(path, c="copy", loglevel="quiet")
         .run()
         )
        tmp_dir.cleanup()
        Logger.info("Done!")

    @animation.wait(("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"), text="Downloading  ", speed=0.1)
    def __archive_download(self, path):
        # FIXME ======================
        url = f"http://cloudac.mildom.com/nonolive/videocontent/playback/getPlaybackDetail?v_id={self.video_id}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
        # ==============================

        v_url = body["body"]["playback"]["source_url"]
        urllib.request.urlretrieve(v_url, path)
        Logger.info("Done!")

    def _videocut(video, last):
        pass


@dataclass
class VideoData:
    user_id: str
    video_id: str


# mdl = MildomDL(url="https://www.mildom.com/playback/10197093/10197093-c0hsn3d2lrnfdsc8tmgg")
# mdl = MildomDL(url="https://www.mildom.com/10105254")
# mdl.download(path="./test.mp4")

# mdl.download(path="./test.mp4",start=0,end=30)
