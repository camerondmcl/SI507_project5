import requests
import json

CACHE_FNAME = 'caching_file.json'
CSV_FNAME = 'articles.csv'

NYT_KEY = 'c709037f926e4214afaf19821be1c844'
GUARD_KEY = 'ec8a24f1-5161-47d2-b631-a32ead64a0c8'

class NYTArticle:
    #represents a NYT article
    def __init__(self, article_diction):
        #creates an NYTArticle object
        self.publication = 'The New York Times'
        self.headline = article_diction['headline']['main']
        if 'byline' in article_diction:
            try:
                self.author = '{} {}'.format(article_diction['byline']['person'][0]['firstname'], article_diction['byline']['person'][0]['lastname'][0] + article_diction['byline']['person'][0]['lastname'][1:].lower())
                #the .lower() is because NYT lists its authors with last names in all caps and I wanted consistency between publications
            except:
                if article_diction['byline']['original'] != None:
                    self.author = article_diction['byline']['original'][3:]
                    #this gets rid of the 'By ' before the name and only runs if the 'author' is listed as a news source like 'REUTERS' rather than a person's name
                else:
                    self.author = 'no author given'
        else:
            self.author = 'no author given'
        #his whole complicated bit above is to deal with articles that either have an empty 'byline' or no 'byline' section at all
        if 'pub_date' in article_diction:
            self.date = article_diction['pub_date'][:10]
        else:
            self.date = 'no date given'
        self.summary = article_diction['snippet']
        self.subject = 'none'
        for k in article_diction['keywords']:
            if k['name'] == 'subject':
                self.subject = k['value']
                break

    def title_length(self):
        #returns the number of words in the headline
        title_lst = self.headline.split(' ')
        for word in title_lst:
            if word == '–' or word == '|':
                title_lst.remove(word)
                #this part is because some headlines have the '–' or '|' which would otherwise be counted as a word
        return len(title_lst)

    def __str__(self):
        #returns class object information in string form for printing
        return 'Publication: {}. Article headline: "{}". Author: {}. Subject: {}. Date published: {}.'.format(self.publication, self.headline, self.author, self.subject, self.date)

class GuardArticle:
    #represents a Guardian article, all functions work basically the same way as the NYTArticle ones do
    def __init__(self, article_diction):
        self.publication = 'The Guardian'
        self.headline = article_diction['fields']['headline']
        self.author = article_diction['fields']['byline']
        self.date = article_diction['webPublicationDate'][:10]
        self.summary = article_diction['fields']['trailText']
        self.subject = article_diction['sectionId']

    def title_length(self):
        title_lst = self.headline.split(' ')
        for word in title_lst:
            if word == '–':
                title_lst.remove(word)
        return len(title_lst)

    def __str__(self):
        return 'Publication: {}. Article headline: "{}". Author: {}. Subject: {}. Date published: {}.'.format(self.publication, self.headline, self.author, self.subject, self.date)

def make_unique_ident(baseurl, params_dict, private_keys=['api-key']):
    #creates a unique identifier for caching, works the same way as code in textbook/problem sets/section exercises
    sorted_keys = sorted(list(params_dict.keys()))
    params = []
    for k in sorted_keys:
        if k not in private_keys:
            params.append('{}-{}'.format(k, params_dict[k]))
    #print(baseurl + '_'.join(params))
    return baseurl + '_'.join(params)

def get_data(baseurl, params_dict):
    #retrieves data from an API, prints out which API it is contacting, and returns the response's text object as a JSON-formatted dictionary
    response = requests.get(baseurl, params_dict)
    if baseurl == nyt_baseurl:
        print('-retrieving data from NYT API-')
    elif baseurl == guard_baseurl:
        print('-retrieving data from Guardian API-')
    return json.loads(response.text)

def cache_data(nyt_ident, nyt_data, guard_ident, guard_data):
    #adds all data and identifiers to the caching dictionary, JSON-formats it, and writes it to cache file (I did it this way using the main cache_diction rather than just adding the current search results to a cache_temp dicitonary so that it would always store results for all searches performed, including those done in past sessions)
    cache_diction[nyt_ident] = nyt_data
    cache_diction[guard_ident] = guard_data
    cache_json = json.dumps(cache_diction)
    f = open(CACHE_FNAME, 'w')
    f.write(cache_json)
    f.close()
    print('-caching data from both APIs-')

def nyt_check_cache(ident):
    #checks caching dicionary for NYT identifier; returns that data if it is there, returns False if not
    if ident in cache_diction:
        print('-retrieving cached NYT data-')
        return cache_diction[ident]
    else:
        print('-NYT data not in cache-')
        return False

def guard_check_cache(ident):
    #same as above but for Guardian (made separate functions for each API just to make testing easier)
    if ident in cache_diction:
        print('-retrieving cached Guardian data-')
        return cache_diction[ident]
    else:
        print('-Guardian data not in cache-')
        return False

def make_nyt_articles(nyt_data):
    #returns a list of NYTArticle objects from a dictionary of NYT data
    nyt_lst = []
    for article in nyt_data['response']['docs']:
        new_article = NYTArticle(article)
        nyt_lst.append(new_article)
    return nyt_lst

def make_guard_articles(guard_data):
    #returns a list of GuardArticle objects from a dictionary of Guardian data
    guard_lst = []
    for article in guard_data['response']['results']:
        new_article = GuardArticle(article)
        guard_lst.append(new_article)
    return guard_lst

def combine_lst(lst1, lst2):
    #combines two lists into a new list
    new_lst = []
    for item in lst1:
        new_lst.append(item)
    for item in lst2:
        new_lst.append(item)
    return new_lst

