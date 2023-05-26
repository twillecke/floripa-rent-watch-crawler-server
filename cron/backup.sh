#!/bin/bash

path="$HOME/backup/"

filename=backup.log
log=$path$filename
days=13

mkdir -p $path

echo '' > $log 

echo -e "\n------- DAY $(date +%d/%m/%Y) ------\n" >> $log

echo -e "Deleting old backups:\n" >> $log

if find $HOME/backup -name '*.sql' -type f -mtime +$days -print -quit | grep -q . ; then
    find $path -name '*.sql' -type f -mtime +$days -exec rm -f {} + -print >> $log
else
    echo "Sorry, we didnt find any old backups." >> $log
fi

echo -e "\nInitializing Backup -- $(date +%H:%M:%S)\n" >> $log

PGPASSFILE=~/.pgpass pg_dump -U postgres -h localhost -p 5432 -d rent_watch -v -f ~/backup/backup_$(date +'%H:%M_%d%m%Y').sql 2>> $log

echo -e "\nFinalizing Backup -- $(date +%H:%M:%S)" >> $log
