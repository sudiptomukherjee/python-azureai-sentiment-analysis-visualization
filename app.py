from flask import Flask, render_template, request, redirect, url_for
import pandas as pd, os, io
import preprocess, sentiment_analysis, visualization

app = Flask(__name__)

@app.route('/')
def upload_form():
    print ('inside upload_form')
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file_post():
    # Check if a file was uploaded
    print('inside upload_file_post')

    if 'file' not in request.files:
        print('No file uploaded')  # Debugging
        return render_template('upload.html', message='No file uploaded')

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        print('No file selected')  # Debugging
        return render_template('upload.html', message='No file selected')

    # Check if the file is a CSV
    if file.filename.endswith('.csv'):
        # Read the contents of the file
        file_contents = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        # Step 1 - Read the CSV file 
        # considering only specific columns
        df = pd.read_csv(file_contents, usecols=['reviews.rating', 'reviews.title', 'reviews.text', 'dateAdded', 'categories'])
        # Debugging: Print the contents of the DataFrame
        print('Raw DataFrame:')
        print(df)

        # Step 2 - Clean and preprocess 
        # Call the clean_data function from preprocess.py
        cleaned_df = preprocess.clean_data(df)        
        # Debugging: Print the first few rows of the cleaned DataFrame
        print('Cleaned DataFrame:')
        print(cleaned_df)

        # Step 3 - Sentiment analysis
        # Extract text for sentiment analysis
        texts = cleaned_df['reviews.text'].tolist()        
        # Analyze sentiment using Azure Text Analytics
        sentiment_scores = sentiment_analysis.analyze_sentiment_azure(texts)        
        # Combine sentiment scores with cleaned DataFrame
        cleaned_df['sentiment'] = sentiment_scores
        # Debugging: Print the first few rows of the analyzed DataFrame
        print('Analyzed DataFrame:')
        print(cleaned_df)

        # Step 4 - Visualizations
        # a. Generate sentiment distributions chart
        sentiment_counts = visualization.generate_sentiment_distribution(cleaned_df)
        chart_sentiment_distributions = 'sentiment_distribution_chart.png'
        chart_sentiment_distributions_path = os.path.join(os.path.dirname(__file__), f'static\{chart_sentiment_distributions}')
        visualization.plot_sentiment_distribution(sentiment_counts, chart_sentiment_distributions_path)
        # b. Generate sentiment trends chart
        sentiment_trends = visualization.generate_sentiment_trends(cleaned_df)
        chart_sentiment_trends = 'sentiment_trends_chart.png'
        chart_sentiment_trends_path = os.path.join(os.path.dirname(__file__), f'static\{chart_sentiment_trends}')
        visualization.plot_sentiment_trends(sentiment_trends, chart_sentiment_trends_path)
        # c. Generate sentiment distribution by category chart
        category_sentiment_counts = visualization.generate_sentiment_distribution_by_category(cleaned_df)
        chart_sentiment_by_category = 'category_sentiment_distribution_chart.png'
        chart_sentiment_by_category_path = os.path.join(os.path.dirname(__file__), f'static\{chart_sentiment_by_category}')
        visualization.plot_sentiment_distribution_by_category(category_sentiment_counts, chart_sentiment_by_category_path)
        # d1. Generate worldclouds - negative
        wodcloud_negative = visualization.generate_word_cloud(cleaned_df, 'negative')
        chart_wordcloud_negative = 'wordcloud_negative_chart.png'
        chart_wordcloud_negative_path = os.path.join(os.path.dirname(__file__), f'static\{chart_wordcloud_negative}')
        visualization.plot_word_cloud(wodcloud_negative, chart_wordcloud_negative_path)
        # d2. Generate worldclouds - positive
        wodcloud_positive = visualization.generate_word_cloud(cleaned_df, 'positive')
        chart_wordcloud_positive = 'wordcloud_positive_chart.png'
        chart_wordcloud_positive_path = os.path.join(os.path.dirname(__file__), f'static\{chart_wordcloud_positive}')
        visualization.plot_word_cloud(wodcloud_positive, chart_wordcloud_positive_path)
        # e. Generate Sentiment score distribution
        sentiment_scores = cleaned_df['sentiment']
        chart_sentiment_scores = 'sentiment_scores_distribution_chart.png'
        chart_sentiment_scores_path = os.path.join(os.path.dirname(__file__), f'static\{chart_sentiment_scores}')
        visualization.plot_sentiment_score_distribution(sentiment_scores, chart_sentiment_scores_path)
        # f. Generate Sentiment heatmap
        chart_sentiment_heatmap = 'sentiment_heatmap_chart.png'
        chart_sentiment_heatmap_path = os.path.join(os.path.dirname(__file__), f'static\{chart_sentiment_heatmap}')
        visualization.plot_sentiment_heatmap(cleaned_df, chart_sentiment_heatmap_path)

        # pass chart data to result page
        return render_template('result.html', 
                               filename=file.filename, 
                               chart_sentiment_distributions=chart_sentiment_distributions, 
                               chart_sentiment_trends=chart_sentiment_trends, 
                               chart_sentiment_by_category=chart_sentiment_by_category,
                               chart_wordcloud_negative=chart_wordcloud_negative,
                               chart_wordcloud_positive=chart_wordcloud_positive,
                               chart_sentiment_scores=chart_sentiment_scores,
                               chart_sentiment_heatmap=chart_sentiment_heatmap)
    else:
        return render_template('upload.html', message='Invalid file format. Please upload a CSV file')

@app.route('/results/<filename>')
def show_results(filename):
    print ('inside show_results')
    # Logic to process the uploaded file and display results
    return render_template('result.html', filename=filename, message='File processed successfully')

if __name__ == '__main__':
    app.run(debug=True)
