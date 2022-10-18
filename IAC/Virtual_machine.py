import pulumi 
import pulumi_gcp as gcp

def create_kub_vm(network,name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,startup_script,service_email):
        default_instance = gcp.compute.Instance(name,
        machine_type=mach_type,
        zone=mach_zone,
        tags=mach_tags,
        name=name,
        boot_disk=gcp.compute.InstanceBootDiskArgs(
            initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                image=mach_image,
            ),
        ),
        network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
            network=mach_netw,
            subnetwork=mach_subnet,
        )],
        metadata_startup_script=startup_script,
        service_account=gcp.compute.InstanceServiceAccountArgs(
            email=service_email,
            scopes=["cloud-platform"],
        ),opts=pulumi.ResourceOptions(depends_on=network))
        return default_instance
def create_jen_vm(network,name,mach_type,mach_zone,mach_tags,mach_image,mach_netw,mach_subnet,startup_script,service_email):
        default_instance = gcp.compute.Instance(name,
        machine_type=mach_type,
        zone=mach_zone,
        tags=mach_tags,
        name=name,
        boot_disk=gcp.compute.InstanceBootDiskArgs(
            initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                image=mach_image,
            ),
        ),
        network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
            network=mach_netw,
            subnetwork=mach_subnet,
            access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()]
        )],
        metadata_startup_script=startup_script,
        service_account=gcp.compute.InstanceServiceAccountArgs(
            email=service_email,
            scopes=["cloud-platform"],
        ),opts=pulumi.ResourceOptions(depends_on=network))
        return default_instance