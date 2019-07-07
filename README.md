## PROJECT NAME : A GUI Assistant with Python

## AIM AND OBJECTIVES : To Automate the various tasks that are performed frequently by a user with the help of a responsive GUI and                                embedded python frameworks and also develop a good understanding and interest in trending python technologies.

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
 
This is how the Homepage tab looks -
<p align="center"> <img src="/Python-Assistant/screenshots/homepage2.JPG"> </p>

**Functionalities Explained** :

The news headlines are fetched from [https://newsapi.org](https://newsapi.org) from different news channels like bbc-news, cnn, times-of-india etc.
The weather forcast information is gathered from [http://api.openweathermap.org](http://api.openweathermap.org).
The live cricket score notification is generated with the help of **win10toast** and **pycricbuzz** modules.

**
