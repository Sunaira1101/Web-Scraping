import requests
from bs4 import BeautifulSoup
import csv

def read_article_urls_from_file(filename):
    with open(filename, 'r') as file:
        article_urls = [line.strip() for line in file if line.strip()]
    return article_urls

def scrape_bd_news_articles(article_urls):
    articles_info = []
    for article_url in article_urls:
        # Send a GET request to the article URL
        response = requests.get(article_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the article page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article title
            article_title_tag = soup.find('h2', class_='MbPT-')
            if article_title_tag:
                article_title = article_title_tag.text.strip()
            else:
                article_title = "Title Not Found"
            
            # Extract article text
            article_text = ""
            article_text_tags = soup.find_all('div', class_='story-element story-element-text') 
            for tag in article_text_tags:
                article_text += tag.text.strip() + "\n"
            
            # Extract article summary (if available)
            article_summary_tag = soup.find('h3', class_='U9-xA')
            if article_summary_tag:
                article_summary = article_summary_tag.text.strip()
            else:
                article_summary = "Summary Not Found"
            
            # Store extracted information in a dictionary
            article_info = {
                'title': article_title,
                'text': article_text,
                'summary': article_summary
            }
            
            # Append the article information to the list
            articles_info.append(article_info)
        else:
            print(f"Failed to retrieve article: {response.status_code}")

    return articles_info

# Example usage
if __name__ == "__main__":
    # Read article URLs from file
    article_urls = read_article_urls_from_file('article_urls_bdnews.txt')
    
    # Scrape the articles
    articles_info = scrape_bd_news_articles(article_urls)
    
    if articles_info:
        # Write the scraped data to a CSV file
        with open('article2_bdnews.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'text', 'summary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for article_info in articles_info:
                writer.writerow(article_info)

