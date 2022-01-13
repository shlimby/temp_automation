# get this directory
path=$( realpath "$0"  ) 
dir=$(dirname "$path")'/'

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "# added by temp automation" >> mycron
# echo "@reboot "$dir"venv/bin/python3 "$dir"run_chat_bot.sh &" >> mycronKU
echo "@reboot cd "$dir" && bash "$dir"run_chat_bot.sh &" >> mycron
#install new cron file
crontab mycron
rm mycron