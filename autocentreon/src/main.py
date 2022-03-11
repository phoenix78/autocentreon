#!/usr/bin/python3

import pymysql
import json
import csv
import os
import getopt
import requests

from configuration import *
from readExtract import *
from autoCentreon import *
import host
from print import *

                    
def main():
    try:

        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                print("--- Help\n")
                print("Options :")
                print("\t -p (pasteli)(Obligatoire), -c (centreon), -d (dns), -r (radius), -a (ansibleHost), -s (secureCRT)")

            elif currentArgument in ("-p", "--pasteli"):
                read_csv(extract_pasteli)
                print_sizelist()
                #print_lists()

            elif currentArgument in ("-c", "--centreon"):
                print("--- Start AutoCentreon")
                autoCentreon(hosts_list, desserte_list, centreon_user, centreon_password)

        
            elif currentArgument in ("-t", "--test"):
                #autoSSH()
                print("--- Start Test")
    except getopt.error as err:
        print(str(err))


if __name__ == "__main__":
    main()
