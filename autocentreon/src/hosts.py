class hosts:
    def __init__(self):
        self.id = None
        self.alias = None
        self.hostname = None
        self.ip = None
        self.etat_sup = None
        self.model = None
        self.geo_coords = None
        self.categories = list()
        self.groups = list()
        self.templates_centreon = list()
        self.collectors_centreon = list()

    # SETS
    def set_id(self, id):
        self.id = id

    def set_alias(self, alias):
        self.alias = alias

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_ip(self, ip):
        self.ip = ip

    def set_etat_sup(self, etat_sup):
        self.etat_sup = etat_sup

    def set_model(self, model):
        self.model = model

    def set_geo_coords(self, geo_coords):
        self.geo_coords = geo_coords

    def set_groups(self, groups):
        for group in groups:
            self.groups.append(group)

    def set_templates_centreon(self, templates_centreon):
        for template in templates_centreon:
            self.templates_centreon.append(template)

    def set_collectors_centreon(self, collectors_centreon):
        for collector in collectors_centreon:
            self.collectors_centreon.append(collector)

    def set_categories(self, categories):
        for category in categories:
            self.categories.append(category)

    # GETS
    def get_id(self):
        return self.id

    def get_alias(self):
        return self.alias

    def get_hostname(self):
        return self.hostname

    def get_ip(self):
        return self.ip

    def get_etat_sup(self):
        return self.etat_sup

    def get_model(self):
        return self.model

    def get_geo_coords(self):
        return self.geo_coords

    def get_groups(self):
        return self.groups

    def get_templates_centreon(self):
        return self.templates_centreon

    def get_collectors_centreon(self):
        return self.collectors_centreon

    def get_categories(self):
        return self.categories

    # METHODS
    def create(self, id, alias, hostname, ip, etat_sup, model, geo_coords, groups, templates_centreon, collectors_centreon, categories):
        self.id = id
        self.alias = alias
        self.hostname = hostname
        self.ip = ip
        self.etat_sup = etat_sup
        self.model = model
        self.geo_coords = geo_coords
        self.groups = groups
        self.templates_centreon = templates_centreon
        self.collectors_centreon = collectors_centreon
        self.categories = categories

    def print(self):
        print("id :", self.id)
        print("alias :", self.alias)
        print("hostname :", self.hostname)
        print("ip :", self.ip)
        print("etat_sup :", self.etat_sup)
        print("model :", self.model)
        print("geo_coords :", self.geo_coords)
        print("groups :", self.groups)
        print("categories :", self.categories)
        print("templates :", self.templates_centreon)
        print("collectors :", self.collectors_centreon)


