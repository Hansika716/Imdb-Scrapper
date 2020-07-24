from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
from IPython.core.display import clear_output
from warnings import warn
import csv

#lists to store the scrapped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

#preparing the monitoring of the loop
start_time = time()
requests = 0

#we need to make 72 requests - requesting 4 pages of years between 2000-2017
#hence we ll be changing url again n again for getting right data
pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000,2018)]

#for every year in the interval 2000-2017
for year_url in years_url:

    #for every page in interval 1 to 4
    for page in pages:

        #make get request
        response = get('https://www.imdb.com/search/title/?release_date=' + year_url + '&sort=num_votes,desc&page='+ page)

        #pause loop
        sleep(randint(8,15))

        #Monitor the requests - by keeping frequencies
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency{} requests/s'.format(requests,requests/elapsed_time))
        clear_output(wait = True)

        #throw a warning for non-200 status code
        if response.status_code != 200:
            warn('Request:{}; Status code: {}'.format(requests,response.staus_code))

        #break loop if no. of requests is greater than 72
        if requests > 72:
            warn('Number of requests was greater than expected')
            break

        #parse the content with beautifulSoup
        html_soup = BeautifulSoup(response.text, 'html.parser')

        #select all 50 movie containers with BeautifulSoup
        movie_containers = html_soup.find_all('div', class_= 'lister-item mode-advanced')

        #for every movie of these 50
        for container in movie_containers:
            #if movie has metascore , then extract
            if container.find('div', class_ = 'ratings-metascore') is not None:
            #name
                name = container.h3.a.text
                names.append(name)
            # The year
                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)
            # The IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)
            # The Metascore
                m_score = container.find('span', class_ = 'metascore').text
                metascores.append(int(m_score))
            # The number of votes
                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))

#making a dictionary of fields to be passed to data frames
Data = {'movies':names, 'year':years, 'imdb': imdb_ratings, 'metascore':metascores, 'votes':votes}
movie_ratings = pd.DataFrame(Data)
#converting string year to integer year
movie_ratings.loc[:,'year']  = movie_ratings['year'].str[-5:-1].astype(int)
#adding normalised imdb for adding in same graph
movie_ratings['n_imdb'] = movie_ratings['imdb']*10
#converting to csv file
movie_ratings.to_csv('movies_data.csv')
print(movie_ratings.info())
