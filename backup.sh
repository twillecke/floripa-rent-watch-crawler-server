#!/usr/bin/bash

PGPASSFILE=~/.pgpass pg_dump -U postgres -h localhost -p 5432 -d rent_watch -f ~/backupdb/"backup_$(date +"%d%m%Y").sql"
