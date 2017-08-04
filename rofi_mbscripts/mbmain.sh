#!/bin/bash

# application variables
ROOT_PATH="$( cd "$( dirname "$0" )" && pwd )"

if [[ -z "$ENABLED_PATH" ]]; then
   ENABLED_PATH="$ROOT_PATH/enabled"
fi

if [[ -z "$SCRIPTS_PATH" ]]; then
   SCRIPTS_PATH="$ROOT_PATH/scripts"
fi

# launcher variables
PROMPT='mbscripts:'

if [[ -z "$LAUNCHER" ]];then
   LAUNCHER='rofi'
fi

function _launcher () {
   rofi -dmenu -p "$PROMPT"
}

#echo "ENABLED_PATH: $ENABLED_PATH"
#echo "SCRIPTS_PATH: $SCRIPTS_PATH"

function list_scripts {
   if find "$ENABLED_PATH" -mindepth 1 -print -quit | grep -q .; then
      for entry in "$ENABLED_PATH"/*; do
         printf '%s\n' "${entry##*/}"
      done
   else
      PROMPT='mbscripts (no scripts enabled):'
      echo ""
   fi
}

target_script=$( list_scripts | _launcher)

if [[ ! -z "$target_script" ]]; then
   LAUNCHER=$LAUNCHER "$ENABLED_PATH/$target_script"
fi
