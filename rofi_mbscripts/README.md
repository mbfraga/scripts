# mbmain

This is simply a tool to manage rofi scripts from a global rofi menu. You can
enable/disable scripts located in ./scripts. Not all of these scripts are
standalone, and they have varying dependencies (some of which are other scripts
of mine (like sshot).

## run

To run, simply run `./mbmain.sh`. This will display a menu with all the scripts
that have been enabled.


## enable disable scripts

To enable a script, run `./mbscript.sh enable <script name>`

To disable a script, run `./mbscript.sh disable <script name>`


## dependencies

* rofi

For specific scripts to work:

1. sshot

2. screenshots

3. define
   * sdcv (dictionary)
   * dictionary file `"dictd_www.dict.org_gcide"`

3. thesaurus
   * sdcv (dictionary)
   * dictionary file `"Moby Thesaurus II"`
