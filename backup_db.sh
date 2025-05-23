#!/bin/bash

# Set variables
BACKUP_DIR="backups"
DB_FILE="db.sqlite3"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sqlite3"

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

# Create database backup
echo "Creating database backup..."
cp $DB_FILE $BACKUP_FILE

# Compress backup file
echo "Compressing backup file..."
gzip $BACKUP_FILE

# Remove backups older than 7 days
echo "Cleaning up old backups..."
find $BACKUP_DIR -name "db_backup_*.sqlite3.gz" -mtime +7 -delete

echo "Backup completed: ${BACKUP_FILE}.gz" 