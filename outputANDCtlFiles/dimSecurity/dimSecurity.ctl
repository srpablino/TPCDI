LOAD DATA
INFILE 'dimSecurity.csv'
APPEND
INTO TABLE dimSecurity
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    SK_SecurityID,
    Symbol,
    Issue,
    Status,
    Name,
    ExchangeID,
    SK_CompanyID,
    SharesOutstanding,
    FirstTrade DATE "YYYY-MM-DD",
    FirstTradeOnExchange DATE "YYYY-MM-DD",
    Dividend,
    IsCurrent,
    BatchID,
    EffectiveDate DATE "YYYY-MM-DD HH24:MI:SS",
    EndDate DATE "YYYY-MM-DD HH24:MI:SS"
)
