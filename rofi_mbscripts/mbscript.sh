#!/bin/bash

ROOT_PATH="$( cd "$( dirname "$0" )" && pwd )"

if [[ -z "$ENABLED_PATH" ]]; then
   ENABLED_PATH="$ROOT_PATH/enabled/"
fi

if [[ -z "$SCRIPTS_PATH" ]]; then
   SCRIPTS_PATH="$ROOT_PATH/scripts/"
fi

echo "ENABLED_PATH: $ENABLED_PATH"
echo "SCRIPTS_PATH: $SCRIPTS_PATH"

function print_help () {

   echo -e "mbscript.sh - manage mbscripts\n"

   echo -e "SYNOPSIS"
   echo -e "\t mbscript.sh [OPTION] SCRIPT"
   echo ""


   echo -e "OPTIONS"
   echo -e "\t -h (--help)\t\t Show help."
   echo ""

   echo -e "COMMAND"
   echo -e "\t enable SCRIPT\t\t Enable SCRIPT."
   echo -e "\t disable SCRIPT\t\t Disable SCRIPT."
   echo ""

}

function enable_script () {
   enabled_path="$ENABLED_PATH/$1"
   script_path="$SCRIPTS_PATH/$1"

   if [[ -f $enabled_path ]];then
      echo "Script '$1' already enabled."
      return
   fi
   if [[ ! -f "$script_path" ]];then
      echo "Script '$1' not found in '$SCRIPTS_PATH'."
      return
   fi
   ln -s "$script_path" "$enabled_path" &&
      echo "Script '$1' enabled."
}

function disable_script () {
   enabled_path="$ENABLED_PATH/$1"
   script_path="$SCRIPTS_PATH/$1"

   if [[ ! -f $enabled_path ]];then
      echo "Script '$1' already disabled."
      return
   fi
   rm $enabled_path && echo "Script '$1' disabled."

}


if [[ $# -eq 0 ]];then
   print_help
else

   if [[ "$1" == "-h" || "$1" == "--help" ]]; then
      print_help
   else
      if [[ $# -ne 2 ]];then
         echo "ERROR: Incorrect number of arguments"
         show_help
         exit 1
      fi

      if [[ "$1" == "enable" ]]; then
         enable_script $2
      elif [[ "$1" == "disable" ]]; then
         disable_script $2
      else
         echo "ERROR: Incorrect command '$1'"
         show_help
         exit 1
      fi
   fi
fi
