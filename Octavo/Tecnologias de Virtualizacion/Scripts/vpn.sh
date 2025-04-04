#!/bin/bash

# -----------------------------------------------------
# 1. Instalar Sudo
# -----------------------------------------------------

apt-get update #Actualiza
apt-get install -y sudo #Instala sudo

# -----------------------------------------------------
# 2. Agrega al usuario de la VM al sudoers
# -----------------------------------------------------

user=$(ls /home/) #Extrae el username

#Lo agrega en el sudoers
echo -e "\n$user\tALL=(ALL:ALL) ALL" >> /etc/sudoers

# -----------------------------------------------------
# 3. Carga los Repositorios y actualiza
# -----------------------------------------------------

#Establece la ruta del archivo
archivo="/etc/apt/sources.list"

# Procesar las líneas para agregar no-free contrib (3-5 y 9-10)
lineas_a_modificar=(3 4 6 7 11 12)

#Abre el archivo y recorre cada linea
for linea_num in "${lineas_a_modificar[@]}"; do
    linea=$(sed -n "${linea_num}p" "$archivo") # Obtener la línea actual

    # Verificar si la línea ya contiene 'non-free contrib'
    if [[ "$linea" != *"non-free contrib"* ]]; then
        sed -i "${linea_num}s/$/ non-free contrib/" "$archivo"
        echo "Línea $linea_num modificada."
    else
        echo "La línea $linea_num ya contiene 'non-free contrib'. No se realizó ningún cambio."
    fi
done

#Actualiza los repositorios
apt-get update && apt-get -y upgrade > /dev/null 2>&1

# -----------------------------------------------------
# 4. Instalar wirewarden
# -----------------------------------------------------
apt-get -y install wireguard wireguard-tools openresolv iptables iptables-persistent
wg genkey | tee privatekey | wg pubkey > publickey

private_key=$(cat /etc/wireguard/privatekey)
public_key=$(cat /etc/wireguard/publickey)

echo $private_key