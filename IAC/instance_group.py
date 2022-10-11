import pulumi 
import pulumi_gcp as gcp
def instance_group(network,name,descr,instances_ig,zone_ig):
    webservers = gcp.compute.InstanceGroup(name,
    description=descr,
    instances=instances_ig,
    named_ports=[
        gcp.compute.InstanceGroupNamedPortArgs(
            name="http",
            port=8080,
        ),
        gcp.compute.InstanceGroupNamedPortArgs(
            name="https",
            port=8443,
        ),
    ],
    zone=zone_ig,
    opts=pulumi.ResourceOptions(depends_on=network))