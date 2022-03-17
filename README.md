# autocentreon
Docker, Postgres and python projets for centreon needs

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
