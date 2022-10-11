import pulumi 
import pulumi_gcp as gcp

def create_VPC(net_name):
    net = gcp.compute.Network(net_name, auto_create_subnetworks=False,name=net_name)
    return net

def create_subnet(network,net,subnet1_name,ip_range,reg):
    subnet = gcp.compute.Subnetwork(subnet1_name,
        ip_cidr_range=ip_range,
        region=reg,
        network=net,
        name=subnet1_name,
        opts=pulumi.ResourceOptions(depends_on=network))
    return subnet
