#!/bin/bash
# Show all 16 terminal colors

for i in {0..7};do
   printf "\033[0;3%dm  %d NORM █████████████ 0;3%dm \033[0m\n" "$i" "$i" "$i"
done
for i in {0..7};do
   printf "\033[1;3%dm 1%d NORM █████████████ 1;3%dm \033[0m\n" "$i" "$i" "$i"
done
