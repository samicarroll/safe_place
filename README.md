# Safe Place 
## Description:
Using XML and HTML parsers (BeautifulSoup and Selenium), our software will scrape information from various websites searching for keywords commonly used in human trafficking. 

## Current Release: 1.0.2:
- contains base code the will search "SkipTheGames" and "Megapersonals"; desired sites for human trafficking. 
- uses selenium chromedriver to search and save all listings on every page for Fort Myers area.
- implemented a keyword list to find common keywords used in human trafficking. 
  - listings that match the keywords are screenshotted and exported to a png titled '' and it will document the title, description, age, and keyword then export to an excel. 
- implemented basic UI for customers; includes login screen, allows user to choose a website to scrape. 

## Installing Packages:
packages needed can be installed in the terminal

> pip install -r requirements.txt


## Future Releases
- Fully functional user interface will be implemented
- Deployment
