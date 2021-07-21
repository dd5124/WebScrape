from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time

# store data
base_url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="
number = []
title = []
year = []
length = []
genre = []
director = []
rating = []
pages = np.arange(1, 902, 100)

# loop through pages
for page in pages:
    response = requests.get(base_url + str(page))
    webPage = response.content
    movie = BeautifulSoup(webPage, 'html.parser')
    movies = movie.findAll('div', class_='lister-item mode-advanced')
    
    # wait before doing another request
    time.sleep(5)
    
    # loop through the movies
    for movie in movies:
        content = movie.find('div', class_='lister-item-content')
        
        # get number rank
        number.append(content.find('span', class_='lister-item-index').text.replace('.',''))
        
        # get title
        title.append(content.h3.a.text)
        
        # get year
        year.append(content.find('span', class_='lister-item-year').text.replace('(','').replace(')',''))
        
        # get length
        length.append(content.find('span', class_='runtime').text.replace(' min',''))
        
        # get genre
        genre.append(content.find('span', class_='genre').text.replace('\n','').replace(' ',''))
        
        # get director
        staff = content.findAll('p', recursive=False)[2]
        director.append(staff.findAll('a')[0].text)
        
        # get rating
        rating.append(content.find('div', class_='inline-block ratings-imdb-rating').attrs.get("data-value", None))

# Store ingredient information as pandas dataframe        
movies_df = pd.DataFrame({
'rank': number,
'title': title,
'year': year,
'length': length,
'genre': genre,
'director': director,
'rating': rating
})

# Convert the movie dataframe to 'movies.csv' file
movies_df.to_csv(r'movies.csv', index = False, header=True)