#!/bin/bash

#----------------------------------------------------
# 1. Captura de datos
#----------------------------------------------------

#Instala mariadb
sudo apt -y install sudo mariadb-server mariadb-client > /dev/null 2>&1



#----------------------------------------------------

#cfg cluster clusterMariaDB
[galera]
wsrep_on = ON
wsrep_cluster_name = {nombreDelCluster}
wsrep_provider = /usr/lib/galera/libgalera_smm.so
wsrep_cluster_address = "gcomm://{ipNodo01},...,{ipNodoN}"
binlog_format = row
default_storage_engine = InnoDB
innodb_autoinc_lock_mode = 2

# Allow server to accept connections on all interfaces.
bind-address = 0.0.0.0
wsrep_node_address={ipDelHost01}