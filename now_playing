#!/bin/bash
# Print now playing from mpd via mpc
# use -n to send notification
# use -p to paste to cursor
#
# Dependencies:
# * mpc
# * notify-send (only for -n)
# * xdotool (only for -p)


# notify-send settings:
ns_urgency="normal" #low/normal/critical
ns_timeexpire="10"
ns_appname=""
ns_summary="mpd now playing:"


HELP_TAB="  "
HELP="Now Playing Script:;\
$HELP_TAB-n for notify-send;\
$HELP_TAB-p for paste to cursor via xdotool;\
$HELP_TAB-h for help"

_show_help () {
   IFS=";"
   for hl in $HELP; do
      echo "$hl"
   done

}

_notify_send () {
   if ! [[ -z "${ns_urgency// }" ]]; then
      urg="-u $ns_urgency"
   else
      urg=""
   fi
   if ! [[ -z "${ns_timeexpire// }" ]]; then
      te="-t $ns_timeexpire"
   else
      te=""
   fi
   if ! [[ -z "${ns_appname// }" ]]; then
      appn="-a $ns_appname"
   else
      appn=""
   fi
   if ! [[ -z "${ns_summary// }" ]]; then
      sum="$ns_summary"
   else
      sum=""
   fi

   notify-send $urg $te $appn "$sum" "$@"
}

if mpc status | awk 'NR==2' | grep playing >/dev/null; then
   np=$(mpc current)
else
   np="Stopped"
fi

if [[ $# -gt 1 ]]; then
   echo "Too many arguments given, only one expected."
   _show_help
   exit 1
fi

if [[ $# -eq 0 ]]; then
   echo "Now Playing: $np"
   exit 0
fi

if   [[ $1 == '-n' ]]; then
   _notify_send "$np"
   exit 0
elif [[ $1 == '-p' ]]; then
   sleep 0.1
   xdotool type --delay 2 "Now Playing: $np"
   exit 0
elif [[ $1 == '-h' ]]; then
   _show_help
   exit 0
else
   echo "Invalid argument."
   _show_help
fi


#EOF
