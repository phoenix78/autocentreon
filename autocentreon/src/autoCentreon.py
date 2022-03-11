from main import *
from configuration import *
import requests
import urllib3
### IMPORTANT DELETE WARNING SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# LOGFILE
import logging
logging.basicConfig(level=logging.DEBUG, filename="logs/autocentreon.log", filemode="a", format='%(asctime)s - %(levelname)s - %(message)s')


# Si host et chost sont égaux
def update_host_parameters(host, chost, token):
    change = False
    if chost["host_alias"] != str(host.role + " " + host.etat_sup):
        setHost(host.hostname + ";alias;" + str(host.role + " " + host.etat_sup), token)
        change = True
    if chost["host_address"] != host.ip:
        setHost(host.hostname + ";address;" + host.ip, token)
        change = True
    if chost["host_activate"] != "1":
        setHost(host.hostname + ";activate;1", token)
        change = True
    if chost["TEMPLATE"] != host.template_centreon:
        setTemplate(host.hostname, host.template_centreon, token)
        change = True
    if chost["POLLER"] != host.collector_centreon:
        setPoller(host.hostname, host.collector_centreon, token)
        change = True
    if chost["HOST_CATEGORY"] != "HC_" + host.desserte:
        addMemberHostCategory("HC_" + host.desserte + ";" + host.hostname, token)
        change = True
    if chost["2d_coords"] != str(host.longitude) + "," + str(host.latitude):
        setHost(host.hostname + ";2d_coords;" + str(host.longitude) + "," + str(host.latitude), token)
        change = True
    # CHECK MULTI GROUP (HG_GROUP + HG_POLLER)
    if "," in chost["HOSTGROUP"]:
        state_group = False
        state_collector = False

        for group in chost["HOSTGROUP"].split(","):
          if group == "HG_" + host.desserte:
            state_group = True
          if group == "HG_" + host.collector_centreon:
            state_collector = True

        if not state_group:
            addMemberGroup("HG_" + host.desserte + ";" + host.hostname, token)
            change = True
        if not state_collector:
            addMemberGroup("HG_" + host.collector_centreon + ";" + host.hostname, token)
            change = True
    else:
        addMemberGroup("HG_" + host.desserte + ";" + host.hostname, token)
        addMemberGroup("HG_" + host.collector_centreon + ";" + host.hostname, token)
        change = True

    ### On applique toujours le template sur un host afin de prendre en compte les dernières modification du template d'hôte
    if change:
      applyTemplate(host.hostname, token)
    return change


# List of equipements for adding them in centreon
def diff_hosts_pasteli(hosts_list, chosts_list, token):
    add_list = []
    restart = False
    for host in hosts_list:
        cond = False
        change = False
        for chost in chosts_list:
            if host.hostname == chost['host_name']:
                change = update_host_parameters(host, chost, token)
                cond = True
            if change:
                restart = True
        if not cond:
          add_list.append(host)
    # S'il y a eu au moins une synchro (update_host_parameter) on redemarre les pollers
    if restart:
        for poller in poller_list:
            applyCFG(poller, token)
            #applyCFG("Central", token)
    return add_list


# List of equipements for delete from centreon
def diff_hosts_centreon(hosts_list, chosts_list, token):
    del_list = []
    for chost in chosts_list:
        cond = False
        for host in hosts_list:
            if chost['host_name'] == host.hostname:
                cond = True
        if not cond:
            # HOST NOT ACTIVATE
            if chost["host_activate"] != "0":
                del_list.append(chost)
    return del_list


def post_show(myObject, action, token):
    heady = {'Content_Type': 'application/json', 'centreon-auth-token':token}
    cmd = requests.post(centreon_host + '/centreon/api/index.php?action=action&object=centreon_clapi', headers=heady,
                        json={"object": myObject, "action": action}, verify=False)
    logging.info("Post show - " + myObject + " " + action)
    cmd = cmd.json()
    return cmd['result']


def post_cfg(action, values, token):
    heady = {'Content-Type': 'application/json', 'centreon-auth-token': token}
    cmd = requests.post(centreon_host + '/centreon/api/index.php?action=action&object=centreon_clapi', headers=heady,
                        json={"action": action, "values": values}, verify=False)
    logging.info("Post CFG - " + action + " " + values)
    cmd = cmd.json()
    return cmd['result']


def post_values(action, myObject, values, token):
    heady = {'Content-Type': 'application/json', 'centreon-auth-token': token}
    cmd = requests.post(centreon_host + '/centreon/api/index.php?action=action&object=centreon_clapi', headers=heady,
                        json={"object": myObject, "action": action, "values": values}, verify=False)
    logging.info("Post Values - " + myObject + " " + action + " " + values)
    cmd = cmd.json()
    return cmd


def getToken(centreon_user, centreon_password):
    token = requests.post(centreon_host + '/centreon/api/index.php?action=authenticate',
                          data={"username": centreon_user, "password": centreon_password}, verify=False)
    token = token.json()
    #print(token)
    return token['authToken']


