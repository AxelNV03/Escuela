#!/bin/bash

# Definir colores (si no están definidos)
verde="\033[0;32m"
reset="\033[0m"

# -----------------------------------------------------
# 0. Funciones
# -----------------------------------------------------

# Función para obtener la IP del equipo según el número ingresado
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
#----------------------------------------------------
# 1. Captura de datos
#----------------------------------------------------

echo -e "\n\t\t${verde}Configuracion de Cliente${reset}\n"

# Solicitar el número de equipo
echo -en "Ingrese el número de cliente: "
read noClient

# Solicitar la llave privada del servidor
echo -en "Ingrese la llave privada del cliente: "
read private_key

# Solicitar la cantidad de clientes
echo -en "Ingrese la llave publica del servidor: "
read public_key

# Solicitar la interfaz de red del servidor
echo -en "Ingrese la IP real del server: "
read ip_server_real

# Solicitar el número de equipo
echo -en "Ingrese el número de equipo: "
read team

# Obtener la IP del equipo según el número ingresado
ip_equipo=$(obtener_ip_equipo $team)

# ------------------------------------------------------
# 2. Creacion de configuracion
# ------------------------------------------------------

touch clientVPN$team.conf
echo "[Interface]" >> clientVPN$team.conf
echo "PrivateKey = $private_key" >> clientVPN$team.conf
echo "ListenPort = 51820" >> clientVPN$team.conf
echo "Address = $ip_equipo.$((noClient+1))/32" >> clientVPN$team.conf
echo "DNS = 8.8.8.8" >> clientVPN$team.conf
echo "" >> clientVPN$team.conf
echo "[Peer]" >> clientVPN$team.conf
echo "PublicKey = $public_key" >> clientVPN$team.conf
echo "AllowedIPs = 0.0.0.0/0" >> clientVPN$team.conf
echo "Endpoint = $ip_server_real:51820" >> clientVPN$team.conf
echo "PersistentKeepalive = 30" >> clientVPN$team.conf

# ------------------------------------------------------
echo -e "\n\t\t${verde}Configuracion de Cliente finalizada${reset}\n"
ls