

import os,json
import sys
import threading

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/root/pyutil')


from  utz import utz,ddict,uos


class test:
    def __init__(self):
        utz.logset()
        utz.print("hhhhhhhhhhhhhhhhhhhh")
        utz.enter2()
        self.uos1=uos()

    def kpods(self, cls):
        utz.enter2()
        

        cmd=" kubectl get namespaces -o json "
        resp=self.uos1.uoscall(cmd)
        # utz.print(resp[uos.BUFOUT])

        respj=json.loads(resp[uos.BUFOUT])
        utz.jprint(respj["items"][0]["kind"])
        return
        

    def gcp_cluster(self, cls ):
        utz.enter2()
         
        cmd=" gcloud container clusters delete {cls} -q  --format=json ".format(cls=cls)
        resp=self.uos1.uoscall(cmd)
        utz.print(resp[uos.BUFOUT])

        # respj=json.loads(resp[uos.BUFOUT])
        # utz.jprint(respj["currentNodeCount"])

        cmd=" gcloud container clusters create {cls} --format=json ".format(cls=cls)
        resp=self.uos1.uoscall(cmd)
        # utz.print(resp[uos.BUFOUT])

        respj=json.loads(resp[uos.BUFOUT])
        utz.print("currentNodeCount")
        utz.jprint(respj[0]["currentNodeCount"])
        return


      
    def thr1(self,ithr):
        utz.enter2()

        cls="cls"+str(ithr)

        # with self._lock:
        utz.print("thread: begin work ithr={ithr}".format(ithr=ithr))
        # nsec=2
        # utz.sleep(nsec,"sleep ithr={ithr} ".format(ithr=ithr))
        self.gcp_cluster(cls)
        self.kpods(cls)
        utz.print("thread: end   work ithr={ithr}".format(ithr=ithr))

        return 

    def thr_run(self):
        utz.enter2()
        self._lock = threading.Lock()

        lst_thr=list()
        for ithr in range(2):
            # utz.sleep(1,"sleep ")
            pthr=threading.Thread(target=self.thr1,args=(ithr,))
            lst_thr.append(pthr)
            pthr.start()

        for pthr in lst_thr:
            pthr.join()

        return 

def main():
    test1=test()

    test1.thr_run()
    # cls="cls1"
    # test1.gcp_cluster(cls)
    # test1.kpods(cls)



    

main()

