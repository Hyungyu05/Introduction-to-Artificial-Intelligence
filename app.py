import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv
import hydra
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 모듈 임포트
from src.data.manager import DataManager
from src.analysis.technical import TechnicalAnalyzer
from src.analysis.sentiment import SentimentAnalyzer
from src.analysis.fundamental import FundamentalAnalyzer
from src.agent.quant_agent import QuantAgent

# 환경변수 로드
load_dotenv()

# --- [설정 및 초기화] ---
st.set_page_config(
    page_title="Quant Agent v2",
    page_icon="📈",
    layout="wide"
)

@st.cache_resource
def get_config():
    """Hydra 설정을 Streamlit 환경에 맞춰 로드"""
    # Hydra 인스턴스 초기화 (재실행 시 충돌 방지)
    if GlobalHydra.instance().is_initialized():
        GlobalHydra.instance().clear()
    
    # config 폴더 위치 지정
    initialize(version_base=None, config_path="config")
    
    # [핵심 수정] overrides를 사용하여 문제가 되는 ${hydra:runtime.cwd} 변수를 제거
    # DB 경로를 단순 상대 경로로 덮어씌웁니다.
    cfg = compose(config_name="config", overrides=["database.path=data/trading_data.duckdb"])
    return cfg

def parse_ticker(user_input):
    """자연어 -> 티커 변환"""
    user_input = user_input.lower().strip()
    ticker_map = {
        "AAPL": ["애플", "apple", "아이폰", "맥북"],
        "TSLA": ["테슬라", "tesla", "일론", "머스크"],
        "GOOGL": ["구글", "google", "알파벳", "유튜브"],
        "META": ["메타", "meta", "페이스북", "인스타"]
    }
    for ticker, keywords in ticker_map.items():
        for kw in keywords:
            if kw in user_input:
                return ticker
    return user_input.upper()

# --- [UI 구성] ---
def main():
    # 사이드바
    with st.sidebar:
        st.title("🤖 Quant Agent v2")
        st.markdown("---")
        st.write("**System Status**")
        st.success("Engine: Ollama (Gemma2:2b)")
        st.success("DB: DuckDB (Local)")
        st.markdown("---")
        st.info("지원 종목: AAPL, TSLA, GOOGL, META")
        
        if st.button("데이터 새로고침 (Setup Data)"):
            st.warning("터미널에서 'python scripts/setup_data.py'를 실행해주세요.")

    # 메인 헤더
    st.title("📈 퀀트 기반 기업 분석 에이전트")
    st.caption("Technical + Sentiment + Fundamental Analysis powered by Local LLM")

    # 채팅 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 어떤 기업을 분석해 드릴까요? (예: '테슬라 분석해줘')"}]

    # 채팅 기록 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("질문을 입력하세요..."):
        # 사용자 메시지 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 에이전트 응답 처리
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # 1. 티커 파싱
            symbol = parse_ticker(prompt)
            
            # 상태창 표시
            with st.status(f"🔍 '{symbol}' 데이터 분석 중...", expanded=True) as status:
                try:
                    cfg = get_config()
                    
                    # DB 경로 절대경로로 변환
                    db_path = cfg.database.path
                    if not os.path.isabs(db_path):
                        db_path = os.path.join(os.getcwd(), db_path)
                    
                    db = DataManager(db_path)
                    
                    # 데이터 로드
                    status.write("📥 데이터베이스 조회 중...")
                    price_df = db.get_price_data(symbol)
                    news_list = db.get_news(symbol)
                    fin_data = db.get_financials(symbol)
                    
                    if price_df.empty:
                        status.update(label="데이터 없음!", state="error")
                        st.error(f"❌ '{symbol}'에 대한 데이터가 없습니다. 먼저 데이터 수집 스크립트를 실행해주세요.")
                        st.stop()

                    # 시각화 (차트)
                    status.write("📊 차트 및 지표 생성 중...")
                    st.line_chart(price_df.set_index("date")["close"], color="#00FF00")
                    
                    # 3가지 분석 실행
                    status.write("🧠 3-Way 분석 파이프라인 가동...")
                    tech_res = TechnicalAnalyzer().analyze(price_df)
                    senti_res = SentimentAnalyzer(cfg.api.ollama.model).analyze(news_list)
                    fund_res = FundamentalAnalyzer().analyze(fin_data)
                    
                    status.write("🤖 LLM 리포트 생성 중...")
                    agent = QuantAgent(cfg.api.ollama.model)
                    
                    # 기술적 지표 요약 텍스트 추출
                    tech_summary = tech_res.get('summary_text', str(tech_res))
                    
                    report = agent.generate_report(symbol, tech_summary, senti_res, fund_res)
                    
                    status.update(label="분석 완료!", state="complete", expanded=False)
                    
                    # 최종 리포트 출력
                    st.markdown(f"### 📊 {symbol} 투자 분석 리포트")
                    st.markdown(report)
                    
                    # 세부 데이터 탭 (보너스 기능)
                    with st.expander("🔎 원본 데이터 및 세부 지표 보기"):
                        tab1, tab2, tab3 = st.tabs(["기술적 지표", "뉴스 요약", "재무제표"])
                        
                        with tab1:
                            st.json(tech_res)
                        with tab2:
                            if news_list:
                                for n in news_list[:3]:
                                    st.write(f"- **{n['title']}** ({n['published_utc']})")
                            else:
                                st.write("뉴스 데이터 없음")
                        with tab3:
                            st.write(fund_res)

                    # 세션에 저장
                    st.session_state.messages.append({"role": "assistant", "content": report})

                except Exception as e:
                    import traceback
                    st.error(f"에러 발생: {e}")
                    st.text(traceback.format_exc())
                    status.update(label="시스템 에러", state="error")

if __name__ == "__main__":
    main()