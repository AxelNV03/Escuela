Negro="\033[0;30m"
Rojo="\033[0;31m"
Verde="\033[0;32m"
Amarillo="\033[0;33m"
Azul="\033[0;34m"
Purpura="\033[0;35m"
Cian="\033[0;36m"
Blanco="\033[0;37m"
reset="\033[0m"


export TERM=xterm-256color
PS1='\[\033[01;32m\]\u@\h:\w\$ \[\033[00m\]'


342
mysql-bin.000011

CREATE USER 'word'@'192.168.0.195' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON wordpress.* TO 'word'@'192.168.0.195';
FLUSH PRIVILEGES;

DROP USER 'server'@'172.23.50.139';
DROP USER 'word'@'172.23.50.139';
