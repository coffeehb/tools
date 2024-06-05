echo "安装基础软件"
apt-get install -y sshpass jq rsync iputils-ping bsdmainutils translate-shell netcat

echo "CPU核心数:"
lscpu|grep 'CPU(s)'|sed -n 1p| awk '{print $2}'
echo "内存:"
free -h|sed -n 2p|awk '{print $2}'|sed 's/[^0-9][^0-9]//'
echo "硬盘:"
df -h|grep -w /|awk '{print $4}'|sed 's/[^0-9]//'
