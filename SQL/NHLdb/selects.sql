SELECT
	'Teams' AS [T]
	, *
FROM
	[NHLdb].[dbo].[Teams]
WHERE
	[Active] = 1
;

SELECT
	'LeagueYears' AS [T]
	, *
FROM
	[NHLdb].[dbo].[LeagueYears]
;

SELECT
	'Conferences' AS [T]
	, *
FROM
	[NHLdb].[dbo].[Conferences]
WHERE
	[Active] = 1
;

SELECT
	'Divisions' AS [T]
	, *
FROM
	[NHLdb].[dbo].[Divisions]
WHERE
	[Active] = 1
;

SELECT
	'LeagueStructures' AS [T]
	, *
FROM
	[NHLdb].[dbo].[LeagueStructures]
;

SELECT
	'GameTypes' AS [T]
	, *
FROM
	[NHLdb].[dbo].[GameTypes]
WHERE
	[Active] = 1
;


SELECT
	[T].[Abbrev]
	, [LY].[ID] AS [LeagueYearID]
	, [T].[ID] AS [TeamID]
	, (CASE 
		WHEN [T].[Abbrev] IN ('BOS', 'BUF', 'DET', 'FLA', 'MTL', 'OTT', 'TBL', 'TOR', 'CAR', 'CBJ', 'NJD', 'NYI', 'NYR', 'PHI', 'PIT', 'WSH') THEN 2
		WHEN [T].[Abbrev] IN ('CHI', 'COL', 'DAL', 'MIN', 'NSH', 'STL', 'UTA', 'WPG', 'ANA', 'CGY', 'EDM', 'LAK', 'SEA', 'SJS', 'VAN', 'VGK', 'ARI') THEN 3
		ELSE NULL
	END) AS [ConferenceID]
	, (CASE 
		WHEN [T].[Abbrev] IN ('BOS', 'BUF', 'DET', 'FLA', 'MTL', 'OTT', 'TBL', 'TOR') THEN 7
		WHEN [T].[Abbrev] IN ('CAR', 'CBJ', 'NJD', 'NYI', 'NYR', 'PHI', 'PIT', 'WSH') THEN 8
		WHEN [T].[Abbrev] IN ('CHI', 'COL', 'DAL', 'MIN', 'NSH', 'STL', 'UTA', 'WPG', 'ARI') THEN 9
		WHEN [T].[Abbrev] IN ('ANA', 'CGY', 'EDM', 'LAK', 'SEA', 'SJS', 'VAN', 'VGK') THEN 10
		ELSE NULL
	END) AS [DivisionID]
FROM
	[NHLdb].[dbo].[LeagueYears] [LY]
CROSS JOIN (
	SELECT
		[T].[ID]
		,[T].[Abbrev]
	FROM
		[NHLdb].[dbo].[Teams] [T]
	WHERE
		([T].[Active] = 1)
		OR ([T].[Abbrev] IN ('ARI'))
) AS [T]
WHERE
	([LY].[ChampYear] IN (2025, 2024, 2023))
	AND (
		(CASE
			WHEN (([T].[Abbrev] = 'ARI') AND ([LY].[ChampYear] = 2025)) THEN 0
			WHEN (([T].[Abbrev] = 'UTA') AND ([LY].[ChampYear] < 2025)) THEN 0
			ELSE 1
		END) = 1
	)
ORDER BY
	[LY].[ID]
	, [T].[Abbrev]



SELECT
	[T].[Abbrev]
	,[C].[Name]
	,[D].[Name]
	,[LY].[YearStr]
FROM
	[NHLdb].[dbo].[LeagueStructures] [LS]
INNER JOIN
	[NHLdb].[dbo].[LeagueYears] [LY]
ON
	[LS].[LeagueYearID] = [LY].[ID]
INNER JOIN
	[NHLdb].[dbo].[Conferences] [C]
ON
	[LS].[ConferenceID] = [C].[ID]
INNER JOIN
	[NHLdb].[dbo].[Divisions] [D]
ON
	[LS].[DivisionID] = [D].[ID]
INNER JOIN
	[NHLdb].[dbo].[Teams] [T]
ON
	[LS].[TeamID] = [T].[ID]
WHERE
	[LY].[ChampYear] = 2025
;