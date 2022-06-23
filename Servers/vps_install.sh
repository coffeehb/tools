# 这是一个用于初始化渗透测试人员自用VPS的脚本
# 来自https://github.com/DFC302/Setup/blob/main/install.sh

#!/bin/bash

# Check if user is root, as we need to be able to create user if user does not exist
# we will also need to install necessary depandancies and tools
function checkIfRoot() {

	if [ ${EUID} -ne 0 ] ; then
		echo -e "[ ${RED}FAILED${NC} ]: Please run as root!"
		exit 1
	
	else
		echo -e "[ ${GREEN}OK${NC} ]: Confirmed user is root."

	fi
}

# Check if user exists before trying to install 
function checkIfUserExists() {
	
	if ! id ${username} > /dev/null 2>&1 ; then
		echo -e "[ ${RED}ERROR${NC} ]: User: ${username} not found on system!"

		# If user does not exist, ask user if they wish to create user for them
		while true ; do
			echo ""
			read -p "Do you want me to create the user for you? [y/n]: " choice

			case ${choice} in
				[Yy]* ) adduser ${username} ; echo -e "[ ${YELLOW}INFO${NC} ]: User created!" ; break;;
				[Nn]* ) echo -e "[ ${YELLOW}INFO${NC} ]: User will not be created at this time!" ; exit;;
				* ) echo "Please answer yes or no.";;
			esac
		done

	else

		if [ ${username} == "root" ] ; then
			echo -e "[ ${YELLOW}WARNING${NC} ]: It is advised that if you have no other users than root, that you make a new user."
			# If user does not exist, ask user if they wish to create user for them
			while true ; do
				echo ""
				read -p $"Do you want to continue with installing everything under root? [y/n]: " choice

				case ${choice} in
					[Yy]* ) echo -e "[ ${YELLOW}INFO${NC} ]: User ignored warning. Proceeding with installation." ; break;;
					[Nn]* ) echo -e "[ ${YELLOW}INFO${NC} ]: Installation aborted!" ; exit;;
					* ) echo "Please answer yes or no.";;
				esac
			done

		else
			echo -e "[ ${GREEN}OK${NC} ]: User found! Continuing..."

		fi
	fi
}

