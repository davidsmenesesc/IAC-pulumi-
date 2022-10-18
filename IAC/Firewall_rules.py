import pulumi
import pulumi_gcp as gcp

def firewall_rule_IAP(network,name_net,name_rule,ports_tcp,target_tag,source_ranges):
    default_firewall = gcp.compute.Firewall(name_rule,
    network=name_net,
    allows=[
        gcp.compute.FirewallAllowArgs(
            protocol="tcp",
            ports=ports_tcp,
        ),
    ],
    source_ranges=source_ranges,
    target_tags=target_tag,
    opts=pulumi.ResourceOptions(network))
def firewall_rule_CICD(network,name_net,name_rule,ports_tcp,target_tag,source_ranges):
    default_firewall = gcp.compute.Firewall(name_rule,
    network=name_net,
    allows=[
        gcp.compute.FirewallAllowArgs(
            protocol="tcp",
            ports=ports_tcp,
        ),
    ],
    source_ranges=source_ranges,
    target_tags=target_tag,
    opts=pulumi.ResourceOptions(network))
def firewall_rule_internal(network,name_net,name_rule,ports,source_ranges):
    default_firewall = gcp.compute.Firewall(name_rule,
        network=name_net,
        allows=[
            gcp.compute.FirewallAllowArgs(
                protocol="tcp",
                ports=ports,
            ),
            gcp.compute.FirewallAllowArgs(
                protocol="udp",
                ports=ports
            ),
            gcp.compute.FirewallAllowArgs(
                protocol="icmp"
            ),
        ],
        source_ranges=source_ranges,
        opts=pulumi.ResourceOptions(network))