from matplotlib import pyplot as plt
import pandas as pd

plt.style.use('ggplot')

data = pd.read_csv('movies_data.csv')
imdb = data['imdb']#it sets it equal to entire imdb column
metascore = data['metascore']
n_imdb = data['n_imdb']

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))

ax1, ax2, ax3 = fig.axes

ax1.hist(imdb, bins = 10, range = (0,10)) #bin range = 1
ax1.set_title('IMDB rating')

ax2.hist(metascore, bins = 10, range = (0,100)) #bin range = 10
ax2.set_title('Metascore rating')

ax3.hist(n_imdb, bins=10, range=(0,100), histtype = 'step', label='n_imdb')
ax3.hist(metascore, bins=10, range=(0,100), histtype = 'step', label='metascore')
ax3.legend(loc = 'upper left')
ax3.set_title('The two Normalised Distributions')
plt.savefig('final_plot.png')
plt.show()
