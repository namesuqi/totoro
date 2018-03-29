# coding=utf-8
# author: Tang Hong
# file information

# local_hosts
stun_hub_ip = "192.168.1.245"
# push_ip = "192.168.1.200"
push_ip = "192.168.1.214"
# push_id = "52:54:00:09:24:CB"
push_hub_ip = "192.168.1.244"
cppc = 1
file_type = "bigfile"
authority = "no"

# SDK and its peer_id
sdk_ip = "192.168.2.35"
peer_id = "0000000436E04668AE7EDDD3F4055039"

# ajax_distribute_url = "http://{0}:32717/ajax/distribute".format(sdk_ip)

# online_hosts
# push_hub_ip = "172.30.0.35"
# ajax_distribute_url = "http://stun-hub.ys-internal.com:8000/distribute_task"
# push_ip = "118.190.153.230"
# push_id = "00:16:3E:06:C3:A6"
getseeds_url = \
    "http://seeds.crazycdn.com/getseeds?pid=00000004F58149C4BC43D39632ECDA8D&fid=69FE050B3C1A42BB9FC43A1D36D6B03C"

# url for post distribute_task to stun-hub
url = "http://{0}:8000/distribute_task".format(stun_hub_ip)
# url = "http://stun-hub.ys-internal.com:8000/distribute_task"
ajax_lsm_url = "http://{0}:32717/ajax/lsm".format(sdk_ip)

download_url = "http://{0}:8001/download_tasks".format(push_hub_ip)
delete_url = "http://{0}:8001/delete_tasks".format(push_hub_ip)


file1 = {
    "file_id": "2C9FA37EBF534C84BD6797ECB981C4E8",
    "file_size": 172917700,
    "url": "http://vodtest.crazycdn.com/test/Ocean_2mbps.ts",
    "ppc": 32
}
file2 = {
    "file_id": "AD8B678ACC5545F0BFBD5BCFB4C20950",
    "file_size": 1447161183,
    "url": "http://c23.myccdn.info/5700a43ee59c295174180064b3819552/5a87b009/mp4/Avatar_20Mbps.mp4",
    "ppc": 304
}
file3 = {
    "file_id": "B5A010DA4CA240BBBFBED4A9423A7AC1",
    "file_size": 172917700,
    "url": "http://c23.myccdn.info/076c9b0081204412b0346d9beb486923/5abc4f25/mp4/Ocean_2mbps.ts",
    "ppc": 32
}
file4 = {
    "file_id": "0046CA8A07F14603ADEF2FC0B6991619",
    "file_size": 775134238,
    "url": "http://c23.myccdn.info/60c92d5eca5db242139b1e63b8d1ad41/5a51b856/mp4/piano.mp4",
    "ppc": 304
}
file5 = {
    "file_id": "057130AA6FD945969C23DE9711281AB1",
    "file_size": 11322052622,
    "url": "http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4",
    "ppc": 304
}
file6 = {
    "file_id": "6057130AA6FD945969C23DE9711281AB1",
    "file_size": 11322052622,
    "url": "http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4",
    "ppc": 304
}
file7 = {
    "file_id": "7057130AA6FD945969C23DE9711281AB1",
    "file_size": 11322052622,
    "url": "http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4",
    "ppc": 304
}
file8 = {
    "file_id": "8057130AA6FD945969C23DE9711281AB1",
    "file_size": 11322052622,
    "url": "http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4",
    "ppc": 304
}
file9 = {
    "file_id": "9057130AA6FD945969C23DE9711281AB1",
    "file_size": 11322052622,
    "url": "http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4",
    "ppc": 304
}
file10 = {
    "file_id": "A057130AA6FD945969C23DE9711281AB1",
    "file_size": 11322052622,
    "url": "http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4",
    "ppc": 304
}

