import hydra
from omegaconf import DictConfig
from src.data.manager import DataManager
from src.data.fetcher import PolygonFetcher
from src.data.fmp_fetcher import FMPFetcher


@hydra.main(version_base=None, config_path="../config", config_name="config")
def main(cfg: DictConfig):
    db = DataManager(cfg.database.path)
    poly = PolygonFetcher(cfg)
    fmp = FMPFetcher(cfg)
    
    for symbol in cfg.symbols:
        print(f"Processing {symbol}...")
        
        # 1. Price
        df = poly.fetch_prices(symbol, cfg.date_range.start, cfg.date_range.end)
        db.save_prices(df, symbol)
        
        # 2. News
        news = poly.fetch_news(symbol)
        db.save_news(news, symbol)
        
        # 3. Financials
        fin_data = fmp.fetch_all(symbol)
        db.save_financials(symbol, fin_data)
        
    print("✅ 데이터 수집 및 저장 완료!")

if __name__ == "__main__":
    main()  