#!/bin/bash

list=($(ls ./sing-box/))
for ((i = 0; i < ${#list[@]}; i++)); do
	sing-box rule-set compile ${list[i]}.json -o ${list[i]}.srs
done