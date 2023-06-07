#!/bin/bash

path="/home/project_files/backup/"

filename=backup.log
log=$path$filename
days=13

mkdir -p $path

echo '' > $log

printf "Starting backup routine.\n\n" >> $log

printf "Saving backup on:\n\n%s\n" "$path" >> $log

printf "\nInitializing Backup -- $(date +%H:%M:%S)\n\n" >> $log

PGPASSFILE=~/.pgpass pg_dump -U postgres -h localhost -p 5432 -d rent_watch -v -f /home/project_files/backup/backup_$(date +'%H:%M_%d%m%Y').sql 2>> $log

printf "\nFinalizing Backup -- $(date +%H:%M:%S)\n" >> $log

printf "\nDeleting old backups:\n" >> $log

if find $path -name '*.sql' -type f -mtime +$days -print -quit | grep -q . ; then
    find $path -name '*.sql' -type f -mtime +$days -exec rm -f {} + -print >> $log
else
    printf "\nNo backups were deleted." >> $log
fi

printf "\n\nClosing backup routine." >> $log
