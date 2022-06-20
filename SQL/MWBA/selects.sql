/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ID]
      ,[Name]
      ,[Country]
      ,[Province]
      ,[City]
      ,[HomeGym]
      ,[Mascot]
      ,[DateAdded]
      ,[PrimaryColour]
      ,[SecondaryColour]
      ,[TertiaryColour]
      ,[IsActive]
      ,[LogoURL]
  FROM [MWBAdb].[dbo].[Teams]
;

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ID]
      ,[Name]
      ,[Country]
      ,[Province]
      ,[City]
  FROM [MWBAdb].[dbo].[Affiliations]
;

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ID]
      ,[Name]
      ,[Affiliation]
      ,[AffiliationsAr]
      ,[Team]
      ,[TeamsAr]
      ,[IsActive]
      ,[DateAdded]
      ,[Number]
      ,[NumbersAr]
  FROM [MWBAdb].[dbo].[Players]
;

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ID]
      ,[Date]
      ,[HostTeam]
      ,[Winner]
      ,[Loser]
      ,[ScoreWinner]
      ,[ScoreLoser]
  FROM [MWBAdb].[dbo].[Games]
;

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ID]
      ,[Name]
      ,[Team]
      ,[IsActive]
      ,[IsHeadCoach]
      ,[DateAdded]
  FROM [MWBAdb].[dbo].[Coaches]

  
SELECT
	[Players].[Name] AS [PlayerName],
	[Teams].[Name] AS [TeamName],
	[Affiliations].[Name] AS [CurrentAffiliation]
FROM
	[Players]
INNER JOIN
	[Teams]
ON
	[Players].[Team] = [Teams].[ID]
INNER JOIN
	[Affiliations]
ON
	[Players].[Affiliation] = [Affiliations].[ID]
;

SELECT
	[Players].[Name] AS [PlayerName],
	[Teams].[Name] AS [TeamName],
	[Affiliations].[Name] AS [CurrentAffiliation]
FROM
	[Players]
INNER JOIN
	[Teams]
ON
	[Players].[Team] = [Teams].[ID]
INNER JOIN
	[Affiliations]
ON
	[Players].[Affiliation] = [Affiliations].[ID]
ORDER BY
	[Affiliations].[Name]
;

SELECT 
	*
FROM
	[Teams]
INNER JOIN
	[Games]
ON
	[Teams].[ID] = [Games].[Winner]
;

-- count # games played

SELECT 
	[TeamName]
	, SUM([GP]) AS [GP] -- Games Played
	, SUM([W]) AS [W] -- Wins
	, SUM([L]) AS [L] -- Losses
	, SUM([PF]) AS [PF] -- Points For
	, SUM([PA]) AS [PA] -- Points Against
	, SUM([PD]) AS [PD] -- Points Difference
	, SUM([APF]) AS [APF] -- Average Points For
	, SUM([APA]) AS [APA] -- Average Points Against
	
	, SUM([PFGW]) AS [PFGW] -- Points For Game Win
	, SUM([PAGW]) AS [PAGW] -- Points Against Game Win
	, SUM([PDGW]) AS [PDGW] -- Points Difference Game Win
	, SUM([APFGW]) AS [APFGW] -- Average Points For Game Win
	, SUM([APAGW]) AS [APAGW] -- Average Points Against Game Win
	
	, SUM([PFGL]) AS [PFGL] -- Points For Game Loss
	, SUM([PAGL]) AS [PAGL] -- Points Against Game Loss
	, SUM([PDGL]) AS [PDGL] -- Points Difference Game Loss
	, SUM([APFGL]) AS [APFGL] -- Average Points For Game Loss
	, SUM([APAGL]) AS [APAGL] -- Average Points Against Game Loss
FROM (
	SELECT 
		[Teams].[Name] AS [TeamName]
		, COUNT(*) AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0.0 AS [APF] -- Average Points For
		, 0.0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0.0 AS [APFGW] -- Average Points For Game Win
		, 0.0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0.0 AS [APFGL] -- Average Points For Game Loss
		, 0.0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
		OR [Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]

	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, COUNT(*) AS [W]
		, 0 AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
	GROUP BY
		[Teams].[Name]

	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, COUNT(*) AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
		OR [Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
		OR [Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) - SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
		OR [Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
		OR [Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
		OR [Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) - SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Winner]
	GROUP BY
		[Teams].[Name]
























		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) - SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APFGL] -- Average Points For Game Loss
		, 0 AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]
		
	UNION

	SELECT 
		[Teams].[Name]
		, 0 AS [GP]
		, 0 AS [W]
		, 0 AS [L]
		, 0 AS [PF]-- + SUM([ScoreLoser]) AS [PF] -- Points For
		, 0 AS [PA] -- Points Against
		, 0 AS [PD] -- Points Difference
		, 0 AS [APF] -- Average Points For
		, 0 AS [APA] -- Average Points Against
	
		, 0 AS [PFGW] -- Points For Game Win
		, 0 AS [PAGW] -- Points Against Game Win
		, 0 AS [PDGW] -- Points Difference Game Win
		, 0 AS [APFGW] -- Average Points For Game Win
		, 0 AS [APAGW] -- Average Points Against Game Win
	
		, 0 AS [PFGL] -- Points For Game Loss
		, 0 AS [PAGL] -- Points Against Game Loss
		, 0 AS [PDGL] -- Points Difference Game Loss
		, 0 AS [APFGL] -- Average Points For Game Loss
		, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APAGL] -- Average Points Against Game Loss
	FROM
		[Teams]
	INNER JOIN
		[Games]
	ON
		[Teams].[ID] = [Games].[Loser]
	GROUP BY
		[Teams].[Name]








) AS [Src]

GROUP BY
	[TeamName]
ORDER BY
	[TeamName]

;

SELECT * FROM [v_GamesInfo];
SELECT * FROM [v_TeamsInfo];
SELECT sum([PD]) FROM [v_TeamsInfo];
