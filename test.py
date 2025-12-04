import sys
import os
import requests
from dotenv import load_dotenv

# .env 로드
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

def debug_fmp_request():
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("❌ .env에서 API 키를 찾을 수 없습니다.")
        return

    symbol = "AAPL"
    base_url = "https://financialmodelingprep.com/api/v3"
    
    # 1. 문서에서 말한 '가장 확실한' Quote 요청 (쿼리 파라미터가 적음)
    # requests 라이브러리가 URL을 어떻게 만드는지 확인
    endpoint = f"/quote/{symbol}"
    url = f"{base_url}{endpoint}"
    params = {"apikey": api_key}
    
    print("----- [진단 1: Quote 요청 URL 구조 확인] -----")
    # Request 객체를 미리 만들어서 URL이 어떻게 찍히는지 봅니다.
    req = requests.Request('GET', url, params=params)
    prepped = req.prepare()
    
    # 키 보안을 위해 출력 시에만 마스킹
    masked_url = prepped.url.replace(api_key, "HIDDEN_KEY")
    print(f"👉 생성된 URL: {masked_url}")
    
    # 실제 요청
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
    # 문서: https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=FY&limit=5&apikey=YOUR_API_KEY
    # 파이썬 딕셔너리로 넘겼을 때 순서나 기호(&, ?)가 잘 붙는지 확인
    
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
    
    # 문서 내용 체크: ?로 시작하고 나머지는 &로 연결되었는가?
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