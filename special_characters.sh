#!/bin/bash
# Creates a menu of special characters via dmenu or rofi Once a character is
# selected, it is pasted to the cursor via xdotool symbols can be added with
# any keyword, but make sure to keep the syntax
#
# syntax: keyword    :$symbol\n
#
# $symbol will be the characters printed via xdotool. Anything between the
# colon and the \n (linebreak) will be pasted, including spaces.
#
# note1: By modifying the cut command at the end of the script, a different
# character rather than colon could be use, in case some of the symbols desired
# have colons in them. For my purpose, this has never been the case.
#
# note2: The xdotool is given a delay because of issues I've had with printing
# long smileys, this could be removed if only single-character symbols are
# desired, and it may improve the experience.
#
# Script Created By: https://github.com/mbfraga Feel free to do anything you
# want with this script.

launcher=dmenu # dmenu/rofi

if [ $# > 0 ]; then
   if [ "$1" == "-d" ]; then
      launcher="dmenu"
   elif [ "$1" == "-r" ]; then
      launcher="rofi"
   fi
fi

if [ "$launcher" == "dmenu" ]; then
   if !(command -v dmenu 2>/dev/null); then
      echo "dmenu not installed, trying rofi..."
      if command -v rofi 2>/dev/null; then
         launcher=rofi
      else
         echo "rofi not installed either, aborting..."
         exit 1
      fi
   fi
fi

if [ "$launcher" == "rofi" ]; then
   if !(command -v rofi 2>/dev/null); then
      echo "dmenu not installed, trying dmenu..."
      if command -v dmenu 2>/dev/null; then
         launcher=dmenu
      else
         echo "dmenu not installed either, aborting..."
         exit 1
      fi
   fi
fi


_rofi () {
      rofi -dmenu -p "(symbols): " $@
}

_dmenu () {
   dmenu $@
}

symbols='
alpha       :α\n
beta        :β\n
gamma       :γ\n
delta       :δ\n
epsilon     :ε\n
zeta        :ζ\n
eta         :η\n
theta       :θ\n
iota        :ι\n
kappa       :κ\n
lambda      :λ\n
mu          :μ\n
nu          :ν\n
xi          :ξ\n
omicron     :ο\n
pi          :π\n
rho         :ρ\n
sigma       :σ\n
tau         :τ\n
upsilon     :υ\n
phi         :φ\n
chi         :χ\n
psi         :ψ\n
omega       :ω\n
              \n
Alpha       :Α\n
Beta        :Β\n
Gamma       :Γ\n
Delta       :Δ\n
Epsilon     :Ε\n
Zeta        :Ζ\n
Eta         :Η\n
Theta       :Θ\n
Iota        :Ι\n
Kappa       :Κ\n
Lambda      :Λ\n
Mu          :Μ\n
Nu          :Ν\n
Xi          :Ξ\n
Omicron     :Ο\n
Pi          :Π\n
Rho         :Ρ\n
Sigma       :Σ\n
Tau         :Τ\n
Upsilon     :Υ\n
Phi         :Φ\n
Chi         :Χ\n
Psi         :Ψ\n
Omega       :Ω\n

accent a    :á\n
accent e    :é\n
accent i    :í\n
accent o    :ó\n
accent u    :ú\n
n tilda     :ñ\n
enie        :ñ\n
ae          :æ\n
diameter    :ø\n
o with stroke :ø\n
thorn       :þ\n
inverted exclamation mark: ¡\n

em-dash     :—\n


circ        :°\n
degrees     :°\n
oo          :°\n
angstroms   :Å\n
tm          :™\n
pound       :£\n
yen         :¥\n
cents       :¢\n
copyright   :©\n
registered  :®\n
plusorminus :±\n
micron      :µ\n
paragraph   :¶\n
middle dot  :·\n
multiplication :×\n
division    :÷\n
gun         :¬\n


sup1        :¹\n
sup2        :²\n
sup3        :³\n
sup4        :⁴\n
sup5        :⁵\n
sup6        :⁶\n
sup7        :⁷\n
sup8        :⁸\n
sup9        :⁹\n
sup0        :⁰\n
sub1        :₁\n
sub2        :₂\n
sub3        :₃\n
sub4        :₄\n
sub5        :₅\n
sub6        :₆\n
sub7        :₇\n
sub8        :₈\n
sub9        :₉\n
sub0        :₀\n

bto         :BaTiO₃\n

smiley_hug1 :(っ´ω｀)っ\n
smiley_hug2 :⊂(´Д`⊂)\n
smiley_mischevious  :(｡◕‿‿◕｡)\n
smiley_frustrated :(屮ﾟДﾟ)屮\n
smiley_fight      :(ง •̀_•́)ง\n
smiley_fight_srz  :(ง ͠° ͟ʖ ͡°)ง\n
smiley_fightL     :L(° O °L)\n
smiley_fin_adventure_time : | (• ◡•)|\n
smiley_dunno      : ¯\(°_o)/¯\n
smiley_dunno2     : ┐( ﾟーﾟ)┌\n
smiley_jake_adventure_time : (❍ᴥ❍ʋ)\n
smiley_wtf: (ಠ_ಠ)\n
smiley_crying: (ಥ_ಥ)\n
smiley_smug: (￣ω￣)\n
smiley_smug2: （￣へ￣）\n


smiley_arab_surprised  :   ة\n
smiley_arab_surprised  :   ت\n
'


if [ "$launcher" == "dmenu" ]; then
   selected_string=$(echo -e $symbols | _dmenu)
elif [ "$launcher" == "rofi" ]; then
   selected_string=$(echo -e $symbols | _rofi)
fi

selected_symbol=$(echo $selected_string | cut -d : -f 2 )
setxkbmap us; xdotool type --delay 100 "$selected_symbol"
