# coding=utf-8
"""
script's author: guzehao
用于远程部署

操作MySQL的底层库
__author__ = 'liwenxuan'
             2017.03.02

e.g.
    db = MysqlDB()   创建对象db
    db.execute(sql).to_rows()       传入sql语句, 结果以[(),(),...]方式按行返回
    db.execute(sql).to_cols()       传入sql语句, 结果以[[], [],...]方式按列返回
    db.execute(sql).to_dict()       传入sql语句, 结果以[{}, {},...]方式以列名/别名为key, 将每行结果作为一个dict返回
    db.execute(sql).one_by_one()    传入sql语句, 结果以[ , ,...]方式先按行再按列一个个返回
    db.execute(sql).only_one()      传入sql语句, 当且仅当结果只有一行一列时, 直接返回
注:
    1. 当前不支持db.execute("select * from 多表连接").to_dict()
    2. sql语句中当数据表的列的数据类型为字符串类型时, 条件需要加'', 如 "select * from table where name = 'lucy'"

"""

import MySQLdb
import string
import time
import json
import os

MYSQL_USER = "ysboss"
MYSQL_HOST = "rm-m5ea8uwgi07hrcw2x.mysql.rds.aliyuncs.com"
MYSQL_PASSWORD = "Yunshang2014"
MYSQL_PORT = 3306
MYSQL_DATABASE = "boss"


class MysqlDB(object):
    def __init__(self, user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_DATABASE):
        start_time = time.time()
        print "Connect to MySQL database by {0}, it should be only call one time!!!".format(user)
        self._conn = MySQLdb.connect(host=host, user=user, passwd=password, port=port, db=db)
        self._cur = self._conn.cursor()
        end_time = time.time()
        print "Connection cost {0} seconds.".format(end_time - start_time)

    def __del__(self):
        self._conn.close()
        print "Disconnect to MySQL"

    def execute(self, sql_command):
        self.sql = sql_command.strip()
        if self.sql.startswith("select" or "SELECT"):
            self._cur.execute(self.sql)
            self._result = self._cur.fetchall()  # [tuple, tuple, ...]
            return self
        else:
            self._cur.execute(self.sql)
            self._conn.commit()
            time.sleep(1)
            print "Commit Successfully"

    def __has_alias__(self):
        # 选取sql语句中的列名
        start = string.find(self.sql, "select " or "SELECT ")
        end = string.find(self.sql, "from " or "FROM ")
        columns = self.sql[start + 6:end]
        # 判断列名是否为"*"
        if string.rfind(columns, " * ") == -1:
            cols = columns.split(", ")
        else:
            table_index = string.find(self.sql[end + 5:].strip(), " ")
            if table_index == -1:
                table_name = self.sql[end + 5:].strip()
            else:
                table_name = self.sql[end + 5:end + 5 + table_index]
            # 获取数据表的所有列名
            self._cur.execute("select COLUMN_NAME from information_schema.columns where table_name = '{0}'".format(table_name))
            self.rows = self._cur.fetchall()
            cols = []
            for row in self.rows:
                for col in row:
                    cols.append(col)

        # 判断是否有别名
        key_list = []
        for col in cols:
            has_alias = string.rfind(col.strip(), " ")
            if has_alias == -1:
                key_list.append(col.strip())
            else:
                key_list.append(col[has_alias + 1:].strip())

        return key_list

    def to_rows(self):
        # 将每行查询结果保存为list
        return [row for row in self._result]

    def only_one(self):
        # 当查询结果只有一行一列时, 直接输出结果
        if len(self._result) == 1:
            if len(self._result[0]) == 1:
                result = self._result[0][0]
                return result
            else:
                print "result:", self._result
                raise ValueError
        else:
            print "result:", self._result
            raise ValueError

    def to_dict(self):
        # 将每行查询结果以别名为key转换为dict, 并将结果保存为list
        results = []
        key_list = self.__has_alias__()
        if len(key_list) != 0:
            for row in self._result:
                result = {}
                for key in range(len(row)):
                    result[key_list[key]] = row[key]
                results.append(result)
        return results

    def to_cols(self):
        # 将每列查询结果转换为一个list, 并将结果保存为list
        results = []
        if len(self._result) != 0:
            for index in range(len(self._result[0])):
                result = [row[index] for row in self._result]
                results.append(result)
        return results

    def one_by_one(self):
        # 将查询结果先按行再按列地转换为一个个string, 并将结果保存为list
        return [result for row in self._result for result in row]

if __name__ == "__main__":
    db = MysqlDB()
    resp = db.execute("select id,hex(file_id),fsize,ppc,psize,start_bitrate,limit_bitrate,avg_bitrate,source from boss.ppc_tenant_files").to_rows()
    # print resp
    # print type(resp)    
    
    files_info_dict = dict()
    
    for i in resp:
        fid = i[0]
        source = i[8]
        file_id = i[1]
        fsize = i[2]
        ppc = i[3]
        psize = i[4]
        start_bitrate = i[5]
        limit_bitrate = i[6]
        avg_bitrate = i[7]
        
        file_info_dict = {
                            "file_id": file_id,
                            "fsize": fsize,
                            "ppc": ppc,
                            "psize": psize,
                            "start_bitrate": start_bitrate,
                            "limit_bitrate": limit_bitrate,
                            "avg_bitrate": avg_bitrate
                            }
    
        # print file_info_dict
    
        files_info_dict[source] = file_info_dict
    
    # print files_info_dict
    
    files_info_json = json.dumps(files_info_dict)
    # print files_info_json 
    f = open('/home/admin/tool/file_info.json', 'w')
    print "write "+str(files_info_json)+" to file_info.json"
    f.write(files_info_json)
    f.close
