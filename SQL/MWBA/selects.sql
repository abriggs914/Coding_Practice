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

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ID]
      ,[Name]
      ,[Country]
      ,[Province]
      ,[City]
  FROM [MWBAdb].[dbo].[Affiliations]

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

  
SELECT
	[Players].[Name] AS [PlayerName],
	[Teams].[Name] AS [TeamName],
	[Affiliations].[Name] AS [CurrentAffiliation]
FROM
	[Players]
LEFT JOIN
	[Teams]
ON
	[Players].[Team] = [Teams].[ID]
LEFT JOIN
	[Affiliations]
ON
	[Players].[Affiliation] = [Affiliations].[ID]


SELECT
	[Players].[Name] AS [PlayerName],
	[Teams].[Name] AS [TeamName],
	[Affiliations].[Name] AS [CurrentAffiliation]
FROM
	[Players]
LEFT JOIN
	[Teams]
ON
	[Players].[Team] = [Teams].[ID]
LEFT JOIN
	[Affiliations]
ON
	[Players].[Affiliation] = [Affiliations].[ID]
ORDER BY
	[Affiliations].[Name] 