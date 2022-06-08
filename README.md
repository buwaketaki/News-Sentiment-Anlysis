# News-Sentiment-Anlysis

### Steps to run the project
1. Clone "main" branch
2. Move into root directory and open the terminal.
3. Execute - ```pip3 install -r requirements.txt``` to install all the required packages. 
4. This project uses Amazom Comprehend DetectSentiment API to predict the sentiments of the articles. To use this you require AWS ACCESS KEY and AWS SECRET ACCESS KEY.
5. In the terminal, run ```python3 analyzer.py```

### Summary of the project files
#### **news.json**
1. File contains the URL of the 10 recent articles extracted from the https://www.aljazeera.com/where/mozambique/ website, , the news text and result of the sentiment analysis performed on these articles. 
2. Attributes: <br />
   **url** - URL of the article <br />
   **contexttent** - Content of the article extracted using beautifulsoup python library. <br />
   **SentimentScore** - Sentiment Score predicted by the Sentiment Analysis model. [Range: 0 to 1 ] <br />
   **Sentiment** - Based on the predicted score, article is categorized into "Positive", "Negative", "Mixed" and "Neutral" sentiments.


#### **analyzer.py**
1. This is the main file which has the code to - perform the web scrapping using beautifulsoup, show the progress using tqdm,  predict the sentiment of the extracted articles and visualize the result of sentiment detection using plotly.

#### **Results Folder**
1. The folder contains the visualization of the Bar Chart showing the result of sentiment analysis. Each articles is shown with its sentiment score and categorization.