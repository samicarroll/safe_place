# Safe Place 
## Description:
Using Selenium, an XML and HTML parser, our software will scrape information from various websites searching for keywords commonly used in human trafficking. 

## Technology Requirements
-Firefox browser
- Google Chrome Browser
- Required packages 

## Installing Packages:
packages needed can be installed in the terminal
```
> pip install -r requirements.txt
```

## Current Release: 1.0.3:
- contains base code the will search "SkipTheGames" and "Megapersonals"; desired sites for human trafficking. 
- uses selenium chromedriver to search and save all listings on every page for Fort Myers area.
- uses a keyword text file 'keyword.txt' to grab a list of desired keywords.
  - listings that match the keywords are screenshotted and exported to a png titled 'megapersonals_[listing number]_keyword' and it will document the listing number, url, title, description, age, and keyword then export to an excel. 
- implemented basic UI for customers; includes login screen, allows user to choose a website to scrape. 
- excel file and screenshots are saved in files located on the user desktop. 

## Future Releases
- Fully functional user interface will be implemented
- Deployment
