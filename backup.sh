#!/usr/bin/bash

PGPASSFILE=~/.pgpass pg_dump -U postgres -h localhost -p 5432 -d rent_watch -f ~/backup/"backup_$(date +"%H:%M_%d%m%Y").sql" 

find /home/gbarbosa1407/backup/ \( -name '*.sql' \) -print0 | sort -zr | sed -nz '3,$p' | xargs -0  rm -f
