# Mildom_dl

this project is currently under development.


## TODO
- [x] archive download
- [ ] live download
- [ ] command support

## Usage

**※未対応**
```bash
$ mildom_dl -u https://www.mildom.com/playback/10738086?v_id=10738086-1598025891 -o out.mp4
```

or 

```py
from mildom_dl.mildomDL import MildomDL

mdl = MildomDL(url="https://www.mildom.com/playback/10738086?v_id=10738086-1598025891")
mdl.download("test.mp4")
```

### 切り抜いて保存

**※未対応**
```bash
$ mildom_dl -u https://www.mildom.com/playback/10738086?v_id=10738086-1598025891 -s 30 -e 530 -o out.mp4
```
or 
```py
...
mdl.download("test.mp4",start=30,end=530)
```