def getAllHostsInfo():
    #sqlquery = "SELECT HST.*,HTPL.host_name AS TEMPLATE,  NS.name AS POLLER, GROUP_CONCAT(HG.hg_name) AS HOSTGROUP FROM centreon.host as HST LEFT JOIN centreon.host_template_relation AS HTR ON HST.host_id=HTR.host_host_id  LEFT JOIN centreon.host AS HTPL ON HTR.host_tpl_id=HTPL.host_id LEFT JOIN centreon.ns_host_relation AS NHR ON NHR.host_host_id=HST.host_id LEFT JOIN centreon.nagios_server AS NS ON NS.id=NHR.nagios_server_id LEFT JOIN centreon.hostgroup_relation AS HGR ON HGR.host_host_id=HST.host_id LEFT JOIN centreon.hostgroup AS HG ON HGR.hostgroup_hg_id=HG.hg_id  WHERE HST.host_register='1' AND HG.hg_name like '%HG%' group by HST.host_name order by HST.host_name, HG.hg_name"
    sqlquery = "SELECT HST.*,HTPL.host_name AS TEMPLATE,EHI.ehi_2d_coords AS 2d_coords, HC.hc_name AS HOST_CATEGORY, NS.name AS POLLER, GROUP_CONCAT(HG.hg_name) AS HOSTGROUP FROM centreon.host as HST LEFT JOIN centreon.host_template_relation AS HTR ON HST.host_id=HTR.host_host_id LEFT JOIN centreon.host AS HTPL ON HTR.host_tpl_id=HTPL.host_id LEFT JOIN centreon.extended_host_information AS EHI ON EHI.host_host_id=HST.host_id LEFT JOIN centreon.hostcategories_relation AS HCR on HCR.host_host_id=HST.host_id LEFT JOIN centreon.hostcategories AS HC on HC.hc_id=HCR.hostcategories_hc_id LEFT JOIN centreon.ns_host_relation AS NHR ON NHR.host_host_id=HST.host_id LEFT JOIN centreon.nagios_server AS NS ON NS.id=NHR.nagios_server_id LEFT JOIN centreon.hostgroup_relation AS HGR ON HGR.host_host_id=HST.host_id LEFT JOIN centreon.hostgroup AS HG ON HGR.hostgroup_hg_id=HG.hg_id WHERE HST.host_register='1' AND HG.hg_name like '%HG%' group by HST.host_name order by HST.host_name, HG.hg_name"
    connection = pymysql.connect(host=centreondb,user=centreonuser,password=centreonpass, cursorclass=pymysql.cursors.DictCursor)
    with connection:
      with connection.cursor() as cursor:
        cursor.execute(sqlquery)
        result = cursor.fetchall()
    return result


def showGroups(token):
    response = post_show("HG", "show", token)
    #for group in response:
    #    print(group['id'], group['name'], group['alias'])
    return response


def showHosts(token):
    response = post_show("HOST", "show", token)
    #for host in response:
    #    print(host['id'], host['name'], host['alias'], host['address'], host['activate'])
    return response


def showHostTemplate(token):
    response = post_show("HTPL", "show", token)
    for ch in response:
        print(ch['id'], ch['name'], ch['alias'], ch['address'], ch['activate'])
    return response


def getAllHostsParameters(token):
    response = post_show("HOST", "show", token)
    for host in response:
        getParameters(host['name'], token)
    return response

def getParameters(chost, token):
    values = chost + ";" + "address|alias|name|snmp_version|snmp_community|timezone|passive_checks_enabled|activate|geo_coords|host_notification_options|2d_coords"
    response = post_values("getparam", "HOST", values, token)
    return response

def getMembersGroups(group, token):
    response = post_values("getmember", "HG", group, token)
    return response['result']

def getAllMembersGroups(token):
    response = post_show("HG", "show", token)
    for group in response:
        res = getMembersGroups(group['name'], token)
        for r in res:
            print("GROUP:", group['name'], r['id'], r['name'])

def getAllTemplate(token):
    response = post_show("HOST", "show", token)
    for host in response:
        res = getTemplate(host['name'], token)
        print(host['name'], ":", res['id'], res['name'])

def getTemplate(host, token):
    response = post_values("gettemplate", "HOST", host, token)
    return response['result'][0]

def setTemplate(host, template, token):
    response = post_values("settemplate", "HOST", host + ";" + template, token)
    applyTemplate(host, token)
    print("UPDATE HOST TEMPLATE:", host, template)
    return response

def setPoller(host, poller, token):
    response = post_values("setinstance", "HOST", host + ";" + poller, token)
    print("UPDATE POLLER:", host, poller)
    return response


def showServiceTemplate(token):
    response = post_show("STPL", "show", token)
    for st in response:
        print(st['id'], st['description'], st['alias'])
    return response


def addGroup(values, token):
    response = post_values("add", "HG", values, token)
    print("ADD GROUP:", values, response)

def addMemberGroup(values, token):
    response = post_values("addmember", "HG", values, token)
    print("ADD MEMBER GROUP:", values, response)

def addHostCategory(values, token):
    response = post_values("add", "HC", values, token)
    print("ADD GROUP CATEGORY:", values, response)

