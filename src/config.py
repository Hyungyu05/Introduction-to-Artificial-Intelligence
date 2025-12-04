import os
import sys
from omegaconf import DictConfig

def validate_config(cfg: DictConfig):
    """
    실행 전 필수 환경변수와 설정이 제대로 되어 있는지 검사합니다.
    """
    missing_vars = []
    
    # 필수 환경변수 체크
    if not os.getenv("POLYGON_API_KEY"):
        missing_vars.append("POLYGON_API_KEY")
    if not os.getenv("FMP_API_KEY"):
        missing_vars.append("FMP_API_KEY")
        
    if missing_vars:
        print("❌ [Critical Error] 필수 환경변수가 .env 파일에 없습니다:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n.env.example 파일을 참고하여 .env 파일을 설정해주세요.")
        sys.exit(1)
        
    # 데이터 디렉토리 생성 확인
    db_path = cfg.database.duckdb.path
    # Hydra 실행 경로 문제 방지를 위해 절대 경로 변환 로직이 있으면 좋지만,
    # 여기서는 단순 존재 여부만 체크하거나 패스합니다.
    return True