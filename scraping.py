
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),

        "hemispheres": hemispheres(browser), 
        "ce_hemisphere": ce_hemisphere(browser), 
        "sch_hemisphere": sch_hemisphere(browser), 
        "sy_m_hemisphere": sy_m_hemisphere(browser),
        "va_m_hemisphere": va_m_hemisphere(browser), 
        
    }

    # Stop webdriver and return data
    #browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres(browser):

    ce_hem_img_url = ce_hemisphere(browser)
    sch_hem_img_url = sch_hemisphere(browser)
    sy_m_hem_img_url = sy_m_hemisphere(browser)
    va_m_hem_img_url = va_m_hemisphere(browser)
    
    hemispheres = [{"Cerberus Hemisphere Enhanced": ce_hem_img_url}, {"Schiaparelli Hemisphere Enhanced": sch_hem_img_url}, {"Syrtis Major Hemisphere Enhanced" : sy_m_hem_img_url}, {"Valles Marineris Hemisphere Enhanced" : va_m_hem_img_url}]
    return hemispheres
    

def ce_hemisphere(browser):

    #Visit URL
    url = 'https://marshemispheres.com/images/full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        ce_img_url = img_soup.select_one('body img').get("src")

    except AttributeError:
        return None

    return ce_img_url

def sch_hemisphere(browser):

    #Visit URL
    url = 'https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        sch_img_url = img_soup.select_one('body img').get('src')

    except AttributeError:
        return None

    return sch_img_url

def sy_m_hemisphere(browser):

    #Visit URL
    url = 'https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        sy_m_img_url = img_soup.select_one('body img').get('src')

    except AttributeError:
        return None

    return sy_m_img_url

def va_m_hemisphere(browser):

    #Visit URL
    url = 'https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        va_m_img_url = img_soup.select_one('body img').get('src')

    except AttributeError:
        return None

    return va_m_img_url



browser.quit()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
