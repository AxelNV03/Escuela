#----------------------------------------------------
#Maestro
#----------------------------------------------------
echo "maestro8A" > /etc/hostname

/etc/hosts --> maestro o esclavo en la segunda linea

sudo nano /etc/mysql//mariadb.conf.d/50-server.cnf  #Bind addres comentado

#En lggong and replication abajo del chown 
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log

#Guardas y sale y creas
sudo mkdir -m 2750 /var/log/mysql
sudo chown mysql /var/log/mysql

#Reinicias
sudo service mariadb restart

#Entras al mariadb
CREATE USER 'replica'@'%' IDENTIFIED BY 'replica';
GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';
FLUSH PRIVILEGES;

#Para mostrar
show master status \g;

#DEbe salir algo como 
MariaDB [(none)]> show master status \g;
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000001 |      771 |              |                  |
+------------------+----------+--------------+------------------+
1 row in set (0.001 sec)

ERROR: No query specified

#----------------------------------------------------
# Esclavo
#----------------------------------------------------

#Creas dirs
sudo mkdir -m 2750 /var/log/mysql
sudo chown mysql /var/log/mysql

#Archivo de conf. Igual abajo de chown
sudo nano /etc/mysql//mariadb.conf.d/50-server.cnf  #Bind addres comentado

#Ahora pones 2
server-id = 2
log_bin = /var/log/mysql/mysql-bin.log


#Entrar a mariadb
#Detener los hilos esclavos:
STOP SLAVE;

#Colocamos el server maestro
#Usa la ip de tu esclavo
CHANGE MASTER TO  MASTER_HOST='192.168.56.101',
MASTER_USER='replica',
MASTER_PASSWORD='replica',
MASTER_LOG_FILE='mysql-bin.000011',
MASTER_LOG_POS=717; #Posicion del master status;

#show slave status. Deben salir lineas raras
show slave status \g;

#Muestra las bases de datos


#Pasate a mestro. crea una base y se debe reflejar en el esclavo aa
