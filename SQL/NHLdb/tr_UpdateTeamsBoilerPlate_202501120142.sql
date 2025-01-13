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
-- Create date: <20258-01-12 0139>
-- Description:	<Maintain Boilerplate columns>
-- =============================================
CREATE TRIGGER [dbo].[tr_UpdateTeamsBoilerPlate] 
   ON [dbo].[Teams]
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
		[NHLdb].[dbo].[Teams]
	SET
		[LastModified] = GETDATE()
		, [DateCreated] = ISNULL([C].[DateCreated], GETDATE())
		, [DateActive] = (CASE 
			WHEN ([I].[Active] = 1) AND ([C].[DateActive] IS NULL) THEN
				GETDATE()
			ELSE
				[C].[DateActive] 
			END
		),
		[DateInactive] = (CASE 
			WHEN ([I].[Active] = 0) AND ([C].[DateInactive] IS NULL) THEN
				GETDATE()
			ELSE
				[C].[DateInactive] 
			END
		)

	FROM
		[NHLdb].[dbo].[Teams] [C]
	INNER JOIN
		INSERTED [I]
	ON
		[C].[ID] = [I].[ID]

	
	-- Set any deleted records to InActive
	UPDATE
		[NHLdb].[dbo].[Teams]
	SET
		[LastModified] = GETDATE()
		, [DateInActive] = GETDATE()
		, [Active] = 0
	FROM
		[NHLdb].[dbo].[Teams] [C]
	INNER JOIN
		DELETED [D]
	ON
		[C].[ID] = [D].[ID]

END
GO
