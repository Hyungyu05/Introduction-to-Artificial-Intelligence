import ollama
from datetime import datetime

class QuantAgent:
    def __init__(self, model_name):
        self.model = model_name

    def generate_report(self, symbol, tech, senti, fund):
        # [수정] 현재 날짜를 YYYY-MM-DD 형식으로 가져옴
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""
        [System Info]
        - Report Date: {today_date} (You must use this date)
        - Role: Senior Quant Analyst
        - Target: {symbol} Investment Report
        - Language: Korean (한국어)
        
        [Input Data]
        1. Technical Analysis:
        {tech}
        
        2. Market Sentiment (News):
        {senti}
        
        3. Fundamental Analysis (Financials):
        {fund}
        
        [Instructions]
        위 데이터를 바탕으로 전문적인 투자 리포트를 작성하세요.
        - 서두에 '작성일: {today_date}'를 명시하세요.
        - '재무제표' 섹션에서 구체적인 숫자가 없다면 '데이터 확인 불가'라고 솔직하게 쓰세요.
        - 결론은 명확한 투자 포지션(매수/매도/관망)으로 끝내세요.
        """
        
        print(f"🤖 에이전트가 {today_date} 기준으로 리포트를 작성 중입니다...")
        
        try:
            resp = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
            return resp['message']['content']
        except Exception as e:
            return f"❌ 리포트 생성 실패: {e}"