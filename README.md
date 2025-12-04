# 📈 Quant Agent v2

**인공지능개론** 수업의 일환으로 개발된 **로컬 LLM 기반 퀀트 투자 분석 에이전트**입니다.
이 프로젝트는 기술적 분석(차트), 뉴스 감성(텍스트), 펀더멘털(재무제표) 데이터를 종합하여 전문적인 투자 리포트를 자동으로 생성합니다.

## 🚀 프로젝트 개요 (Overview)

* **목표:** 서로 다른 형태의 이종 데이터(시계열, 텍스트, 재무 데이터)를 결합하여 주식 분석 프로세스를 자동화합니다.
* **핵심 로직:** 결정론적(Deterministic)인 3단계 분석 파이프라인과 LLM의 추론 능력을 결합했습니다.
* **분석 대상:** 주요 기술주 (AAPL, TSLA, GOOGL, META)

## 🛠️ 기술 스택 (Tech Stack)

* **Language:** Python 3.10
* **AI Engine:** Ollama (Gemma2:2b) - *On-premise / Local Environment*
* **Database:** DuckDB (OLAP 최적화 인메모리 DB)
* **Framework:** Hydra (설정 관리), Streamlit (웹 UI)
* **Data Sources:** Polygon.io (주가/뉴스), Financial Modeling Prep (재무제표)

## ✨ 핵심 기능 (Key Features)

1.  **하이브리드 분석 아키텍처 (Hybrid Analysis)**
    * **Technical:** `pandas-ta`를 활용한 추세 및 모멘텀 분석 (RSI, 이동평균선).
    * **Sentiment:** 뉴스 헤드라인을 LLM에 주입하여 시장 심리(긍정/부정) 추출.
    * **Fundamental:** 복잡한 재무제표 JSON 데이터를 파싱하여 건전성 지표(PER, ROE 등) 평가.

2.  **Pure Python 구현 (No LangChain)**
    * LangChain이나 LangGraph 같은 무거운 오케스트레이션 프레임워크를 사용하지 않고, **자체 에이전트 워크플로우**를 설계했습니다.
    * 이를 통해 실행 속도를 최적화하고, 프롬프트 엔지니어링 과정을 100% 제어할 수 있습니다.

3.  **로컬 LLM 통합 (Local LLM)**
    * Ollama를 통해 외부 API 비용 없이, 데이터 유출 걱정 없는 안전한 분석 환경을 구축했습니다.

## 🏗️ 시스템 아키텍처 (Architecture)

```mermaid
graph TD
    User[사용자 입력] -->|Streamlit UI| Agent
    
    subgraph Data Layer
        DB[(DuckDB)]
    end
    
    subgraph Analysis Pipeline
        DB --> Tech[기술적 분석 모듈]
        DB --> Senti[감성 분석 모듈]
        DB --> Fund[펀더멘털 분석 모듈]
    end
    
    subgraph Reasoning
        Tech --> Context
        Senti --> Context
        Fund --> Context
        Context --> Prompt
        Prompt --> LLM[Ollama (Gemma2)]



    end
    
    LLM --> Report[최종 투자 리포트]
