#!/bin/bash

# This file is accessible as https://multi.netlify.app/go.sh

# If not specify, default meaning of return value:
# 0: Success
# 1: System error
# 2: Application error
# 3: Network error

# CLI arguments
proxy=''
help=''
force=''
check=''
remove=''
version=''
vsrc_root='/tmp/v2ray'
extract_only=''
local=''
local_install=''
error_if_uptodate=''

cur_ver=""
new_ver=""
zipfile="/tmp/v2ray/v2ray.zip"
v2ray_running=0

cmd_install=""
cmd_update=""
software_updated=0
key="V2Ray"
key_lower="v2ray"
repos="v2fly/v2ray-core"

systemctl_cmd=$(command -v systemctl 2>/dev/null)

#######color code########
red="31m"      # Error message
green="32m"    # Success message
yellow="33m"   # Warning message
blue="36m"     # Info message

xray_set(){
    key="Xray"
    key_lower="xray"
    repos="XTLS/Xray-core"
    vsrc_root='/tmp/xray'
    zipfile="/tmp/xray/xray.zip"
}

#########################
while [[ $# > 0 ]]; do
    case "$1" in
        -p|--proxy)
        proxy="-x ${2}"
        shift # past argument
        ;;
        -h|--help)
        help="1"
        ;;
        -f|--force)
        force="1"
        ;;
        -c|--check)
        check="1"
        ;;
        -x|--xray)
        xray_set
        ;;
        --remove)
        remove="1"
        ;;
        --version)
        version="$2"
        shift
        ;;
        --extract)
        vsrc_root="$2"
        shift
        ;;
        --extractonly)
        extract_only="1"
        ;;
        -l|--local)
        local="$2"
        local_install="1"
        shift
        ;;
        --errifuptodate)
        error_if_uptodate="1"
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done

###############################
colorEcho(){
    echo -e "\033[${1}${@:2}\033[0m" 1>& 2
}

archAffix(){
    case "$(uname -m)" in
      'i386' | 'i686')
        machine='32'
        ;;
      'amd64' | 'x86_64')
        machine='64'
        ;;
      'armv5tel')
        machine='arm32-v5'
        ;;
      'armv6l')
        machine='arm32-v6'
        grep Features /proc/cpuinfo | grep -qw 'vfp' || machine='arm32-v5'
        ;;
      'armv7' | 'armv7l')
        machine='arm32-v7a'
        grep Features /proc/cpuinfo | grep -qw 'vfp' || machine='arm32-v5'
        ;;
      'armv8' | 'aarch64')
        machine='arm64-v8a'
        ;;
      'mips')
        machine='mips32'
        ;;
      'mipsle')
        machine='mips32le'
        ;;
      'mips64')
        machine='mips64'
        ;;
      'mips64le')
        machine='mips64le'
        ;;
      'ppc64')
        machine='ppc64'
        ;;
      'ppc64le')
        machine='ppc64le'
        ;;
      'riscv64')
        machine='riscv64'
        ;;
      's390x')
        machine='s390x'
        ;;
        *)
        echo "error: The architecture is not supported."
        exit 1
        ;;
    esac

	return 0
}

zipRoot() {
    unzip -lqq "$1" | awk -e '
        NR == 1 {
            prefix = $4;
        }
        NR != 1 {
            prefix_len = length(prefix);
            cur_len = length($4);

            for (len = prefix_len < cur_len ? prefix_len : cur_len; len >= 1; len -= 1) {
                sub_prefix = substr(prefix, 1, len);
                sub_cur = substr($4, 1, len);

                if (sub_prefix == sub_cur) {
                    prefix = sub_prefix;
                    break;
                }
            }

            if (len == 0) {
                prefix = "";
                nextfile;
            }
        }
        END {
            print prefix;
        }
    '
}

downloadV2Ray(){
    rm -rf /tmp/$key_lower
    mkdir -p /tmp/$key_lower
    local pack_name=$key_lower
    [[ $key == "Xray" ]] && pack_name=$key
    download_link="https://github.com/$repos/releases/download/${new_ver}/${pack_name}-linux-${machine}.zip"
    colorEcho ${blue} "Downloading $key: ${download_link}"
    curl ${proxy} -L -H "Cache-Control: no-cache" -o ${zipfile} ${download_link}
    if [ $? != 0 ];then
        colorEcho ${red} "Failed to download! Please check your network or try again."
        return 3
    fi
    return 0
}

