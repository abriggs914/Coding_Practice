SELECT TOP 10 * FROM [ScotiaTransactions] WHERE [Amount] < 0 ORDER BY [Amount]
SELECT TOP 10 * FROM [ScotiaTransactions] WHERE [Amount] < 0 ORDER BY [Amount] DESC

SELECT
	TOP 10
		MIN([Amount]) AS [Amount]
FROM
	[ScotiaTransactions]
INNER JOIN
	[ScotiaTransactionTypes] 
ON
	[ScotiaTransactions].[TransactionTypeID] = [ScotiaTransactionTypes].[TransactionTypeID] 
WHERE
	[Amount] < 0
ORDER BY
	[Amount]


SELECT TOP 10 * FROM [ScotiaTransactions] INNER JOIN [ScotiaTransactionTypes] ON [ScotiaTransactions].[TransactionTypeID] = [ScotiaTransactionTypes].[TransactionTypeID] WHERE [Amount] < 0 ORDER BY [Amount] DESC