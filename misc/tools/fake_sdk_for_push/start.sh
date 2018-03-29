#!/usr/bin/env bash
sdk_num=$1
fid_start=$2
rm -rf /home/admin/JKZ/log/
mkdir /home/admin/JKZ/log/
if [ $# == $3 ]
then
fid_end=$3
i=${fid_start}
while [[ ${i} -lt ${fid_end} ]]
do
cd /home/admin/JKZ/log/
python /home/admin/JKZ/fake_sdk.py ${sdk_num} ${i} &
pid_array[$i]=$!
let "i++"
done
echo ${pid_array[@]} > /home/admin/JKZ/pids
else
cd /home/admin/JKZ/log/
python /home/admin/JKZ/fake_sdk_random.py ${sdk_num} ${fid_start} &
pid_array[$i]=$!
echo ${pid_array[@]} > /home/admin/JKZ/pids
fi