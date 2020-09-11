import sys
import argparse

from mildom_dl.mildomDL import MildomDL

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',required=True,help="mildom video url")
    parser.add_argument('-s','--start',type=int,help="video start secs")
    parser.add_argument('-e','--end',type=int,help="video end secs")
    parser.add_argument('-o','--output',required=True,help="video outputpath")


    args = parser.parse_args()
    print(args)
    mdl = MildomDL(url=args.url)
    start = args.start
    if start == None:
        start = 0
    mdl.download(args.output,start=start,end=args.end)
