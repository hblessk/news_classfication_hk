from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages= [100, 100, 100, 71, 94, 73]         #페이지당 20개씩이다. 뉴스는. 순서대로 페이지 숫자를 센 것
                                        #100페이 정도까지 크롤링. 너무 적은 데이터는 복사해서 수량을 늘려줘야함.
url='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'

options = webdriver.ChromeOptions()
# options.add_argumnet('headless')
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
# driver.get(url)
#
# x_path = '//*[@id="section_body"]/ul[1]/li[1]/d1/dt[2]/a'
# x_path = '//*[@id="section_body"]/ul[1]/li[1]/d1/dt[2]/a'
# x_path = '//*[@id="section_body"]/ul[1]/li[1]/d1/dt[2]/a'
# #x_path = '//*[@id="main_content"]/div/div[2]/div[1]/div[2]/div[1]/ul/li[1]/div[2]/a'
# #x_path = '//*[@id="main_content"]/div/div[2]/div[1]/div[3]/div[1]/ul/li[1]/div[2]/a'
#
# title = driver.find_element('xpath', x_path).text
#
#
# print(title)

df_title = pd.DataFrame()

for i in range(0, 6):              #section
    titles = []
    for j in range(1, 11):          #page
       url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
       driver.get(url)
       time.sleep(0.2)
       for k in range(1, 5):    # x_path
           for l in range(1, 6):   # x_path
               x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
               try:
                    title = driver.find_element('xpath', x_path).text
                    print(title)
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
               except NoSuchElementException as e:                                          #에러를 살리기 위해서. 하나도 안 놓치기 위해서
                   x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)    #dt뒤에 [2]숫자같은게 있으면 안됨.


                   title = driver.find_element('xpath', x_path).text
                   title = re.compile('[^가-힣 ]').sub(' ', title)
                   titles.append(title)
               except:
                    print('error', i, j, k, l )


    if j % 10 == 0: #j가 10에 배수가 될때마다 한번씩 한다. 10페이지마다 한번씩 저장하겠다.
        df_section_title = pd.DataFrame(titles, columns=['titles'])
        df_section_title['category'] = category[i]
        df_title = pd.concat([df_title, df_section_title], ignore_index=True)
        df_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(category[i], j),
                        index=False)
        titles = []                    #에러가 날 경우에 시간


#time.sleep(10)

# # for i in range(0, 6):
#     titles = []
#     for j in range(1, pages[i]):
#
#         x_path = ''