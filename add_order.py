"""Register new order codes (shows 'being made' until a video is added):  python add_order.py G002 G003"""
import json,sys
d=json.load(open('orders.json'))
for c in sys.argv[1:]: d.setdefault(c.upper(),{"video":""})
json.dump(d,open('orders.json','w'),indent=2); print(sorted(d))
