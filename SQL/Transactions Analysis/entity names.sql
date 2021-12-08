
CREATE PROCEDURE [dbo].[sp_GroupEntities]
	@nameIn AS NVARCHAR(MAX) = NULL
AS
BEGIN

	DECLARE @i AS INTEGER;
	DECLARE @c2 AS INTEGER;
	DECLARE @kName AS NVARCHAR(MAX);

	DECLARE @known AS TABLE ([ID] INTEGER IDENTITY(1, 1), [Name] NVARCHAR(MAX), [KnownName] NVARCHAR(MAX));
	INSERT INTO @known ([Name], [KnownName]) VALUES
	('amazon', 'amazon'),
	('amzn', 'amazon'),
	('irving', 'irving'),
	('liquor', 'nb liquor'),
	('aliant', 'bell'),
	('bell', 'bell'),
	('bk', 'burger king'),
	('burger king', 'burger king'),
	('cineplex', 'cineplex'),
	('cnb', 'cnb'),
	('spotify', 'spotify'),
	('sobeys', 'sobeys'),
	('tim horton', 'tim horton'),
	('wendy', 'wendy'),
	('walmart', 'walmart'),
	('wal-mart', 'walmart'),
	('unb', 'unb'),
	('university of new', 'unb'),
	('wnba', 'wnba'),
	('dairy q', 'dairy queen'),
	('mcdon', 'mcdonalds'),
	('subway', 'subway'),
	('costco', 'costco'),
	('canadian tire', 'canadian tire'),
	('keiths service centre', 'keiths service centre')
	;
	
	SET @c2 = (SELECT COUNT(*) FROM @known);

	IF @nameIn IS NOT NULL BEGIN
		SET @nameIn = LOWER([dbo].[sv_RemoveNumbers]([dbo].[sv_RemoveSymbols](@nameIn)));
		WHILE @i < @c2 BEGIN
			SET @i = @i + 1;
			SET @kName = (SELECT [Name] FROM @known)
			IF @nameIn LIKE ('%' + @kName + '%') BEGIN
				SET @nameIn = @kName;
			END
		END
		SELECT @nameIn AS [ParsedName]
	END
	ELSE BEGIN
		DECLARE @AllNames AS TABLE ([ID] INTEGER IDENTITY(1, 1), [Name] NVARCHAR(MAX));
		INSERT INTO @AllNames SELECT LOWER([dbo].sv_RemoveSymbols([dbo].sv_RemoveNumbers([Entity]))) FROM [ScotiaTransactions];

		--SELECT * FROM @AllNames

		DECLARE @PreGroup AS TABLE ([ID] INTEGER IDENTITY(1, 1), [Name] NVARCHAR(MAX));

		DECLARE @h AS BIT;
		DECLARE @j AS INTEGER;
		DECLARE @c1 AS INTEGER;
		DECLARE @tName AS NVARCHAR(MAX);
		DECLARE @rName AS NVARCHAR(MAX);

		SET @c1 = (SELECT COUNT(*) FROM @AllNames);
		SET @i = 0;

		WHILE @i < @c1 BEGIN
			SET @i = @i + 1;
			SET @tName = (SELECT [Name] FROM @AllNames WHERE [ID] = @i);
			SET @j = 0;
			SET @h = 0;
			WHILE @j < @c2 BEGIN
				SET @j = @j + 1;
				SET @kName = (SELECT [Name] FROM @known WHERE [ID] = @j);
				IF @j = 1 BEGIN 
					PRINT '@tName: ' + @tName + ', @kName: ' + @kName;
				END
				IF @tName LIKE ('%' + @kName + '%') BEGIN
					SET @rName = (SELECT [KnownName] FROM @known WHERE [ID] = @j);
					INSERT INTO @PreGroup ([Name]) VALUES (@rName);
					SET @h = 1;
					SET @j = @c2;
				END
			END
			IF @h = 0 BEGIN
				INSERT INTO @PreGroup ([Name]) VALUES (@tName);
			END
		END

		--SELECT * FROM @PreGroup
		SELECT [Name] FROM @PreGroup GROUP BY [Name]
	END
END

--SELECT
--	[Entity]
--FROM (
--	SELECT LTRIM(RTRIM(REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--				REPLACE(
--					REPLACE(
--						LOWER([dbo].sv_RemoveSymbols([dbo].sv_RemoveNumbers([Entity]))),
--						'!',
--						''
--						),
--					'frede',
--					''),
--					'fred',
--					''
--				),
--					'wate',
--					''),
--					'dart',
--					''
--				),
--					'flor',
--					''),
--					'cent',
--					''
--				),
--					'rich',
--					''),
--					'toro',
--					''
--				),
--					'wood',
--					''),
--					'pert',
--					''
--				),
--					'fpos',
--					''),
--					'hanw',
--					''
--				),
--					'opos',
--					''),
--					'stoc',
--					''
--				),
--					'store',
--					''),
--					'restaurant',
--					''
--				),
--					'beec',
--					''),
--					'orom',
--					''
--				),
--					'lak',
--					''),
--					'bris',
--					''
--				),
--					'  ',
--					' '),
--					'rictonnbc',
--					''
--				),
--					'waas',
--					''),
--					'www',
--					''
--				),
--					'nbc',
--					''),
--					'q',
--					''
--				)
--				))
--	AS [Entity] FROM [ScotiaTransactions] GROUP BY [Entity]
--) AS [A]
--GROUP BY [Entity]
--ORDER BY [Entity]
----SELECT regexp_replace([Entity], '[[:digit:]]+', '#') FROM [ScotiaTransactions]