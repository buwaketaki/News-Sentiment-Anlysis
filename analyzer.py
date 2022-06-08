from turtle import title, width
import requests
import boto3
from bs4 import BeautifulSoup
from tqdm import tqdm
import plotly
import plotly.express as px
import json

comprehend = boto3.client(service_name='comprehend', 
            region_name='us-west-2', 
            aws_access_key_id='ADD YOUR AWS ACCESS KEY',
            aws_secret_access_key= 'ADD YOUR AWS SECRET KEY')

domain = "https://www.aljazeera.com"

r1 = requests.get('https://www.aljazeera.com/where/mozambique/')
coverpage = r1.content
soup1 = BeautifulSoup(coverpage, 'html.parser')

news_list = soup1.find_all('article', attrs={'class': lambda e: e.startswith('gc u-clickable-card') if e else False}) 

links=[]
article_dict = {}

for n in news_list:
    links.append(n.find('a')['href'])

for link in tqdm(links[:11]):
    if len(article_dict) == 10:
        break
    wblink = domain + link
    article = requests.get(wblink)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    article = soup_article.find('div', class_="wysiwyg wysiwyg--all-content css-1ck9wyi")
    if article is not None:
        ptags = article.find_all('p')
        text = ""
        for i in ptags:
            text = text+ i.get_text()
        response = comprehend.detect_sentiment(Text=text[:4000], LanguageCode='en')
        article_dict[wblink] = {'text': text,
        'analysis': {'Sentiment':  response['Sentiment'], 'SentimentScore': response['SentimentScore']}}

json_object = json.dumps(article_dict, indent = 4)
with open("news.json", "w") as outfile:
    outfile.write(json_object)

# bar graph for each news
bar_graph_data=[]
labels = [a.split("/")[-1][:30]+"..." for a in article_dict.keys()]
senti_dict = {}
for senti in ['Positive','Negative','Neutral','Mixed']:
    for a in article_dict:
        if senti in senti_dict:
            senti_dict[senti].append(article_dict[a]['analysis']['SentimentScore'][senti])
        else:
            senti_dict[senti] =[article_dict[a]['analysis']['SentimentScore'][senti]]
for s in senti_dict:
    bar_graph_data.append(plotly.graph_objs.Bar(x=labels,
        y=list(senti_dict[s]),
        name=s))

layout = plotly.graph_objs.Layout(
    barmode='stack',
    margin=plotly.graph_objs.layout.Margin(
       b = 20
   )
)
fig = plotly.graph_objs.Figure(data=bar_graph_data, layout=layout)
fig.update_traces(width=0.3)
plotly.offline.plot(fig)
