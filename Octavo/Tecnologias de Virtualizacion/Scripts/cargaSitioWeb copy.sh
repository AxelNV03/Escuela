#!/bin/bash

verde="\033[1;32m"
amarillo="\033[0;33m"
reset="\033[0m"
# ----------------------------------------------------------
# 1. Crea el directorio y lo monta 
# ----------------------------------------------------------

#Pregunta el nombre del directorio
echo -en "${amarillo}\nIngresa el nombre y dominio del sitio a crear (ejemplo: hola.gob.mx).\n> ${reset}"
read site_name

#User actual
user=$(whoami) #"cerimice"
origin="/home/$user/sitios/$site_name"
destino="/var/www/$site_name"


#Crea el directorio en la carpeta del user actual
sudo mkdir -p $origin

#crea el directorio en la carpeta de sitios de /var
sudo mkdir -p $destino

#Monta el sitio con bind
sudo mount --bind $origin $destino

# ----------------------------------------------------------
# 2. Crea el archivo de configuracion del sitio y lo activa
# ----------------------------------------------------------

#Crea el archivo de configuracion
sudo touch /etc/apache2/sites-available/$site_name.conf

#Agrega el contenido al archivo
echo "<VirtualHost *:80>
    ServerAdmin webmaster@$site_name
    DocumentRoot $destino
    ServerName $site_name

    <Directory $destino>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Order allow,deny
        allow from all
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>" | sudo tee /etc/apache2/sites-available/$site_name.conf > /dev/null

#Activa el sitio
sudo a2ensite $site_name.conf

#Lo carga al fstab para no hacer el bind cada vez que se reinicie
#echo "$origin /var/www/html/sitios/$site_name none nodev,nosuid,noexec,noatime,bind 0 0" >> /etc/fstab
echo "$origin $destino none nodev,nosuid,noexec,noatime,bind 0 0" | sudo tee -a /etc/fstab > /dev/null

#Reinicia apache
sudo systemctl restart apache2

# ----------------------------------------------------------
# 3. Solicita al usuario el codigo del sitio
# ----------------------------------------------------------

#Crea el archivo index.html
echo "Borra esto y pega el codigo html del index de tu pagina" | sudo tee -a $origin/index.html >/dev/null

#Abre el archivo para editar
sudo nano $origin/index.html

#Reinicia apache
sudo systemctl restart apache2

#Meustra msj de fionalizacion
echo -e "\n${verde}Sitio Activado correctamente!.\n${reset}"
# ----------------------------------------------------------