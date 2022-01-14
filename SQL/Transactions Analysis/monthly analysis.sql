
--EXEC [dbo].sp_CollectEntityData @entity_name='bws', @start_date='2015-12-10', @end_date='2025-12-10'
--EXEC [dbo].sp_CollectEntityData @entity_name='walmart', @start_date='2015-12-10', @end_date='2025-12-10'
--EXEC [dbo].sp_CollectEntityData @entity_name='nslsc', @start_date='2015-12-10', @end_date='2025-12-10'
--EXEC [dbo].sp_CollectEntityData @entity_name='bath', @start_date='2015-12-10', @end_date='2025-12-10'
--EXEC [dbo].sp_CollectEntityData @entity_name='cnb', @start_date='2015-12-10', @end_date='2025-12-10'
--EXEC [dbo].sp_CollectEntityData @entity_name='irving', @start_date='2015-12-10', @end_date='2025-12-10'
--EXEC [dbo].sp_CollectEntityData @entity_name='amazon', @start_date='2015-12-10', @end_date='2025-12-10'
--EXEC [dbo].sp_CollectEntityData @entity_name='fred', @start_date='2015-12-10', @end_date='2025-12-10'

DECLARE @data TABLE ([ID] INT IDENTITY(1, 1), [Date] DATETIME, [# Debits] INT, [# Credits] INT, [# Tranasactions] INT, [Total Spent] FLOAT, [Total Earned] FLOAT, [Total] FLOAT)

DECLARE @i INT;
DECLARE @d AS DATETIME;

SET @d = (SELECT MIN([Date]) FROM [ScotiaTransactions]);

WHILE @d < GETDATE() BEGIN
	
	INSERT INTO @data ([Date], [# Debits], [# Credits], [# Tranasactions], [Total Spent], [Total Earned], [Total])
	SELECT
		[Date],
		SUM([# Debits]),
		SUM([# Credits]),
		SUM([# Debits]) + SUM([# Credits]),
		SUM([Total Spent]),
		SUM([Total Earned]),
		SUM([Total])
	FROM (
		SELECT
			@d AS [Date],
			COUNT(*) AS [# Debits],
			0 AS [# Credits],
			0 AS [# Tranasactions],
			SUM([Amount]) AS [Total Spent],
			0 AS [Total Earned],
			SUM([Amount]) AS [Total]
		FROM
			[ScotiaTransactions]
		WHERE
			[Date] BETWEEN @d AND DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, [dbo].sv_EndOfMonth(@d))))
			AND [Amount] < 0
		UNION (
			SELECT
				@d AS [Date], 
				0 AS [# Debits],
				COUNT(*) AS [# Credits],
				0 AS [# Tranasactions],
				0 AS [Total Spent],
				SUM([Amount]) AS [Total Earned],
				SUM([Amount]) AS [Total]
			FROM
				[ScotiaTransactions]
			WHERE
				[Date] BETWEEN @d AND DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, [dbo].sv_EndOfMonth(@d))))
				AND [Amount] >= 0
		)
	) AS [Src]
	GROUP BY
		[Date]

	SET @d = DATEADD(DAY, 1, [dbo].sv_EndOfMonth(@d));

END

SELECT * FROM @data
SELECT
	SUM([# Credits]) AS [# Credits],
	SUM([# Debits]) AS [# Debits],
	SUM([# Tranasactions]) AS [# Transactions],
	SUM([Total Spent]) AS [Total Spent],
	SUM([Total Earned]) AS [Total Earned],
	SUM([Total]) AS [Total]
FROM
	@data
SELECT COUNT(*) AS [# Non-Transaction Months] FROM @data WHERE [Total] IS NULL