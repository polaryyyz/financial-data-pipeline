-- Top 10 companies by market capitalization
SELECT
	symbol,
	"companyName",
	"marketCap_billions"
FROM companies
ORDER BY "marketCap_billions" DESC
LIMIT 10;

-- Average market capitalization by sector
SELECT
	sector,
	ROUND(AVG("marketCap_billions")::numeric, 2) AS avg_market_cap_billions
FROM companies
GROUP BY sector
ORDER BY avg_market_cap_billions DESC;

-- Price history for a company
SELECT
	symbol,
	price,
	snapshot_at
FROM company_snapshots
WHERE symbol = 'AAPL'
ORDER BY snapshot_at;

-- Number of companies by sector

SELECT
	sector,
	COUNT(*) AS company_count
FROM companies
GROUP BY sector
ORDER BY company_count DESC;

-- Largest company in each sector

SELECT
	sector,
	symbol,
	"companyName",
	"marketCap_billions"
FROM (
	SELECT
		sector,
		symbol,
		"companyName",
		"marketCap_billions",
		ROW_NUMBER() OVER (
			PARTITION BY sector
			ORDER BY "marketCap_billions" DESC
		) AS rank
	FROM companies
) ranked_companies
WHERE rank = 1
ORDER BY "marketCap_billions" DESC;

-- Price evolution between first and latest snapshot

WITH ranked_snapshots AS (
	SELECT
		symbol,
		price,
		snapshot_at,
		ROW_NUMBER() OVER (
			PARTITION BY symbol
			ORDER BY snapshot_at ASC
		) AS first_rank,
		ROW_NUMBER() OVER (
			PARTITION BY symbol
			ORDER BY snapshot_at DESC
		) AS latest_rank
	FROM company_snapshots
),

first_prices AS (
	SELECT
		symbol,
		price AS first_price
	FROM ranked_snapshots
	WHERE first_rank = 1
),

latest_prices AS (
	SELECT
		symbol,
		price AS latest_price
	FROM ranked_snapshots
	WHERE latest_rank = 1
)

SELECT
	first_prices.symbol,
	first_price,
	latest_price,
	ROUND(
		(
			(latest_price - first_price)
			/ first_price * 100
		)::numeric,
		2
	) AS price_change_percent
FROM first_prices
JOIN latest_prices
	ON first_prices.symbol = latest_prices.symbol
ORDER BY price_change_percent DESC;