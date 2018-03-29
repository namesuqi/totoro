# coding=utf-8
# test scenes design
from misc.tools.vod_strategy.const import FILE_ID_NOT_EXIST, FILE_ID_EXIST

REPORT_FILE_SCENES = {
    "Case-1: sdk report not exist file status": [FILE_ID_NOT_EXIST, 20, ["downloading", "interrupt", "done"]],
    "Case-2: sdk report exist file with done": [FILE_ID_EXIST, 10, ["done"]],
    "Case-3: sdk report exist file without done": [FILE_ID_EXIST, 20, ["downloading", "interrupt", "none"]]
}
# report_file_scenes {"scene": [file_id, peer_num, file_status_list]}
# Case-1(tc-1349 & tc-1315): 节点汇报不存在文件(downloading, interrupt, done), 预期：不添加到雷锋池中，下发delete task
# Case-2(tc-1313): 节点汇报文件（该文件存在）缓存done，预期：节点被添加到雷锋池
# Case-3(tc-1314): 节点汇报文件（该文件存在）缓存downloading, interrupt, none时，预期：该节点不会被添加到雷锋池


