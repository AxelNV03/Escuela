#!/bin/bash

# ---------------------------------------------------
# 0. Funciones
# ---------------------------------------------------

# Definir colores (si no están definidos)
verde="\033[0;32m"
reset="\033[0m"

# Función de Host Anfitrión del cluster
config(){
    echo -e "\n\t\t${verde}Configuracion de Host${reset}\n"
    
    #Instala mariadb
    sudo apt -y install sudo mariadb-server mariadb-client > /dev/null 2>&1

    # Tipo de accion
    echo -en "ELija una opcion:\n\t1. Maquina Nueva\n\t2. Agregar IP\n> "
    read n

    echo -en "¿La maquina actual es el cluster principal?\n1. Si\n2. Non\> "
    read c

    # Tipo de maquina
    if [ $n -eq 1 ]; then
        # Maquina nueva
        maquina_nueva
    elif [ $n -eq 2 ]; then
        # Agregar IP
        agregar_ip
    else
        echo "Opcion no valida"
        exit 1
    fi

    # Reinicia el servicio de MariaDB
    if [ $c -eq 1 ]; then
        sudo service mariadb stop
        sudo galera_new_cluster
        sudo systemctl start mariadb
    else
        sudo systemctl restart mariadb
    fi
}

# Para Galera
agregar_ip(){
    file=/etc/mysql/mariadb.conf.d/50-server.cnf

    # Preguntar la cantidad de IPs a agregar
    echo -en "Cantidad de IPs a agregar: "
    read n

    # Captura de IPs
    ips=()
    for i in $(seq 1 $n); do
        echo -en "IP $i: "
        read ip
        ips+=("$ip")
    done

    # Convertir el array a una cadena separada por comas
    ips_string=$(IFS=,; echo "${ips[*]}")
    ips_string=${ips_string//,/, } # Agregar espacio después de cada coma

    # Reemplaza "archivo.conf" con la ruta a tu archivo
    sed -i "s/\(wsrep_cluster_address = \"gcomm:[^\"]*\)\"/\1, $ips_string\"/" "$file"

    # Muestra mensaje de éxito
    echo -e "\n${verde}1. Se agregaron $n IPs al archivo de 50-server.cnf${reset}"
}

maquina_nueva(){
    file=/etc/mysql/mariadb.conf.d/50-server.cnf

    # Comentar el bind-address y pega lo de galera al final
    sudo sed -i 's/^bind-address/#bind-address/' $file
    
    # Muestra las ips del host
    echo -en "\nIps de la maquina actual:\n\t$(hostname -I)\n\n"

    # Datos
    echo -en "Nombre del cluster: "
    read clusterName
    echo -en "Cantidad de IPs a agregar: "
    read n
    echo -en "IP del host actual: "
    read local_ip

    # Validar la cantidad de IPs
    if [ $n -le 0 ]; then
        echo "Sin IPs a agregar"
    else
        # Captura de IPs
        ips=()
        for i in $(seq 1 $n); do
            echo -en "IP $i: "
            read ip
            ips+=("$ip")
        done

        # Convertir el array a una cadena separada por comas
        ips_string=$(IFS=,; echo "${ips[*]}")
        ips_string=${ips_string//,/, } # Agregar espacio después de cada coma
    fi


    # Crear el archivo de configuración
    echo -e "\n[galera]" >> $file
    echo "wsrep_on = ON" >> $file
    echo "cluster_name = $clusterName" >> $file
    echo "wsrep_provider = /usr/lib/galera/libgalera_smm.so" >> $file

    # Agregar las IPs al archivo de configuración
    if [ $n -le 0 ]; then
        echo "wsrep_cluster_address = \"gcomm://$local_ip\"" >> $file
    else
        echo "wsrep_cluster_address = \"gcomm://$local_ip, $ips_string\"" >> $file
    fi

    # Restante de la configuración
    echo "binlog_format = row" >> $file
    echo "default_storage_engine = InnoDB" >> $file
    echo "innodb_autoinc_lock_mode = 2" >> $file
    echo -e "\n# Allow server to accept connections on all interfaces." >> $file
    echo "bind-address = 0.0.0.0" >> $file
    echo "wsrep_node_address = $local_ip" >> $file
    
    # Muestra mensaje de éxito
    echo -e "\n${verde}1. Lineas de 50-server.cnf configuradas${reset}"
    exit 0
}

#----------------------------------------------------
# 1. Inicio
#----------------------------------------------------
config