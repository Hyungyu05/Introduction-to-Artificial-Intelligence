import os
import sys
from omegaconf import DictConfig

def validate_config(cfg: DictConfig):
    """
    실행 전 필수 환경변수와 설정이 제대로 되어 있는지 검사합니다.
    """
    missing_vars = []
    
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
        
    db_path = cfg.database.duckdb.path

    return True