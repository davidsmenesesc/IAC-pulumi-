import pulumi 
import pulumi_gcp as gcp
def router(network,rout_name,region,name_netw,nat_name):
    router = gcp.compute.Router(rout_name,
        region=region,
        network=name_netw,
        bgp=gcp.compute.RouterBgpArgs(
            asn=64514,
        ),opts=pulumi.ResourceOptions(depends_on=network))
    nat = gcp.compute.RouterNat("nat",
    router=router.name,
    region=router.region,
    nat_ip_allocate_option="AUTO_ONLY",
    source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
    log_config=gcp.compute.RouterNatLogConfigArgs(
        enable=True,
        filter="ERRORS_ONLY",
    ),opts=pulumi.ResourceOptions(depends_on=router))
 
