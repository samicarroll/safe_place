# A Safe Place: Web Scraping Application
## Description:
Using Selenium, an XML and HTML parser, our software will scrape information from various websites searching for keywords commonly used in human trafficking. 

## Translation of keywords in Spanish 
- Escorte: Escort
- Policia: police 
- LLamarme: Call me

## Technology Requirements
- Google Chrome Browser
- Required packages 
- MacOS or Windows Operating System

## Installing Packages:
packages needed can be installed in the terminal
```
> pip install -r requirements.txt
```

## Current Release: 1.0.5:
- contains base code that will search "SkipTheGames" and "Megapersonals"; desired sites for human trafficking. 
- uses selenium chromedriver to search and save all listings on every page for Fort Lauderdale, Fort Myers, Miami, Tampa, and Sarasota areas.
- uses a keyword text file 'keyword.txt' to grab a list of desired keywords.
  - listings that match the keywords are screenshotted and exported to a png titled '[screenshot number]_megapersonals.png' and it will document the listing number, url, title, description, age, and keyword then export to an excel. 
- implemented database for users username and password
  - new users will be able to register a username and password
- implemented basic UI for customers; includes login screen, allows user to choose a website to scrape. 
- excel file and screenshots are saved in folders located on the user desktop.
- desktop folders are created in the following directory:
```
user/desktop/megapersonals/[location]/screenshots/[timestamp]/[screenshot number]_megapersonals.png
user/desktop/megapersonals/[location]/excel_files/[timestamp]/megapersonals_[timestamp].xlsx
```
<img width="1428" alt="Screenshot 2023-05-03 at 11 52 16 AM" src="https://user-images.githubusercontent.com/62121500/235970210-e312ea58-e6be-4628-b062-5f120ca27d84.png">

