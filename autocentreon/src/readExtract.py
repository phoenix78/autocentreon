from main import *
from configuration import *
from host import *
from collections import namedtuple


def check_input_extract(role, etat, hostname, model, ip, desserte, template):
    res = 0
    # ERROR
    if etat == "":
        print("ERROR IN ETAT SUP - L'EQUIPEMENT:", hostname, "n'a pas de etat")
        res = 1
    if ip == "" and etat != "ZERO":
        print("ERROR Association IP / ETAT SUP - l'équipement:", hostname,
              "n'a pas d'adresse IP et est en supervision:", etat)
        res = 1

    # WARNING
    if hostname == "" and etat != "ZERO":
        print("WARNING IN HOSTNAME - L'EQUIPEMENT:", role, etat, model, ip, desserte, "n'a pas de nom")
    if model == "" and etat != "ZERO":
        print("WARNING IN MODEL - L'EQUIPEMENT:", hostname, "n'a pas de model")
    if role == "" and etat != "ZERO":
        print("WARNING IN MODEL - L'EQUIPEMENT:", hostname, "n'a pas de role")
    if desserte == "" and etat != "ZERO":
        print("WARNING IN MODEL - L'EQUIPEMENT:", hostname, "n'a pas de desserte")
    if template == "" and etat != "ZERO":
        print("WARNING IN MODEL - L'EQUIPEMENT:", hostname, "n'a pas de template")

    return res

def read_csv(extract_pasteli):
    print("--- Read Pasteli Extract: ", extract_pasteli.replace('\\', '/'))
    Headers = namedtuple('Headers', 'role, etat, equipement, model, ip, template, poller, longitude, latitude, group')
    file = open(extract_pasteli, newline='', encoding='latin-1')
    with file as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        response = 0
        for header in map(Headers._make, spamreader):
            # Variables
            role = header.role.split(":")[-1].upper().replace("È", "E").replace("É", "E").replace("Î", "I").replace(" ", "")
            etat = header.etat
            hostname = header.equipement
            model = header.model.upper().replace(" ", "_").replace("-","").upper()
            ip = header.ip
            template = header.template
            poller = header.poller
            longitude = header.longitude
            latitude = header.latitude
            desserte = header.group.split(perimeter.upper() + " - ")[-1].upper()\
                .replace(" - ","_").replace("-","_").replace(" ","_").replace("(","").replace(")","").replace("__","_")\
                .replace("È", "E").replace("É", "E").replace("Î", "I").replace("Ç", "C")


            # ON VERIFIE CHAQUE VARIABLE
            if check_input_extract(role, etat, hostname, model, ip, desserte, template) == 1:
                response = 1

            # Create List
            ## EQUIPEMENT DIFFERENT DE ZERO UNIQUEMENT !
            if etat != "ZERO" or "":
                host = Host(role + " " + etat, hostname, ip, role, etat, model, desserte, template, poller, longitude, latitude)
                hosts_list.append(host)
                if desserte not in desserte_list:
                   desserte_list.append(desserte)
                if poller not in poller_list:
                    poller_list.append(poller)
                if template not in template_list:
                    template_list.append(poller)
                if model not in model_list:
                   model_list.append(model)

        # ATTENTION POP HEADER du CSV !
        desserte_list.pop(0)
        model_list.pop(0)
        hosts_list.pop(0)
        poller_list.pop(0)
        template_list.pop(0)

        if response == 1:
            print("ERROR -- ERROR BELOW, PLEASE CHECK BEFORE RE-EXECUTE")
            sys.exit(1)
