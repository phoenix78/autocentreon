# autocentreon
Docker, Postgres and python projets for centreon needs
### Prerequisite

* Centreon platform installed up and running
* Configure "autocentreon.conf" in "autocentreon/src/" with your credentials
* Configure user for SQL MariaDB Connection (autocentreon.conf)
* Add Manually Host Template and Pollers (Collector) in Centreon web Plaform like in the "inventory.csv file"
* Configure your inventory list ("inventory/date.csv")   

Exemple : 
   ``` json
   {
        "inventory-path" : "inventory",
        "centreon-database" : {
            "host" : "192.168.1.5",
            "username":"autotrap",
            "password":"centreon"
        },
        "centreon-api" : {
            "host" : "192.168.1.5",
            "username":"clapi",
            "password":"clapi"
        },
        "postgres": {
            "host" : "172.17.0.2",
            "username" : "postgres",
            "password" : "autocentreon",
            "database" : "postgres",
            "port" : "5432"
        }
    }
   ```

### Installation

_Follow these steps for run the project._

1. Clone the repo
   ```sh
   git clone git@github.com:phoenix78/autocentreon.git
   ```
2. Navigate to autocentreon folder
   ```sh
   cd autocentreon
   ```
3. Build and Run containers 
   ```sh
   make
   ```

Output : 
   ```shell
    Make: Starting environment containers.
    Recreating autoCentreon ... done
    Recreating database     ... done
   ```

3. Check logs 
   ```sh
   docker logs autoCentreon
   ```

Output : 
   ```shell
    root@shark:/home/shark/autocentreon# docker logs autoCentreon
    Hosts list: 27
    Groups list: 28
    Templates list: 1
    Categories list: 28
    Collectors list: 1
    AUTOCENTREON - SUCCESS CONNECT - Token Centreon : <token>
    AUTOCENTREON - EQUIPEMENTS A AJOUTER: 0
    AUTOCENTREON - EQUIPEMENTS A SUPPRIMER: 0
    AUTOCENTREON - Pas besoin de redemarrer les Pollers - Aucun equipements ajouté ou supprimé dans centreon
   ```

<p align="right">(<a href="#top">back to top</a>)</p>
