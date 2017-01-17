#!/bin/bash
# Show all 16 terminal colors

for i in {0..7};do
   printf "\033[0;3${i}m  ${i} NORM █████████████ 0;3${i}m \033[0m\n"
done
for i in {0..7};do
   printf "\033[1;3${i}m 1${i} NORM █████████████ 1;3${i}m \033[0m\n"
done
