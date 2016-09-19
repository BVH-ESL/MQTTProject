# test get JSON data form localhost by node.js
# kanitkon khancure 08/31/2016
import urllib, json
url = "http://localhost:3000/jsontest"
output = json.load(urllib.urlopen(url))
print output["payloadSize"]
print output["delay"]
