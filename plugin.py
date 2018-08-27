import subprocess
import time
import sys
import re
from pthread import Pthread

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

def get_thread(tmpfile,scheduler=""):
#scheduler :"condor" or other else
    #get hostname

    hostname = subprocess.check_output("hostname",shell=True).decode('utf-8')
    #[0:-1] used for delete "/n"
    hostname = hostname[0:-1]
    print(hostname)
    #get system status
    #file_sys = open('./system_message.txt','w')

    #file_sys.close()

    #get pids
    cmd = "pstree -lp "+scheduler
    #open file in only write method
    file_thread = open(tmpfile,'w')
    #file_thread.write("ppid,time,pid,user,cpu,mem,vsz,rss,command,slotid,node,runtime,stat,startime\n")
    #file_thread.write("ppid,time,pid,user,cpu,mem,vsz,rss,command,slotid,node,runtime,stat,startime,kb_rd_s,kb_wr_s,kb_ccwr_s\n")
    #let shell execute command
    cmd_output = subprocess.check_output(cmd,shell=True)
    cmd_text = cmd_output.decode('utf-8')
    #find root
    regex_p = re.compile(r'\((\d+)\)-\+')
    is_match = regex_p.findall(cmd_text)
    if is_match:
        root_pid = is_match[0]
        print(root_pid)
        sub_root = is_match[1]
        print(sub_root)
    else:
        print ("can't find specific thread!")
        return 3
    #regex
    regex_p = re.compile(r'\w\((\d+)\)')
    #get all of pid
    pids = regex_p.findall(cmd_text)
    #print(pids)
    pthread = []
    #regex_p = re.compile(r'\s+(\d+)\s+(\d+)\s+(\w+)\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)\s+(\d+)\s+(\d+)\s+(\w+)\s+(\S+)\s+(\w+)\s+(\S+)')
    regex_io= re.compile(r'Average:\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)')
    for index,pid in enumerate(pids):
        #print(pid)
        pthread.append(Pthread(pid))
        pthread[index].setnode(hostname)
        pthread[index].settime(time.time())
        #get thread detail message
        cmd = "ps h -o ppid,pid,user,pcpu,pmem,rss,vsz,comm,time,stat,bsdstart -p "+pid

        cmd_pid_output = subprocess.check_output(cmd,shell=True)
        cmd_pid_text = cmd_pid_output.decode('utf-8')
        cmd_pid_text = cmd_pid_text.replace("<defunct>","")
        #is_match = regex_p.search(cmd_pid_text)
        if cmd_pid_text !="":

            is_match = cmd_pid_text.split()
            pthread[index].setppid(is_match[0])
            pthread[index].setuser(is_match[2])
            pthread[index].setcpu(is_match[3])
            pthread[index].setmem(is_match[4])
            pthread[index].setrss(is_match[5])
            pthread[index].setvsz(is_match[6])
            pthread[index].setcommand(is_match[7])
            pthread[index].setruntime(transtime(is_match[8]))
            pthread[index].setstat(is_match[9])
            pthread[index].setstarttime(is_match[10])
        else:
            pthread[index].setppid(pthread[index-1].getpid())
            pthread[index].setuser(pthread[index-1].getuser())
            pthread[index].setcpu(pthread[index-1].getcpu())
            pthread[index].setmem(pthread[index-1].getmem())
            pthread[index].setrss(pthread[index-1].getrss())
            pthread[index].setvsz(pthread[index-1].getvsz())
            pthread[index].setcommand(pthread[index-1].getcommand())
            pthread[index].setruntime(transtime(pthread[index-1].getruntime()))
            pthread[index].setstat(pthread[index-1].getstat())
            pthread[index].setstarttime(pthread[index-1].getstarttime())
        #print (cmd_pid_text)

        #cmd = "pidstat -d 1 1 -p "+pid

        #cmd_pid_output = subprocess.check_output(cmd,shell=True)
        #cmd_pid_text = cmd_pid_output.decode('utf-8')
        #is_match = regex_io.search(cmd_pid_text)
        #print(cmd_pid_text)
        #is_match = cmd_pid_text.split()
        #if is_match :
        #    pthread[index].setkb_rd_s(is_match.group(2))
        #    pthread[index].setkb_wr_s(is_match.group(3))
        #    pthread[index].setkb_ccwr_s(is_match.group(4))
        #else :
        #    pthread[index].setkb_rd_s(pthread[index-1].getkb_rd_s())
        #    pthread[index].setkb_wr_s(pthread[index-1].getkb_wr_s())
        #    pthread[index].setkb_ccwr_s(pthread[index-1].getkb_ccwr_s())
            #pthread[index].setiodelay(is_match.group(6))
        #get slotid
        chkppid = 0
        if pthread[index].getppid() == sub_root:
            chkppid = index
            cmd = "cat /proc/"+str(pid)+"/cmdline"
            cmd_pid_output = subprocess.check_output(cmd,shell=True)
            cmd_pid_text = cmd_pid_output.decode('utf-8')
            regex = re.compile(r'slot(\d+)')
            is_match = regex.search(cmd_pid_text)
            if is_match:
                pthread[index].setslotid(is_match.group(1))
        else :
            for offset in range(1,index-chkppid):
                if pthread[index].getppid() == pthread[index-offset].getpid():
                    pthread[index].setslotid(pthread[index-offset].getslotid())
                    break
            #pthread[index].setslotid(cmd_pid_text[])
    for index in range(len(pthread)):
        if index > 2 :
            if index == len(pthread)-1 or pthread[index].getpid() != pthread[index+1].getppid():
                pthread[index].setleaf(1)
                cmd = "readlink -f /proc/"+pthread[index].getpid()+"/exe"
                cmd_abpath_output = subprocess.check_output(cmd,shell=True)
                cmd_abpath_text = cmd_abpath_output.decode('utf-8')
                pthread[index].setcmdabpath(cmd_abpath_text.strip())
        file_thread.write(pthread[index].buildmessage())



    file_thread.close()
    return 0


if __name__=="__main__":
    #get_thread(condor)
    exitcode = get_thread(sys.argv[1],'condor')
    print("exitcode:"+str(exitcode))
