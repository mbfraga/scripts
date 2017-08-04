#!/bin/bash
# author mbfraga@gmail.com
# Wrapper on top of maim that provides a few more functionalities. It can take
# a screenshot of a specified display.

# dependencies
#   xrandr
#   maim
#   curl
#   xclip


# Possible aliases
# sshot

# To implement
# possibility to add delay with -d
# store list of screenshots

# possible colors to assign to maim
LIGHTRED=".96,0.55,0.41,1.0"
MAGENTA="0.7,0.3,0.7,1.0"

# Settings
DEST=~/Pictures/screenshots/
IMGNAME="sshot-`date +'%d-%m-%Y_%H:%M:%S'`.png"
IMGLOC=$DEST$IMGNAME
DELAY=false
SELECTION_SETTINGS="--bordersize=3 --color=$MAGENTA"
SCREENSHOT_TYPE=""

if [[ -z $SSHOT_UPLOAD ]]; then
   SSHOT_UPLOAD=true
fi

if [[ -z $ROFI_PLUGIN ]]; then
   ROFI_PLUGIN=false
fi

# Print help
function sm_help () {
   echo -e "sshot.sh - take screenshot and upload to ptpb.pw\n"
   echo -e "SYNOPSIS"
   echo -e "	sshot.sh [OPTION] [COMMAND]\n"
   echo -e "OPTION"
   echo -e "	-d [delay]	-add delay"
   echo -e "			e.g., sshot -d 10 DP-0\n"
   echo -e "COMMAND"
   echo -e "	all		-take screenshot of entire screen\n"
   echo -e "	<display>	-take screenshot of specific display using its proper name (check xrandr). e.g. DP-0"
   echo -e "			e.g., sshot.sh DP-0\n"
   echo -e "	<display #>	-take screenshot of specific display using its number. e.g. 0, 1"
   echo -e "			e.g., sshot.sh 0\n"
   echo -e "	sel|selection	-take screenshot of area or window selected by user (interactive)\n"
}


# Print some helpful information in case of ERROR
function sm_cry () {
   echo "DELAY: $DELAY"
   echo "DELAY_TIME: $DELAY_TIME"
   echo "SCREENSHOT_TYPE: $SCREENSHOT_TYPE"
   echo "TARGET_DISP: $TARGET_DISP"
   echo "TARGET_GEOM: $TARGET_GEOM"
   echo "IMGLOC: $IMGLOC"
}


# Check that the screenshot file was actually created
function check_img () {
   if [[ -f $@ ]]; then
      return
   else
      echo "Something went wrong and screenshot was not taken. Exiting..."
      sm_cry
      exit 1
   fi
}


