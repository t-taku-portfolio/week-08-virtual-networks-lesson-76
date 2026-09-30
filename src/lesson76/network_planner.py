import ipaddress


def create_IPv4_obj(vpc_cidr: str) -> object:
    try:
        cidr_address_object = ipaddress.IPv4Network(vpc_cidr)
    except ipaddress.AddressValueError:
        print(f'[ERROR] the vpc cidr is not a valid IPv4 address: {vpc_cidr}')
    except ipaddress.NetmaskValueError:
        print(f'[ERROR] the mask is not valid for IPv4 address: {vpc_cidr}')

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
    The host IPs are shown when their number is less than 50.
    """

    max_host_IPs = 50

    target_IPv4_obj = create_IPv4_obj(subnet_cidr)
    total_addresses_int = target_IPv4_obj.num_addresses

    hosts_IPs_list = []
    if total_addresses_int < max_host_IPs:
        hosts_IPs_list.extend(list(target_IPv4_obj.hosts()))
    else:
        hosts_IPs_list.append(target_IPv4_obj.network_address)
        print("[Warning] Too many total addresses. List returns network address only")

    return {"total_addresses" : total_addresses_int,
        "host_IPs" : hosts_IPs_list}



def Validate_route_security(route_table: list) -> str:
    return "the_return"



# save the execution results as a formatted JSON report: network_plan_report.json

target_IPv4 = "10.0.0.0/8"
print(calculate_subnets(target_IPv4))
print(audit_subnet_capacity(target_IPv4))