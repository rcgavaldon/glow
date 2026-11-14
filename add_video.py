"""Attach a timelapse to an order:  python add_video.py G001 https://youtu.be/XXXX
Then push:  git add -A && git commit -m "G001 video" && git push"""
import json,sys
code,url=sys.argv[1].upper(),sys.argv[2]
d=json.load(open('orders.json'))
d.setdefault(code,{})['video']=url
json.dump(d,open('orders.json','w'),indent=2)
print('set',code,'->',url)
