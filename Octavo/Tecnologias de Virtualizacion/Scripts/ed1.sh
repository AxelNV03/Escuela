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
apt-get update && apt-get -y upgrade

# -----------------------------------------------------
# 4. Crea al usuario Cerimice y su folder en home
# -----------------------------------------------------

user="cerimice" #Nombre del usuario
psswd="qwerty0987654321" #Crea su contrasenia

#Crea el usuario
sudo useradd -m -s /bin/bash $user

#Le agrega la contrasenia
echo "$user:$psswd" | sudo chpasswd

#Lo agrega en el sudoers
echo -e "\n$user\tALL=(ALL:ALL) ALL" >> /etc/sudoers

# -----------------------------------------------------
# 5. Instalar paquetes (Apache, Mariadb, Wget, php)
# -----------------------------------------------------

#Instala todo de golpe
apt-get -y install sudo wget apt-transport-https gpg openssh-server openssh-client mariadb-server mariadb-client apache2 apache2-utils php8.2 php8.2-bcmath php8.2-cgi php8.2-cli php8.2-curl php8.2-enchant php8.2-imagick php8.2-http php8.2-imagick php8.2-intl php8.2-maxminddb php8.2-mbstring php8.2-mcrypt php8.2-mysql php8.2-ps php8.2-pspell php8.2-psr php8.2-readline php8.2-sqlite3 php8.2-xml php8.2-xmlrpc php8.2-xsl php8.2-zip libapache2-mod-php

#Actualiza
apt-get update && apt-get -y upgrade

# -----------------------------------------------------
# 6. instalar java
# -----------------------------------------------------

#Agrega adoptium a los APT
wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor | tee /etc/apt/trusted.gpg.d/adoptium.gpg > /dev/null

#extrae y guarda el repositorio correspondiente a debian
echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list

#Actualiza
apt-get update && apt-get -y upgrade

#Instala java
apt-get -y install temurin-21-jdk

# -----------------------------------------------------
# 7. Configurar mariadb y creacion de Usuario
# -----------------------------------------------------

#Cambia el localhost por 0.0.0.0
sudo sed -i 's/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf

# Crea el usuario
sudo mariadb <<EOF
DROP USER IF EXISTS 'cerimice'@'%';
CREATE USER 'cerimice'@'%' IDENTIFIED BY '1234567890';
GRANT ALL PRIVILEGES ON *.* TO 'cerimice'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

#Restablece el servicio
sudo systemctl restart mariadb

# -----------------------------------------------------
# 9. Configurar y montar sitio 
# -----------------------------------------------------

#Actualiza repos
sudo apt-get update && sudo apt-get -y upgrade

#Crea el php de prueba en la carpeta de sitios
echo "<?php phpinfo(); ?>" | sudo  tee /var/www/html/prueba.php

#Crea el directorio de sitios en htnml
sudo mkdir /var/www/html/sitios

#Usuario actual
user="cerimice" #$(whoami)

#Crea la carpeta sitios en la /home del user actual
mkdir /home/$user/sitios

#Monta el sitio
sudo mount --bind /home/$user/sitios /var/www/html/sitios

#Reinicia apache
sudo systemctl restart apache2