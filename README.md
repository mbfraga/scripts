# scripts

## usage

I simply add this directory to PATH, but you could just use symlinks or run
scripts in ~/bin

## list of scripts

List of useful scripts I use daily...for the most part.

* colors256.sh -- lists the 256 terminal colors.

* colorsterm.sh -- list the first 16 terminal colors.

* listspecchars -- prints the special_character_list (used for personal st hook

* mbmain -- manage rofi_mbscripts (enable/disable/run)

* now_playing.sh -- print now playing (can send to notify-send or paste to
    cursor via xdotool.

* print_i3layout.py -- prints the current i3 layout. Useful as a didactic tool
    for learning how i3 works. `watch ./print_i3layout.py` is particularly
    useful.

* rofication-gui.py -- manage notifications via a rofi interface (depends on
    eventd)

* special_character_list -- a list of special characters that can be sent to
    rofi/dmenu/fzf and parsed easily.

* special_characters.sh -- displays special_character_list in dmenu or rofi,
    and pastes (via xdotool) the selection to the cursor. Alternative or
    complementary to compose key.

* sshot -- wrapper for maim to take screenshots. Adds the ability to easily
    select a target display for the screenshot, and also can upload to ptpb.pw.


## rofi_mbscripts

Quirky yet simplistic set of scripts and management tools for a set of rofi
scripts.

Use mbmain to manage them.

```
mbmain enable **scriptname**

mbmain disable **scriptname**
```

Then just run mbmain, select the right script. As of now, there is no way to go
back to the original menu. Fixing this is not hard, but would make things a bit
dirtier and I'm not sure I like the idea anyway.
