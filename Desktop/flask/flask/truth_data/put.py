from requests import put,get,post

warehouse={}

warehouse_list=["shanghai","beijing"]
px = 34
py = 56
receive = 60
send = 90
storage = 80

for wh_i in warehouse_list:
    warehouse[wh_i]={}
    warehouse[wh_i]["position"]=[px,py]
    warehouse[wh_i]["send"]=send
    warehouse[wh_i]["receive"]=receive
    warehouse[wh_i]["storage"]={}
    warehouse[wh_i]["storage"]["通用"]=storage

print(warehouse)

put("http://192.168.204.132:5000/infer/status/2016-10-01")
