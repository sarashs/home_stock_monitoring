import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class SentimentAnalysis:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.messages = [
        {"role": "system", "content": "You are a financial data analyst. You can read through the company 10-K forms and decide whether or not the companies financial situation is sound. You can also read the news and decide whether its sentiment is positive or negative."}]

    def analyze_news(self, text, ticker):
        self.messages.append({"role": "user", "content": f"given the following text tell me if the sentiment around {ticker} stock is positive, negative or neutral. where positive means that the stock is a good investment and negative means that the stock is not a good investment. neutral means that you cannot decide. Your response should be one word either positive, negative or neutral. \n '''{text}'''"})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0,
        )
        self.messages.pop()
        content = response['choices'][0]['message']['content']
        sentiment = content if ("positive" in content.lower() or "negative" in content.lower() or "neutral" in content.lower()) else None

        return sentiment
    
if __name__=="__main__":
    S = SentimentAnalysis()
    sentiment = S.analyze_news("apple stock went down real bad and it sucked today.", "AAPL")
    if sentiment:
        print(f"test result: {sentiment}")
    else:
        print("test failed")
