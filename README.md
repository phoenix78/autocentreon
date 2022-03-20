# autocentreon
Docker, Postgres and python projets for centreon needs
### Configuration and Installation Prerequisite
#### Centreon Plateform 
* Centreon platform installed up and running
* Configure user for SQL MariaDB Connection (autocentreon.conf)
* Add Manually Host Template and Pollers (Collector) in Centreon web Plaform like in the "inventory.csv file"
* Add User un centreon web Platforms who can reach Centreon API

#### Script and VM
* Install _Docker_, _Docker-compose_ and _Make_ on your VM
* Configure _"autocentreon.conf"_ in "autocentreon/src/" with your credentials
* Configure your inventory list ("inventory/date.csv")
* Follow this columns order for : hostname, alias, IP, etat_sup, model, templates, pollers, groups, categories
* Setup a _.env_ file in root project directory with : 
   ``` shell
   POSTGRES_PASSWORD="phoenix"
   ```

Exemple autocentreon.conf : 
   ``` json
   {
        "inventory-path" : "inventory",
        "centreon-database" : {
            "host" : "192.168.1.5",
            "username":"centreon-db-user",
            "password":""
        },
        "centreon-api" : {
            "host" : "192.168.1.5",
            "username":"centreon-api-user",
            "password":""
        },
        "postgres": {
            "host" : "172.17.0.2",
            "username" : "postgres",
            "password" : "",
            "database" : "postgres",
            "port" : "5432"
        }
    }
   ```

### Run project 

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

Result Output : 
   ```shell
    Make: Starting environment containers.
    Recreating autoCentreon ... done
    Recreating database     ... done
   ```

4. Check Autocentreon logs 
   ```sh
   docker logs autoCentreon
   ```

Result Output : 
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
