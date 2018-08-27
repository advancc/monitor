"""
@version: 2.0
@author: 易培淮
@mail: yiph@ihep.ac.cn
@file: monitor.py
@time: 20180825
"""
#功能：获取linux进程信息

import subprocess
from pthread import Pthread
import re
import sys

def get_pid(app_name):
    # cmd_message= subprocess.check_output('ps aux |grep "'+app_name+'"|grep -v grep', shell=True).decode('utf-8')
    cmd = 'ps aux |grep "'+app_name+'"|grep -v grep'
    cmd_message = send_cmd(cmd)
    if cmd_message != "":
        pid = cmd_message.split()[1]
        return pid
    else:
        print(app_name+" is not running.")
        return -1

def send_cmd(cmd):
    try:
        msg = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as grepexc:
        # print ("error code", grepexc.returncode, grepexc.output)
        return ""
    else:
        return msg

def get_thread_msg(pid):
    cmd = "ps h -o ppid,pid,user,pcpu,pmem,rss,vsz,comm,time,stat,bsdstart -p " + pid
    cmd_message = send_cmd(cmd)
    return cmd_message

def monitor(app):
    pid = get_pid(app)
    if pid != -1:
        p =Pthread(pid)
        msg = get_thread_msg(pid)
        is_match = msg.split()
        p.setppid(is_match[0])
        p.setuser(is_match[2])
        p.setcpu(is_match[3])
        p.setmem(is_match[4])
        p.setrss(is_match[5])
        p.setvsz(is_match[6])
        p.setcommand(is_match[7])
        p.setruntime(transtime(is_match[8]))
        p.setstat(is_match[9])
        p.setstarttime(is_match[10])
        return 0,p.buildmessage()
    else:
        return 3,app+" is not running."

def transtime(runtime):
    regex_p = re.compile(r'((\d+)-)?((\d+):)?(\d+):(\d+)')
    is_match = regex_p.findall(runtime)
    newruntimestamp =0
    if is_match[0][1].strip():
        newruntimestamp += int(is_match[0][1])*86400
    if is_match[0][3].strip():
        newruntimestamp += int(is_match[0][3])*3600
    newruntimestamp += int(is_match[0][4])*60
    newruntimestamp += int(is_match[0][5])
    return newruntimestamp

def run(app_name_list,file_name):
    file = open(file_name, 'w')
    exit = 0
    for item in app_name_list:
        exitcode,msg = monitor(item)
        if exitcode != 3:
            file.write(msg)
        else:
            exit = 3
    return exit

if __name__== "__main__":
    exitcode = run(sys.argv[1],sys.argv[2])
    # 传参示例
    # exitcode = run(["/usr/sbin/acpid"], "tempfile.txt")
    print("exitcode:" + str(exitcode))
