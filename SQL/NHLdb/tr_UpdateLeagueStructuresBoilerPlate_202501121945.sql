USE [NHLdb]
GO
/****** Object:  Trigger [dbo].[tr_UpdateLeagueStructuresBoilerPlate]    Script Date: 2025-01-12 7:44:18 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Avery Briggs>
-- Create date: <2025-01-12 1944>
-- Description:	<Maintain Boilerplate columns>
-- =============================================
CREATE TRIGGER [dbo].[tr_UpdateLeagueStructuresBoilerPlate] 
   ON [dbo].[LeagueStructures]
   AFTER INSERT, DELETE, UPDATE
AS 
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	-- Prevent recursive calls
	IF TRIGGER_NESTLEVEL() > 1 BEGIN
		RETURN;
	END

	UPDATE
		[NHLdb].[dbo].[LeagueStructures]
	SET
		[LastModified] = GETDATE()
		, [DateCreated] = ISNULL([C].[DateCreated], GETDATE())
	FROM
		[NHLdb].[dbo].[LeagueStructures] [C]
	INNER JOIN
		INSERTED [I]
	ON
		[C].[ID] = [I].[ID]

END
