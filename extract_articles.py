import requests
from bs4 import BeautifulSoup
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

nltk.download('punkt')
nltk.download('stopwords')

# Function to preprocess text data
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Text Cleaning
    clean_text = re.sub(r'[^\w\s]', '', ' '.join(filtered_tokens))
    
    return clean_text

# Function to extract articles from Dawn.com
def extract_articles_dawn():
    url = "https://www.dawn.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")
    titles = []
    descriptions = []
    for article in articles:
        # Find the title
        title_element = article.find("h2")
        if title_element:
            titles.append(title_element.text.strip())
        else:
            titles.append("Title not found")

        # Find the description
        description_element = article.find("div", class_="story__excerpt")
        if description_element and description_element.text.strip():
            descriptions.append(description_element.text.strip())
        else:
            descriptions.append("Description not found")

    # Preprocess descriptions
    preprocessed_descriptions = [preprocess_text(description) for description in descriptions]

    return titles, preprocessed_descriptions

# Function to extract articles from BBC.com
def extract_articles_bbc():
    url = "https://www.bbc.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")
    titles = []
    descriptions = []
    for article in articles:
        # Find the title
        title_element = article.find("h3")
        if title_element and title_element.text.strip():
            titles.append(title_element.text.strip())
        else:
            titles.append("Title not found")

        # Find the description
        description_element = article.find("p", class_="promo__summary")
        if description_element and description_element.text.strip():
            descriptions.append(description_element.text.strip())
        else:
            descriptions.append("Description not found")

    # Preprocess descriptions
    preprocessed_descriptions = [preprocess_text(description) for description in descriptions]

    return titles, preprocessed_descriptions

# Function to save articles to CSV
# Function to save articles to CSV
def save_to_csv(titles, descriptions, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Description'])
        
        if titles and descriptions:  # Check if both lists are not empty
            for title, description in zip(titles, descriptions):
                writer.writerow([title, description])
        else:
            print("No articles found to save.")


if __name__ == "__main__":
    # Extract articles from Dawn.com
    dawn_titles, dawn_descriptions = extract_articles_dawn()
    # Extract articles from BBC.com
    bbc_titles, bbc_descriptions = extract_articles_bbc()

    # Save Dawn.com articles to CSV
    save_to_csv(dawn_titles, dawn_descriptions, 'dawn_articles.csv')

    # Save BBC.com articles to CSV
    save_to_csv(bbc_titles, bbc_descriptions, 'bbc_articles.csv')

    print("Articles saved to CSV files.")
