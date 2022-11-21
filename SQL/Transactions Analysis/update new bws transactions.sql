BEGIN TRAN;

DECLARE @tid AS INT;
SELECT @tid = 17;

UPDATE
	[ScotiaTransactions]
SET
	[TransactionTypeID] = @tid
WHERE
	[TransactionTypeID] IS NULL
	AND [ScotiaTransactions].[Entity] LIKE '%bws%'

SELECT * FROM [ScotiaTransactions] WHERE [TransactionTypeID] = @tid

ROLLBACK;
COMMIT;