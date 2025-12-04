import os
import hydra
from omegaconf import DictConfig
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@hydra.main(version_base=None, config_path="../config", config_name="config")
def main(cfg: DictConfig):
    db_path = cfg.database.path
    
    if not os.path.isabs(db_path):
        original_cwd = hydra.utils.get_original_cwd()
        db_path = os.path.join(original_cwd, db_path)

    print(f"Target DB Path: {db_path}")

    if os.path.exists(db_path):
        print("=" * 50)
        print(f"⚠️  경고: 데이터베이스 파일({db_path})을 삭제하려고 합니다.")
        print("삭제하면 수집된 모든 주가, 뉴스, 재무 데이터가 사라집니다.")
        print("=" * 50)
        
        response = input("정말로 초기화 하시겠습니까? (y/n): ").strip().lower()
        
        if response == 'y':
            try:
                os.remove(db_path)
                wal_path = db_path + ".wal"
                if os.path.exists(wal_path):
                    os.remove(wal_path)
                    
                print(f"✅ 데이터베이스가 성공적으로 삭제되었습니다. setup_data.py를 다시 실행하세요.")
            except PermissionError:
                print("❌ 삭제 실패: 파일이 현재 사용 중입니다.")
                print("   VS Code, Python 프로세스, 혹은 DB 뷰어 프로그램을 종료하고 다시 시도해주세요.")
            except Exception as e:
                print(f"❌ 오류 발생: {e}")
        else:
            print("취소되었습니다.")
    else:
        print(f"ℹ️  삭제할 데이터베이스 파일이 없습니다: {db_path}")

if __name__ == "__main__":
    main()