function determineOS() {
	OS=$(cat /etc/*-release | head -n 1 | cut -d' ' -f1)
	echo -e "[ ${YELLOW}INFO${NC} ]: Operating system determined: ${GREEN}${OS}${NC}"
}

# update the system -- do not upgrade -- do not want to break anything
function updateSystem() {
	OS=$(cat /etc/*-release | head -n 1 | cut -d' ' -f1)

	if [[ ${OS} =~ "Fedora" ]] ; then

		echo -e "[ ${YELLOW}INFO${NC} ]: System is updating.."
		dnf update -y
		echo -e "[ ${YELLOW}INFO${NC} ]: System updated!"

	elif [[ ${OS} =~ "Ubuntu" ]] || [[ ${OS} =~ "Debian" ]] ; then

		echo -e "[ ${YELLOW}INFO${NC} ]: System is updating.."
		apt update -y 
		echo -e "[ ${YELLOW}INFO${NC} ]: System updated!"
	fi
}

# We need certain dependencies in order to continue with proper installation
function installDependencies() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing dependencies now..."
	OS=$(cat /etc/*-release | head -n 1 | cut -d' ' -f1)

	if [[ ${OS} =~ "Fedora" ]] ; then

		dnf install python3 python3-pip -y

		dnf install jq snapd git bind-utils whois libpcap-devel nodejs vim curl wget tree zip nmap ruby-devel java-latest-openjdk.x86_64 -y
		ln -s /var/lib/snapd/snap /snap
		pip3 install --upgrade pip
		pip3 install requests
		pip3 install pyOpenSSL --upgrade
		

	elif [[ ${OS} =~ "Ubuntu" ]] || [[ ${OS} =~ "Debian" ]] ; then

		apt-get -y install jq snapd git dnsutils whois python3 python3-pip libpcap-dev nodejs vim curl wget tree zip nmap ruby-full default-jdk
		ln -s /var/lib/snapd/snap /snap
		pip3 install --upgrade pip
		pip3 install requests
		pip3 install pyOpenSSL --upgrade
		
	fi
}

# Create tool directory inside usernames home directory
function createToolsDirectory() {

	# if user is not root
	if [ ${username} != "root" ] ; then
		# Create directory to store tools in
		if [ ! -d /home/${username}/tools ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: /home/${username}/tools not found!"
			echo -e "[ ${YELLOW}INFO${NC} ]: Creating /home/${username}/tools now!"
			mkdir /home/${username}/tools
			echo -e "[ ${YELLOW}INFO${NC} ]: /home/${username}/tools created!"

		else
			echo -e "[ ${GREEN}OK${NC} ]: /home/${username}/tools found!"
			echo -e "[ ${YELLOW}INFO${NC} ]: Moving into /home/${username}/tools directory now!"

		fi

	# if user is root
	elif [ ${username} == "root" ] ; then
		# Create directory to store tools in
		if [ ! -d /root/tools ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: tools not found!"
			echo -e "[ ${YELLOW}INFO${NC} ]: Creating tools folder now!"
			mkdir /root/tools
			echo -e "[ ${YELLOW}INFO${NC} ]: tools created!"

		else
			echo -e "[ ${GREEN}OK${NC} ]: tools found!"
			echo -e "[ ${YELLOW}INFO${NC} ]: Moving into tools directory now!"

		fi

	fi
}

function installGo() {
	# This function will call a certain function to install Golang based on user's shell

	echo -e "[ ${YELLOW}INFO${NC} ]: Attempting to install golang."

	curl -sLO https://get.golang.org/$(uname)/go_installer && chmod +x go_installer && ./go_installer && rm go_installer

	# if user is not root
	if [[ ${username} != "root" ]] ; then
		if [ ! -d /home/${username}/go ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: No go home directory found! Creating one now."
			mkdir /home/${username}/go

		fi

		if [ -n "$ZSH_VERSION" ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: User appears to be using zsh."

			if ! grep -qx "export GOROOT=/usr/local/go" /home/${username}/.zshrc  ; then

				echo -e "\nexport GOROOT=/usr/local/go" >> /home/${username}/.zshrc
				echo "export GOPATH=/home/${username}/go" >> /home/${username}/.zshrc
				echo "export PATH=\$PATH:snap/bin:\${GOPATH}/bin:\${GOROOT}/bin" >> /home/${username}/.zshrc

			fi

			source /home/${username}/.zshrc

			checkGoLang

		elif [ -n "$BASH_VERSION" ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: User appears to be using bash."

			if ! grep -qx "export GOROOT=/usr/local/go" /home/${username}/.bashrc ; then
				echo -e "\nexport GOROOT=/usr/local/go" >> /home/${username}/.bashrc
				echo "export GOPATH=/home/${username}/go" >> /home/${username}/.bashrc
				echo "export PATH=\$PATH:snap/bin:\${GOPATH}/bin:\${GOROOT}/bin" >> /home/${username}/.bashrc
			fi

			source /home/${username}/.bashrc

			checkGoLang

		else
			echo -e "[ ${YELLOW}INFO${NC} ]: Could not determine shell. Assuming bash..."

			if ! grep -qx "export GOROOT=/usr/local/go" /home/${username}/.zshrc ; then
				echo -e "\nexport GOROOT=/usr/local/go" >> /home/${username}/.bashrc
				echo "export GOPATH=/home/${username}/go" >> /home/${username}/.bashrc
				echo "export PATH=\$PATH:snap/bin:\${GOPATH}/bin:\${GOROOT}/bin" >> /home/${username}/.bashrc
			fi

			source /home/${username}/.bashrc

			checkGoLang

		fi

	elif [[ ${username} == "root" ]] ; then
		# if [ ! -d /root/go ] ; then
		# 	echo -e "[ ${YELLOW}INFO${NC} ]: No go home directory found! Creating one now."
		# 	mkdir /root/go

		# fi

		if [ -n "$ZSH_VERSION" ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: User appears to be using zsh."

			if ! grep -qx "export GOROOT=/usr/local/go" /root/.zshrc ; then
				echo -e "\nexport GOROOT=/usr/local/go" >> /root/.zshrc
				echo "export GOPATH=/root/go" >> /root/.zshrc
				echo "export PATH=\$PATH:snap/bin:\${GOPATH}/bin:\${GOROOT}/bin" >> /root/.zshrc
			fi

			source .zshrc

			checkGoLang

		elif [ -n "$BASH_VERSION" ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: User appears to be using bash."

			if ! grep -qx "export GOROOT=/usr/local/go" /root/.bashrc ; then
				echo -e "\nexport GOROOT=/usr/local/go" >> /root/.bashrc
				echo "export GOPATH=/root/go" >> /root/.bashrc
				echo "export PATH=\$PATH:snap/bin:\${GOPATH}/bin:\${GOROOT}/bin" >> /root/.bashrc
			fi

			source .bashrc

			checkGoLang

		else
			echo -e "[ ${YELLOW}INFO${NC} ]: Could not determine shell. Assuming bash..."

			if ! grep -qx "export GOROOT=/usr/local/go" /root/.bashrc ; then
				echo -e "\nexport GOROOT=/usr/local/go" >> /root/.bashrc
				echo "export GOPATH=/root/go" >> /root/.bashrc
				echo "export PATH=\$PATH:snap/bin:\${GOPATH}/bin:\${GOROOT}/bin" >> /root/.bashrc
			fi

			source .bashrc

			checkGoLang

		fi

	fi
}

function checkGoLang() {
	if ! $(command -v /root/.go/bin/go version &> /dev/null) ; then
		echo -e "[ ${RED}ERROR${NC} ]: Golang version not detected. May need manual installation."

	elif $(command -v /root/.go/bin/go version &> /dev/null) ; then
		echo -e "[ ${GREEN}PASSED${NC} ]: $(/root/.go/bin/go version) detected!"

	fi
}

function installAmass() {

	if ! $(command -v amass -h &> /dev/null) ; then
		echo -e "[ ${YELLOW}INFO${NC} ]: Installing amass."
		snap install amass

	else
		echo -e "[ ${YELLOW}INFO${NC} ]: Amass found!"
	fi
}

function installAssetfinder() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing assetfinder."
	/root/.go/bin/go install github.com/tomnomnom/assetfinder@latest
}

function installSubfinder() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing subfinder."
	/root/.go/bin/go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
}

function installHttprobe() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing httprobe."
	/root/.go/bin/go install github.com/tomnomnom/httprobe@latest
}

function installAquatone() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing aquatone."
	latestVersion=$(curl -s https://api.github.com/repos/michenriksen/aquatone/releases/latest | jq ."assets"[]."browser_download_url" | head -n 1 | sed 's/"//g')
	wget ${latestVersion}
	unzip -u aquatone_linux_amd64_*
	mv aquatone /root/go/bin
	rm LICENSE* README* aquatone_linux_amd64_1.7.0.zip*
}

function installFFUF() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing FFUF."
	/root/.go/bin/go install github.com/ffuf/ffuf@latest
}

function installGAU() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing gau."
	/root/.go/bin/go install github.com/lc/gau/v2/cmd/gau@latest
}

function installWaybackurls() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing waybackurls."
	/root/.go/bin/go install github.com/tomnomnom/waybackurls@latest
}

function installHTTPX() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing HTTPX."
	/root/.go/bin/go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
}

function installSubjack() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing subjack."
	/root/.go/bin/go install github.com/haccer/subjack@latest

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/subjack ] ; then
			git clone https://github.com/haccer/subjack.git /home/${username}/tools/subjack
		fi

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/tools/subjack ] ; then
			git clone https://github.com/haccer/subjack.git /root/tools/subjack
		fi

	fi

}

function installNaabu() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing naabu."
	/root/.go/bin/go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
}

function installSublister() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing sublist3r."

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/Sublist3r ] ; then
			git clone https://github.com/aboul3la/Sublist3r.git /home/${username}/tools/Sublist3r
			cd /home/${username}/tools/Sublist3r/ && pip3 install -r requirements.txt

			cd /home/${username}/
		fi

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/tools/Sublist3r ] ; then
			git clone https://github.com/aboul3la/Sublist3r.git /root/tools/Sublist3r
			cd /root/tools/Sublist3r/ && pip3 install -r requirements.txt

			cd /root
		fi

	fi

}

function installDnsgen() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing dnsgen."

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/dnsgen ] ; then
			git clone https://github.com/ProjectAnte/dnsgen /home/${username}/tools/dnsgen
			rm /home/${username}/tools/dnsgen/dnsgen/words.txt && cp footprint/wordlist/custom_alterations.txt /home/${username}/tools/dnsgen/dnsgen/words.txt
			cd /home/${username}/tools/dnsgen && pip3 install -r requirements.txt
			python3 setup.py install

			cd /home/${username}/

		fi

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/tools/dnsgen ] ; then
			git clone https://github.com/ProjectAnte/dnsgen /root/tools/dnsgen
			rm /root/tools/dnsgen/dnsgen/words.txt && cp /root/footprint/wordlist/custom_alterations.txt /root/tools/dnsgen/dnsgen/words.txt
			cd /root/tools/dnsgen && pip3 install -r requirements.txt
			python3 setup.py install

			cd /root

		fi

	fi

}

function installLinkFinder() {

		echo -e "[ ${YELLOW}INFO${NC} ]: Installing LinkFinder."

        if [ ${username} != "root" ] ; then

        if [ ! -d /home/${username}/tools/LinkFinder ] ; then
                    git clone https://github.com/GerbenJavado/LinkFinder.git /home/${username}/tools/LinkFinder

        fi

        cd /home/${username}/tools/LinkFinder && pip3 install -r requirements.txt && python3 setup.py install && cd /home/${username}/


        elif [ ${username} == "root" ] ; then

        if [ ! -d /root/tools/LinkFinder ] ; then
            git clone https://github.com/GerbenJavado/LinkFinder.git /root/tools/LinkFinder

        fi

        cd /root/tools/LinkFinder && pip3 install -r requirements.txt && python3 setup.py install && cd /root/

        fi

}

function installDNSScan() {

		echo -e "[ ${YELLOW}INFO${NC} ]: Installing DNSscan."

        if [ ${username} != "root" ] ; then

        if [ ! -d /home/${username}/tools/dnscan ] ; then
            git clone https://github.com/rbsec/dnscan.git /home/${username}/tools/dnscan

        fi

        cd /home/${username}/tools/dnscan && pip3 install -r requirements.txt && pip3 install packaging &&  cd /home/${username}/

        elif [ ${username} == "root" ] ; then

        if [ ! -d /root/tools/dnscan ] ; then
                    git clone https://github.com/rbsec/dnscan.git /root/tools/dnscan

        fi

        cd /root/tools/dnscan && pip3 install -r requirements.txt && pip3 install packaging && cd /root/
        fi

}

installASN() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing ASN script."

	OS=$(cat /etc/*-release | head -n 1 | cut -d' ' -f1)

	if [[ ${OS} =~ "Fedora" ]] ; then
		dnf install curl whois bind bind-utils ipcalc grepcidr nc aha -y

	elif [[ ${OS} =~ "Ubuntu" ]] || [[ ${OS} =~ "Debian" ]] ; then
		# install prerequisites
		apt -y install bind9-host mtr-tiny ipcalc grepcidr ncat aha

	fi

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/asn ] ; then
			git clone https://github.com/nitefood/asn.git /home/${username}/tools/asn
        fi

        cd /home/${username}/tools/asn && cp /home/${username}/tools/asn/asn /usr/bin/asn && chmod 0755 /usr/bin/asn

    elif [ ${username} == "root" ] ; then

    	if [ ! -d /root/tools/asn ] ; then
			git clone https://github.com/nitefood/asn.git /root/tools/asn
        fi

        cd /root/tools/asn && cp /root/tools/asn/asn /usr/bin/asn && chmod 0755 /usr/bin/asn

    fi

}

installDNSRecon() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing DNSRecon."

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/dnsrecon ] ; then
			git clone https://github.com/darkoperator/dnsrecon.git /home/${username}/tools/dnsrecon
        fi

        cd /home/${username}/tools/dnsrecon && pip3 install -r requirements.txt

    elif [ ${username} == "root" ] ; then

    	if [ ! -d /root/tools/dnsrecon ] ; then
			git clone https://github.com/darkoperator/dnsrecon.git /root/tools/dnsrecon
        fi

        cd /root/tools/dnsrecon && pip3 install -r requirements.txt

    fi

}

install403Bypasser() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing 403Bypasser."

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/403bypasser ] ; then
			git clone https://github.com/yunemse48/403bypasser.git /home/${username}/tools/403bypasser
        fi

        cd /home/${username}/tools/403bypasser && pip3 install -r requirements.txt

    elif [ ${username} == "root" ] ; then

    	if [ ! -d /root/tools/403bypasser ] ; then
			git clone https://github.com/yunemse48/403bypasser.git /root/tools/403bypasser
        fi

        cd /root/tools/403bypasser && pip3 install -r requirements.txt

    fi
}

function installGF() {
	# Guides
	# https://medium.com/@dhaliwalsargam/gf-tool-installation-8fcd285a4be2
	# https://github.com/tomnomnom/gf
	
	# install gf, clone patterns from repos
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing gf."

	go get github.com/tomnomnom/gf@latest

	echo -e "[ ${YELLOW}INFO${NC} ]: Fetching patterns from repos."

	# if user is not root
	if [[ ${username} != "root" ]] ; then

		if [ ! -d /home/${username}/tools/gf ] ; then
			git clone https://github.com/tomnomnom/gf /home/${username}/tools/gf
		
		elif [ -d /home/${username}/tools/gf ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: gf repo already exists! Skipping."

		fi

		if [ ! -d /home/${username}/tools/Gf-Patterns ] ; then
			git clone https://github.com/1ndianl33t/Gf-Patterns /home/${username}/tools/Gf-Patterns

		elif [ -d /home/${username}/tools/Gf-Patterns ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: Gf-Patterns repo already exists! Skipping."
		fi

		# make private directory to hold gf patterns
		if [ ! -d /home/${username}/.gf ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: No .gf directory. Creating one now."
			mkdir /home/${username}/.gf

		elif [ -d /home/${username}/.gf ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: .gf directory already exists! Skipping."

		fi

		# copy patterns from cloned repos into private gf folder in user's home directory
		echo -e "[ ${YELLOW}INFO${NC} ]: Copying gf patterns to .gf directory".
		cp /home/${username}/tools/gf/examples/*.json /home/${username}/.gf/
		cp /home/${username}/tools/Gf-Patterns/*.json /home/${username}/.gf

		if [ -n "$ZSH_VERSION" ] ; then

			if ! grep -qx "source /home/${username}/tools/gf/gf-completion.zsh" /home/${username}/.zshrc ; then
				echo "source /home/${username}/tools/gf/gf-completion.zsh" >> /home/${username}/.zshrc 

			fi

		elif [ -n "$BASH_VERSION" ] ; then

			if ! grep -qx "source /home/${username}/tools/gf/gf-completion.bash" /home/${username}/.bashrc ; then
				echo "source /home/${username}/tools/gf/gf-completion.bash" >> /home/${username}/.bashrc 
			fi

		else
			# assume bash
			if ! grep -qx "source /home/${username}/tools/gf/gf-completion.bash" /home/${username}/.bashrc ; then
				echo "source /home/${username}/tools/gf/gf-completion.bash" >> /home/${username}/.bashrc
			fi

		fi

	elif [[ ${username} == "root" ]] ; then

		if [ ! -d /root/tools/gf ] ; then
			git clone https://github.com/tomnomnom/gf /root/tools/gf
		
		elif [ -d /root/tools/gf ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: gf repo already exists! Skipping."

		fi

		if [ ! -d /root/tools/Gf-Patterns ] ; then
			git clone https://github.com/1ndianl33t/Gf-Patterns /root/tools/Gf-Patterns

		elif [ -d /root/tools/GF-Patterns ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: Gf-Patterns repo already exists! Skipping."
		fi

		# make private directory to hold gf patterns
		if [ ! -d /root/.gf ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: No .gf directory. Creating one now."
			mkdir .gf
		elif [ -d /root/.gf ] ; then
			echo -e "[ ${YELLOW}INFO${NC} ]: .gf directory already exists! Skipping."

		fi

		# copy patterns from cloned repos into private gf folder in user's home directory
		echo -e "[ ${YELLOW}INFO${NC} ]: Copying gf patterns to .gf directory".
		cp /root/tools/gf/examples/*.json /root/.gf/
		cp /root/tools/Gf-Patterns/*.json /root/.gf

		if [ -n "$ZSH_VERSION" ] ; then

			if ! grep -qx "source /root/tools/gf/gf-completion.zsh" /root/.zshrc ; then
				echo "source /root/tools/gf/gf-completion.zsh" >> /root/.zshrc
			fi 

		elif [ -n "$BASH_VERSION" ] ; then

			if ! grep -qx "source /root/tools/gf/gf-completion.bash" /root/.bashrc ; then
				echo "source /root/tools/gf/gf-completion.bash" >> /root/.bashrc
			fi 

		else
			# assume bash
			if ! grep -qx "source /root/tools/gf/gf-completion.bash" /root/.bashrc ; then
				echo "source /root/tools/gf/gf-completion.bash" >> /root/.bashrc
			fi

		fi
	fi
}

function installSecLists() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Grabbing SecLists wordlists."
	
	if [ ${username} != "root" ] ; then
		
		if [ ! -d /home/${username}/wordlists ] ; then
		    mkdir /home/${username}/wordlists
		fi
		
		if [ ! -d /home/${username}/wordlists/SecLists ] ; then
			git clone https://github.com/danielmiessler/SecLists.git /home/${username}/wordlists/SecLists	
		fi
	
	elif [ ${username} == "root" ] ; then
		
		if [ ! -d /root/wordlists ] ; then
		    mkdir /root/wordlists
		fi
		
		if [ ! -d /root/wordlists/SecLists ] ; then
			git clone https://github.com/danielmiessler/SecLists.git /root/wordlists/SecLists
		fi
		
	fi
}

function installCloudFlair() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing CloudFlair."

	if [ ${username}  != "root" ] ; then
		
		if [ ! -d /home/${username}/tools/cloudflair/ ] ; then
			git clone https://github.com/christophetd/cloudflair.git /home/${username}/tools/cloudflair
			cd /home/${username}/tools/cloudflair && pip3 install -r  requirements.txt

		fi
		

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/tools/cloudflair/ ] ; then
			git clone https://github.com/christophetd/cloudflair.git /home/${username}/tools/cloudflair
			cd /root/tools/cloudflair && pip3 install -r  requirements.txt

		fi
		

	fi
}

# Install Mobile Tools

function makeMobileDir() {

	if [ ${username}  != "root" ] ; then
		
		if [ ! -d /home/${username}/mobile/ ] ; then
			mkdir /home/${username}/mobile

		fi

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/mobile/ ] ; then
			mkdir /root/mobile/

		fi

	fi
}

function installAPKTools() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing APKTools."

	# https://ibotpeaches.github.io/Apktool/install/

    # Download Linux wrapper script (Right click, Save Link As apktool)
    # Download apktool-2 (find newest here)
    # Rename downloaded jar to apktool.jar
    # Move both files (apktool.jar & apktool) to /usr/local/bin (root needed)
    # Make sure both files are executable (chmod +x)
    # Try running apktool via cli

	# get latest version like 2.16.1
	latestVersion=$(curl -s https://api.github.com/repos/iBotPeaches/Apktool/releases | jq .[]."name" | cut -d' ' -f2 | sed 's/"//g' | head -n 1 | sed 's/^[v]//g')

	# get apktool script, latest version, and move to /usr/local/bin with correct permissions
	wget "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool" && wget "https://github.com/iBotPeaches/Apktool/releases/download/v${latestVersion}/apktool_${latestVersion}.jar"
	mv "apktool_${latestVersion}.jar" apktool.jar
	chmod +x apktool*
	mv apktool* /usr/local/bin/ && chmod +x /usr/local/bin/apktool*
}

function installAPKLeaks() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing APKLeaks."

	if [ ${username}  != "root" ] ; then
		
		if [ ! -d /home/${username}/tools/apkleaks/ ] ; then
			git clone https://github.com/dwisiswant0/apkleaks.git /home/${username}/tools/apkleaks

		fi

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/tools/apkleaks/ ] ; then
			git clone https://github.com/dwisiswant0/apkleaks.git /root/tools/apkleaks

		fi

	fi
	
}

function installGMapsAPIScanner() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing gmapsapiscanner."

	if [ ${username}  != "root" ] ; then
		
		if [ ! -d /home/${username}/tools/gmapsapiscanner/ ] ; then
			git clone https://github.com/ozguralp/gmapsapiscanner.git /home/${username}/tools/gmapsapiscanner

		fi

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/tools/gmapsapiscanner/ ] ; then
			git clone https://github.com/ozguralp/gmapsapiscanner.git /root/tools/gmapsapiscanner

		fi

	fi
	
}

function getFridaScript() {
	
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing frida SSL bypass script."

	if [ ${username}  != "root" ] ; then
		
		if [ ! -d /home/${username}/tools/frida-android-unpinning/ ] ; then
			git clone https://github.com/httptoolkit/frida-android-unpinning.git /home/${username}/tools/frida-android-unpinning

		fi

	elif [ ${username} == "root" ] ; then

		if [ ! -d /root/tools/gmapsapiscanner/ ] ; then
			git clone https://github.com/httptoolkit/frida-android-unpinning.git /root/tools/frida-android-unpinning

		fi

	fi

}

function installOWASPZap() {

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing OWASPZap."

	snap install zaproxy --classic

}

function checkRuby() {
	
	if ! $(command -v ruby --version &> /dev/null) ; then
		echo -e "[ ${RED}ERROR${NC} ]: Ruby version not detected. May need manual installation."

	elif $(command -v ruby --version &> /dev/null) ; then
		echo -e "[ ${GREEN}PASSED${NC} ]: $(ruby --version | awk '{print $1 $2}') detected!"

	fi
}

function installLazys3() {
	checkRuby

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing lazys3."

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/lazys3 ] ; then
			git clone https://github.com/nahamsec/lazys3.git /home/${username}/tools/lazys3
        fi

    elif [ ${username} == "root" ] ; then

    	if [ ! -d /root/tools/lazys3 ] ; then
			git clone https://github.com/nahamsec/lazys3.git /root/tools/lazys3
        fi

    fi
}

function checkJava() {

	if ! $(command -v java --version &> /dev/null) ; then
		echo -e "[ ${RED}ERROR${NC} ]: Java version not detected. May need manual installation."

	elif $(command -v java --version &> /dev/null) ; then
		echo -e "[ ${GREEN}PASSED${NC} ]: $(Java --version | awk '{print $1 $2}') detected!"

	fi
}

function installIISShortNameScanner() {
	checkJava

	echo -e "[ ${YELLOW}INFO${NC} ]: Installing IIS ShortName Scanner."

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/IIS-ShortName-Scanner ] ; then
			git clone https://github.com/irsdl/IIS-ShortName-Scanner.git /home/${username}/tools/IIS-ShortName-Scanner
        fi

    elif [ ${username} == "root" ] ; then

    	if [ ! -d /root/tools/IIS-ShortName-Scanner ] ; then
			git clone https://github.com/irsdl/IIS-ShortName-Scanner.git /root/tools/IIS-ShortName-Scanner
        fi

    fi
}

function installXNLinkfinder() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing xnlinkfinder."

	if [ ${username} != "root" ] ; then

		if [ ! -d /home/${username}/tools/xnlinkfinder ] ; then
			git clone https://github.com/xnl-h4ck3r/xnLinkFinder.git /home/${username}/tools/xnlinkfinder
        fi

        cd /home/${username}/tools/xnlinkfinder && python3 setup.py install

    elif [ ${username} == "root" ] ; then

    	if [ ! -d /root/tools/xnlinkfinder ] ; then
			git clone https://github.com/xnl-h4ck3r/xnLinkFinder.git /root/tools/xnlinkfinder
        fi

        cd /root/tools/xnlinkfinder/xnlinkfinder && python3 setup.py install

    fi
}

function installWebAnalyze() {
	echo -e "[ ${YELLOW}INFO${NC} ]: Installing webanalyze."
	/root/.go/bin/go get -v -u github.com/rverton/webanalyze/cmd/webanalyz && webanalyze -update
}

function main() {

	DATE=$(date)

	RED='\033[0;31m'
	GREEN='\033[0;32m'
	YELLOW='\033[0;33m'
	NC='\033[0m'
	

	# Check if user is root and if user's supplied username exists -- get OS
	checkIfRoot
	checkIfUserExists
	determineOS

	# Update system before we begin.
	updateSystem

	# Download needed dependencies
	installDependencies

	# Create tool directory
	createToolsDirectory

	# install golang
	installGo
	
	cp -r /root/.go /usr/local/go # removed from go function

	# install tools
	installAmass
	installAssetfinder
	installSubfinder
	installHttprobe
	installAquatone
	installGAU
	installFFUF
	installWaybackurls
	installSubjack
	installNaabu
	installSublister
	installDnsgen
	installHTTPX
	installGF
	installLinkFinder
	installDNSScan
	installASN
	installDNSRecon
	install403Bypasser
	installSecLists
	installCloudFlair
	installLazys3
	installIISShortNameScanner
	installXNLinkfinder
	installWebAnalyze

	# mobile
	makeMobileDir
	installAPKTools
	installAPKLeaks
	installGMapsAPIScanner
	getFridaScript

	# DAST
	installOWASPZap

	if [ ${username} != "root" ] ; then
	    cp -r /root/go/ /home/${username}/
	fi

	echo -e "[ ${YELLOW}INFO${NC} ]: Installation complete."
	echo -e "[ ${YELLOW}INFO${NC} ]: Installed tools are located in ~/tools directory."
	echo ""
	echo -e "[ ${YELLOW}INFO${NC} ]: You may need to restart the terminal for everything to take effect"
	echo -e "[ ${YELLOW}INFO${NC} ]: Don't forget to source your .bashrc/.zshrc file."
	echo -e "[ ${YELLOW}INFO${NC} ]: [ How-To? ]: source ~/.bashrc or source ~/.zshrc"
	echo -e "[ ${YELLOW}INFO${NC} ]: The correct frida server will also still need to be downloaded for your device."

	exit
}

if [ -z $1 ] ; then
	echo -e "[ ${YELLOW}USAGE${NC} ]: bash install.sh username"
	exit 1

else
	username=$1
	main
fi