# Upload image and notify via notify-send
function upload() {
   if [[ ! -z $1 ]]; then
      #p=1 == long url
      #sunset=432000 kill screenshot after 5 days
      $(curl -F c=@${1} -F p=1 sunset=432000 https://ptpb.pw &>/tmp/curl.progress)
      wait
      url=$(tail -n-2 /tmp/curl.progress | head -n1 | cut -c6-)

      regex='(https?|http)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'
      if [[ ! $url =~ $regex ]]; then
         echo "Upload failed..."
         sm_cry
         echo -e "Curl output:\n------------\n"
         cat /tmp/curl.progress
         notify-send "Upload failed... /tmp/curl.progress"
         exit 1
      else
         notify-send "Screenshot taken" "${url}" && \
         echo -n "$url" | xclip -i -selection primary && \
         echo -n "$url" | xclip -i -selection clipboard
      fi
   fi
}


function _maim() {
   if [[ ! $DELAY = true ]]; then
      maim "$@"
   else
      maim -d "$DELAY_TIME" "$@"
#      if hash notify-send.sh 2>/dev/null; then
#         notid=$(notify-send.sh --print-id sshot "Screenshot in ${DELAY_TIME}s...")
#      fi
   fi
   if [[ $? -eq 1 ]]; then
      echo "Error in maim. In most cases, it just means the selection was cancelled (which is normal behavior)."
      exit 1
   fi
}


function parseargs () {
   re='^-?[0-9]+$'
   if [[ $# -eq 0 ]]; then
      SCREENSHOT_TYPE="all"
   elif [[ $# -eq 1 ]]; then
      if [[ "$1" == "-h" ]]; then
         sm_help
         exit 0
      elif [[ "$1" == "all" ]]; then
         SCREENSHOT_TYPE="all"
      elif [[ "$1" == "sel" ]] || [[ $1 == "selection" ]]; then
         SCREENSHOT_TYPE="sel"
      elif [[ $1 =~ $re ]]; then
         SCREENSHOT_TYPE="dispnum"
         TARGET_DISP_NUM=$1
      else
         SCREENSHOT_TYPE="display"
         TARGET_DISP=$1
      fi
   # only case for 2 arguments will be sshot.sh -d 10
   elif [[ $# -eq 2 ]]; then
      if [[ $1 == "-d" ]]; then
         DELAY=true
         DELAY_TIME=$2
         SCREENSHOT_TYPE="all"
      else
         echo -e "ERROR: Too many arguments."
         echo -e "If -d option is used, it must be followed by a number."
         echo -e "e.g., sshot -d 10 (will take a screenshot of entire screen after 10s"      
         echo -e "NOTE: sshot.sh -d 10 will be the only case where two arguments should be used"
         echo ""
         sm_help
         exit 1
      fi
   # every other case with -d [delay_time] will have three arguments
   elif [[ $# -eq 3 ]]; then
      if [[ $1 == "-d" ]]; then
         DELAY=true
         DELAY_TIME=$2
         if [[ "$3" == "-h" ]]; then
            sm_help
            exit 0
         elif [[ "$3" == "all" ]]; then
            SCREENSHOT_TYPE="all"
         elif [[ "$3" == "sel" ]] || [[ $3 == "selection" ]]; then
            SCREENSHOT_TYPE="sel"
         elif [[ $3 =~ $re ]]; then
            SCREENSHOT_TYPE="dispnum"
            TARGET_DISP_NUM=$3
         else
            SCREENSHOT_TYPE="display"
            TARGET_DISP=$3
         fi
      else
         echo -e "ERROR: Too many arguments."
         echo -e "If -d option is used, it must be followed by a number."
         echo -e "e.g., sshot -d 10 (will take a screenshot of entire screen after 10s"      
         echo ""
         sm_help
         exit 1
      fi
   else
      echo -e "ERROR: sshot.sh only takes zero, one or two arguments.\n"
      sm_help
      exit 1
   fi
}


function mainf() {
   parseargs "$@"
   if [[ $SCREENSHOT_TYPE == "all" ]]; then
      _maim "$IMGLOC"
      wait
      check_img "$IMGLOC"

   elif [[ $SCREENSHOT_TYPE == "sel" ]]; then
      _maim ''$SELECTION_SETTINGS'' -s "$IMGLOC"
      wait
      check_img "$IMGLOC"

   elif [[ $SCREENSHOT_TYPE == "display" ]] || [[ $SCREENSHOT_TYPE == "dispnum" ]]; then
      IFS=$'\n'
      disp_ct=0
      for disps in $(xrandr | grep " connected") 
      do
         disp_ct=$((disp_ct+1))
         #echo display: $disps
         IFS=$' '
         disp=($(echo -n "$disps" | awk {'printf ("%s %s %s %s", $1, $2, $3, $4)'}))

         if [[ $disp_ct == "$TARGET_DISP_NUM" ]]; then
            TARGET_DISP=${disp[0]}
         fi

         if [[ "$TARGET_DISP" == ${disp[0]} ]]; then
            TARGET_GEOM=${disp[2]}
         fi
         IFS=$'\n'
      done

      if [[ -z "$TARGET_GEOM" ]]; then
         echo -e "ERROR: Something went wrong and display geometry was not found\n"
         sm_cry
         exit 1
      else
         _maim -g "$TARGET_GEOM" "$IMGLOC"
         wait
         check_img "$IMGLOC"
      fi

   fi

   if [[ $SSHOT_UPLOAD = true ]];then 
      upload "${IMGLOC}"
   fi
   exit 0
}



mainf $@



