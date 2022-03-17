import glob
import json
import csv
from hosts import *
import requests
import urllib3
from apiCentreon import *


class autocentreon:
    def __init__(self):
        self.conf_file = None
        self.centreon_host = None
        self.centreon_api_username = None
        self.centreon_api_password = None
        self.centreon_db_host = None
        self.centreon_db_username = None
        self.centreon_db_password = None

        self.categories = list()
        self.groups = list()
        self.collectors = list()
        self.templates = list()
        self.hosts = list()

    def set_conf_file(self, conf_file):
        self.conf_file = conf_file

    def set_centreon_host(self, centreon_host):
        self.centreon_host = centreon_host

    def set_centreon_api_username(self, centreon_api_username):
        self.conf_file = centreon_api_username

    def set_centreon_api_password(self, centreon_api_password):
        self.conf_file = centreon_api_password

    def set_centreon_db_host(self, centreon_db_host):
        self.centreon_db_host = centreon_db_host

    def set_centreon_db_username(self, centreon_db_username):
        self.centreon_db_username = centreon_db_username

    def set_centreon_db_password(self, centreon_db_password):
        self.conf_file = centreon_db_password

    def set_collectors(self, collectors):
        self.conf_file = collectors

    def set_templates(self, templates):
        self.templates = templates

    def set_hosts(self, hosts):
        self.hosts = hosts

    def set_groups(self, groups):
        self.groups = groups

    def get_hosts(self):
        return self.hosts

    def get_groups(self):
        return self.groups

    def get_centreon_host(self):
        return self.centreon_host

    def get_centreon_api_username(self):
        return self.centreon_api_username

    def get_centreon_api_password(self):
        return self.centreon_api_password

    def load_csv(self, csv_file=glob.glob("inventory/*.csv")[-1]):
        with open(csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            count = 0
            for row in csv_reader:
                host = hosts()
                hostname = row[0]
                alias = row[1]
                ip = row[2]
                etat_sup = row[3]
                model = row[4]
                templates = row[5].split(",")
                collectors = row[6].split(",")
                geo_coords = row[7]
                groups = row[8].split(",")
                categories = row[9].split(",")
                if etat_sup != "ZERO":
                    for cat in categories:
                        if cat not in self.categories:
                            self.categories.append(cat)
                    for group in groups:
                        if group not in self.groups:
                            self.groups.append(group)
                    for template in templates:
                        if template not in self.templates:
                            self.templates.append(template)
                    for poller in collectors:
                        if poller not in self.collectors:
                            self.collectors.append(poller)
                    host.create(id=count, alias=alias, hostname=hostname, ip=ip,
                                etat_sup=etat_sup, model=model, geo_coords=geo_coords,
                                groups=groups, templates_centreon=templates,
                                collectors_centreon=collectors, categories=categories)
                    self.hosts.append(host)
                    count += 1
        self.hosts.pop(0)
        self.groups.pop(0)
        self.templates.pop(0)
        self.collectors.pop(0)
        self.categories.pop(0)
        return self.hosts

    def load_conf(self, conf_file='autocentreon.conf'):
        conf = open(conf_file)
        data = json.load(conf)
        self.conf_file = conf_file
        self.centreon_host = data["centreon-api"]["host"]
        self.centreon_api_username = data["centreon-api"]["username"]
        self.centreon_api_password = data["centreon-api"]["password"]
        self.centreon_db_host = data["centreon-database"]["host"]
        self.centreon_db_username = data["centreon-database"]["username"]
        self.centreon_db_password = data["centreon-database"]["password"]

    def print_conf(self):
        print("## Configuration file readed:", self.conf_file)
        print("\tcentreon_host:", self.centreon_host, "\t\tcentreon_db_host:", self.centreon_db_host)
        print("\tcentreon_api_username:", self.centreon_api_username, "\tcentreon_db_username:",
              self.centreon_db_username)

    def print_lists(self):
        print("## Hosts list:", len(self.hosts))
        for host in self.hosts:
            print("\t", host.__dict__)

        print("## Groups list:", len(self.groups))
        for group in self.groups:
            print("\t", group)

        print("## Categories list:", len(self.categories))
        for category in self.categories:
            print("\t", category)

        print("## Templates list:", len(self.templates))
        for template in self.templates:
            print("\t", template)

        print("## Pollers list:", len(self.collectors))
        for poller in self.collectors:
            print("\t", poller)

    def print_sizelists(self):
        print("## Hosts list:", len(self.hosts))
        print("## Groups list:", len(self.groups))
        print("## Templates list:", len(self.templates))
        print("## Categories list:", len(self.categories))
        print("## Collectors list:", len(self.collectors))



    # Main AutoCentreon
    def execute(self):
        token = getToken(self.centreon_host, self.centreon_api_username, self.centreon_api_password)
        get_centreon_api_host(self.centreon_host)
        print("AUTOCENTREON - SUCCESS CONNECT - Token Centreon :", token)
        logging.info("AUTOCENTREON - SUCCESS CONNECT - Token Centreon : " + token)

        ## DELETE HOSTS
        #delAllHosts(token)
        #delAllGroups(token)

        all_hosts_info = getAllHostsInfo(self.centreon_db_host, self.centreon_db_username, self.centreon_db_password)
        ## No more usefull
        # getAllTemplate(token)
        # showHosts(token)
        # showGroups(token)
        # showServiceTemplate(token)
        # showHostTemplate(token)


        # LIST OF HOST NOT IN CENTREON and UPDATE HOST IN CENTREON
        add_hosts = diff_hosts_pasteli(self.hosts, all_hosts_info, self.collectors, token)
        delete_hosts = diff_hosts_centreon(self.hosts, all_hosts_info, token)

        print("AUTOCENTREON - EQUIPEMENTS A AJOUTER:", len(add_hosts))
        logging.info("Nombre d'équipements à ajouter dans centreon: " + str(len(add_hosts)))
        for i in add_hosts:
            print("Add -", i.hostname)

        print("AUTOCENTREON - EQUIPEMENTS A SUPPRIMER:", len(delete_hosts))
        logging.info("Nombre d'équipements à désactiver dans centreon: " + str(len(delete_hosts)))
        for i in delete_hosts:
            print("Del -", i["host_name"])

        # Desactivate Host not in Pasteli
        for host in delete_hosts:
            # delHost(host, token)
            setHost(host["host_name"] + ";activate;0", token)

        # ADD HOST in GROUP
        for host in add_hosts:
            # Add Group and HC (Object may already exist)
            addGroup("HG_" + host.groups[0] + ";" + host.groups[0], token)
            addGroup("HG_" + host.collectors_centreon[0] + ";" + host.collectors_centreon[0], token)
            addHostCategory("HC_" + host.categories[0] + ";" + "HC_" + host.categories[0], token)

            # Add Host in Group
            addHost(host.hostname + ";" + str(host.id) + ";" + host.ip + ";" + host.templates_centreon[0] + ";" +
                host.collectors_centreon[0] + ";" + "HG_" + host.groups[0], token)

            # Add Host in Category and other Groups
            addMemberGroup("HG_" + host.collectors_centreon[0] + ";" + host.hostname, token)
            addMemberHostCategory("HC_" + host.groups[0] + ";" + host.hostname, token)

            setHost(host.hostname + ";2d_coords;" + host.geo_coords, token)

            applyTemplate(host.hostname, token)
            print("---")

        # SET ALL SERVICES DEPENDENCIES
        # os.system("ssh centreon@10.200.1.238 '/usr/lib/centreon/scripts/Indus_Dependencies.sh -R'")

        # Restart CFG Configuration for Poller 1
        if len(add_hosts) or len(delete_hosts) != 0:
            for poller in self.collectors:
                applyCFG(poller, token)
                # applyCFG("Central", token)
        else:
            print(
                "AUTOCENTREON - Pas besoin de redemarrer les Pollers - Aucun equipements ajouté ou supprimé dans centreon")
            logging.info(
                "AUTOCENTREON - Pas besoin de redemarrer les Pollers - Aucun equipements ajouté ou supprimé dans centreon")


