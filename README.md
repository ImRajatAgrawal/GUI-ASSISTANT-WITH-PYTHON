## PROJECT NAME : 
A GUI Assistant with Python

# AIM AND OBJECTIVES : 
To Automate the various tasks that are performed frequently by a user with the help of a responsive GUI and                             embedded python frameworks and also develop a good understanding and interest in trending python technologies.

# BENEFITS :
 1. Ease of Access
 2. Entertainment
 3. Developing Advanced python programming skills.
 4. Broaden the concept of artificial intelligence.
 
 # IMPLEMENTATION : 
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

## Voice Assistant Tab:
An interactive Voice Assistant named 'JARVIS' to whom you can ask questions and also provide commands to perform tasks like searching for something, opening tools like youtube, google etc. some more AI functionalities are like whenever you open the voice assistant tab it greets you with a message and also you can chat by asking basic questions.
<p align="center"><img src="/Python-Assistant/screenshots/voiceassistant.JPG"></p>

The interaction functionality is implemented using the **speech_recognition** module and the voice of 'JARVIS' is chosen from voice property available in the pyttsx3 library. The search results are fetched from the options available like google,amazon-books,youtube etc. Apart from this you can ask general knowledge questions whose results are fetched from **WolframeAplha** module in python. 

## Music Tab :
A simple music player made using tkinter for entertainment purpose. It lets you to add music tracks to your playlist and play them whenever you want. Some more basic functionalities like play,pause,rewind,stop, adjust music volume are also provided.

<p align="center"><img src="/Python-Assistant/screenshots/musicplayer.JPG"></p>

The sound and other music player functionalities are implemented with the help of **pygame mixer** module and file manipulation techniques in python respectively.

## Images Tab :
With the emergance of computer vision python has made it very easy to gain high level understanding from digital images or videos.
The Image Tab provides functionalities to perform different operations on images so that they can be further used in data analysis.
The different options that are provided are - detecting edges,blurring an image , extract text , transposing,creating thumbnails, resizing etc. 

An Additional functionality is provided for downloading images from web. you can just type something and you will find that related images are downloaded in the specified output directory.

This is implemented using the google_images_download module in python. 

The following arguments are provided as a dictionary to the response object.

arguments ={
             "keywords": self.downloadimg.get(),
             "format": "jpg",
             "limit": 4,
             "print_urls": True,
             "size": "medium",
             "aspect_ratio": "panoramic",
             "output_directory": r"C:\Users\hp\Desktop\mynewimages",
             "safe_search": True,
             "help": True
            
            }

