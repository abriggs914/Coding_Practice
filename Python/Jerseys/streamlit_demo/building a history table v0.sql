
SELECT * 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE 
	TABLE_SCHEMA = 'dbo' 
	AND
	TABLE_NAME = 'Conferences'

/*

SELECT
	(CASE WHEN 1 <> NULL THEN 1 ELSE 0 END)
	,(CASE WHEN 0 <> NULL THEN 1 ELSE 0 END)
*/
	
DECLARE @c TABLE (
	[ID] INT IDENTITY(0, 1),
	[Name] NVARCHAR(MAX),
	[A] NVARCHAR(MAX),
	[B] NVARCHAR(MAX),
	[C] NVARCHAR(MAX)
)
DECLARE @i TABLE (
	[ID] INT IDENTITY(0, 1),
	[Name] NVARCHAR(MAX),
	[A] NVARCHAR(MAX),
	[B] NVARCHAR(MAX),
	[C] NVARCHAR(MAX)
)
DECLARE @d TABLE (
	[ID] INT IDENTITY(0, 1),
	[Name] NVARCHAR(MAX),
	[A] NVARCHAR(MAX),
	[B] NVARCHAR(MAX),
	[C] NVARCHAR(MAX)
)

-- do an insert
	INSERT INTO @c (
		[Name], [A], [B], [C]
	)
	VALUES
		('Avery', 'A1', 'B2', 'C3')
	;
	INSERT INTO @i (
		[Name], [A], [B], [C]
	)
	VALUES
		('Avery', 'A1', 'B2', 'C3')
	;
	INSERT INTO @d (
		[Name], [A], [B], [C]
	)
	VALUES
		(NULL, NULL, NULL, NULL)
	;

SELECT '@c' AS [T], * FROM @c
SELECT '@i' AS [T], * FROM @i
SELECT '@d' AS [T], * FROM @d

SELECT
	[C].[ID],
	NULL,
	(CASE
		WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 'Name'
		WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 'Name'
		WHEN [D].[Name] <> [C].[Name] THEN 'Name'
		ELSE NULL
	END) AS [ModifiedColumn],
	(CASE
		WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 'INSERT'
		WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 'DELETE'
		WHEN [D].[Name] <> [C].[Name] THEN 'UPDATE'
		ELSE NULL
	END) AS [Modification],
	[D].[Name] AS [ValueBefore],
	[I].[Name] AS [ValueAfter]
FROM
	@c [C]
INNER JOIN
	@i [I]
ON
	[C].[ID] = [I].[ID]
LEFT JOIN
	@d [D]
ON
	[C].[ID] = [D].[ID]
WHERE 
	(CASE
		WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 1
		WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 1
		WHEN [D].[Name] <> [C].[Name] THEN 1
		ELSE 0
	END) > 0
	;

SELECT
	(CASE 
		WHEN OBJECT_ID('@c', 'U') IS NOT NULL THEN 1
		ELSE 0
	END) AS [A]