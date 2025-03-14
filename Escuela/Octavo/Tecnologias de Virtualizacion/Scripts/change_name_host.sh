#!/bin/bash

# -----------------------------------------------------
# 1. Cambiar nombre del host 
# -------------------------------------------------
verde="\033[1;32m"
reset="\033[0m"

echo -en "${verde}\n\tIngresa el nombre del nuevo host: ${reset}"
read new_host

#Cambia el nombre del host
echo $new_host | sudo tee /etc/hostname > /dev/null

#Cambia el nombre del host en el archivo hosts
sudo sed -i "s/^127.0.1.1[[:space:]]\+[[:alnum:]-]\+$/127.0.1.1\t$new_host/" /etc/hosts

#Reinicia el servicio
echo -e "\n${verde}Finalizado. Reiniciando Maquina ${reset}"
sleep 3
sudo reboot


