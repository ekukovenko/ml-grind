import pandas as pd
from bs4 import BeautifulSoup
from parser import Parser


class SteamParser(Parser):
    def __init__(self) -> None:
        self.url = ("https://steamcommunity.com/app/730/reviews"
                    "/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=russian")
        self.source = "steamcommunity.com"
        self.scroll = True

    def get_product_list(self) -> None:
        content_list = super().get_page_content(url=self.url, scroll=self.scroll)

        text_column = []
        rate_column = []

        for content in content_list:
            soup = BeautifulSoup(content, features="lxml")
            raw_list = soup.find_all('div', attrs={'class': 'apphub_UserReviewCardContent'})

            for review in raw_list:
                card_text_content = review.find('div', class_='apphub_CardTextContent')
                if card_text_content:
                    date_posted = card_text_content.find('div', class_='date_posted')
                    if date_posted:
                        date_posted.decompose()
                    text = card_text_content.get_text(strip=True)
                else:
                    text = None

                title = review.find('div', class_='title')
                if title:
                    title_text = title.get_text(strip=True)
                else:
                    title_text = None

                text_column.append(text)
                rate_column.append(title_text)

        data = {
            'text': text_column,
            'rate': rate_column,
        }
        df = pd.DataFrame(data)
        df.to_csv('steam_dataset.csv', index=False, encoding='utf-8-sig')
