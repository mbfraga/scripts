#!/bin/bash

ROOT_PATH="$( cd "$( dirname "$0" )" && pwd )"

if [[ -z "$LAUNCHER" ]];then
   LAUNCHER='rofi'
fi

case $LAUNCHER in
   "rofi")
   COMMAND="rofi -dmenu -p mbscripts:"
   ;;
   "dmenu")
   COMMAND='dmenu'
   ;;
   *)
esac

if [[ -z "$ENABLED_PATH" ]]; then
   ENABLED_PATH="$ROOT_PATH/enabled"
fi

if [[ -z "$SCRIPTS_PATH" ]]; then
   SCRIPTS_PATH="$ROOT_PATH/scripts"
fi

#echo "ENABLED_PATH: $ENABLED_PATH"
#echo "SCRIPTS_PATH: $SCRIPTS_PATH"

function list_scripts {
   for entry in "$ENABLED_PATH"/*; do
      printf '%s\n' "${entry##*/}"
   done
}
target_script=$( list_scripts | $COMMAND)

if [[ ! -z "$target_script" ]]; then
   LAUNCHER=$LAUNCHER "$ENABLED_PATH/$target_script"
fi
