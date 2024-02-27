import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import seaborn as sns

figure_size = (10, 6)
plt.rcParams['font.size'] = 16

def generate_sentiment_distribution(cleaned_df):
    sentiment_counts = cleaned_df['sentiment'].value_counts()
    return sentiment_counts

def plot_sentiment_distribution(sentiment_counts, filename):
    plt.figure(figsize=figure_size)
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140,
             explode=[0.1, 0.1, 0.1, 0.1],
             pctdistance=0.8,
             colors=sns.color_palette('Set2'))
    #plt.title('Overall Sentiment Distribution')
    plt.axis('equal')
    plt.legend(title='Sentiment')
    plt.savefig(filename)  # Save the chart as an image file

def generate_sentiment_trends(dataframe):
    dataframe['dateAdded'] = pd.to_datetime(dataframe['dateAdded'])
    dataframe['sentiment_numeric'] = dataframe['sentiment'].apply(convert_sentiment_to_numeric)
    sentiment_trends = dataframe.groupby(dataframe['dateAdded'].dt.date)['sentiment_numeric'].mean()
    return sentiment_trends

def plot_sentiment_trends(sentiment_trends, chart_image_path):
    plt.figure(figsize=figure_size)
    plt.plot(sentiment_trends.index, sentiment_trends.values, marker='o', linestyle='-')
    #plt.title('Sentiment Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chart_image_path)

def convert_sentiment_to_numeric(sentiment):
    if sentiment == 'positive':
        return 1
    elif sentiment == 'negative':
        return -1
    elif sentiment == 'neutral':
        return 0
    elif sentiment == 'mixed':
        return 0  # TODO: handle'mixed' differently if needed
    else:
        return None
    
def generate_sentiment_distribution_by_category(dataframe):
    # Group by category columns and sentiment, then count occurrences
    sentiment_distribution = dataframe.groupby(dataframe.filter(like='categories_').columns.tolist() + ['sentiment']).size().unstack(fill_value=0)
    return sentiment_distribution

def plot_sentiment_distribution_by_category(sentiment_distribution, chart_image_path):
    # Plot the sentiment distribution for each category
    plt.figure(figsize=figure_size)
    sentiment_distribution.plot(kind='bar', stacked=True, ax=plt.gca())
    #plt.title('Sentiment Distribution Across Different Product Categories')
    plt.xlabel('Product Categories')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    plt.savefig(chart_image_path)

def generate_word_cloud(dataframe, sentiment):
    # Filter dataframe based on sentiment
    sentiment_df = dataframe[dataframe['sentiment'] == sentiment]    
    # Combine text from all reviews
    text = ' '.join(sentiment_df['reviews.text'])    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    return wordcloud

def plot_word_cloud(wordcloud, chart_image_path):
    plt.figure(figsize=figure_size)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(chart_image_path)

def plot_sentiment_score_distribution(sentiment_scores, chart_image_path):
    # Plot the distribution of sentiment scores using a histogram or density plot
    plt.figure(figsize=figure_size)
    plt.hist(sentiment_scores, bins=10, density=True, 
             color='skyblue',
             alpha=0.7)
    #plt.title('Sentiment Score Distribution')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Density')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chart_image_path)

def plot_sentiment_heatmap(sentiment_df, chart_image_path):
    # Exclude non-numeric columns (e.g., text reviews)
    numeric_df = sentiment_df.select_dtypes(include=['number'])
    # Calculate correlation matrix
    correlation_matrix = numeric_df.corr()
    # Create heatmap
    plt.figure(figsize=figure_size)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    #plt.title('Correlation Heatmap of Sentiment Scores and Other Variables')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(chart_image_path)