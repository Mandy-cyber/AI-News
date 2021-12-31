from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sqlite3

#----------------------------------------------------------------------------------------------------#
#SETTING UP DATABASE STUFF
#Connection and cursor
conn = sqlite3.connect('listofnews.db')
cursor = conn.cursor()

#Create Table
createTable = """CREATE TABLE IF NOT EXISTS
news(id INTEGER PRIMARY KEY autoincrement, newsTitle TEXT, newsLink TEXT)"""
cursor.execute(createTable)

#----------------------------------------------------------------------------------------------------#
#SETTING UP BROWSER
#headless mode + stop with the annoying output
chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
chrome_options.add_argument("--log-level=3")
#going to google and finding searchbar
browser.get("https://www.google.com")
searchbar = browser.find_element_by_name("q")
searchbar.click()
#just doing this part so we can go to the news page one time and do all searching from that page
searchbar.send_keys("news")
searchbar.send_keys(Keys.RETURN)
news_page = browser.find_element_by_xpath("""//*[@id="hdtb-msb"]/div[1]/div/div[4]/a""")
news_page.click()

#----------------------------------------------------------------------------------------------------#
#CATEGORIES TO SEARCH FOR NEWS IN
#will come back later and reword some of these category names for more relevant results
categories = ["Sports", "Military & War", "Weather", "Product Design", "Ethics", "Development", "Gaming", "Healthcare"
            , "Education", "Accessibility", "Crypto", "Space", "Transportation", "Home Design", "Renewable Energy", "LGBTQ"
            , "Laws", "Children", "Physics", "Mathematics", "Chemistry", "Art", "Culture", "Social Media", "Astrophysics", "Crime"
            , "Entertainment", "Finance", "Anime", "Science Fiction", "Manufacturing", "Logistics", "Space"]

#----------------------------------------------------------------------------------------------------#
#SCRAPING NEWS TITLES AND LINKS
news = {} #empty dictionary for news titles and links
for category in categories: #repeat the process for every category
    searchbar = browser.find_element_by_name("q")
    searchbar.click()
    searchbar.clear()
    searchbar.send_keys(f"Artificial Intelligence {category} tech news") #search for news
    searchbar.send_keys(Keys.RETURN)
    for x in range(1,11): #each page has 10 news titles
        try: #because sometimes things go wonky lol
            if x == 10: #the tenth news title has a different x-path format than the previous 9
                news_title = browser.find_element_by_xpath(f"""//*[@id="rso"]/div[{x}]/g-card/div/div/a/div/div/div[2]""")
            else:
                news_title = browser.find_element_by_xpath(f"""//*[@id="rso"]/div[{x}]/g-card/div/div/a/div/div[2]/div[2]""")
            #finding 'a' element so we can get the link of the title
            a = browser.find_element_by_xpath(f"""//*[@id="rso"]/div[{x}]/g-card/div/div/a""")
            a = a.get_attribute("href")
            news[news_title.text] = a #adding to dictionary
        except:
            continue

#----------------------------------------------------------------------------------------------------#
#ADDING TO DATABASE
table_name = "news"
for y in news: #itering over each key/value pair in the dict
    # print('->', y, ': ', news[y])
    newsTitle = y
    newsLink = news[y]
    #writing in this format so that metacharacters in the links, especially, dont confuse the system. love you StackOverflow
    cursor.execute("INSERT INTO {tableName} (newsTitle, newsLink) VALUES(?, ?)".format(tableName=table_name),
    (newsTitle, newsLink))
conn.commit() #save!!

# DISPLAYALL = cursor.execute("SELECT * FROM news")
# fullNews = cursor.fetchall()
# print(fullNews)

#----------------------------------------------------------------------------------------------------#
#all done *salsa emoji*

