import rumps
import requests
from bs4 import BeautifulSoup

class StockApp(rumps.App):
    def __init__(self):
        super(StockApp, self).__init__("Stock App", "📈")

        # 기본 종목 목록
        self.stocks = [
            ("네이버", "035420", 4, 229000),
            ("고영", "098460", 61, 16120),
            ("오로스테크놀로지", "322310", 40, 24450),
            ("KODEX 인버스", "114800", 1018, 4530),
            ("코스닥 150선물인버스", "251340", 191, 4155),
        ]
        self.current_stock_index = 0

        self.stock_price = rumps.MenuItem(title="주가 로딩 중...")
        self.menu = [self.stock_price, None, "종목 추가", "종목 삭제", None, "종료"]

        self.timer = rumps.Timer(self.update_stock_price, 6)
        self.timer.start()

        self.update_stock_price(None)

    def fetch_stock_price(self, stock_name, stock_code, shares, average_price):
        try:
            url = f"https://finance.naver.com/item/main.naver?code={stock_code}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')

            price_tag = soup.select_one("p.no_today span.blind")
            yesterday_tag = soup.select_one("td.first span.blind")

            if price_tag and yesterday_tag:
                price = int(price_tag.text.replace(",", ""))
                prev_close = int(yesterday_tag.text.replace(",", ""))

                rate = ((price - prev_close) / prev_close) * 100
                day_emoji = "📈" if rate > 0 else ("📉" if rate < 0 else "➖")
                rate_str = f"{rate:+.2f}%"

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
        if not self.stocks:
            self.stock_price.title = "종목 없음"
            self.title = "📉 없음"
            return

        stock_name, stock_code, shares, average_price = self.stocks[self.current_stock_index]
        price_info = self.fetch_stock_price(stock_name, stock_code, shares, average_price)
        self.stock_price.title = price_info

        self.current_stock_index = (self.current_stock_index + 1) % len(self.stocks)

    @rumps.clicked("종목 추가")
    def add_stock(self, _):
        response = rumps.Window(
            "종목명, 종목코드, 수량, 평균단가를 쉼표로 구분해 입력해 주세요.\n예: 카카오,035720,10,60000",
            "종목 추가", default_text=""
        ).run()

        if response.clicked:
            try:
                name, code, quantity, avg = [s.strip() for s in response.text.split(",")]
                self.stocks.append((name, code, int(quantity), int(avg)))
                rumps.alert(f"{name} 추가 완료!")
            except Exception:
                rumps.alert("입력 형식이 잘못됐어요! 다시 시도해 주세요.")

    @rumps.clicked("종목 삭제")
    def delete_stock(self, _):
        if not self.stocks:
            rumps.alert("삭제할 종목이 없어요!")
            return

        choices = "\n".join(f"{i+1}. {s[0]}" for i, s in enumerate(self.stocks))
        response = rumps.Window(
            f"삭제할 종목 번호를 입력해 주세요:\n\n{choices}", "종목 삭제"
        ).run()

        if response.clicked:
            try:
                index = int(response.text) - 1
                if 0 <= index < len(self.stocks):
                    removed = self.stocks.pop(index)
                    rumps.alert(f"{removed[0]} 삭제 완료!")
                else:
                    rumps.alert("잘못된 번호입니다.")
            except Exception:
                rumps.alert("숫자로 입력해 주세요.")

    @rumps.clicked("종료")
    def quit_app(self, _):
        rumps.quit_application()


if __name__ == "__main__":
    StockApp().run()
