#!/bin/bash

path="/home/project_files/backup/"

filename=backup.log
log=$path$filename
days=13

mkdir -p $path

echo "\n------- DAY $(date +%d/%m/%Y) ------\n" >> $log

echo "Deleting old backups:\n" >> $log

if find $path -name '*.sql' -type f -mtime +$days -print -quit | grep -q . ; then
    find $path -name '*.sql' -type f -mtime +$days -exec rm -f {} + -print >> $log
else
    echo "Sorry, we didnt find any old backups." >> $log
fi

echo  "\nInitializing Backup -- $(date +%H:%M:%S)\n" >> $log

PGPASSFILE=/home/project_files/.pgpass pg_dump -U postgres -h localhost -p 5432 -d rent_watch -v -f $path/backup_$(date +'%H:%M_%d%m%Y').sql 2>> $log

echo  "\nFinalizing Backup -- $(date +%H:%M:%S)" >> $log
