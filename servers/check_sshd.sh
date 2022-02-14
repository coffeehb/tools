function check_sshd() {
    if [[ ${BAYMAX_INIT_DISABLE_SSHD} != "true" && -f /usr/sbin/sshd ]]; then
        if ! (ps aux |grep sshd |grep -q -v grep); then
            echo "[monitor] sshd exited, restarting"
            /usr/sbin/sshd
        fi
    fi
}

while sleep 15; do
    echo "monitor alive" > /tmp/monitor.log
    check_sshd &> /tmp/check_sshd.log
done
