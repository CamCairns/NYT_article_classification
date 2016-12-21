## Classifying Articles from the New York Times

A small project to demonstrate NLP and text classification using a corpus derived from the New York Times. The goal was to classify articles into one of five 'news desk' categories (Arts, Business, Obituaries, World, Sport) based on the stories headline and body text.

A longer writeup and discussion of results can be found on my website [INSERT LINK HERE]

This repo contains two separate directories:

* `generate_corpus`: contains code to generate the nyt article corpus using the NYT API.
* `classify_articles`: Self-contained classification script. Reads in the corpus, creates an 80:20 train/test split and applies a Naive Bayes model. Plots a confusion matrix and writes the 10 most dicriminating words for each article category.

### The NYT Article Search API

First thing you have to do is signup and register as a developer. API Keys are assigned by API, so make sure you specify the [Article Search API](http://developer.nytimes.com/docs/read/article_search_api_v2).

Once you have recieved an API key set it as environmntal variable `nyt_api_key` in your `.bash_profile`:

    export nyt_api_key=<YOUR API KEY>

Even before you register, you can use the NYT's handy API Console to interactively test your queries: http://developer.nytimes.com/io-docs

The [Article Search API](http://developer.nytimes.com/docs/read/article_search_api_v2) is pretty flexible; you can call it with no parameters except for your `api-key` and it will return (presumably) a list of articles, in reverse chronological order, starting from Sept. 18, 1851. However, it only returns 10 articles per request. And it won't let you paginate beyond a `page` parameter of `100` (i.e. you can't go to `page` 100000 to retrieve the 1,000,000th oldest Times article). To put it another way, you can only paginate through a maximum of 10,000 results, so you'll have to facet your search.

A lot more information about the article can be pulled out, but for the classication project we only need the title and body text.


