Design:
* User uploads the csv file containing customer feedback.
* Python flask app is responsible for reading the input data, cleansing, and preprocessing (removing empty rows, duplicates, column formatting etc.) for sentiment analysis.
* After cleanup, the data is sent to Azure AI service endpoint for sentiment analysis.
* Flask app receives the analyzed data and generates below visualizations on the webpage:
 o Overall sentiment distribution: Pie chart
 o Sentiment trends over time: Line chart 
 o Common words in negative and positive reviews: Word cloud
 o Sentiment Score Distribution: Histogram
 o Sentiment Distribution: Heatmap

Architecture diagram:
![image](https://github.com/sudiptomukherjee/python-azureai-sentiment-analysis-visualization/assets/12342105/22b2c1af-911b-4c38-bdff-5fb158437816)

Screenshots:
![image](https://github.com/sudiptomukherjee/python-azureai-sentiment-analysis-visualization/assets/12342105/1072d605-6fa1-43da-af00-2fe08e40a6f9)

![image](https://github.com/sudiptomukherjee/python-azureai-sentiment-analysis-visualization/assets/12342105/67eb4602-6b3c-4007-8b1c-c0570ed783ea)
