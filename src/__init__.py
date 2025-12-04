import os
from dotenv import load_dotenv

# 패키지가 임포트될 때 .env 파일을 최우선으로 로드합니다.
# 이렇게 하면 프로젝트 어디서든 os.getenv()를 안전하게 쓸 수 있습니다.
load_dotenv()