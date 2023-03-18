#! /bin/bash
zgrep -v '"fileContent" :' $1 | grep -v '"chunkData" :' > $2
tr -cd '\11\12\15\40-\176' < $2 > $3

