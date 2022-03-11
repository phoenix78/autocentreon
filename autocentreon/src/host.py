class Host:
    def __init__(self, id_pasteli, hostname, ip, role, etat_sup, model, desserte, template, poller, longitude, latitude):
        self.id = id_pasteli
        self.role = role
        self.hostname = hostname
        self.ip = ip
        self.etat_sup = etat_sup
        self.model = model
        self.desserte = desserte
        self.template_centreon = template
        # self.collector_centreon = poller
        self.collector_centreon = "Central"

        if longitude == "":
            self.longitude = "0"
        else:
            self.longitude = longitude

        if latitude == "":
            self.latitude = "0"
        else:
            self.latitude = latitude
        if "COMM" in hostname:
            self.comm = True
        else:
            self.comm = False