installSoftware(){
    component=$1
    if [[ -n `command -v $component` ]]; then
        return 0
    fi

    getPMT
    if [[ $? -eq 1 ]]; then
        colorEcho ${red} "The system package manager tool isn't APT or YUM, please install ${component} manually."
        return 1
    fi
    if [[ $software_updated -eq 0 ]]; then
        colorEcho ${blue} "Updating software repo"
        $cmd_update
        software_updated=1
    fi

    colorEcho ${blue} "Installing ${component}"
    $cmd_install $component
    if [[ $? -ne 0 ]]; then
        colorEcho ${red} "Failed to install ${component}. Please install it manually."
        return 1
    fi
    return 0
}

# return 1: not apt, yum, or zypper
getPMT(){
    if [[ -n `command -v apt-get` ]];then
        cmd_install="apt-get -y -qq install"
        cmd_update="apt-get -qq update"
    elif [[ -n `command -v yum` ]]; then
        cmd_install="yum -y -q install"
        cmd_update="yum -q makecache"
    elif [[ -n `command -v zypper` ]]; then
        cmd_install="zypper -y install"
        cmd_update="zypper ref"
    else
        return 1
    fi
    return 0
}

normalizeVersion() {
    if [ -n "$1" ]; then
        case "$1" in
            v*)
                echo "$1"
            ;;
            *)
                echo "v$1"
            ;;
        esac
    else
        echo ""
    fi
}

# 1: new V2Ray. 0: no. 2: not installed. 3: check failed. 4: don't check.
getVersion(){
    if [[ -n "$version" ]]; then
        new_ver="$(normalizeVersion "$version")"
        return 4
    else
        ver="$(/usr/bin/$key_lower/$key_lower -version 2>/dev/null)"
        [[ -z $ver ]] && ver="$(/usr/bin/$key_lower/$key_lower version 2>/dev/null)"
        retval=$?
        cur_ver="$(normalizeVersion "$(echo "$ver" | head -n 1 | cut -d " " -f2)")"
        tag_url="https://api.github.com/repos/$repos/releases/latest"
        new_ver="$(normalizeVersion "$(curl ${proxy} -H "Accept: application/json" -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0" -s "${tag_url}" --connect-timeout 10| grep 'tag_name' | cut -d\" -f4)")"

        if [[ $? -ne 0 ]] || [[ $new_ver == "" ]]; then
            colorEcho ${red} "Failed to fetch release information. Please check your network or try again."
            return 3
        elif [[ $retval -ne 0 ]];then
            return 2
        elif [[ $new_ver != $cur_ver ]];then
            return 1
        fi
        return 0
    fi
}

stopV2ray(){
    colorEcho ${blue} "Shutting down $key service."
    if [[ -n "${systemctl_cmd}" ]] || [[ -f "/lib/systemd/system/$key_lower.service" ]] || [[ -f "/etc/systemd/system/$key_lower.service" ]]; then
        ${systemctl_cmd} stop $key_lower
    fi
    if [[ $? -ne 0 ]]; then
        colorEcho ${yellow} "Failed to shutdown $key service."
        return 2
    fi
    return 0
}

startV2ray(){
    if [ -n "${systemctl_cmd}" ] && [[ -f "/lib/systemd/system/$key_lower.service" || -f "/etc/systemd/system/$key_lower.service" ]]; then
        ${systemctl_cmd} start $key_lower
    fi
    if [[ $? -ne 0 ]]; then
        colorEcho ${yellow} "Failed to start $key service."
        return 2
    fi
    return 0
}

