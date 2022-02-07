-- Assigning TransactionType Ids to existing ScotiaTransactions
-- 2022-01-24

--SELECT [TransactionType], [TransactionTypeID] FROM [ScotiaTransactionTypes] GROUP BY [TransactionType], [TransactionTypeID] ORDER BY [TransactionType]
--SELECT [TransactionSubType] FROM [ScotiaTransactionTypes] GROUP BY [TransactionSubType] ORDER BY [TransactionSubType]

BEGIN TRAN;

DECLARE @id AS INT;
SET @id = 11;

SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] IS NULL

UPDATE
	[ScotiaTransactions]
SET
	[TransactionTypeID] = @id
WHERE
	[TransactionID] IN  ()
	
SELECT * FROM [ScotiaTransactionTypes] ORDER BY [TransactionType], [TransactionSubType]
SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] IS NULL ORDER BY [TransactionTypeID], [Date] DESC
SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] IS NOT NULL ORDER BY [TransactionTypeID], [Date] DESC
SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] = @id ORDER BY [TransactionTypeID], [Entity]

ROLLBACK;
COMMIT;

SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] = 23 ORDER BY [Entity]