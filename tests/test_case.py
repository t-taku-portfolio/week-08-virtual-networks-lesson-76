from lesson76 import network_planner


def test_normal_case1():
    """
    Happy path 
    """
    network_planner.create_IPv4_obj("10.0.0.0/8")