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
    
    # 1. 별칭 사전 (Aliases Map)
    # 여기에 인식시키고 싶은 단어들을 계속 추가하면 됩니다.
    ticker_map = {
        "AAPL": ["애플", "apple", "아이폰", "맥북","에플","appl"],
        "TSLA": ["테슬라", "tesla", "일론", "머스크"],
        "GOOGL": ["구글", "google", "알파벳", "유튜브"],
        "META": ["메타", "meta", "페이스북", "인스타"]
    }

    # 2. 문장에서 키워드 찾기
    for ticker, keywords in ticker_map.items():
        for kw in keywords:
            if kw in user_input:
                return ticker
    
    # 3. 키워드가 없으면 입력값을 그대로 티커로 가정하고 반환
    # (예: 사용자가 "NVDA"라고 입력했을 경우)
    return user_input.upper()

@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig):
    # 1. 사용자 입력 받기
    user_query = input("\n💬 분석하고 싶은 종목을 입력하세요 : ")
    
    # 2. 자연어 -> 티커 변환
    symbol = parse_ticker_from_input(user_query)
    
    # # 변환된 결과 확인 메시지 (사용자 안심용)
    # if symbol != user_query.upper():
    #     print(f"🤖 '{user_query}'를 '{symbol}' 종목으로 인식했습니다.")

    # 3. DB 경로 처리
    db_path = cfg.database.path
    if not os.path.isabs(db_path):
        db_path = os.path.join(hydra.utils.get_original_cwd(), db_path)
        
    db = DataManager(db_path)
    
    # 4. Load Data
    price_df = db.get_price_data(symbol)
    news_list = db.get_news(symbol)
    fin_data = db.get_financials(symbol)
    
    # 데이터 유무 체크
    if price_df.empty:
        print(f"\n❌ '{symbol}'에 대한 데이터가 준비되지 않았습니다. 서비스에 불편을 드려 죄송합니다.")
        print(f"   (지원 종목: AAPL, TSLA, GOOGL, META)")
        # print("   만약 지원 종목이라면 'scripts/setup_data.py'를 먼저 실행해주세요.")
        return

    print(f"🚀 {symbol} 데이터 분석을 시작합니다...")

    # 5. Analyze
    tech_res = TechnicalAnalyzer().analyze(price_df)
    senti_res = SentimentAnalyzer(cfg.api.ollama.model).analyze(news_list)
    fund_res = FundamentalAnalyzer().analyze(fin_data)
    
    # 6. Generate Report
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