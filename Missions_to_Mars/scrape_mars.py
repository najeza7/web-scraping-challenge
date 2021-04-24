# Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    
    ########## NASA MARS NEWS #############
    # URL of page to be scraped
    url_news= 'https://redplanetscience.com/'
    browser.visit(url_news)

    # HTML object
    html_news = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_news = bs(html_news, 'html.parser')
    # Look for all the 'div's' that contain the news
    results = soup_news.find_all('div', class_='list_text')

    # Create empty lists to store what we need
    news_title = []
    news_p = []

    # Loop to find the title and summary of each news
    for result in results:
        title = result.find('div', class_='content_title').text
        p = result.find('div', class_='article_teaser_body').text
        news_title.append(title)
        news_p.append(p)

    
    ########## JPL MARS SPACE IMAGES #############

    # URL of page to be scraped
    fi_url = 'https://spaceimages-mars.com/'

    browser.visit(fi_url)

    # HTML object
    html_fi = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_fi = bs(html_fi, 'html.parser')

    # Look for the image we want
    images = soup_fi.find_all('img', class_= 'headerimage fade-in')

    # Get the source of the image
    fi_url_2 = images[0]['src']

    # Create the complete url
    featured_image_url = fi_url + fi_url_2

    
    ########## NASA  FACTS #############

    # URL of page to be scraped
    mfacts_url = 'https://galaxyfacts-mars.com/'

    # Extract the tables of the url with pandas
    tables = pd.read_html(mfacts_url)

    # Get the table we want 
    mars_facts = tables[0]

    # Change the names of the columns
    mars_facts.columns = ['Description', 'Mars', 'Earth']

    # Change the index of the table to Description
    mars_facts.set_index('Description')

    # Convert the table to html
    html_mars_table = mars_facts.to_html()

    
    ########## MARS HEMISPHERES #############

    # URL of page to be scraped
    h_url = 'https://marshemispheres.com/'
    browser.visit(h_url)

    # HTML object
    html_h = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_h = bs(html_h, 'html.parser')

    # Find all the 'div's' that contain the information we need
    hemispheres = soup_h.find_all('div', class_='description')

    # Create an empty list to save the information
    hemisphere_images_urls = []

    # Loop to obtain the information of each hemisphere 
    for hemisphere in hemispheres:
        h3 = hemisphere.find('h3')
        ti = h3.text
        ti = ti.split(sep = 'Hemisphere')
        title = ti[0]+'Hemisphere'
        link = hemisphere.find('a')
        href = link['href']
        browser.visit(h_url + href)
        html_h2 = browser.html
        soup_h2 = bs(html_h2, 'html.parser')
        img_url = soup_h2.find_all('img', class_='wide-image')[0]['src']
        hemisphere_images_urls.append({'title':title, 'img_url': h_url+img_url })
    
    scraped_data = {
        'news_title' : news_title,
        'news_p' : news_p,
        'featured_image_url' : featured_image_url,
        'html_mars_table' : html_mars_table,
        'hemisphere images_urls' : hemisphere_images_urls,
    }

    # Close browser
    browser.quit()

    return scraped_data