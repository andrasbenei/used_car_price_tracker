# Price tracker

This is a project in which I want to monitor the used car prices in Hungary and Germany. To do this, I use Beautiful Soup to download the data and Python to clean and
analyze it. I want to be able to determine proper selling/purchasing prices at a given date, find over / undervalued cars and identify trends on the market. I also want 
to compare the Hungarian and German markets to see any relevant differences.

Current status:
- 'Download' script downloads the data with a given searching setup from Hasznaltauto.hu and saves it in 'data.csv'. 'Analyze.ipynb' shows a possible cleaning and analyzing 
process.

Next steps:
- Create 'main.csv' to collect data every day. This should contain new columns to show how long was and add active on the site: Time-in, Time-out, Days_advertised
- Create a new script to run 'Download' every day, cross-check the downloaded data with 'main.py', add the Time-out date to 'main.py' if an advertisement is missing from the 
daily dataset, add new lines from the daily dataset to 'main.py'
- Improve the Analyze file: make it dynamic to show results with every input of data. Also it should identify trends like increasing/decreasing advertising time.
- Create another download file to download data from Mobile.de. Compare the German market with the Hungarian.
