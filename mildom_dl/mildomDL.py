import ffmpeg
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

class MildomDL():
    def __init__(self,url):
        self.url = url
        if not self.isMildomURL(url):
            raise Exception("おっと、これはミルダムのURLじゃないみたいだ。")

        self.isLive = False

        info = self.info()
        self.user_id = info.user_id
        self.video_id = info.video_id

    def isMildomURL(self,url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == "www.mildom.com":
             return True


    def info(self):
        if self.isLive:
            pass
        else:
            useridS = re.search(r"playback/", self.url).span()[1]
            aida = re.search(r"\?v_id=", self.url).span()
            useridE = aida[0]
            videoidS = aida[1]
            user_id = self.url[useridS:useridE]
            # FIXME urlのラストが"/"だった場合
            video_id = self.url[videoidS::]

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
                return response.read().decode()
        except urllib.request.HTTPError:
            base_m3u8_url = "https://d3ooprpqd2179o.cloudfront.net/vod/jp/{user_id}/{video_id}/origin/raw/{video_id}_raw.m3u8"
            url = base_m3u8_url.format(user_id=self.user_id,video_id=self.video_id)
            with urllib.request.urlopen(url) as response:
                return response.read().decode()


    def download(self,path="aaaj:.mp4",start=0,end=None):
        base_ts_url = "https://d3ooprpqd2179o.cloudfront.net/vod/jp/{user_id}/{video_id}/transcode/raw/{video_id}-0_raw{ts_id}.ts"
        base_ts_url = "https://d3ooprpqd2179o.cloudfront.net/vod/jp/{user_id}/{video_id}/origin/raw/{video_id}_raw-0000.ts"
        if self.isLive:
            print("live動画は対応していません。")
            return
        if os.path.isfile(path):
            raise Exception("The file already exists.,ファイルが既に存在します。")
        isAllVideo = False
        ts_paths = []
        if end is None:
            if start == 0:
                isAllVideo = True
            m3u8 = self.getm3u8()
            m3u8_splited = m3u8.split("\n")
            last_ts = m3u8.split("\n")[-3]
            print(last_ts)
            ls = re.search(r"raw",last_ts).span()[1]
            le = re.search(r".ts",last_ts).span()[0]
            end = str(ls)+str(le)
            print(end)
            end = int(end)

        #  4秒 ts
        start_time = start // 4
        end_time   = end //4

        ts_url = [base_ts_url.format(user_id=self.user_id,video_id=self.video_id,ts_id=ts_id) for ts_id in range(start_time,end_time+1)]

        tmp_dir = tempfile.TemporaryDirectory()
        tmp_dir_name = tmp_dir.name
        ts_files = []
        for index,url in tqdm(enumerate(ts_url)):
            filename = tmp_dir_name + '/'+ str(index) + ".ts"
            ts_files.append(filename)
            #urllib.request.urlretrieve(url, filename)
            try:
                data = urllib.request.urlopen(url, timeout=10).read()
                with open(filename, mode="wb") as f:
                    f.write(data)
            except urllib.request.HTTPError:
                print("VIDEO DOWNLOAD FORBIDDEN ERROR")
        print(ts_files)

        m3u8_dir = tmp_dir_name + "/tmp.txt"
        with open(tmp_dir_name + "/tmp.txt", "w") as fp:
            lines = [f"file '{line}'" for line in ts_files]
            fp.write("\n".join(lines))

        download_filename = tmp_dir_name + "/v.mp4"
        ffmpeg.input(m3u8_dir, f="concat", safe=0).output(download_filename, c="copy").run(capture_stdout=True, capture_stderr=True)    
        if isAllVideo:
            shutil.move(download_filename,path)
        else:
            cut_lasttime = end - start
            ffmpeg.input(download_filename).output(path,t=cut_lasttime,ss=0).run()
        tmp_dir.cleanup()
        print("Done!")

    def _videocut(video,last):
        pass


@dataclass
class VideoData:
    user_id:str
    video_id:str




#mdl = MildomDL(url="url")
#mdl.download(path="./test.mp4")
#mdl.download(path="./test.mp4",start=0,end=30)
