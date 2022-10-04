DECLARE @t1 AS TABLE ([ID] INT IDENTITY(1, 1), [Num] INT);
DECLARE @t2 AS TABLE ([ID] INT IDENTITY(1, 1), [Num] INT);
DECLARE @t3 AS TABLE ([ID] INT IDENTITY(1, 1), [Num] INT);

INSERT INTO @t1 ([Num]) VALUES (1), (2), (3), (4), (5);
INSERT INTO @t2 ([Num]) VALUES (1), (2), (3), (4);
INSERT INTO @t3 ([Num]) VALUES (2), (3), (4);

SELECT
	'@t1 & @t2' AS [Table]
	,*
FROM 
	@t1
INNER JOIN
	@t2
ON
	[@t1].[Num] = [@t2].[Num]
;

SELECT
	'@t1 & @t3' AS [Table]
	,*
FROM 
	@t1
INNER JOIN
	@t3
ON
	[@t1].[Num] = [@t3].[Num]
;

SELECT
	'@t2 & @t3' AS [Table]
	,*
FROM 
	@t2
INNER JOIN
	@t3
ON
	[@t2].[Num] = [@t3].[Num]
;

SELECT
	'@t1 & @t2 & @t3' AS [Table]
	,*
FROM 
	@t1
INNER JOIN
	@t2
ON
	[@t1].[Num] = [@t2].[Num]
INNER JOIN
	@t3
ON
	[@t1].[Num] = [@t3].[Num]
;

SELECT
	'@t1 & @t2 & @t3 L t11' AS [Table]
	,*
FROM 
	@t1
INNER JOIN
	@t2
ON
	[@t1].[Num] = [@t2].[Num]
INNER JOIN
	@t3
ON
	[@t1].[Num] = [@t3].[Num]
LEFT OUTER JOIN
	@t1 AS [t11]
ON
	[@t1].[Num] = [t11].[Num]
;