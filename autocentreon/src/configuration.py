import glob
import sys

perimeter = "infranet"
extract_pasteli = glob.glob("inventory/" + perimeter.upper() + "*.csv")[-1]  # Extract Local

### Centreon
#centreon_host = "https://10.200.1.238"
centreon_host = "http://192.168.1.5"
centreon_user = "clapi"
centreon_password = "clapi"

### CENTREON DB
centreondb = "192.168.1.5"
centreonuser = "autotrap"
centreonpass = "centreon"

### POSTGRES 
sqlhost = "172.17.0.2"
sqluser = "postgres"
sqlpassword = "infranetdb"
sqldb = "postgres"
sqlport = "5432"

### Arguments
argumentList = sys.argv[1:]
options = "hpcdrasbt"
long_options = ["help", "pasteli", "centreon", "dns", "radius", "ansible", "securecrt", "bdd", "test"]


### Lists Extract Temporaire
desserte_list = []
model_list = []
hosts_list = []
poller_list = []
template_list = []