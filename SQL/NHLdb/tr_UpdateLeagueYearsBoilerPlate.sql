-- ================================================
-- Template generated from Template Explorer using:
-- Create Trigger (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- See additional Create Trigger templates for more
-- examples of different Trigger statements.
--
-- This block of comments will not be included in
-- the definition of the function.
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Avery Briggs>
-- Create date: <2025-01-12 1742>
-- Description:	<Maintain boilerplate>
-- =============================================
CREATE TRIGGER [tr_UpdateLeagueYearsBoilerPlate]
   ON  [dbo].[LeagueYears]
   AFTER INSERT,DELETE,UPDATE
AS 
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for trigger here
	
	-- Prevent recursive calls
	IF TRIGGER_NESTLEVEL() > 1 BEGIN
		RETURN;
	END

	UPDATE
		[NHLdb].[dbo].[LeagueYears]
	SET
		[LastModified] = GETDATE()
		, [DateCreated] = ISNULL([C].[DateCreated], GETDATE())
	FROM
		[NHLdb].[dbo].[LeagueYears] [C]
	INNER JOIN
		INSERTED [I]
	ON
		[C].[ID] = [I].[ID]


END
GO
