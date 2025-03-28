USE [NHLdb]
GO
/****** Object:  Trigger [dbo].[tr_UpdateDivisionsBoilerPlate]    Script Date: 2025-01-12 7:00:17 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Avery Briggs>
-- Create date: <2025-01-12 1900>
-- Description:	<Maintain Boilerplate columns>
-- =============================================
CREATE TRIGGER [dbo].[tr_UpdateDivisionsBoilerPlate] 
   ON [dbo].[Divisions]
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
		[NHLdb].[dbo].[Divisions]
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
		[NHLdb].[dbo].[Divisions] [C]
	INNER JOIN
		INSERTED [I]
	ON
		[C].[ID] = [I].[ID]

	
	-- Set any deleted records to InActive
	UPDATE
		[NHLdb].[dbo].[Divisions]
	SET
		[LastModified] = GETDATE()
		, [DateInActive] = GETDATE()
		, [Active] = 0
	FROM
		[NHLdb].[dbo].[Divisions] [C]
	INNER JOIN
		DELETED [D]
	ON
		[C].[ID] = [D].[ID]

END
