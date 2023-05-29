import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = os.environ.get("YOUR_STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("YOUR_NEWS_API_KEY")

TWILIO_ACCOUNT_SID = "ACb19b2054a0a3fbc5732431560d8bd4ea"
TWILIO_AUTH_TOKEN = os.environ.get("YOUR_TWILIO_AUTH_TOKEN")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Use https://www.alphavantage.co/documentation/#daily

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
# print(data)

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
# e.g. [new_value for (key, value) in dictionary.items()]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
# print(yesterday_closing_price)


# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing = day_before_yesterday_data['4. close']
# print(day_before_yesterday_closing)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
# print(diff_percent)

# If percentage is greater than 0.1 then print("Get News").

if abs(diff_percent) > 0.1:

    ## https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,

    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()
    articles = news_data["articles"]
    # print(news_articles)

    # Use Python slice operator to create a list that contains the first 3 articles.
    # Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = [article for article in articles[:3]]
    # print(three_articles)

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']},\n\nBrief: {article['description']}" for article in three_articles]
    # print(formatted_articles)

    # Send each article as a separate message via Twilio.
    for article in formatted_articles:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
            body=article,
            from_='+12183877347',
            to='+923402822957'
        )

        print(message.sid)

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
