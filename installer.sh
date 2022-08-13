sudo apt update
sudo apt-get install libpangocairo-1.0-0 -y
apt install python3-pip -y
pip3 install -r requirements.txt
sudo apt install postgresql postgresql-client -y
sudo -u postgres createdb ptdb
sudo -u postgres psql ptdb < db.sql
cat << EOF > ~/.pgpass
127.0.0.1:5432:ptdb:pt:PTXP@ASS0
EOF
chmod 0600 ~/.pgpass
