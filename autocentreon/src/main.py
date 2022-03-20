from hosts import *
from autocentreon import *


def main():
    autoC = autocentreon()

    # Load conf file in class
    autoC.load_conf()
    #autoC.print_conf()

    # Load CSV file in class
    autoC.load_csv(csv_file="inventory/20220103.csv")

    autoC.print_sizelists()
    #autoC.print_lists()

    # Execute
    autoC.execute()

if __name__ == "__main__":
    main()