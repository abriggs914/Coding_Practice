DECLARE @Years TABLE ([ID] INT IDENTITY(1, 1), [Year] INT);
INSERT INTO @Years SELECT YEAR([Date]) FROM [ScotiaTransactions] GROUP BY YEAR([Date]) ORDER BY YEAR([Date])

DECLARE @EntityData TABLE (
	[Entity Search Pattern] NVARCHAR(MAX),
	[Total Spent] FLOAT,
	[Max Credit] FLOAT,
	[Min Debit] FLOAT,
	[Avg Amount] FLOAT,
	[# Transactions] INT,
	[First Date] DATETIME,
	[Last Date] DATETIME,
	[# Days] INT,
	[$ / Day] INT
);

DECLARE @eNames TABLE ([Name] NVARCHAR(MAX));
DECLARE @eName AS NVARCHAR(MAX);
DECLARE @y AS INT;
DECLARE @i AS INT;
DECLARE @j AS INT;
DECLARE @c1 AS INT;
DECLARE @c2 AS INT;
DECLARE @sd AS DATETIME;
DECLARE @ed AS DATETIME;
SET @i = 0;
SET @c1 = (SELECT COUNT(*) FROM @years);
SET @c2 = (SELECT COUNT(*) FROM [ScotiaTransactions]);

WHILE @i < @c1 BEGIN
	SET @i = @i + 1;
	SET @j = 0;
	SET @y = (SELECT [Year] FROM @Years WHERE [ID] = @i);
	SET @sd = CAST(@y AS NVARCHAR(4)) + '-01-01';
	SET @ed = CAST(@y AS NVARCHAR(4)) + '-12-31 23:59:59';
	WHILE @j < @c2 BEGIN
		SET @j = @j + 1;
		SET @eName = (SELECT [Entity] FROM [ScotiaTransactions] WHERE [TransactionID] = @j);
		INSERT INTO @eNames EXEC [dbo].[sp_GroupEntities] @nameIn=@eName;
		PRINT 'A @eName: ' + @eName + ', @sd: ' + CAST(@sd AS NVARCHAR(MAX)) + ', @ed: ' + CAST(@ed AS NVARCHAR(MAX))
		SET @eName = (SELECT TOP 1 [Name] FROM @eNames);
		INSERT INTO @EntityData (
			[Entity Search Pattern],
			[Total Spent],
			[Max Credit],
			[Min Debit],
			[Avg Amount],
			[# Transactions],
			[First Date],
			[Last Date],
			[# Days],
			[$ / Day]
		)
		EXEC [dbo].[sp_CollectEntityData] @entity_name=@eName, @start_date=@sd, @end_date=@ed;
		DELETE FROM @eNames WHERE 1=1;
		PRINT 'B @eName: ' + @eName + ', @sd: ' + CAST(@sd AS NVARCHAR(MAX)) + ', @ed: ' + CAST(@ed AS NVARCHAR(MAX))
	END
	--IF @i = 1 BEGIN
	--	SET @i = @c1;
	--END
END

SELECT * FROM @Years;

SELECT * FROM @EntityData
SELECT * FROM @EntityData WHERE [Entity Search Pattern] = 'skyfall'

SELECT
	[Entity Search Pattern],
	YEAR(MIN([First Date])) AS [Year],
	AVG([Total Spent]) AS [Total Spent],
	MAX([Max Credit]) AS [Max Credit],
	MIN([Min Debit]) AS [Min Debit],
	AVG([Avg Amount]) AS [Avg Amount],
	AVG([# Transactions]) AS [# Transactions],
	MIN([First Date]) AS [First Date],
	MAX([Last Date]) AS [Last Date],
	MAX([# Days]) AS [# Days],
	AVG([$ / Day]) AS [$ / Day]
FROM 
	@EntityData
GROUP BY
	[Entity Search Pattern],
	YEAR([First Date])
HAVING
	YEAR(MIN([First Date])) IS NOT NULL
ORDER BY
	[First Date],
	[Entity Search Pattern];