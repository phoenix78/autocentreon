from main import *
from configuration import *
import os
import getpass
from xmlParser import *

import psycopg2


def printSelectTable(values, table, cur, conn):
    cur = con.cursor()
    cur.execute("SELECT " + values + " from " + table)
    rows = cur.fetchall()

    for row in rows:
        print(row, "\n")


def createTables(cur, conn):
    hosts_table = (
        """
        CREATE TABLE hosts (
           network_name varchar NOT NULL,
           router_name varchar NOT NULL,
           software_version varchar NOT NULL,
           serial_number varchar NOT NULL,
           model varchar NOT NULL,
           re_card boolean,
           update_time timestamp
        )
        """)

    address_table = (
        """ 
        CREATE TABLE address (
          hostname varchar,
          ifname varchar,
          address varchar,
          network varchar,
          update_time timestamp
        )
        """)

    interfaces_table = (
    """
    CREATE TABLE interfaces (
      hostname varchar NOT NULL,
      name varchar NOT NULL,
      description varchar NOT NULL,
      adminstatus varchar NOT NULL,
      operstatus varchar,
      update_time timestamp
    )
    """)

    instances_table = (
        """
    CREATE TABLE instances (
      hostname varchar,
      name varchar NOT NULL,
      type varchar NOT NULL,
      rd varchar,
      rt varchar,
      interface varchar,
      update_time timestamp
    )
    """)

    pasteli_table = (
    """
    CREATE TABLE pasteli (
      id serial,
      role varchar,
      sup_state varchar,
      equipement varchar,
      model varchar,
      ip_sup varchar,
      deploiement varchar
    )
    """)

    pems_table = (
    """
    CREATE TABLE pems (
      hostname varchar NOT NULL,
      name varchar NOT NULL,
      description varchar NOT NULL,
      adminstatus varchar NOT NULL,
      operstatus varchar,
      update_time timestamp
    )
    """)

    iface_table = (
    """
    CREATE TABLE iface (
      hostname varchar NOT NULL,
      version varchar NOT NULL,
      snmp varchar NOT NULL,
      interface varchar NOT NULL,
      address varchar NOT NULL,
      description varchar
    )
    """)

    cur.execute(hosts_table)
    cur.execute(address_table)
    cur.execute(interfaces_table)
    cur.execute(instances_table)
    cur.execute(pasteli_table)
    cur.execute(pems_table)
    cur.execute(iface_table)
    conn.commit()
    print("Tables created successfully")

def fillPasteli(role, sup_state, equipement, model, ip_sup, deploiement, conn, cur):
    sql = "INSERT INTO PASTELI (role, sup_state, equipement, model, ip_sup, deploiement) VALUES " \
          "('" + role + "','" + sup_state + "','" + equipement + "','" + model + "','" + ip_sup + "','" + deploiement + "')"
    print(sql)
    cur.execute(sql)
    conn.commit()


def fillIface(host, version, snmp, interface, address, description, conn, cur):
    sql = "INSERT INTO iface (hostname, version, snmp, interface, address, description) VALUES " \
          "('" + host + "','" + version + "','" + snmp + "','" + interface + "','" + address + "','" + description + "')"
    print(sql)
    cur.execute(sql)
    conn.commit()


def dropTable(table, cur, conn):
    sql = "DROP TABLE " + table
    cur.execute(sql)
    conn.commit()
    print("Drop Table", table)

def insertTable(value, table, cur, conn):
    sql = "INSERT INTO " + table + " VALUES ('" + value + "')"
    cur.execute(sql)
    conn.commit()

def printTable(table, cur):
    sql = "SELECT * FROM " + table
    cur.execute(sql)
    print("Print Table:", table)
    print(cur.fetchall())


def dbConnect(sqlhost, sqldb, sqluser, sqlpassword, sqlport):
    print("Trying Connect to DBHOST:", sqlhost, "DB:", sqldb, "User:", sqluser, "Port:", sqlport)
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s" % (sqlhost, sqldb, sqluser, sqlpassword, sqlport))
    cur = conn.cursor()
    print("-- CONNECTED TO", sqldb)
    return cur, conn


def dbDisconnect(conn):
    conn.close()
    print("-- Disconnected")



def autoDB():
    cur, conn = dbConnect(sqlhost, sqldb, sqluser, sqlpassword, sqlport)

    # Drop All tables
    dropTable("hosts", cur, conn)
    dropTable("address", cur, conn)
    dropTable("interfaces", cur, conn)
    dropTable("instances", cur, conn)
    dropTable("pasteli", cur, conn)
    dropTable("pems", cur, conn)
    dropTable("iface", cur, conn)

    createTables(cur, conn)

    '''
    for host in hosts_list:
        fillPasteli(host.role, host.etat_sup, host.hostname, host.model, host.ip, host.desserte, conn, cur)
    '''

    list_data = confParser()
    for data in list_data:
        for value in data.values():
             if (value.split(";")[0] or value.split(";")[1] or value.split(";")[2] or value.split(";")[3] or value.split(";")[4] or value.split(";")[5]) != None:
                fillIface(value.split(";")[0], value.split(";")[1], value.split(";")[2], value.split(";")[3], value.split(";")[4], value.split(";")[5], conn, cur)

    dbDisconnect(conn)
