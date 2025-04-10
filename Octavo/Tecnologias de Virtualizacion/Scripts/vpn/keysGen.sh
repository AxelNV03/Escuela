#!/bin/bash

# -----------------------------------------------------
# 0. Funciones
# -----------------------------------------------------

# Definir colores (si no están definidos)
verde="\033[0;32m"
reset="\033[0m"

# Función de Host Anfitrión del servidor VPN
host_anfitrion() {
    apt-get -y install wireguard wireguard-tools openresolv iptables iptables-persistent > /dev/null 2>&1
    clear
    echo -e "\n\t\t${verde}Configuracion de Host Anfitrion${reset}\n"
    echo -en "Ingrese el numero de claves a generar: "
    read n

    # Llamar a la función para generar claves
    generar_claves $n

}

# Funcion para generar las claves
generar_claves() {
    n=$1 # Número de claves a generar
    path=$(pwd)

    # Para generar las IPS 
    echo -en "Ingrese el numero de equipo: "
    read team

    # Obtener la IP del equipo según el número ingresado
    ip_equipo=$(obtener_ip_equipo $team)
    
   # Crear el archivo claves.txt
    touch $path/llaves.txt

    # Bucle para generar las llaves
    for ((i=0; i<n+1; i++)); do
        # Generar las llaves privada y pública
        wg genkey | tee privatekey | wg pubkey > publickey

        # Leer las llaves generadas
        private_key=$(cat privatekey)
        public_key=$(cat publickey)

        # Verificar si es el primer ciclo
        if ((i == 0)); then
            echo "# Llaves del servidor" >> $path/llaves.txt
            echo "IP  --> $ip_equipo.1/24" >> $path/llaves.txt
        else
            echo "# Llaves del cliente 0$i" >> $path/llaves.txt
        fi

        # Escribir las llaves en el archivo
        if ((i != 0)); then
            echo "IP  --> $ip_equipo.$((i+1))/32" >> $path/llaves.txt
        fi
        echo "Pri --> $private_key" >> $path/llaves.txt
        echo "Pub --> $public_key" >> $path/llaves.txt
        echo -e "" >> $path/llaves.txt


        # Eliminar archivos temporales de llaves
        rm privatekey publickey
    done
    
    # Muestra el contenido del archivo de llaves
    # clear
    cat $path/llaves.txt
}

# Función de Host Anfitrión del servidor VPN
obtener_ip_equipo() {
    local numero_equipo=$1

    case $numero_equipo in
        1) echo "11.0.0" ;;
        2) echo "12.0.0" ;;
        3) echo "13.0.0" ;;
        4) echo "14.0.0" ;;
        5) echo "15.0.0" ;;
        6) echo "16.0.0" ;;
        7) echo "17.0.0" ;;
        8) echo "18.0.0" ;;
        9) echo "19.0.0" ;;
        10) echo "20.0.0" ;;
        11) echo "21.0.0" ;;
        *) echo "Número de equipo inválido" ;;
    esac
}

# -----------------------------------------------------
# 1. Generar claves
# -----------------------------------------------------
host_anfitrion

echo -en "\n${verde}Llaves guardadas en llaves.tx\nSe utilizaran en el script del servidor${reset}\n\n"
