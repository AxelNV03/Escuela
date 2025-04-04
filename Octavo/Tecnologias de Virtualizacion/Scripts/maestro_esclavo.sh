#!/bin/bash

#Colores
rojo="\033[1;31m"
verde="\033[1;32m"
amarillo="\033[1;33m"
reset="\033[0m"


#----------------------------------------------------
# 0. funciones
#----------------------------------------------------

#Funcion para la maquina maestro
maestro() {
    sudo mariadb -e "CREATE USER 'replica'@'%' IDENTIFIED BY 'replica';"
    sudo mariadb -e "GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';"

    #Ejecuta el comando show master status
    sql=$(echo "SHOW MASTER STATUS\G;" | sudo mariadb)

    #Extrae el valor de position
    position=$(echo "$sql" | grep -oP 'Position: \K\d+')
    file=$(echo "$sql" | grep -oP 'File: \K\S+')

    #Muestra los valores
    echo -e "${verde}\tFile: ${reset}$file"
    echo -e "${verde}\tPosition: ${reset}$position"
    echo -e "${amarillo}\nAhora configura la maquina Esclava\n"
    sudo mariadb
}

#Funcion para la maquina esclavo
esclavo() {
    echo -en "\n${amarillo}IP de la maquina Maestra(ejemplo: 192.168.56.105):${reset}\n> "
    read ip
    echo -en "\n${amarillo}File de la maquina maestra (ejemplo: mysql-bin.000001):${reset}\n> "
    read file
    echo -en "\n${amarillo}Position de la maquina maestra (ejemplo: 771):${reset}\n> "
    read position

    sudo mariadb -e "STOP SLAVE;"
    sudo mariadb -e "CHANGE MASTER TO MASTER_HOST='$ip', MASTER_USER='replica', MASTER_PASSWORD='replica', MASTER_LOG_FILE='$file', MASTER_LOG_POS=$position;"
    sudo systemctl restart mariadb
    echo -e "\n${verde}3. Host Esclavo configurado${reset}"
    echo -e "${verde}\n\tConfiguracion Finalizada${reset}\n"
    sudo mariadb
}

# Función para modificar una línea en el archivo de configuración de MariaDB
conf_db(){
    server_id=$1

    # Definir la ruta y las lineas del archivo de configuración
    ruta="/etc/mysql/mariadb.conf.d/50-server.cnf"
    lines="\nserver-id = $server_id\nlog_bin = /var/log/mysql/mysql-bin.log"

    # Agrega las líneas al archivo de configuración
    agregar_lineas "$ruta" "$lines"    

    #Comenta la linea de bind
    sudo awk 'NR == 27 { $0 = "#" $0 } { print }' "$ruta" > temp && sudo mv temp "$ruta"

    echo -e "${verde}1. Lineas de 50-server.cnf configuradas${reset}"

    # creas las carpetas con sus permisos correspondientes
    sudo mkdir -m 2750 /var/log/mysql
    sudo chown mysql /var/log/mysql

    echo -e "${verde}2. Directorios Creados${reset}"

    # Reinicia el servicio de MariaDB
    sudo systemctl restart mariadb
}

# Función para agregar líneas al archivo de configuración de MariaDB
agregar_lineas(){
    local path="$1"
    local new_lines="$2"
    linea_buscar="# \$ sudo chown mysql /var/log/mysql"

    sudo awk -v linea="$linea_buscar" -v nuevo="$new_lines" '
    {
        print
        if ($0 == linea) {
            printf "%s\n", nuevo
        }
    }' "$path" > temp && sudo mv temp "$path"
}

#----------------------------------------------------
# 1. Captura de datos
#----------------------------------------------------
echo -en "\n${rojo}Nota:${reset} Debes tener la configuracion de la ED1 y el adaptador puente activo"
echo -en "\n${amarillo}Elige el tipo de maquina\n\t1. Maestro\n\t2. Esclavo${reset}\n\nElige una opcion:  "
read tipo

# Validación de la opción
if [ "$tipo" -eq 1 ]; then
    maquina="Maestro"
elif [ "$tipo" -eq 2 ]; then
    maquina="Esclavo"
else
    echo -e "\n\t${rojo}Opción no válida. Cerrando script${reset}\n"
    exit 1
fi

# Solicitar el server-id
echo -en "¿Elige el ${verde}server-id${reset} de la maquina $maquina? (ejemplo: 1): "
read server_id

#----------------------------------------------------
# 2. Configuración de lasmáquinas 
#----------------------------------------------------
#Actualiza el sistema
sudo apt update && sudo apt upgrade -y > /dev/null
echo -e "\n${amarillo}Configurando la maquina como $maquina.${reset}\n"
conf_db "$server_id"
sleep 1

# Tipo de maquina
if [ "$tipo" -eq 1 ]; then
    echo -e "${verde}3. Usuario replica creado y configurado${reset}"
    echo -e "\n${amarillo}Comfiguracion Finalizada. \n ${reset}"
    echo -e "\t${verde}server-id: ${reset}$server_id"
    maestro        
else
    esclavo 
fi

