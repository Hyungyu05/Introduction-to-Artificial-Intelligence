import ollama

class SentimentAnalyzer:
    def __init__(self, model="gemma2:2b"):
        self.model = model

    def analyze(self, news_list: list) -> str:
        if not news_list:
            return "최근 뉴스 없음"
            
        headlines = "\n".join([f"- {n['title']}" for n in news_list])
        prompt = f"""
        다음 뉴스 헤드라인들을 읽고 해당 기업에 대한 시장 감성을 요약해줘:
        {headlines}
        
        결과는 한 줄로 요약하고, 긍정/부정/중립 중 하나를 선택해. (한국어로)
        """
        try:
            resp = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
            return resp['message']['content']
        except:
            return "감성 분석 실패 (LLM 에러)"