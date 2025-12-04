import pandas as pd
import pandas_ta as ta

class TechnicalAnalyzer:
    def analyze(self, df: pd.DataFrame) -> dict:
        if df.empty or len(df) < 30:
            return {"summary": "데이터 부족으로 분석 불가"}
        
        # Calculate Indicators
        df.set_index('date', inplace=True)
        rsi = df.ta.rsi(length=14).iloc[-1]
        sma_20 = df.ta.sma(length=20).iloc[-1]
        close = df['close'].iloc[-1]
        
        trend = "상승" if close > sma_20 else "하락"
        rsi_status = "과매수" if rsi > 70 else "과매도" if rsi < 30 else "중립"
        
        return {
            "close": close,
            "rsi": rsi,
            "trend": trend,
            "status": rsi_status,
            "summary_text": f"현재가 {close}는 20일 이평선 {trend} 추세이며, RSI({rsi:.1f}) 기준 {rsi_status} 구간입니다."
        }