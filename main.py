import rumps
import requests
from bs4 import BeautifulSoup

class StockApp(rumps.App):
    def __init__(self):
        super(StockApp, self).__init__("Stock App", "📈")

        self.stock_price = rumps.MenuItem(title="주가 로딩 중...")
        self.menu = [self.stock_price]

        self.stocks = [
            ("네이버", "035420", 4, 229000),
            ("DGB금융지주", "139130", 104, 9540),
            ("종근당", "185750", 12, 81800),
            ("고영", "098460", 61, 16120),
            ("삼성전자", "005930", 16, 59500),
            ("오로스테크놀로지", "322310", 40, 24450),
        ]
        self.current_stock_index = 0

        self.timer = rumps.Timer(self.update_stock_price, 6)
        self.timer.start()

        self.update_stock_price(None)

    def fetch_stock_price(self, stock_name, stock_code, shares, average_price):
        try:
            url = f"https://finance.naver.com/item/main.naver?code={stock_code}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')

            # 현재가
            price_tag = soup.select_one("p.no_today span.blind")
            # 전일 종가
            yesterday_tag = soup.select_one("td.first span.blind")

            if price_tag and yesterday_tag:
                price = int(price_tag.text.replace(",", ""))
                prev_close = int(yesterday_tag.text.replace(",", ""))

                # 전일 대비 변동률 계산
                rate = ((price - prev_close) / prev_close) * 100
                day_emoji = "📈" if rate > 0 else ("📉" if rate < 0 else "➖")
                rate_str = f"{rate:+.2f}%"

                # 내 수익률 계산
                if average_price > 0:
                    return_ratio = ((price - average_price) / average_price) * 100
                    return_emoji = "📈" if return_ratio > 0 else ("📉" if return_ratio < 0 else "➖")
                    return_ratio_str = f"{return_ratio:+.2f}%"
                else:
                    return_ratio_str = "N/A"
                    return_emoji = ""

                title_text = f"{stock_name} {price:,}원 {day_emoji} {rate_str} {return_emoji} {return_ratio_str}"
                self.title = title_text
                return title_text
            else:
                return f"{stock_name} 정보 불러오기 실패"
        except Exception as e:
            return f"{stock_name} 오류: {e}"

    def update_stock_price(self, _):
        stock_name, stock_code, shares, average_price = self.stocks[self.current_stock_index]
        price_info = self.fetch_stock_price(stock_name, stock_code, shares, average_price)
        self.stock_price.title = price_info

        self.current_stock_index = (self.current_stock_index + 1) % len(self.stocks)

if __name__ == "__main__":
    app = StockApp()
    app.run()
