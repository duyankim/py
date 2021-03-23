
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(stock_name):
    me = "***"
    my_pw = "***"
    you = "***"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "알림"
    msg['From'] = me
    msg['To'] = you

    html = '주목할 주식' + stock_name
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(me, my_pw)
    s.sendmail(me, you, msg.as_string())
    s.quit()


def get_stock():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome(
        "C:/Users/USER/Desktop/chromedriver_win32 (1)/chromedriver.exe", options=options)

    codes = ['005930', '035420', '017670', '096770', '035720']
    #삼성전자, 네이버, SK텔레콤, SK이노베이션, 카카오

    for code in codes:

        url = 'https://m.stock.naver.com/item/main.nhn#/stocks/'+code+'/total'

        driver.get(url)

        time.sleep(2)

        # 크롬에서 HTML 정보를 가져오고 BeautifulSoup을 통해 검색하기 쉽도록 가공
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        name = soup.select_one(
            '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div.stock_info > div.item_wrp > div.elips_wrp > h2').text

        current_price = soup.select_one(
            '#header > div.end_header_topinfo > div.flick-container > div > div:nth-child(2) > div.stock_info > div.stock_wrp > div.price_wrp > strong').text

        rate = soup.select_one(
            '#header > div.end_header_topinfo > div.flick-container > div > div:nth-child(2) > div.stock_info > div.stock_wrp > div.price_wrp > div.gap_wrp > span.gap_rate > span.rate').text

        print(name, current_price, rate)

        if(float(rate) > -5):
            print('send', name)
            send_mail(name)

    print('==========')

    driver.quit()


def job():
    get_stock()


def run():
    schedule.every(150).seconds.do(job)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    run()
