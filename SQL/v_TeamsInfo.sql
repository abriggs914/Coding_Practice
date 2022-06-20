USE [MWBAdb]
GO

/****** Object:  View [dbo].[v_TeamsInfo]    Script Date: 2022-06-19 11:58:39 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


ALTER VIEW [dbo].[v_TeamsInfo]
AS


	SELECT
		[Src].[TeamID]
		, [TeamName]
		, [Teams].[City]
		, [Teams].[Country]
		, [Teams].[DateAdded]
		, [Teams].[HomeGym]
		, [Teams].[IsActive]
		, [Teams].[LogoURL]
		, [Teams].[Mascot]
		, [Teams].[PrimaryColour]
		, [Teams].[Province]
		, [Teams].[SecondaryColour]
		, [Teams].[TertiaryColour]
		--, [Teams].*
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

		, SUM([NumPlayers]) AS [NumPlayers] -- Number Players
	FROM (
		SELECT 
			[Teams].[ID] AS [TeamID]
			, [Teams].[Name] AS [TeamName]
			, COUNT(*) AS [GP]
			, 0 AS [W]
			, 0 AS [L]
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PF] -- Points For
			, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PA] -- Points Against
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) - SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PD] -- Points Difference
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APF] -- Average Points For
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

			, 0 AS [NumPlayers] -- Number Players
		FROM
			[Teams]
		INNER JOIN
			[Games]
		ON
			[Teams].[ID] = [Games].[Winner]
			OR [Teams].[ID] = [Games].[Loser]
		GROUP BY
			[Teams].[ID]
			, [Teams].[Name]
		
		UNION

		SELECT 
			[Teams].[ID] AS [TeamID]
			, [Teams].[Name]
			, 0 AS [GP]
			, COUNT(*) AS [W]
			, 0 AS [L]
			, 0 AS [PF] -- Points For
			, 0 AS [PA] -- Points Against
			, 0 AS [PD] -- Points Difference
			, 0 AS [APF] -- Average Points For
			, 0 AS [APA] -- Average Points Against
	
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PFGW] -- Points For Game Win
			, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PAGW] -- Points Against Game Win
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) - SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PDGW] -- Points Difference Game Win
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APFGW] -- Average Points For Game Win
			, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APAGW] -- Average Points Against Game Win
	
			, 0 AS [PFGL] -- Points For Game Loss
			, 0 AS [PAGL] -- Points Against Game Loss
			, 0 AS [PDGL] -- Points Difference Game Loss
			, 0 AS [APFGL] -- Average Points For Game Loss
			, 0 AS [APAGL] -- Average Points Against Game Loss

			, 0 AS [NumPlayers] -- Number Players
		FROM
			[Teams]
		INNER JOIN
			[Games]
		ON
			[Teams].[ID] = [Games].[Winner]
		GROUP BY
			[Teams].[ID]
			, [Teams].[Name]
	
		UNION

		SELECT
			[Teams].[ID] AS [TeamID]
			,[Teams].[Name]
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
	
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PFGL] -- Points For Game Loss
			, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PAGL] -- Points Against Game Loss
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) - SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) AS [PDGL] -- Points Difference Game Loss
			, SUM((CASE WHEN [Winner] = [Teams].[ID] THEN [ScoreWinner] WHEN [Loser] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APFGL] -- Average Points For Game Loss
			, SUM((CASE WHEN [Loser] = [Teams].[ID] THEN [ScoreWinner] WHEN [Winner] = [Teams].[ID] THEN [ScoreLoser] ELSE 0 END)) / NULLIF((COUNT(*) + 0.0), 0.0) AS [APAGL] -- Average Points Against Game Loss

			, 0 AS [NumPlayers] -- Number Players
		FROM
			[Teams]
		INNER JOIN
			[Games]
		ON
			[Teams].[ID] = [Games].[Loser]
		GROUP BY
			[Teams].[ID]
			, [Teams].[Name]

		UNION

		SELECT 
			[Teams].[ID] AS [TeamID]
			, [Teams].[Name]
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
			, 0 AS [PDGL] -- Points Difference Game Loss
			, 0 AS [APFGL] -- Average Points For Game Loss
			, 0 AS [APAGL] -- Average Points Against Game Loss

			, COUNT(*) AS [NumPlayers] -- Number Players
		FROM
			[Teams]
		INNER JOIN
			[Players]
		ON
			[Teams].[ID] = [Players].[Team]
		WHERE
			[Players].[IsActive] = 1
		GROUP BY
			[Teams].[ID]
			, [Teams].[Name]

	) AS [Src]
	INNER JOIN
		[Teams]
	ON
		[Src].[TeamID] = [Teams].[ID]

	GROUP BY
		[TeamID]
		, [TeamName]
		, [Teams].[City]
		, [Teams].[Country]
		, [Teams].[DateAdded]
		, [Teams].[HomeGym]
		, [Teams].[IsActive]
		, [Teams].[LogoURL]
		, [Teams].[Mascot]
		, [Teams].[PrimaryColour]
		, [Teams].[Province]
		, [Teams].[SecondaryColour]
		, [Teams].[TertiaryColour]
--GO


