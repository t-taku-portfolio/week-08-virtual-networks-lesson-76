import datetime
import ipaddress
import json
import zoneinfo
from pathlib import Path


def create_IPv4_obj(vpc_cidr: str) -> object:
    try:
        cidr_address_object = ipaddress.IPv4Network(vpc_cidr)
    except ipaddress.AddressValueError:
        raise ValueError(f'[ERROR] the vpc cidr is not a valid IPv4 address: {vpc_cidr}')
    except ipaddress.NetmaskValueError:
        raise ValueError(f'[ERROR] the mask is not valid for IPv4 address: {vpc_cidr}')

    return cidr_address_object



def calculate_subnets(vpc_cidr: str, prefix= 1) -> list:
    """
    Takes a parent VPC CIDR and generate smaller subnet blocks
    """

    the_subnet_blocks = list(create_IPv4_obj(vpc_cidr).subnets(prefixlen_diff= prefix))

    the_subnet_blocks_with_prefixlen = []
    for network_obj in the_subnet_blocks:
        the_subnet_blocks_with_prefixlen.append(network_obj.with_prefixlen)

    return the_subnet_blocks_with_prefixlen



def audit_subnet_capacity(subnet_cidr: str) -> dict:
    """
    Returns total addresses, cloud provider reserved address (5), and usable host IP.
    The host IPs are shown when their number is less than 64.
    """

    max_host_IPs = 64

    target_IPv4_obj = create_IPv4_obj(subnet_cidr)
    total_addresses_int = target_IPv4_obj.num_addresses

    hosts_IPs_list = []
    if total_addresses_int < max_host_IPs:
        for host_IPv4_obj in target_IPv4_obj.hosts():
            hosts_IPs_list.append(str(host_IPv4_obj.with_prefixlen))
    else:
        hosts_IPs_list.append(str(target_IPv4_obj.network_address))
        print("[Warning] Too many total addresses. List includes network address only")

    return {"total_addresses" : total_addresses_int,
        "host_IPs" : hosts_IPs_list}



def validate_route_security(route_table: list) -> str:
    """
    If 0.0.0.0/0 points to an Internet Gateway, return PUBLIC_WARNING. The route table is for Azure.
    """

    for properties in route_table:
        is_target_default_root = (create_IPv4_obj(properties["addressPrefix"]).prefixlen == 0)
        is_destination_igw = (properties["nextHopType"] == "Internet")
        if is_target_default_root and is_destination_igw:
            return "PUBLIC_WARNING"
        
    return "SECURE_PRIVATE"



def save_as_json(obj_dict: dict, target_dir= None) -> str:
    # save the execution results as a formatted JSON report: network_plan_report.json

    JAPAN_TOKYO = zoneinfo.ZoneInfo("Asia/Tokyo")
    timestamp = datetime.datetime.now(JAPAN_TOKYO).strftime("%Y_%m_%d")
    obj_dict["timestamp"] = timestamp

    if target_dir is None:
        target_dir = Path.cwd()
    file_path = Path(target_dir) / "network_plan_report.json"

    try:
        with open(file_path, "w") as f:
            json.dump(obj= obj_dict, fp= f, indent= 4)
    except FileNotFoundError:
        print("Target file is not found")
        raise

    return file_path



if __name__ == "__main__":
    # run and verify, validate, save as JSON

    cidr_IPv4 = "10.0.0.0/8"
    the_rout_table = []

    target_json = {
        "subnets" : calculate_subnets(cidr_IPv4),
        "subnet_capacity" : audit_subnet_capacity(cidr_IPv4),
        "default_root_status" : validate_route_security(the_rout_table)
    }

    save_as_json(obj_dict= target_json)