def csv_formatter(article):
    #takes an article object (works for either type) and returns the article's information formatted as a CSV string
    csv_str = '{},{},{},{},{},{},{}'.format(article.headline, article.author, article.date, article.subject, article.summary, article.publication, article.title_length())
    return csv_str

def make_csv(search_term, nyt_articles, guard_articles):
    #creates a new custom-named CSV file and writes the data from a single search to it
    print('-writing data to CSV file-')
    csv_header = 'Headline,Author,Date,Subject,Summary,Publication,Number of Words in Title'
    search_temp = search_term.split(' ')
    search_joined = '_'.join(search_temp)
    #above two lines are just for neater, space-less filenames
    csv_f = open('{}_{}'.format(search_joined, CSV_FNAME), 'w')
    csv_f.write(csv_header)
    csv_f.write('\n')
    all_articles = combine_lst(nyt_articles, guard_articles)
    for article in all_articles:
        csv_f.write(csv_formatter(article))
        csv_f.write('\n')
    csv_f.close()
    print('-CSV file successfully written-')

def avg_words(nyt_articles, guard_articles):
    #prints out the average number of words in headlines from each publication
    nyt_num_words = 0
    for article in nyt_articles:
        nyt_num_words += article.title_length()
        nyt_avg_words = float(nyt_num_words) / float(len(nyt_articles))
    guard_num_words = 0
    for article in guard_articles:
        guard_num_words += article.title_length()
        guard_avg_words = float(guard_num_words) / float(len(guard_articles))
    print('Average number of words in a New York Times headline: {}'.format(nyt_avg_words))
    print('Average number of words in a Guardian headline: {}'.format(guard_avg_words))
    return [nyt_avg_words, guard_avg_words]


def run_search(search_term):
    #runs a search on both APIs using search terms, caches the data, creates class instances from it, and calls functions to store it in a CSV file and print the average number of words in headlines from each publication; returns the average number of words as a list with NYT as item 0 and Guardian as item 1 for the sake of keeping track of average title lengths across multiple searches
    print('-running search on NYT and Guardian APIs with term "{}"-'.format(search_term))

    nyt_params = {}
    nyt_params['q'] = search_term
    nyt_params['api-key'] = NYT_KEY
    nyt_ident = make_unique_ident(nyt_baseurl, nyt_params)

    guard_params = {}
    guard_params['q'] = search_term
    guard_params['api-key'] = GUARD_KEY
    guard_params['page-size'] = 10
    guard_params['show-fields'] = 'all'
    guard_ident = make_unique_ident(guard_baseurl, guard_params)

    nyt_temp = nyt_check_cache(nyt_ident)
    guard_temp = guard_check_cache(guard_ident)
    #storing results of '_check_cache()' functions in temp variables so that they each only have to be called once
    if nyt_temp == False or guard_temp == False:
        nyt_data = get_data(nyt_baseurl, nyt_params)
        guard_data = get_data(guard_baseurl, guard_params)
        cache_data(nyt_ident, nyt_data, guard_ident, guard_data)
        #if the data is not cached, it retrieves the data from both apis, stores it in '_data' variables, and caches it
    elif nyt_temp != False and guard_temp != False:
        nyt_data = nyt_temp
        guard_data = guard_temp
        #if the data is already cached, it just stores the cached data in '_data' variables
        #originally I had additional elif statements here and a 'cache_one()' function (as opposed to 'cache_both()', which existed instead of 'cache_data()') for if one set of API data was cached but not the other to retrieve and cache only the missing data but I figured the way the program is set up there should never be a case where one set of data is cached but not the other so it would be much simpler to remove it
    #print(nyt_data)
    #print(guard_data)

    #test_nyt = NYTArticle(nyt_data['response']['docs'][0])
    #test_guard = GuardArticle(guard_data['response']['results'][0])
    #print(test_nyt)
    #print(test_guard)
    #print(test_nyt.title_length())
    #print(test_guard.title_length())

    nyt_articles = []
    nyt_articles = make_nyt_articles(nyt_data)
    guard_articles = []
    guard_articles = make_guard_articles(guard_data)
    #for item in nyt_articles:
    #    print(item)
    #for item in guard_articles:
    #    print(item)
    #print(csv_formatter(nyt_articles[0]))
    #print(csv_formatter(guard_articles[0]))
    make_csv(search_term, nyt_articles, guard_articles)
    return avg_words(nyt_articles, guard_articles)

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_diction = json.loads(cache_contents)
    cache_file.close()
    print('-cache file successfully opened-')
except:
    print('-no cache file exists-')
    cache_diction = {}
#I copied this code from the online textbook/section exercise, just added the print statement for testing

nyt_baseurl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
guard_baseurl = 'https://content.guardianapis.com/search'

search_term = input('-enter a search term:-\n')

avg_temp = []
avg_temp = run_search(search_term)
#print(avg_temp[0])
avg_so_far = [avg_temp[0], avg_temp[1]]
user_input = input('-run another search? Y / N-\n').lower()
while user_input != 'n':
    if user_input == 'y':
        search_term = input('-enter another search term:-\n')
        avg_temp = run_search(search_term)
        avg_so_far[0] += avg_temp[0]
        avg_so_far[1] += avg_temp[1]
        user_input = input('-run another search? Y / N-\n').lower()
    else:
        user_input = input('-invalid input, please enter "Y" or "N"-\n').lower()
print('-total average number of words in all NYT article headlines: {}-'.format(round(avg_so_far[0], 2)))
print('-total average number of words in all Guardian article headlines: {}-'.format(round(avg_so_far[1], 2)))
