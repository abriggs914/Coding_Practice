-- Assigning TransactionType Ids to existing ScotiaTransactions
-- 2022-01-24

--SELECT [TransactionType], [TransactionTypeID] FROM [ScotiaTransactionTypes] GROUP BY [TransactionType], [TransactionTypeID] ORDER BY [TransactionType]
--SELECT [TransactionSubType] FROM [ScotiaTransactionTypes] GROUP BY [TransactionSubType] ORDER BY [TransactionSubType]

BEGIN TRAN;

DECLARE @id AS INT;
SET @id = 14;

SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] IS NULL

UPDATE
	[ScotiaTransactions]
SET
	[TransactionTypeID] = @id
WHERE
	[TransactionID] = 1708
	
SELECT * FROM [ScotiaTransactionTypes] ORDER BY [TransactionType], [TransactionSubType]
SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] IS NOT NULL ORDER BY [Entity]
SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] IS NULL ORDER BY [Entity]
SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] = @id ORDER BY [Entity]

ROLLBACK;
COMMIT;