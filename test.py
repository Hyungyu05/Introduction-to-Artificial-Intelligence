import sys
import os
import requests
from dotenv import load_dotenv


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

def debug_fmp_request():
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("❌ .env에서 API 키를 찾을 수 없습니다.")
        return

    symbol = "AAPL"
    base_url = "https://financialmodelingprep.com/api/v3"
    

    endpoint = f"/quote/{symbol}"
    url = f"{base_url}{endpoint}"
    params = {"apikey": api_key}
    
    print("----- [진단 1: Quote 요청 URL 구조 확인] -----")
    req = requests.Request('GET', url, params=params)
    prepped = req.prepare()
    
    masked_url = prepped.url.replace(api_key, "HIDDEN_KEY")
    print(f"👉 생성된 URL: {masked_url}")
    
    try:
        resp = requests.Session().send(prepped, timeout=10)
        print(f"👉 응답 코드: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ Quote 요청 성공! (키와 URL 생성 방식은 정상임)")
        else:
            print(f"❌ Quote 요청 실패: {resp.text}")
    except Exception as e:
        print(f"❌ 연결 오류: {e}")

    print("\n----- [진단 2: 재무제표 요청 (파라미터 여러 개)] -----")

    
    endpoint = f"/income-statement/{symbol}"
    url = f"{base_url}{endpoint}"
    params = {
        "period": "annual",
        "limit": 1,
        "apikey": api_key
    }
    
    req = requests.Request('GET', url, params=params)
    prepped = req.prepare()
    
    masked_url = prepped.url.replace(api_key, "HIDDEN_KEY")
    print(f"👉 생성된 URL: {masked_url}")
    

    if "?" in masked_url and "&" in masked_url:
        print("✅ URL 구조 정상 (?와 &가 올바르게 포함됨)")
    
    try:
        resp = requests.Session().send(prepped, timeout=10)
        print(f"👉 응답 코드: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            if data:
                print(f"✅ 재무제표 데이터 수신 성공! (매출: {data[0].get('revenue')})")
            else:
                print("⚠️ 요청은 성공했으나 데이터가 빔 (무료 플랜 제한 가능성)")
        elif resp.status_code == 403:
            print("⛔ 403 Forbidden 발생")
            print("   -> URL 구조는 맞으나, 서버가 '이 키로는 이 데이터를 줄 수 없다'고 거절함.")
            print("   -> 원인: 무료(Basic) 플랜은 '분기(quarter)' 데이터 접근이 막힘")
        else:
            print(f"❌ 에러: {resp.text}")
            
    except Exception as e:
        print(f"❌ 연결 오류: {e}")

if __name__ == "__main__":
    debug_fmp_request()