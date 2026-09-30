import ipaddress


def calculate_subnets(vpc_cidr: str, prefix= 1) -> str:
    """
    Takes a parent VPC CIDR and generate smaller subnet blocks
    """

    try:
        cidr_address_object = ipaddress.IPv4Network(vpc_cidr)
    except ipaddress.AddressValueError:
        print(f'[ERROR] the vpc cidr is not a valid IPv4 address: {vpc_cidr}')
    except ipaddress.NetmaskValueError:
        print(f'[ERROR] the mask is not valid for IPv4 address: {vpc_cidr}')

    the_subnet_blocks = list(cidr_address_object.subnets(prefixlen_diff= prefix))

    the_subnet_blocks_str = []
    for a in the_subnet_blocks:
        the_subnet_blocks_str.append(a.with_prefixlen)

    return the_subnet_blocks_str



def audit_subnet_capacity(subnet_cidr: str) -> str:
    """
    Returns total addresses, cloud provider reserved address (5), and usable host IP
    """

    
    return "the_return"

def Validate_route_security(route_table: list) -> str:
    return "the_return"

# save the execution results as a formatted JSON report: network_plan_report.json

print(calculate_subnets("10.0.0.0/8"))