CREATE TABLE rawtbl (
    c_code CHAR(6) NOT NULL,
    data_month TINYINT NOT NULL,
    data_year SMALLINT NOT NULL,
    quater VARCHAR(6) NOT NULL,
    assets BIGINT NOT NULL,
    assets_aver BIGINT NOT NULL,
    current_assets BIGINT NOT NULL,
    inventories BIGINT NOT NULL,
    non_current_assets BIGINT NOT NULL, # 비유동자산
    tangible_assets BIGINT NOT NULL, # 유형자산
    intangible_assets BIGINT NOT NULL, # 무형자산
    liabilities_and_equity BIGINT NOT NULL, # 부채 및 자본총계
    liabilities BIGINT NOT NULL, # 부채
    liabilities_aver BIGINT NOT NULL, # 부채 평균
    current_liabilities BIGINT NOT NULL, # 유동부채
    payables BIGINT NOT NULL, # 단기차입금
    total_equity BIGINT NOT NULL, # 총자본
    total_equity_aver BIGINT NOT NULL, # 총자본 평균
    controlling_shareholder BIGINT NOT NULL, # 지배주주 지분
    capital_stock BIGINT NOT NULL, # 자본금
    capital_surplus BIGINT NOT NULL, # 자본잉여금
    sales BIGINT NOT NULL, # 매출
    cost_of_goods_sold BIGINT NOT NULL, # 매출원가
    gross_profit BIGINT NOT NULL, # 매출총이익
    operating_profit BIGINT NOT NULL, # 영업이익
    net_income BIGINT NOT NULL, # 당기순이익
    total_comprehensive_income BIGINT NOT NULL, # 총포괄손익
    net_income_of_controlling_shareholders BIGINT NOT NULL, # 지배주주 순이익
    eps BIGINT NOT NULL, # eps
    bps BIGINT NOT NULL, # bps
    eps_adjusted BIGINT NOT NULL, # eps_수정
    bps_adjusted BIGINT NOT NULL, # bps_수정
    bps_adjusted_nontreasurystock BIGINT NOT NULL, # bps_수정(자사주차감)
    PRIMARY KEY (c_code, data_year, quater),
    FOREIGN KEY (c_code) REFERENCES comtbl (c_code)
);