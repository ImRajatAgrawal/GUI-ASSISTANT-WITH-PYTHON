## PROJECT NAME : 
A GUI Assistant with Python

## AIM AND OBJECTIVES : 
To Automate the various tasks that are performed frequently by a user with the help of a responsive GUI and                             embedded python frameworks and also develop a good understanding and interest in trending python technologies.

## BENEFITS :
 1. Ease of Access
 2. Entertainment
 3. Developing Advanced python programming skills.
 4. Broaden the concept of artificial intelligence.
 
 ## IMPLEMENTATION : 
 Initial Phase is GUI Development Using Tkinter.
 The GUI root window consists of a TabControl Panel with 7 Tabs -
 - Home
 - Dictionary
 - Translate
 - BookStore
 - Voice Assistant
 - Music 
 - Images
 
 ## Home Tab :
This tab shows general information like current-time, News Headlines and weather Forecast. It also provides the functionality of getting weather forecast for different places in the world. Keeping Entertainment in mind there is notification facility which updates the user with live cricket scores in small intervals of time.
 
This is how the Homepage tab looks like -
<p align="center"> <img src="/Python-Assistant/screenshots/homepage2.JPG"> </p>

**Functionalities Explained** :

The news headlines are fetched from [https://newsapi.org](https://newsapi.org) from different news channels like bbc-news, cnn, times of india etc.

The weather forcast information is gathered from [http://api.openweathermap.org](http://api.openweathermap.org).

The live cricket score notification is generated with the help of **win10toast** and **pycricbuzz** modules.

## Dictionary Tab :
An interactive dictionary in python providing meaning of a plethora of words. Added a functionality for suggesting the user with similar words if user has entered a word that does not exist in the dictionary. 

<p align="center"><img src="/Python-Assistant/screenshots/dictionary.JPG"></p>

The dictionary data is contained in the json file **data.json** from where the meaning is fetched by passing the word as key.

## Translate Tab :
A Language translator for translating english sentences into different languages provided in the list.
<p align="center"><img src="/Python-Assistant/screenshots/translate.JPG"></p>
It is implemented using the translate module available in python.

## Bookstore Tab :
A Bookstore designed with the help of tkinter and sqlite3 database functionality . It allows you to add details about books that you read frequently into the database so that you can search about them whenever required. Also a online book search functionality is provided which helps the user to search for a particular book online using its title.

<p align="center"><img src="/Python-Assistant/screenshots/bookstore.JPG"></p>
The online searching of books is performed with the help of **googlebooksapi** which provides results in json format. 
