# Python-C--sync
bash & rsync  
alt cronjob & rsync

chmod +x sync.sh  
crontab -e  
*/15 * * * * /path/to/sync.sh /path/to/source /path/to/replica /path/to/logfile.log  
