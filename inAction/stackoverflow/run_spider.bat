@echo off
cmd /k "cd /d C:\Users\kwang6\eBayWorks\VENV\Scripts & activate.bat & cd /d C:\Users\kwang6\eBayWorks\gitRepo\Scrapy_Samples\inAction\stackoverflow & scrapy crawl SO_Badge_counter & deactivate"

echo Finished
exit