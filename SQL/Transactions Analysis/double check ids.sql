SELECT
	*
FROM
	[ScotiaTransactions]
LEFT JOIN
	[ScotiaTransactionTypes]
ON
	[ScotiaTransactions].[TransactionTypeID] = [ScotiaTransactionTypes].[TransactionTypeID]
ORDER BY
	[Date] DESC
;

SELECT
	*
FROM
	[ScotiaTransactions]
LEFT JOIN
	[ScotiaTransactionTypes]
ON
	[ScotiaTransactions].[TransactionTypeID] = [ScotiaTransactionTypes].[TransactionTypeID]
ORDER BY
	 [TransactionID] DESC
;

SELECT * FROM (
SELECT
	ROW_NUMBER() OVER(
		ORDER BY [TransactionID]
	) AS [Row#],
	[TransactionID]
FROM
	[ScotiaTransactions]
) AS [Src]
WHERE
	[Row#] <> [TransactionID]
ORDER BY
	 [TransactionID] DESC
;
