import sys
import os
import pandas as pd
import duckdb
import hydra
from omegaconf import DictConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@hydra.main(version_base=None, config_path="../config", config_name="config")
def main(cfg: DictConfig):
    db_path = cfg.database.path
    if not os.path.isabs(db_path):
        db_path = os.path.join(hydra.utils.get_original_cwd(), db_path)
    
    output_dir = os.path.join(os.path.dirname(db_path), "exports")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📂 데이터베이스 경로: {db_path}")
    print(f"📂 CSV 저장 경로: {output_dir}\n")

    if not os.path.exists(db_path):
        print("❌ 데이터베이스 파일이 없습니다. scripts/setup_data.py를 먼저 실행하세요.")
        return

    conn = duckdb.connect(db_path)
    
    tables_df = conn.execute("SHOW TABLES").df()
    if tables_df.empty:
        print("⚠️ 저장된 테이블이 없습니다.")
        return
    
    tables = tables_df['name'].tolist()
    
    for table_name in tables:
        print(f"Processing table: {table_name}...")
        
        df = conn.execute(f"SELECT * FROM {table_name}").df()
        
        if df.empty:
            print(f"  ⚠️ {table_name} 테이블이 비어있습니다.")
            continue
            
        csv_path = os.path.join(output_dir, f"{table_name}.csv")
        
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        print(f"  ✅ 저장 완료: {csv_path}")
        print(f"  👀 데이터 미리보기 ({len(df)} rows):")
        print(df.head(3))
        print("-" * 30)

    print("\n🎉 모든 변환 작업이 완료되었습니다! 'data/exports' 폴더를 확인해보세요.")

if __name__ == "__main__":
    main()