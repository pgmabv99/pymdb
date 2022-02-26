

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



        cmd=" kubectl get pods -o json "
        resp=uos1.uoscall(cmd)
        # utz.print(resp[uos.BUFOUT])


        respj=json.loads(resp[uos.BUFOUT])
        utz.jprint(respj["items"][0]["kind"])

        return


    def aks_build(self):
        utz.enter2()
        uos1=uos()

        grp="pgmabv88"
        cls="pgmabv88"
        ipname="pgmabv88"


        cmd="az aks delete   --name {cls} --resource-group {grp} --yes"\
                            .format(cls=cls,grp=grp)
        resp=uos1.uoscall(cmd)
         
        cmd="az aks create   --name {cls} --resource-group {grp} \
                            --ssh-key-value /home/azureuser/.ssh/authorized_keys \
                            --node-count 1"\
                            .format(cls=cls,grp=grp)
        resp=uos1.uoscall(cmd)
        if resp[uos.RC] !=0 :
            utz.print("exiting")
            return
        respj=json.loads(resp[uos.BUFOUT])
        utz.jprint(respj)
        clientid=respj["servicePrincipalProfile"]["clientId"]

        #enable monitoring 
        cmd="az aks enable-addons -a monitoring  --name {cls} --resource-group {grp}"\
                            .format(cls=cls,grp=grp)
        resp=uos1.uoscall(cmd)
        if resp[uos.RC] !=0 :
            utz.print("exiting")
            return
        respj=json.loads(resp[uos.BUFOUT])
        utz.jprint(respj)
        clientid=respj["servicePrincipalProfile"]["clientId"]
            
        cmd="az role assignment create \
            --assignee {clientid} \
            --role \"Network Contributor\" \
            --scope /subscriptions/cbff8ae6-7d79-4b2d-bf97-d9fc382bc181/resourceGroups/{grp}"\
                            .format(clientid=clientid,cls=cls,grp=grp)
        resp=uos1.uoscall(cmd)
        if resp[uos.RC] !=0 :
            utz.print("exiting")
            return
        respj=json.loads(resp[uos.BUFOUT])
        utz.jprint(respj)

        #allow external IP for k8s service
        cmd="az aks get-credentials --resource-group {grp} --name {cls} \
                                    --overwrite-existing"\
                            .format(cls=cls,grp=grp)
        resp=uos1.uoscall(cmd)
        if resp[uos.RC] !=0 :
            utz.print("exiting")
            return
        utz.print(resp[uos.BUFOUT])

        #recreate public IP and save in the file
        cmd="az network public-ip delete \
            --resource-group {grp}\
            --name {ipname}"\
                            .format(ipname=ipname,grp=grp)
        resp=uos1.uoscall(cmd)
        cmd="az network public-ip create \
            --resource-group {grp}\
            --name {ipname} \
            --sku Standard \
            --allocation-method static"\
                            .format(ipname=ipname,grp=grp)
        resp=uos1.uoscall(cmd)
        if resp[uos.RC] !=0 :
            utz.print("exiting")
            return
        respj=json.loads(resp[uos.BUFOUT])
        utz.jprint(respj)
        ip=respj["publicIp"]["ipAddress"]
        utz.print(ip)

        f = open("pydjango_ip.txt", "w")
        f.write(ip)
        f.close()
        #https://docs.microsoft.com/en-us/azure/aks/static-ip

   
    def docker_build(self):
        utz.enter2()
        uos1=uos()

        img="pgmabv99/pydjango"
        cnt="pydjango"
        usr="pgmabv99"
        pwd="Lena8484"


        cmd="docker rm -f {cnt}"\
                            .format(cnt=cnt)
        resp=uos1.uoscall(cmd)

        cmd="docker rmi -f {img}"\
                            .format(img=img)
        resp=uos1.uoscall(cmd)


        cmd="docker build . --tag {img}"\
                            .format(img=img)
        resp=uos1.uoscall_nowait(cmd)

        cmd="docker login -u {usr} -p {pwd}"\
                            .format(usr=usr,pwd=pwd)
        resp=uos1.uoscall(cmd)

        cmd="docker push {img}"\
                            .format(img=img)
        resp=uos1.uoscall_nowait(cmd)

    def k8s_build(self):
        utz.enter2()
        uos1=uos()
        replicas=2
        grp="pgmabv88"

        # uos1.uoscall_nowait("kubectl delete pods --all")

        uos1.uoscall_nowait("kubectl delete services --all")
        uos1.uoscall_nowait("kubectl delete deployments  --all")
        uos1.uoscall_nowait("docker login -u pgmabv99 -p Lena8484")

        #replace pattern in Yaml
        f = open("pydjango_ip.txt", "r")
        ip=f.read()
        f.close()

        f = open("pydjango.yaml", "r")
        txt=f.read()
        f.close()

        txt2=txt.format(replicas=replicas,ip=ip,grp=grp)
        f1 = open("pydjango_tmp.yaml", "w")
        f1.write(txt2)
        f1.close()


        uos1.uoscall_nowait("kubectl apply -f pydjango_tmp.yaml")

        # uos1.uoscall_nowait("kubectl get pods -o json -l app=pydjango")
        # uos1.uoscall_nowait("kubectl logs -l app=pydjango ")
        # uos1.uoscall_nowait("kubectl cluster-info dump > junk_dump.txt ")
        # loop untill status shows IP

        #wait for deployment replica to be filled
        while True:
            resp=uos1.uoscall("kubectl get pods -o json")
            if resp[uos.RC] !=0 :
                utz.print("exiting")
                return
            respj=json.loads(resp[uos.BUFOUT])
            items=respj["items"]
            nbad=0
            for item in items:
                phase=item["status"]["phase"]
                msg=""
                if phase!="Running":
                    nbad+=1
                    if "conditions" in item["status"]:
                        msglist=item["status"]["conditions"] 
                        for msg2 in msglist:
                            msg+=msg2.get("message","")+"\n"
                    else:
                        msg+="waiting for conditions in json"
                    utz.print(item["metadata"]["name"],item["status"]["phase"],msg)
            if nbad==0:
                utz.print("all {replicas} replicas are running".format(replicas=replicas))
                break
            utz.sleep(3, "Not running {nbad} .wait for next state".format(nbad=nbad))


        #wait for deployment replica to be filled
        # while True:
        #     resp=uos1.uoscall("kubectl get deployment pydjango -o json")
        #     if resp[uos.RC] !=0 
        #         utz.print("exiting")
        #         return
        #     respj=json.loads(resp[uos.BUFOUT])
        #     utz.jprint(respj)
        #     st=respj["status"]
        #     if "availableReplicas" in st:
        #         utz.print("replicas ", st["availableReplicas"])
        #         if replicas == st["availableReplicas"]:
        #             break
        #     utz.sleep(3, "wait for next state")

        # wait for service to have ip
        while True:
            resp=uos1.uoscall("kubectl get service pydjango -o json")
            if resp[uos.RC] !=0 :
                utz.print("exiting")
                return
            respj=json.loads(resp[uos.BUFOUT])
            # utz.jprint(respj)
            lb=respj["status"]["loadBalancer"]
            if "ingress" in lb:
                ip=lb["ingress"][0]["ip"]
                utz.print("ip",ip)
                break
            utz.sleep(5, "wait for next state")

    def k8s_logs(self):
        utz.enter2()
        uos1=uos()
        uos1.uoscall_nowait("rm -r logs")
        uos1.uoscall_nowait("mkdir logs")
        resp=uos1.uoscall("kubectl get pods -o json")
        if resp[uos.RC] !=0 :
            utz.print("exiting")
            return
        respj=json.loads(resp[uos.BUFOUT])
        items=respj["items"]
        for item in items:
            pod=item["metadata"]["name"]
            with  open("logs/"+pod+"_stat.txt","w") as f:
                f.write(utz.jstring(item["status"]))
            resp=uos1.uoscall("kubectl describe pod  {pod}".format(pod=pod), \
                    file_name="logs/"+pod+"_describe.txt")
            resp=uos1.uoscall("kubectl logs  {pod}".format(pod=pod), \
                    file_name="logs/"+pod+"_log.txt")

    
   



test1=test()
# azinit1.aks_build()
test1.kpods()
# azinit1.docker_build()
# azinit1.k8s_build()
#azinit1.k8s_logs()


# 




