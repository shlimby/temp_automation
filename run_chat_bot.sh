# get this directory
path=$( realpath "$0"  ) 
dir=$(dirname "$path")'/'
cd $dir 

# echo $(pwd) >> test.log
sudo ./venv/bin/python3 chat_bot.py