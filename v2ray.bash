# bash completion for v2ray                             -*- shell-script -*-
function _auto_tab() {
	local options_array=("start" "stop" "restart" "status" "update" "add" "del" "info" "port" "tls" "tfo" "stream" "cdn" "stats" "clean" "log" "new" "-h" "-v")
	local add_array=("wechat" "utp" "srtp" "dtls" "wireguard" "socks" "mtproto" "ss")
	local cur pre

	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"

	case $prev in
		'v2ray')
			COMPREPLY=( $(compgen -W "${options_array[*]}" -- $cur) ) ;;
		'add')
			COMPREPLY=( $(compgen -W "${add_array[*]}" -- $cur) );;
		'*')
			COMPREPLY=( $(compgen -d -f ${cur}) ) ;;
	esac

	return 0
}
complete -F _auto_tab v2ray