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

echo -e "\n\t\t${verde}Configuracion de Host Anfitrion${reset}\n"

# Solicitar la llave privada del servidor
echo -en "Ingrese la llave privada del server: "
read private_key

# Solicitar la cantidad de clientes
echo -en "Ingrese la cantidad de clientes: "
read n

# Solicitar la interfaz de red del servidor
echo -en "Ingrese la interfaz de red del servidor: "
read interfaz

# Solicitar el número de equipo
echo -en "Ingrese el número de equipo: "
read team

# Obtener la IP del equipo según el número ingresado
ip_equipo=$(obtener_ip_equipo $team)

# ------------------------------------------------------
# 2. Creacion de configuracion
# ------------------------------------------------------

# Crear el archivo de configuración del servidor
cat <<EOL > /etc/wireguard/wgvpn0$team.conf
[Interface]
Address = $ip_equipo.1/24
PrivateKey = $private_key
ListenPort = 51820

#Rutas para manejar el trafico y tener acceso a la red
PostUp = sysctl -w net.ipv4.ip_forward=1; iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o $interfaz -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0; iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o $interfaz -j MASQUERADE

EOL

# ciclo for para agregar los clientes
for ((i=0; i<n; i++)); do
    echo "# PC cliente $((i+1))" >> /etc/wireguard/wgvpn0$team.conf
    echo "[Peer]" >> /etc/wireguard/wgvpn0$team.conf
    
    echo -en "\n Ingrese la llave publica del cliente $((i+1)): "
    read public_key

    echo "PublicKey = $public_key" >> /etc/wireguard/wgvpn0$team.conf
    echo "AllowedIPs = $ip_equipo.$((i+2))/32" >> /etc/wireguard/wgvpn0$team.conf
    echo -e "" >> /etc/wireguard/wgvpn0$team.conf
done

# ------------------------------------------------------
sudo systemctl start wg-quick@wgvpn0$team
sudo wg show
echo -en "\n${verde}Archivo de configuración creado${reset}\n"