installV2Ray(){
    # Install $key binary to /usr/bin/$key_lower
    if [[ $key == "V2Ray" && `unzip -l $1|grep v2ctl` ]];then
        unzip_param="$2v2ctl"
        chmod_param="/usr/bin/$key_lower/v2ctl"
    fi
    mkdir -p /etc/$key_lower /var/log/$key_lower && \
    unzip -oj "$1" "$2${key_lower}" "$2geoip.dat" "$2geosite.dat" $unzip_param -d /usr/bin/$key_lower && \
    chmod +x /usr/bin/$key_lower/$key_lower $chmod_param || {
        colorEcho ${red} "Failed to copy $key binary and resources."
        return 1
    }

    # Install V2Ray server config to /etc/v2ray
    if [ ! -f /etc/$key_lower/config.json ]; then
        local port="$(($RANDOM + 10000))"
        local uuid="$(cat '/proc/sys/kernel/random/uuid')"

        if [[ $key == "Xray" ]];then
            cat > /etc/$key_lower/config.json <<EOF
{
  "inbounds": [{
    "port": 10086,
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "23ad6b10-8d1a-40f7-8ad0-e3e35cd38297",
          "level": 1,
          "alterId": 64
        }
      ]
    }
  }],
  "outbounds": [{
    "protocol": "freedom",
    "settings": {}
  },{
    "protocol": "blackhole",
    "settings": {},
    "tag": "blocked"
  }],
  "routing": {
    "rules": [
      {
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "blocked"
      }
    ]
  }
}
EOF
            sed -i "s/10086/${port}/g; s/23ad6b10-8d1a-40f7-8ad0-e3e35cd38297/${uuid}/g;" /etc/$key_lower/config.json
        else
            unzip -pq "$1" "$2vpoint_vmess_freedom.json" | \
            sed -e "s/10086/${port}/g; s/23ad6b10-8d1a-40f7-8ad0-e3e35cd38297/${uuid}/g;" - > \
            /etc/$key_lower/config.json || {
                colorEcho ${yellow} "Failed to create $key configuration file. Please create it manually."
                return 1
            }
        fi

        colorEcho ${blue} "port:${port}"
        colorEcho ${blue} "uuid:${uuid}"
    fi
}


installInitScript(){
    if [[ -e /.dockerenv ]]; then
        if [[ $key_lower == "v2ray" ]];then
            if [[ ${new_ver} =~ "v4" ]];then
                sed -i "s/run -c/-config/g" /root/run.sh
            else
                sed -i "s/-config/run -c/g" /root/run.sh
            fi
        fi
        return
    fi
    if [[ ! -f "/etc/systemd/system/$key_lower.service" && ! -f "/lib/systemd/system/$key_lower.service" ]]; then
        cat > /etc/systemd/system/$key_lower.service <<EOF
[Unit]
Description=${key} Service
After=network.target nss-lookup.target

[Service]
Type=simple
User=root
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ExecStart=/usr/bin/$key_lower/$key_lower run -c /etc/$key_lower/config.json
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
        systemctl enable $key_lower.service
    fi
    if [[ $key_lower == "v2ray" ]];then
        local modify_service=0
        local check_run="`cat /etc/systemd/system/$key_lower.service|grep ExecStart|grep run`"
        if [[ ${new_ver} =~ "v4" ]];then
            if [[ $check_run ]];then
                modify_service=1
                sed -i "s?^ExecStart.*?ExecStart=/usr/bin/$key_lower/$key_lower -config /etc/$key_lower/config.json?g" /etc/systemd/system/$key_lower.service
            fi
        elif [[ -z $check_run ]];then
            modify_service=1
            sed -i "s?^ExecStart.*?ExecStart=/usr/bin/$key_lower/$key_lower run -c /etc/$key_lower/config.json?g" /etc/systemd/system/$key_lower.service
        fi
        if [[ $modify_service == 1 ]];then
            systemctl daemon-reload
            systemctl restart $key_lower
        fi
    fi
}

Help(){
  cat - 1>& 2 << EOF
./go.sh [-h] [-c] [--remove] [-p proxy] [-f] [--version vx.y.z] [-l file] [-x]
  -h, --help            Show help
  -p, --proxy           To download through a proxy server, use -p socks5://127.0.0.1:1080 or -p http://127.0.0.1:3128 etc
  -f, --force           Force install
      --version         Install a particular version, use --version v3.15
  -l, --local           Install from a local file
      --remove          Remove installed V2Ray/Xray
  -x, --xray            Xray mod
  -c, --check           Check for update
EOF
}

