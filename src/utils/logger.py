import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    모듈별로 표준화된 로거를 생성하여 반환합니다.
    """
    logger = logging.getLogger(name)
    
    # 중복 핸들러 방지 (Hydra가 로깅을 잡고 있을 수 있으나, 명시적 설정이 안전함)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # 콘솔 출력 핸들러
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger