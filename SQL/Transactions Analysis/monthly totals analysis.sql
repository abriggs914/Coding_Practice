-- Scotia Transaction Median Values

DECLARE @hpy AS INTEGER;
SET @hpy = 1;

DECLARE @T AS TABLE ([ID] INT, [Val] FLOAT, [Date] DATETIME);
INSERT INTO @T ([ID], [Val], [Date]) 
SELECT [TransactionID], [Amount], [Date] FROM [ScotiaTransactions] ORDER BY [Date] DESC;

--SELECT * FROM @T
	
DECLARE @years TABLE ([ID] INT IDENTITY(1, 1), [Year] INT);
INSERT INTO @years
SELECT MONTH([Date]) FROM @T GROUP BY MONTH([Date]);

DECLARE @medians TABLE ([ID] INT IDENTITY(1, 1), [Year] INT, [A] FLOAT, [B] FLOAT);

DECLARE @c1 as INTEGER;
DECLARE @c2 as INTEGER;
DECLARE @lh as INTEGER;
DECLARE @rh as INTEGER;
DECLARE @i AS INTEGER;
SET @i = 0;
SELECT @c1 = COUNT(*) FROM @years;
SELECT @c2 = COUNT(*) FROM @YEARS;
IF @c2 % 2 = 1 BEGIN
	SET @c2 = @c2 - 1;
	SET @c2 = @c2 / 2;
END
WHILE @i < @c1 BEGIN

	SET @lh = ((
				(SELECT COUNT(*) FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1)) / 2)
				+ (CASE WHEN (SELECT COUNT(*) FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1)) % 2 = 1 THEN 1 ELSE 0 END)
				);
	IF @lh < 0 BEGIN
		SET @lh = 0;
	END

	SET @rh = ((
				(SELECT COUNT(*) FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1)) / 2)
				+ (CASE WHEN (SELECT COUNT(*) FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1)) % 2 = 1 THEN 1 ELSE 0 END)
				);
	IF @rh < 0 BEGIN
		SET @rh = 0;
	END

	INSERT INTO @medians ([Year], [A], [B]) 
		SELECT 
		--(
		--(SELECT MAX([Val]) * 10000 AS [Val] FROM (SELECT TOP ((SELECT COUNT(*) FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1)) / 2) [Val] FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1) ORDER BY MONTH([Date]), [Val]) AS TopHalf)
		--+ (SELECT MIN([Val]) * 10000 AS [Val] FROM (SELECT TOP (((SELECT COUNT(*) FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1)) / 2) + (CASE WHEN (SELECT COUNT(*) FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1)) % 2 = 1 THEN -1 ELSE 0 END)) [Val] FROM @T WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1) ORDER BY MONTH([Date]) DESC, [Val] DESC) AS BottomHalf)
		--) / 2 AS [Median]),
		(SELECT [Year] FROM @years WHERE [ID] = @i + 1),
		(SELECT MAX([Val]) * @hpy AS [Val] FROM 
			(SELECT TOP (@lh)
				[Val] FROM
				@T 
				WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1) ORDER BY MONTH([Date]), [Val]) AS [A]),
		(SELECT MIN([Val]) * @hpy AS [Val] FROM 
			(SELECT TOP (@rh)
				[Val] FROM
				@T 
				WHERE MONTH([Date]) = (SELECT [Year] FROM @years WHERE [ID] = @i + 1) ORDER BY MONTH([Date]) DESC, [Val] DESC) AS [B])
	
	SET @i = @i + 1;

END
;

SELECT * FROM @T;
SELECT * FROM @years
SELECT @c1 AS [C1], @c2 AS [C2]
SELECT [Year], CAST(([A] + [B]) / 2 AS MONEY) AS [Median Annual Salary] FROM @medians ORDER BY [Year] DESC

SELECT
	MONTH([Date]) AS [Year],
	MAX([Amount]) AS [Highest Credit],
	MIN([Amount]) AS [Highest Debit],
	AVG([Amount]) AS [Avg Amount],
	COUNT([Amount]) AS [# Transactions],
	(([A] + [B]) / 2) AS [Median]
FROM
	[ScotiaTransactions]
LEFT JOIN
	@medians
ON
	[@medians].[Year] = MONTH([ScotiaTransactions].[Date])
GROUP BY
	MONTH([Date]), [A], [B]
ORDER BY
	[Year] DESC