# encoding=utf-8
# Author=JKZ
# 将所有log文件汇总写入Excel中，用于Origin绘图（有待更新）
import glob
import xlwt


def write_log_to_sheet(log_path=""):
    # stupid fun
    # 循环将log文件数据转入到Excel中
    f_log = open(log_path, 'r')
    all_lines = f_log.readlines()
    f_log.close()
    file_id = all_lines[0]
    raw_timestamp = eval(all_lines[2].split(",")[1])  # 日志中最小的timestamp
    f_xls = xlwt.Workbook()  # 创建工作簿

    sheet = f_xls.add_sheet(unicode(file_id[0:31]), cell_overwrite_ok=True)  # 创建sheet

    sdk_dict = {}
    k = 2
    for eachline in all_lines[2:]:
        # print eachline,
        s = eachline.split(",")  # FID-SDK NO., timestamp, req chunk_id, rsp status_code
        i = sdk_dict.get(s[0], 1)  # sheet行号，按FID-SDK NO.区分
        j = int(s[0].split("-")[-1])  # sheet列号，按FID-SDK NO.区分，每个SDK占3列，占k列
        if s[0] not in sdk_dict.keys():  # 第一行标识FID-SDK
            # print s[0]
            sheet.write_merge(0, 0, k*j, k*j + 1, s[0])

        relative_time = float(s[1]) - int(raw_timestamp)  # timestamp - raw_timestamp
        req_chunk_id = int(s[2])
        rsp_status_code = int(s[3])
        sheet.write(i, k*j, relative_time)
        sheet.write(i, k*j + 1, req_chunk_id)
        if k == 3:
            sheet.write(i, 3*j + 2, rsp_status_code)
        sdk_dict[str(s[0])] = i + 1

    f_xls.save('{0}.xls'.format(log_path.replace(".log", "")))  # 保存文件
    print "Finished."


def count_spent_time(log_path):
    f_log = open(log_path, 'r')
    all_lines = f_log.readlines()
    f_log.close()
    file_id = all_lines[0]
    file_info = all_lines[1]
    sdk_spent_dict = dict()
    for eachline in all_lines[2:]:
        msg = eachline.split(",")
        sdk_uuid = msg[0]
        timestamp = float(msg[1])
        if sdk_uuid not in sdk_spent_dict.keys():
            sdk_spent_dict[sdk_uuid] = [0, 1]  # [start_time, end_time]
            sdk_spent_dict[sdk_uuid][0] = timestamp
        else:
            sdk_spent_dict[sdk_uuid][1] = timestamp
    spent_time_list = list()
    for value in sdk_spent_dict.values():
        spent_time_list.append(value[1]-value[0])

    return spent_time_list

if __name__ == "__main__":
    # write_log_to_sheet("log/201712112113/10.log")
    gz_files = glob.glob("log\\201712131322_ppc2\\*.log")
    all_spent_time_list = list()
    for f in gz_files:
        s = f.replace("\\", "/")
        print s
        # write_log_to_sheet(s)
        one_list = count_spent_time(s)
        all_spent_time_list += one_list
    all_spent_time_list.sort()

    f_xls = xlwt.Workbook()  # 创建工作簿
    sheet = f_xls.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    for i in range(len(all_spent_time_list)):
        sheet.write(i, 0, all_spent_time_list[i])
        sheet.write(i, 1, i+1)
    f_xls.save('demo.xls')

    # f_log = open("test.log", 'w')
    # for i in all_spent_time_list:
    #     f_log.write(str(i))
    #     f_log.write("\n")
    # f_log.close()
