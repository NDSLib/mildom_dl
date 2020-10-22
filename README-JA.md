# Mildom_dl
開発中です。

(日本語/[English](https://github.com/NDSLib/mildom_dl/blob/master/README.md))

## インストール方法
```bash
$ pip3 install git+https://github.com/NDSLib/mildom_dl
```


## 使い方


```bash
$ mildom-dl -u https://www.mildom.com/playback/10738086?v_id=10738086-1598025891 -o out.mp4
```

or 

```py
from mildom_dl.mildomDL import MildomDL

mdl = MildomDL(url="https://www.mildom.com/playback/10738086?v_id=10738086-1598025891")
mdl.download("test.mp4")                                           
```

### 動画を切り抜いて保存


args :
    -s : 開始時間（秒)
    -e : 終了時間 (秒)


```bash
$ mildom-dl -u https://www.mildom.com/playback/10738086?v_id=10738086-1598025891 -s 30 -e 530 -o out.mp4
```
or 
```py
...
mdl.download("test.mp4",start=30,end=530)
```


# 引数
```
-u URL
-o 出力先ファイル名

-s 開始時間(指定しなくてもおｋ)
-e 終了時間(指定しなくてもおｋ)
```
