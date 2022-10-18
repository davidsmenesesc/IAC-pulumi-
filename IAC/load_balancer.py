import pulumi
import pulumi_gcp as gcp


def load_balancer(name_bck_sv,name_url_map,hosts_lb,name_patcher,name_httpro,name_fwr,port_range_fwr,instance_groups):
    tcp_health_check = gcp.compute.HealthCheck("tcp-health-check",
    check_interval_sec=1,
    tcp_health_check=gcp.compute.HealthCheckTcpHealthCheckArgs(
        port=30001,
    ),
    timeout_sec=1)
    default_backend_service = gcp.compute.BackendService(name_bck_sv,
    port_name="http",
    protocol="HTTP",
    health_checks=tcp_health_check,
    backends=instance_groups,
    timeout_sec=10,
    load_balancing_scheme="EXTERNAL_MANAGED")
    default_url_map = gcp.compute.URLMap(name_url_map,
        description="a description",
        default_service=default_backend_service.id,
        host_rules=[gcp.compute.URLMapHostRuleArgs(
            hosts=hosts_lb,
            path_matcher=name_patcher,
        )],
        path_matchers=[gcp.compute.URLMapPathMatcherArgs(
            name=name_patcher,
            default_service=default_backend_service.id,
            path_rules=[gcp.compute.URLMapPathMatcherPathRuleArgs(
                paths=["/*"],
                service=default_backend_service.id,
            )],
        )])
    default_target_http_proxy = gcp.compute.TargetHttpProxy(name_httpro,
        description="a description",
        url_map=default_url_map.id)
    default_global_forwarding_rule = gcp.compute.GlobalForwardingRule(name_fwr,
        target=default_target_http_proxy.id,
        port_range=port_range_fwr,
        load_balancing_scheme="EXTERNAL_MANAGED")
def load_balancer_base():
    default_backend_service = gcp.compute.BackendService("defaultbackendservice",
    port_name="http",
    protocol="HTTP",
    timeout_sec=10,
    load_balancing_scheme="EXTERNAL_MANAGED")
    default_url_map = gcp.compute.URLMap("defaulturlmap",
    description="a description",
    default_service=default_backend_service.id,
    host_rules=[gcp.compute.URLMapHostRuleArgs(
        hosts=["mysite.com"],
        path_matcher="allpaths",
    )],
    path_matchers=[gcp.compute.URLMapPathMatcherArgs(
        name="allpaths",
        default_service=default_backend_service.id,
        path_rules=[gcp.compute.URLMapPathMatcherPathRuleArgs(
            paths=["/*"],
            service=default_backend_service.id,
        )],
    )])
    default_target_http_proxy = gcp.compute.TargetHttpProxy("defaulttargethttpproxy",
        description="a description",
        url_map=default_url_map.id)
    default_global_forwarding_rule = gcp.compute.GlobalForwardingRule("defaultglobalforwardingrule",
        target=default_target_http_proxy.id,
        port_range="80",
        load_balancing_scheme="EXTERNAL_MANAGED")