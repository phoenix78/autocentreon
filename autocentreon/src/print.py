from main import *
from host import *
from configuration import *


def print_sizelist():
    count_switch = 0
    count_router = 0
    print("#### DESSERTE LIST:", len(desserte_list))
    print("#### MODEL LIST:", len(model_list))
    print("#### HOSTS LIST:", len(hosts_list))
    for host in hosts_list:
        if host.comm:
            count_switch = count_switch + 1
        else:
            count_router = count_router + 1

    print("----- SWITCHS:", count_switch)
    print("----- ROUTERS:", count_router)


def print_lists():
    print("#### DESSERTE LIST:", len(desserte_list))
    for i in desserte_list:
        print(i)
    print("###############################################################")
    print("#### MODEL LIST:", len(model_list))
    for i in model_list:
        print(i)
    print("###############################################################")
    print("#### HOST LIST: ", len(hosts_list))
    for host in hosts_list:
        print(host.id, host.hostname, host.ip, host.role, host.model, host.etat_sup, host.desserte, host.template_centreon[0], host.comm)
