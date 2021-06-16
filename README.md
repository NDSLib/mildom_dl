# Mildom_dl

this project is currently under development.

([日本語](https://github.com/NDSLib/mildom_dl/blob/master/README-JA.md)/English)

## How to install mildom_dl

```bash
$ pip3 install git+https://github.com/NDSLib/mildom_dl
```


## TODO
- [x] archive download
- [x] live download
- [x] command support
- [ ] Resolution Change support

## Usage

 video
```bash
$ mildom-dl -u https://www.mildom.com/playback/10738086?v_id=10738086-1598025891 -o out.mp4
```

 live
```bash
$ mildom-dl -u https://www.mildom.com/10038177 -o out.mp4
```

or 

```py
from mildom_dl.mildomDL import MildomDL

mdl = MildomDL(url="https://www.mildom.com/playback/10738086?v_id=10738086-1598025891")
mdl.download("test.mp4")
```

### 切り抜いて保存(not working)

args :
    -s : start（seconds)
    -e : end (seconds)


```bash
$ mildom-dl -u https://www.mildom.com/playback/10738086?v_id=10738086-1598025891 -s 30 -e 530 -o out.mp4
```
or 
```py
...
mdl.download("test.mp4",start=30,end=530)
```

# args
```
-u URL
-o output filename

-s start time (seconds)
-e end time (seconds)
```
