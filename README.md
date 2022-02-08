# College Football Recruiting Class Evaluator

## Project Overview
This Python project utilizes web scraping to evaluate the recruiting class of a given college football team, in a given season.

## Data Overview
Data comes from [247 Sports](https://247sports.com/), which is widely considered the best database for college football and basketball recruiting and news.  For each major college football team, the website tracks its recruiting class for historical years, the present year, and future years.  The site lists the players who have committed to a given team.  

Each player has an individual profile too.  These profiles list biographical information, as well as the recruiting sites prospect rating, a float between 0 and 1, with values closer to 1 representing a higher rating.  The individual profiles also list what schools have extended a scholarship offer to the athlete.  

## Evaluating a Recruiting Class
247 Sports evaluates recruiting classes according to the ratings of the athletes that make up the class.  This is one good way to look at it, as the site has a network of talent evaluators across the country who scout the players and assign the ratings systematically.  However, a different approach is to look at how many scholarship offers an athlete has, and who they are from.  The more an athlete is sought after by the major programs, the better a recruit he would tend to be.  

This project evaluates a team's recruiting class based on average number of scholarship offers each of its members has received.  Only scholarship offers from a team in one of the Power Five conferences counts toward the average.  A max number of scholarships can be set when evaluating the team to avoid skewing the average.  

The script calculates the number of players in the class, their average number of offers, and lists the players who have more than 10 scholarship offers.  The end result includes quantitative data points that allow for recruiting classes to be compared for different schools, and/or for different years. 
