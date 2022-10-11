from typing import NewType
import pulumi
import pulumi_gcp as gcp

def cloud_sql_instance(network,private_name,instance_name,sql_region,version,tier_db,database_name):
    private_ip_address = gcp.compute.GlobalAddress("privateaddress",
    purpose="VPC_PEERING",
    address_type="INTERNAL",
    prefix_length=16,
    network=private_name,
    opts=pulumi.ResourceOptions(depends_on=network))

    private_vpc_connection = gcp.servicenetworking.Connection("privateVpcConnection",
    network=private_name,
    service="servicenetworking.googleapis.com",
    reserved_peering_ranges=[private_ip_address.name],
    opts=pulumi.ResourceOptions(depends_on=private_ip_address))

    instance = gcp.sql.DatabaseInstance(instance_name,
    region=sql_region,
    name=instance_name,
    database_version=version,
    root_password="root",
    settings=gcp.sql.DatabaseInstanceSettingsArgs(
        tier=tier_db,
        ip_configuration=gcp.sql.DatabaseInstanceSettingsIpConfigurationArgs(
            ipv4_enabled=False,
            private_network=private_name
        )
    ),
    deletion_protection=False,
    opts=pulumi.ResourceOptions(depends_on=private_vpc_connection))
    database = gcp.sql.Database(database_name, instance=instance.name,opts=pulumi.ResourceOptions(depends_on=instance))
    return instance

def user_db(user_name,instance_name,host,password):
    users=gcp.sql.User(user_name,
    name=user_name,
    instance=instance_name,
    host=host,
    password=password)
    return users
    