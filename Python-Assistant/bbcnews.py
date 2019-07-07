import requests
import  random
import  urllib.request
import  textwrap
import  json

def searchbooks(user_input):
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q="
    with urllib.request.urlopen(base_api_link + user_input) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
    return obj["items"][0]
    # volume_info = obj["items"][1]
    # print(obj["totalItems"],volume_info["id"])
    # authors = obj["items"][1]["volumeInfo"]["authors"]
    #
    # # displays title, summary, author, domain, page count and language
    # print("\nTitle:", volume_info["volumeInfo"]["title"])
    # print("\nSummary:\n")
    # print(textwrap.fill(volume_info["searchInfo"]["textSnippet"], width=65))
    # print("\nAuthor(s):", ",".join(authors))
    # print("\nPublic Domain:", volume_info["accessInfo"]["publicDomain"])
    # print("\nPage count:", volume_info["volumeInfo"]["pageCount"])
    # print("\nLanguage:", volume_info["volumeInfo"]["language"])
    # print("\n***")

def NewsFromBBC():
    # BBC news api
    newschannels=["cnn","espn","espn-cric-info","national-geographic","the-hindu","the-times-of-india","the-new-york-times","bbc-news"]
    main_url = " https://newsapi.org/v1/articles?source="+random.choice(newschannels)+"&sortBy=top&apiKey=4dbc17e007ab436fb66416009dfb59a8"

    # fetching data in json format
    open_bbc_page = requests.get(main_url).json()

    # getting all articles in a string article
    article = open_bbc_page["articles"]

    # empty list which will
    # contain all trending news
    # results = []
    #
    # for ar in article:
    #     results.append(ar["title"])
    return  article

def getweather(city_name):
    # Enter your API key here
    api_key = "Your Api key"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # # print following values
        # print(" Temperature (in kelvin unit) = " +
        #       str(current_temperature) +
        #       "\n atmospheric pressure (in hPa unit) = " +
        #       str(current_pressure) +
        #       "\n humidity (in percentage) = " +
        #       str(current_humidiy) +
        #       "\n description = " +
        #       str(weather_description))
        return " Temperature = " + str('%.2f'%(current_temperature-273.15)) +" degree C\n Atmospheric pressure (in hPa unit) = " +str(current_pressure) +"\n Humidity = " +str(current_humidiy) +"%\n Description = " +str(weather_description+"\nCity = "+city_name)
    else:
        return "N"
#searchbooks()
