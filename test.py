

import os,json
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/root/pyutil')


from  utz import utz,ddict,uos

class test:
    def __init__(self):
        utz.logset()
        utz.print("hhhhhhhhhhhhhhhhhhhh")
        utz.enter2()

    def kpods(self):
        utz.enter2()
        uos1=uos()

        cmd=" kubectl get namespaces -o json "
        resp=uos1.uoscall(cmd)
        # utz.print(resp[uos.BUFOUT])

        respj=json.loads(resp[uos.BUFOUT])
        utz.jprint(respj["items"][0]["kind"])
        return

        

    def gcp_cluster(self):
        utz.enter2()
        uos1=uos()

        cls="cls1"

        cmd=" gcloud container clusters delete {cls} -q  --format=json ".format(cls=cls)
        resp=uos1.uoscall(cmd)
        utz.print(resp[uos.BUFOUT])

        # respj=json.loads(resp[uos.BUFOUT])
        # utz.jprint(respj["currentNodeCount"])


        cmd=" gcloud container clusters create {cls} --format=json ".format(cls=cls)
        resp=uos1.uoscall(cmd)
        # utz.print(resp[uos.BUFOUT])

        respj=json.loads(resp[uos.BUFOUT])
        utz.print("currentNodeCount")
        utz.jprint(respj[0]["currentNodeCount"])
        return







    
   



test1=test()

# test1.kpods()
test1.gcp_cluster()

