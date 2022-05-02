/****** Script for SelectTopNRows command from SSMS  ******/

DECLARE @t1 AS TABLE ([ID] INT IDENTITY(1, 1), [N Transactions] INT, [DateC] NVARCHAR(7), [Amount] FLOAT, [Entity] NVARCHAR(MAX));
DECLARE @t2 AS TABLE ([ID] INT IDENTITY(1, 1), [N Transactions] INT, [DateC] NVARCHAR(7), [Amount] FLOAT, [Entity] NVARCHAR(MAX));
DECLARE @d AS TABLE ([ID] INT IDENTITY(1, 1), [DateC] NVARCHAR(7));

INSERT INTO @t1
SELECT
	COUNT([TransactionID]) AS [N Transactions]
	, CAST(YEAR([Date]) AS NVARCHAR(4)) + '-' + RIGHT('00' + CAST(MONTH([Date]) AS NVARCHAR(2)), 2) AS [DateC]
	,SUM([Amount]) AS [Amount]
	,[Entity]
FROM
	[master].[dbo].[ScotiaTransactions]
WHERE
	YEAR([Date]) >= 2021
GROUP BY
	YEAR([Date])
	, MONTH([Date])
	, [Entity]
ORDER BY
	[Entity]
	, [DateC]
;

INSERT INTO @d
SELECT 
	[DateC]
FROM
	@t1
GROUP BY
	[DateC]

DECLARE @i AS INTEGER;
DECLARE @c AS INTEGER;
DECLARE @cd AS NVARCHAR(7); 
DECLARE @md AS NVARCHAR(7); 

SELECT @i = 0;
SELECT @c = COUNT(*) FROM @t1;
SELECT @cd = MIN([DateC]) FROM @t1
SELECT @md = MAX([DateC]) FROM @t1

WHILE @cd < @md BEGIN
	INSERT INTO @t2
	SELECT
		SUM([N Transactions]) AS [N Transactions]
		, @cd AS [DateC]
		, SUM([Amount]) AS [Amount]
		, [Entity]
	FROM
		@t1
	WHERE
		[DateC] <= @cd
	GROUP BY
		[Entity]
	;
	SET @i = @i + 1;
	SELECT @cd = [DateC] FROM @d WHERE [ID] = @i;
END

SELECT
	*
FROM
	@t1
ORDER BY
	[Entity]
	, [DateC]

SELECT
	*
FROM
	@t2
ORDER BY
	[Entity]
	, [DateC]