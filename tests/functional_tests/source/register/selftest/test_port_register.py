from source.testdb.initializer.setup_classes import SetupClasses

def init_unittest(request):
    sc = SetupClasses(request)
    return sc


def test_register_tcp_port(request):
    sc = init_unittest(request)
    sc.port_register.get_registered_tcp_port(prefix="unittest")
    sc.port_register.get_registered_tcp_port(prefix="unittest2")
    assert isinstance(sc.port_register.registered_tcp_ports["unittest"], int)
    assert isinstance(sc.port_register.registered_tcp_ports["unittest2"], int)
    assert sc.port_register.registered_tcp_ports["unittest"] != sc.port_register.registered_tcp_ports["unittest2"]


def test_get_already_registered_tcp_port(request):
    sc = init_unittest(request)
    sc.port_register.get_registered_tcp_port(prefix="unittest")
    assert sc.port_register.registered_tcp_ports["unittest"] == sc.port_register.get_registered_tcp_port(prefix="unittest")
