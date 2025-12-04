class FundamentalAnalyzer:
    def analyze(self, data: dict) -> str:
        # 안전한 파싱을 위한 헬퍼
        def get_val(cat, key, div=1, fmt="{:.2f}"):
            try:
                val = data.get(cat, [])[0].get(key, 0)
                return fmt.format(val / div)
            except:
                return "N/A"

        rev = get_val('income_statement', 'revenue', 1e9, "{:.2f}B")
        net = get_val('income_statement', 'netIncome', 1e9, "{:.2f}B")
        per = get_val('ratios', 'priceEarningsRatio')
        roe = get_val('ratios', 'returnOnEquity', 0.01, "{:.1f}%") # raw is usually 0.15 for 15%
        debt = get_val('ratios', 'debtRatio')

        return (
            f"최근 분기 매출 {rev}, 순이익 {net}. "
            f"PER {per}배, ROE {roe}, 부채비율 {debt}. "
            f"펀더멘털 관점에서 건전성을 유지하고 있는지 확인이 필요합니다."
        )