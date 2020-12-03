# Nature Article Recommender

Nature, the world's leading multidisciplinary science journal, is an amazing resource for those in scientific fields or with STEM backgrounds.  Unfortunately, because scientific writing often reflects the precision and rigor demanded by the research process, the language tends to be esoteric and difficult for the layperson to learn from.  

Now more than ever it is important for everyone to stay current on events in the scientific world and sift through the minefield of misinformation.  This project is aimed at building a content-based recommender system that allows people to get up to date research relating to their topic of interest, with ideally as little complexity as possible.

[Check out my app](https://tranquil-retreat-91817.herokuapp.com) and feel free to provide any feedback!

### Data Used

- Scraped 30,000 news articles from [Nature](https://www.nature.com) dating back to 1998. 
- Built a custom NLP pipeline with corpus-specific stop words to process article text

### Tools Used

- Python
- BeautifulSoup: Web scraping
- NumPy and Pandas: Data structures
- NLTK and SpaCy: text preprocessing
- Scikit-learn: TF-IDF vectorizer
- Non-Negative Matrix Factorization: Topic Modeling
- Dash/Plotly: Interactive web app
- Heroku: App deployment
