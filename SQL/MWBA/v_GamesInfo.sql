USE MWBAdb
GO

CREATE VIEW [dbo].[v_GamesInfo]
AS
	SELECT
		[Games].*
		, [Games].[ScoreWinner] - [Games].[ScoreLoser] AS [Diff]
		, (SELECT [Teams].[Name] FROM [Teams] WHERE [Winner] = [Teams].[ID]) AS [WinnerTeam]
		, (SELECT [Teams].[Name] FROM [Teams] WHERE [Loser] = [Teams].[ID]) AS [LoserTeam]
		, (SELECT [Teams].[City] FROM [Teams] WHERE [HostTeam] = [Teams].[ID]) AS [Location]
	FROM
		[Games]