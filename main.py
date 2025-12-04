import hydra
from omegaconf import DictConfig
from src.data.manager import DataManager
from src.analysis.technical import TechnicalAnalyzer
from src.analysis.sentiment import SentimentAnalyzer
from src.analysis.fundamental import FundamentalAnalyzer
from src.agent.quant_agent import QuantAgent
import os
import sys

def parse_ticker_from_input(user_input: str) -> str:
    """
    사용자 입력(자연어)에서 티커를 추론하는 함수
    """
    user_input = user_input.lower().strip()
    

    ticker_map = {
        "AAPL": ["애플", "apple", "아이폰", "맥북","에플","appl"],
        "TSLA": ["테슬라", "tesla", "일론", "머스크"],
        "GOOGL": ["구글", "google", "알파벳", "유튜브"],
        "META": ["메타", "meta", "페이스북", "인스타"]
    }

    for ticker, keywords in ticker_map.items():
        for kw in keywords:
            if kw in user_input:
                return ticker
    

    return user_input.upper()

@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig):
    user_query = input("\n💬 분석하고 싶은 종목을 입력하세요 : ")
    

    symbol = parse_ticker_from_input(user_query)
    


    db_path = cfg.database.path
    if not os.path.isabs(db_path):
        db_path = os.path.join(hydra.utils.get_original_cwd(), db_path)
        
    db = DataManager(db_path)
    
    price_df = db.get_price_data(symbol)
    news_list = db.get_news(symbol)
    fin_data = db.get_financials(symbol)
    
    if price_df.empty:
        print(f"\n❌ '{symbol}'에 대한 데이터가 준비되지 않았습니다. 서비스에 불편을 드려 죄송합니다.")
        print(f"   (지원 종목: AAPL, TSLA, GOOGL, META)")
        return

    print(f"🚀 {symbol} 데이터 분석을 시작합니다...")

    tech_res = TechnicalAnalyzer().analyze(price_df)
    senti_res = SentimentAnalyzer(cfg.api.ollama.model).analyze(news_list)
    fund_res = FundamentalAnalyzer().analyze(fin_data)
    
    agent = QuantAgent(cfg.api.ollama.model)
    report = agent.generate_report(
        symbol, 
        tech_res.get('summary_text', str(tech_res)), 
        senti_res, 
        fund_res
    )
    
    print("\n" + "="*60)
    print(f"📈 {symbol} 투자 분석 리포트")
    print("="*60)
    print(report)
    print("="*60)

if __name__ == "__main__":
    main()