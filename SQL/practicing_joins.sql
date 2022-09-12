DECLARE @table_1 AS TABLE ([ID] INT IDENTITY(1, 1), [Num] INT);
INSERT INTO @table_1 ([Num]) VALUES
	(-40),
	(-36),
	(-14),
	(-4),
	(10),
	(11)

DECLARE @table_2 AS TABLE ([ID] INT IDENTITY(1, 1), [Num] INT);
INSERT INTO @table_2 ([Num]) VALUES
	(-37),
	(-15),
	(-7),
	(-1),
	(13),
	(11)

DECLARE @table_id AS INT = 0;

-- 1
SELECT @table_id = @table_id + 1;
SELECT
	@table_id AS [Table#],
	*
FROM 
	@table_1
LEFT JOIN
	@table_2
ON
	[@table_1].[Num] = [@table_2].[Num]
;

-- 2
SELECT @table_id = @table_id + 1;
SELECT
	@table_id AS [Table#],
	*
FROM 
	@table_1
LEFT JOIN
	@table_2
ON
	[@table_1].[Num] = [@table_2].[Num]
WHERE
	[@table_2].[Num] IS NOT NULL

-- 3
SELECT @table_id = @table_id + 1;
SELECT
	@table_id AS [Table#],
	*
FROM 
	@table_1
LEFT OUTER JOIN
	@table_2
ON
	[@table_1].[Num] = [@table_2].[Num]

-- 4
SELECT @table_id = @table_id + 1;
SELECT
	@table_id AS [Table#],
	*
FROM 
	@table_1
INNER JOIN
	@table_2
ON
	[@table_1].[Num] = [@table_2].[Num]