def addMemberHostCategory(values, token):
    response = post_values("addmember", "HC", values, token)
    print("ADD MEMBER HOST CATEGORY:", values, response)

def setMemberHostCategory(values, token):
    response = post_values("setmember", "HC", values, token)
    print("SET MEMBER HOST CATEGORY:", values, response)

def addHost(values, token):
    response = post_values("add", "HOST", values, token)
    print("ADD HOST:", values, response)


def setHost(values, token):
    response = post_values("setparam", "HOST", values, token)
    print("UPDATE HOST:", values, response['result'])


def setGroup(values, token):
    response = post_values("setmember", "HG", values, token)
    print("SET GROUP:", values, response)


def delHost(values, token):
    response = post_values("del", "HOST", values, token)
    print("DEL HOST:", values, response)


def delAllHosts(token):
    response = post_show("HOST", "show", token)
    for host in response:
        delHost(host['name'], token)
    return response


def delGroup(values, token):
    response = post_values("del", "HG", values, token)
    print("DEL GROUP:", values, response)


def delAllGroups(token):
    response = post_show("HG", "show", token)
    for group in response:
        delGroup(group['name'], token)
    return response


# "hosts;ServiceDescription;iftrap"
def addService(values, token):
    response = post_values("add", "SERVICE", values, token)
    print("ADD SERVICE:", values, response)


# "hosts;ServiceDescription;Activate;1"
def setService(values, token):
    response = post_values("setparam", "SERVICE", values, token)
    print("SET SERVICE:", values, response)


# "hosts;ServiceDescription;Activate;0"
def delService(values, token):
    response = post_values("del", "SERVICE", values, token)
    print("DEL SERVICE:", values, response)


def applyTemplate(values, token):
    response = post_values("applytpl", "HOST", values, token)
    print("APPLY TPL:", values, response)


# Configuration Functions
def pollerGenerate(values, token):
    response = post_cfg("POLLERGENERATE", values, token)
    print(response)


def pollerTest(values, token):
    response = post_cfg("POLLERTEST", values, token)
    print(response)


def cfgMove(values, token):
    response = post_cfg("CFGMOVE", values, token)
    print(response)


def pollerRestart(values, token):
    response = post_cfg("POLLERRESTART", values, token)
    print(response)


# ALL Configuration Function in One
def applyCFG(values, token):
    response = post_cfg("APPLYCFG", values, token)
    print("APPLY CFG : ")
    if "OK" in response[2]:
        print(response[1])
        print(response[2])
        print(response[3])
    else:
        print(response)


# Main AutoCentreon
def autoCentreon(hosts_list, desserte_list, centreon_user, centreon_password):
    token = getToken(centreon_user, centreon_password)
    print("AUTOCENTREON - SUCCESS CONNECT - Token Centreon :", token)
    logging.info("AUTOCENTREON - SUCCESS CONNECT - Token Centreon : " + token)
   
    all_hosts_info = getAllHostsInfo()
    #getAllTemplate(token)
    #showHosts(token)
    #showGroups(token)
    #showServiceTemplate(token)
    #showHostTemplate(token)

    #delAllHosts(token)
    #delAllGroups(token)
   
    # LIST OF HOST NOT IN CENTREON and UPDATE HOST IN CENTREON
    add_hosts = diff_hosts_pasteli(hosts_list, all_hosts_info, token)
    delete_hosts = diff_hosts_centreon(hosts_list, all_hosts_info, token)
    
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
        #delHost(host, token)
        setHost(host["host_name"] + ";activate;0", token)

    # ADD HOST in GROUP
    for host in add_hosts:
        #Add Group and HC (Object may already exist)
        addGroup("HG_" + host.desserte + ";" + host.desserte, token)
        addGroup("HG_" + host.collector_centreon + ";" + host.collector_centreon, token)
        addHostCategory("HC_" + host.desserte + ";" + "HC_" + host.desserte, token)

        #Add Host in Group
        addHost(host.hostname + ";" + str(host.id) + ";" + host.ip + ";" + str(host.template_centreon) + ";" + str(host.collector_centreon) + ";" + "HG_" + host.desserte, token)

        # Add Host in Category and other Groups
        addMemberGroup("HG_" + host.collector_centreon + ";" + host.hostname, token)
        addMemberHostCategory("HC_" + host.desserte + ";" + host.hostname, token)

        setHost(host.hostname + ";2d_coords;" + str(host.longitude) + "," + str(host.latitude), token)

        applyTemplate(host.hostname, token)
        print("---")
    
    #SET ALL SERVICES DEPENDENCIES
    #os.system("ssh centreon@10.200.1.238 '/usr/lib/centreon/scripts/Indus_Dependencies.sh -R'")
    
    # Restart CFG Configuration for Poller 1
    if len(add_hosts) or len(delete_hosts) != 0:
        for poller in poller_list:
            applyCFG(poller, token)
            #applyCFG("Central", token)
    else:
        print("AUTOCENTREON - Pas besoin de redemarrer les Pollers - Aucun equipements ajouté ou supprimé dans centreon")
        logging.info("AUTOCENTREON - Pas besoin de redemarrer les Pollers - Aucun equipements ajouté ou supprimé dans centreon")

