# install arpspoof (dsniff)
apt-get -y install dsniff

# install mitmproxy
apt-get -y install python3-dev python3-pip libffi-dev libssl-dev
pip3 install --user mitmproxy

# install BeautifulSoup
pip3 install beautifulsoup4

#ARP
pip3 install ArpSpoof
#Update
apt update && apt upgrade -y
