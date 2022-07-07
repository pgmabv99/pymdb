
#pip install google-cloud-container
#pip install google-cloud-domains
import google.auth
from google.cloud import storage
from google.cloud import container 
from google.cloud import domains_v1 

class gke:
    def __init__(self) -> None:
        self.gcpkeys='/root/gcpkeys.json'
        self.zone='us-east4'
        self.credentials, self.project_id = google.auth.default()
        print("project_id", self.project_id)

        self.storage_client = storage.Client(credentials=self.credentials)
        self.container_client = container.ClusterManagerClient(credentials=self.credentials)
        self.domains_client = domains_v1.DomainsClient(credentials=self.credentials)


    def buckets(self):
        print("buckets=====================")
        buckets = list(self.storage_client.list_buckets())
        for bucket in buckets:
            print(bucket)
 

    def clusters(self) :
        print("clusters===================")
        

        parent = 'projects/{}/locations/{}'.format(self.project_id, self.zone)
        
        resp=self.container_client.list_clusters(parent=parent, project_id=None, zone=None)
        clusters=resp.clusters
        for cluster in clusters:
            print("cluster_name:",cluster.name)

        self.node_pools(cluster.name)
      
    
    
    def node_pools(self, cluster):
        print("==node pools===================")

        parent = 'projects/{}/locations/{}/clusters/{}'.format(self.project_id, self.zone, cluster)
        resp=self.container_client.list_node_pools(parent=parent, project_id=None, zone=None, cluster_id=None)
        for node_pool in resp.node_pools:
            print("==name :", node_pool.name,
                  "machine-type:", node_pool.config.machine_type)   

    
    def domains(self) :
        print("domains===================")
        

        parent = 'projects/{}/locations/{}'.format(self.project_id,self.zone)
        
        resp=self.domains_client.list_registrations(parent=parent)
        print(resp)


 

gke=gke()
# gke.buckets()
# gke.clusters()
gke.domains()

#