@echo off

REM Set the working directory to the location of your Python scripts
cd /d "D:\Reylian's Space\Mandiri\TwitterBrandAbuse"

echo Running script 1...
python crawl_query.py

echo Running script 2...
python crawl_replies.py

echo Running script 3...
python clean_tweet.py"

echo All scripts have been executed.
pause