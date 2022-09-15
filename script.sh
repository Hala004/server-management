#!/bin/sh

`cat /proc/meminfo | head -5 | awk {'print $2'} > /file_serv_1`

`iostat | head -4 | tail -1 |awk {'print $1 "   " $2  "    " $3 "    " $4 "   " $5 "   " $6'} > /file_serv_2`