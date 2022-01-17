

CREATE PROCEDURE [dbo].[sp_EntityTransactionsAnalysis]
AS BEGIN

DECLARE @start_date AS DATETIME;
DECLARE @end_date AS DATETIME;
DECLARE @entity_name AS NVARCHAR(MAX);
DECLARE @mode AS CHAR(1);

SET @start_date ='2015-12-10';
SET @end_date = '2025-12-10';
SET @entity_name = '  irvinG ';
-- 'd'	-	daily DEFAULT
-- 'w'	-	weekly
-- 'm'	-	monthly
-- 'a'	-	annualy
SET @mode = 'd';

DECLARE @data TABLE ([ID] INT IDENTITY(1, 1), [Date] DATETIME, [# Debits] INT, [# Credits] INT, [# Tranasactions] INT, [Total Spent] FLOAT, [Total Earned] FLOAT, [Total] FLOAT)

DECLARE @i INT;
DECLARE @d AS DATETIME;

--SET @d = (SELECT MIN([Date]) FROM [ScotiaTransactions]);
SET @d = @start_date;

IF @mode = 'a' BEGIN
	--SELECT 'annualy' AS [X]

	WHILE @d < @end_date BEGIN
	
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
				[Date] BETWEEN @d AND DATEADD(DAY, 364, DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d))))
				AND [Amount] < 0
				AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
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
					[Date] BETWEEN @d AND DATEADD(DAY, 364, DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d))))
					AND [Amount] >= 0
					AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
			)
		) AS [Src]
		GROUP BY
			[Date]

		SET @d = DATEADD(YEAR, 1, @d);

	END

END
ELSE IF @mode = 'w' BEGIN
	--SELECT 'weekly' AS [X]

	WHILE @d < @end_date BEGIN
	
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
				[Date] BETWEEN @d AND DATEADD(DAY, 6, DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d))))
				AND [Amount] < 0
				AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
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
					[Date] BETWEEN @d AND DATEADD(DAY, 6, DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d))))
					AND [Amount] >= 0
					AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
			)
		) AS [Src]
		GROUP BY
			[Date]

		SET @d = DATEADD(DAY, 7, @d);

	END
END
ELSE IF @mode = 'm' BEGIN
	--SELECT 'monthly' AS [X]
	WHILE @d < @end_date BEGIN
	
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
				AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
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
					AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
			)
		) AS [Src]
		GROUP BY
			[Date]

		SET @d = DATEADD(DAY, 1, [dbo].sv_EndOfMonth(@d));

	END
END
ELSE BEGIN
-- Default
	--SELECT 'daily' AS [X]
	WHILE @d < @end_date BEGIN
	
		INSERT INTO @data ([Date], [# Debits], [# Credits], [# Tranasactions], [Total Spent], [Total Earned], [Total])
		SELECT
			[Date],
			SUM([# Debits]),
			SUM([# Credits]),
			SUM([# Debits]) + SUM([# Credits]),
			SUM([Total Spent]),
			SUM([Total Earned]),
			AVG([Total])
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
				[Date] BETWEEN @d AND DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d)))
				AND [Amount] < 0
				AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
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
					[Date] BETWEEN @d AND DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d)))
					AND [Amount] >= 0
					AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
			)
		) AS [Src]
		GROUP BY
			[Date]

		SET @d = DATEADD(DAY, 1, @d);

	END
END








--WHILE @d < GETDATE() BEGIN
	
--	INSERT INTO @data ([Date], [# Debits], [# Credits], [# Tranasactions], [Total Spent], [Total Earned], [Total])
--	SELECT
--		[Date],
--		SUM([# Debits]),
--		SUM([# Credits]),
--		SUM([# Debits]) + SUM([# Credits]),
--		SUM([Total Spent]),
--		SUM([Total Earned]),
--		AVG([Total])
--	FROM (
--		SELECT
--			@d AS [Date],
--			COUNT(*) AS [# Debits],
--			0 AS [# Credits],
--			0 AS [# Tranasactions],
--			SUM([Amount]) AS [Total Spent],
--			0 AS [Total Earned],
--			SUM([Amount]) AS [Total]
--		FROM
--			[ScotiaTransactions]
--		WHERE
--			[Date] BETWEEN @d AND DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d)))
--			AND [Amount] < 0
--			AND LOWER(TRIM([Entity])) LIKE '%' + LOWER(TRIM(@entity_name)) + '%'
--			AND [Date] BETWEEN @start_date AND (CASE WHEN @start_date <> @end_date THEN @end_date ELSE DATEADD() END)
--		UNION (
--			SELECT
--				@d AS [Date], 
--				0 AS [# Debits],
--				COUNT(*) AS [# Credits],
--				0 AS [# Tranasactions],
--				0 AS [Total Spent],
--				SUM([Amount]) AS [Total Earned],
--				SUM([Amount]) AS [Total]
--			FROM
--				[ScotiaTransactions]
--			WHERE
--				[Date] BETWEEN @d AND DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, @d)))
--				AND [Amount] >= 0
--		)
--	) AS [Src]
--	GROUP BY
--		[Date]

--	SET @d = DATEADD(DAY, 1, @d);

--END

SELECT * FROM @data
--SELECT
--	SUM([# Credits]) AS [# Credits],
--	SUM([# Debits]) AS [# Debits],
--	SUM([# Tranasactions]) AS [# Transactions],
--	SUM([Total Spent]) AS [Total Spent],
--	SUM([Total Earned]) AS [Total Earned],
--	SUM([Total]) AS [Total]
--FROM
--	@data
--SELECT COUNT(*) AS [# Non-Transaction Days] FROM @data WHERE [Total] IS NULL
END