remove(){
    if [[ -n "${systemctl_cmd}" ]] && [[ -f "/etc/systemd/system/$key_lower.service" ]];then
        if pgrep "$key_lower" > /dev/null ; then
            stopV2ray
        fi
        systemctl disable $key_lower.service
        rm -rf "/usr/bin/$key_lower" "/etc/systemd/system/$key_lower.service"
        if [[ $? -ne 0 ]]; then
            colorEcho ${red} "Failed to remove $key."
            return 0
        else
            colorEcho ${green} "Removed $key successfully."
            colorEcho ${blue} "If necessary, please remove configuration file and log file manually."
            return 0
        fi
    elif [[ -n "${systemctl_cmd}" ]] && [[ -f "/lib/systemd/system/$key_lower.service" ]];then
        if pgrep "$key_lower" > /dev/null ; then
            stopV2ray
        fi
        systemctl disable $key_lower.service
        rm -rf "/usr/bin/$key_lower" "/lib/systemd/system/$key_lower.service"
        if [[ $? -ne 0 ]]; then
            colorEcho ${red} "Failed to remove $key."
            return 0
        else
            colorEcho ${green} "Removed $key successfully."
            colorEcho ${blue} "If necessary, please remove configuration file and log file manually."
            return 0
        fi
    else
        colorEcho ${yellow} "$key not found."
        return 0
    fi
}

checkUpdate(){
    echo "Checking for update."
    version=""
    getVersion
    retval="$?"
    if [[ $retval -eq 1 ]]; then
        colorEcho ${blue} "Found new version ${new_ver} for $key.(Current version:$cur_ver)"
    elif [[ $retval -eq 0 ]]; then
        colorEcho ${blue} "No new version. Current version is ${new_ver}."
    elif [[ $retval -eq 2 ]]; then
        colorEcho ${yellow} "No $key installed."
        colorEcho ${blue} "The newest version for $key is ${new_ver}."
    fi
    return 0
}

main(){
    #helping information
    [[ "$help" == "1" ]] && Help && return
    [[ "$check" == "1" ]] && checkUpdate && return
    [[ "$remove" == "1" ]] && remove && return

    local arch=$(uname -m)
    archAffix

    # extract local file
    if [[ $local_install -eq 1 ]]; then
        colorEcho ${yellow} "Installing $key via local file. Please make sure the file is a valid $key package, as we are not able to determine that."
        new_ver=local
        rm -rf /tmp/$key_lower
        zipfile="$local"
    else
        # download via network and extract
        installSoftware "curl" || return $?
        getVersion
        retval="$?"
        if [[ $retval == 0 ]] && [[ "$force" != "1" ]]; then
            colorEcho ${blue} "Latest version ${cur_ver} is already installed."
            if [ -n "${error_if_uptodate}" ]; then
              return 10
            fi
            return
        elif [[ $retval == 3 ]]; then
            return 3
        else
            colorEcho ${blue} "Installing $key ${new_ver} on ${arch}"
            downloadV2Ray || return $?
        fi
    fi

    local ziproot="$(zipRoot "${zipfile}")"
    installSoftware unzip || return $?

    if [ -n "${extract_only}" ]; then
        colorEcho ${blue} "Extracting $key package to ${vsrc_root}."

        if unzip -o "${zipfile}" -d ${vsrc_root}; then
            colorEcho ${green} "$key extracted to ${vsrc_root%/}${ziproot:+/${ziproot%/}}, and exiting..."
            return 0
        else
            colorEcho ${red} "Failed to extract $key."
            return 2
        fi
    fi

    if pgrep "$key_lower" > /dev/null ; then
        v2ray_running=1
        stopV2ray
    fi
    installV2Ray "${zipfile}" "${ziproot}" || return $?
    installInitScript "${zipfile}" "${ziproot}" || return $?
    if [[ ${v2ray_running} -eq 1 ]];then
        colorEcho ${blue} "Restarting $key service."
        startV2ray
    fi
    colorEcho ${green} "$key ${new_ver} is installed."
    rm -rf /tmp/$key_lower
    return 0
}

main
