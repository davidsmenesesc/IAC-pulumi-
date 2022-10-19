import pulumi 
import pulumi_gcp as gcp
import Virtual_machine as vm
import Firewall_rules as fw
import NAT_Router as nt
import VPC as VPC
import instance_group as ig
import cloud_sql_instance as sql
import load_balancer as lb

if __name__ == "__main__":
    #Create network
    #Var: name
        name_netw="movie-analyst-network"
        vpc=VPC.create_VPC(name_netw)
    #Create subnet
    #subnet_name,ip_range,reg,net
        subnet_name= "management-subnet"
        ip_range= "10.0.0.0/24"
        reg="us-east1"
        subnet_CICD=VPC.create_subnet(vpc,name_netw,subnet_name,ip_range,reg)
        subnet_name= "kubernetes-subnet"
        ip_range= "10.0.1.0/24"
        reg="us-east1"
        subnet_kube=VPC.create_subnet(vpc,name_netw,subnet_name,ip_range,reg)
    # #Create firewall rule for activating IAP service only protocol TCP
    # #VAR: name_net,name_rule,ports_tcp,fire_tags,source_ranges
        name_rule="allow-ssh-from-iap"
        ports_tcp=["22"]
        target_tag=["http-tag"]
        source_ranges=["35.235.240.0/20"]
        fw.firewall_rule_IAP(vpc,name_netw,name_rule,ports_tcp,target_tag,source_ranges)
    # #Create firewall rule for internal connection between machines
    # #VAR: name_net,name_rule,ports_tcp,fire_tags,source_ranges
        name_rule="allow-internal-machines"
        ports_tcp=["8080"]
        source_ranges=["0.0.0.0/0"]
        #fw.firewall_rule_internal(vpc,name_netw,name_rule,ports_tcp,source_ranges)
    # #Create firewall rule for internal connection between machines
    # #VAR: name_net,name_rule,ports_tcp,fire_tags,source_ranges
        name_rule="allow-kubernetes-internal"
        ports_tcp=["6443","10250","2379","2380","10251","10252","10255","3000"]
        source_ranges=["10.0.1.0/25"]
        fw.firewall_rule_internal(vpc,name_netw,name_rule,ports_tcp,source_ranges)
    # #Create firewall rule for internal connection between machines
    # #VAR: name_net,name_rule,ports_tcp,fire_tags,source_ranges
        name_rule="allow-lb-internal"
        ports_tcp=["30001"]
        source_ranges=["35.191.0.0/16","130.211.0.0/22"]
        fw.firewall_rule_internal(vpc,name_netw,name_rule,ports_tcp,source_ranges)
    # #Create firewall rule for internal connection between machines
    # #VAR: name_net,name_rule,ports_tcp,fire_tags,source_ranges
        name_rule="allow-cicd-internal"
        ports_tcp=["22","6443"]
        source_ranges=["10.0.0.0/25"]
        fw.firewall_rule_internal(vpc,name_netw,name_rule,ports_tcp,source_ranges)
    # #VAR: network,name_net,name_rule,ports_tcp,target_tag,source_ranges
        name_rule="allow-external-cicd"
        ports_tcp=["8080"]
        source_ranges=["186.155.18.82"]
        target_tag1=["cicd"]
        fw.firewall_rule_CICD(vpc,name_netw,name_rule,ports_tcp,target_tag1,source_ranges)
    #Create router for internet access
    #VAR: rout_name,region,name_netw
        rout_name="nat-config"
        region="us-east1"
        nat_name="nat-router-us-a-east1"
        nt.router(vpc,rout_name,region,name_netw,nat_name)
    # #Create cloudsql instance
    # #Instance_name,sql_region,version,tier_db,database_name
        instance_name="moviedb"
        sql_region="us-east1"
        version="MYSQL_8_0"
        tier_db="db-custom-1-3840"
        database_name="movie_db"
        sqlinstance=sql.cloud_sql_instance(vpc,vpc.id,instance_name,sql_region,version,tier_db,database_name)
    #Create user
    #user_name,instance_name,host,password
        sql.user_db(user_name="user",instance_name=sqlinstance.name,host="%",password="password")
    #Create virtual machines for kubernetes
    #Startup script
    #VAR: name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,startup_script,service_email
        mach_name="node-master-b"
        mach_type="e2-medium"
        mach_zone="us-east1-b"
        mach_tags=["http-server","https-server","web","http-tag"]
        mach_image="projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220905"
        mach_netw=name_netw
        with open('scripts.txt','r') as init_script:
            data = init_script.read()
        script = data   
        mach_subnet="kubernetes-subnet"
        service_email="998637135499-compute@developer.gserviceaccount.com"
        vm1=vm.create_kub_vm(subnet_kube,mach_name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,script,service_email)
    #Create worker node 
        mach_name="node-worker-b"
        mach_type="e2-medium"
        mach_zone="us-east1-b"
        mach_tags=["http-server","https-server","web","http-tag"]
        mach_image="projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220905"
        mach_netw=name_netw
        mach_subnet="kubernetes-subnet"
        service_email="998637135499-compute@developer.gserviceaccount.com"
        vm2=vm.create_kub_vm(subnet_kube,mach_name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,script,service_email)
    #Create virtual machines for kubernetes
    #Startup script
    #VAR: name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,startup_script,service_email
        mach_name="node-master-c"
        mach_type="e2-medium"
        mach_zone="us-east1-c"
        mach_tags=["http-server","https-server","web","http-tag"]
        mach_image="projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220905"
        mach_netw=name_netw
        with open('scripts.txt','r') as init_script:
            data = init_script.read()
        script = data   
        mach_subnet="kubernetes-subnet"
        service_email="998637135499-compute@developer.gserviceaccount.com"
        vm3=vm.create_kub_vm(subnet_kube,mach_name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,script,service_email)
    #Create worker node 
        mach_name="node-worker-c"
        mach_type="e2-medium"
        mach_zone="us-east1-c"
        mach_tags=["http-server","https-server","web","http-tag"]
        mach_image="projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220905"
        mach_netw=name_netw
        mach_subnet="kubernetes-subnet"
        service_email="998637135499-compute@developer.gserviceaccount.com"
        vm4=vm.create_kub_vm(subnet_kube,mach_name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,script,service_email)
    #Create machine for db 
        mach_name="database-machine"
        mach_type="e2-micro"
        mach_zone="us-east1-c"
        mach_tags=["http-server","https-server","web","http-tag"]
        mach_image="projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220905"
        mach_netw=name_netw
        mach_subnet="management-subnet"
        script=""
        service_email="998637135499-compute@developer.gserviceaccount.com"
        vm5=vm.create_kub_vm(subnet_kube,mach_name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,script,service_email)
    #Create machine for CICD
        with open('script-jenkins.txt','r') as init_script:
            data_jen = init_script.read()
        script_jen = data_jen   
        mach_name="cicd-machine"
        mach_type="e2-medium"
        mach_zone="us-east1-c"
        mach_tags=["http-server","https-server","web","http-tag","cicd"]
        mach_image="projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220905"
        mach_netw=name_netw
        mach_subnet="management-subnet"
        script=script_jen
        service_email="998637135499-compute@developer.gserviceaccount.com"
        vm5=vm.create_jen_vm(subnet_kube,mach_name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,script,service_email)
    #Create instance groups
        name_instance_group="zone-b-kube"
        description="Zone b for ig"
        instance2=vm2.self_link
        instances=[]
        instances.append(instance2)
        zone="us-east1-b"
        instanceg1=ig.instance_group(vpc,name_instance_group,description,instances,zone)
    #Create instance groups
        name_instance_group="zone-c-kube"
        description="Zone c for ig"
        instance2=vm4.self_link
        instances=[]
        instances.append(instance2)
        zone="us-east1-c"
        instanceg2=ig.instance_group(vpc,name_instance_group,description,instances,zone)
        #Creation of the load balancer
        #name_bck_sv,name_url_map,hosts_lb,name_patcher,name_httpro,name_fwr,port_range_fwr
        lb.load_balancer(name_bck_sv="mvi-bck-sv",name_url_map="lb-mvi",hosts_lb=["mviapp.com"],name_patcher="patcher-mvi",name_httpro="mvi-proxy",name_fwr="mvi-rule",port_range_fwr=8080,instance_groups=[gcp.compute.BackendServiceBackendArgs(group=instanceg1.id,),gcp.compute.BackendServiceBackendArgs(group=instanceg2.id,)])
        #lb.load_balancer_base()
