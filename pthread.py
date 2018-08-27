class Pthread():
    def __init__(self,pid):
        self.pid  = pid
        self.ppid = -1
        self.user = "nobody"
        #cpu use ratio
        self.cpu  = -1
        #mem use ratio
        self.mem  = -1
        #virtual memory
        self.vsz  = -1
        #real memory
        self.rss  = -1
        self.leaf = -1
        self.cmdabpath = ""
        self.command = "nocommand"
        self.slotid = -1
        self.node = "nonode"
        #cache time
        self.time = -1
        #runtime
        self.runtime = -1
        self.stat  = "nostat"
        self.starttime = -1
        self.kb_rd_s = -1
        self.kb_wr_s = -1
        self.kb_ccwr_s = -1
        #self.iodelay = -1


    def getpid(self):
        return self.pid
    def setpid(self,newpid):
        self.pid = newpid
    def getppid(self):
        return self.ppid
    def setppid(self,newppid):
        self.ppid = newppid
    def getuser(self):
        return self.user
    def setuser(self,newuser):
        self.user = newuser
    def getcpu(self):
        return self.cpu
    def setcpu(self,newcpu):
        self.cpu = newcpu
    def getmem(self):
        return self.mem
    def setmem(self,newmem):
        self.mem = newmem
    def getvsz(self):
        return self.vsz
    def setvsz(self,newvsz):
        self.vsz = newvsz
    def getrss(self):
        return self.rss
    def setrss(self,newrss):
        self.rss = newrss
    def getcommand(self):
        return self.command
    def setcommand(self,newcommand):
        self.command = newcommand
    def getleaf(self):
        return self.leaf
    def setleaf(self,newleaf):
        self.leaf = newleaf
    def getcmdabpath(self):
        return self.cmdabpath
    def setcmdabpath(self,newcmdabpath):
        self.cmdabpath = newcmdabpath
    def getslotid(self):
        return self.slotid
    def setslotid(self,newslotid):
        self.slotid = newslotid
    def getnode(self):
        return self.node
    def setnode(self,newnode):
        self.node = newnode
    def gettime(self):
        return self.time
    def settime(self,newtime):
        self.time = newtime
    def getruntime(self):
        return self.runtime
    def setruntime(self,newruntime):
        self.runtime = newruntime
    def getstat(self):
        return self.stat
    def setstat(self,newstat):
        self.stat = newstat
    def getstarttime(self):
        return self.starttime
    def setstarttime(self,newstarttime):
        self.starttime = newstarttime
    def getkb_rd_s(self):
        return self.kb_rd_s
    def setkb_rd_s(self,newkb_rd_s):
        self.kb_rd_s = newkb_rd_s
    def getkb_wr_s(self):
        return self.kb_wr_s
    def setkb_wr_s(self,newkb_wr_s):
        self.kb_wr_s = newkb_wr_s
    def getkb_ccwr_s(self):
        return self.kb_ccwr_s
    def setkb_ccwr_s(self,newkb_ccwr_s):
        self.kb_ccwr_s = newkb_ccwr_s
    '''
    def getiodelay(self):
        return self.iodelay
    def setiodelay(self,newiodelay):
        self.iodelay = newiodelay
    '''
    def buildmessage(self,form="csv"):
        if form =="csv":
            message = str(self.ppid)+","+str(self.time)+","+str(self.pid)+","+self.user+","+str(self.cpu)+","+str(self.mem)+","+str(self.vsz)+","+str(self.rss)+","+self.command+","+str(self.slotid)+","+str(self.leaf)+","+str(self.cmdabpath)+","+self.node+","+str(self.runtime)+","+self.stat+","+str(self.starttime)+"\n"
            #message = str(self.ppid)+","+str(self.time)+","+str(self.pid)+","+self.user+","+str(self.cpu)+","+str(self.mem)+","+str(self.vsz)+","+str(self.rss)+","+self.command+","+str(self.slotid)+","+self.node+","+str(self.runtime)+","+self.stat+","+str(self.starttime)+","+str(self.kb_rd_s)+","+str(self.kb_wr_s)+","+str(self.kb_ccwr_s)+"\n"
            return message

