USE [master]
GO
/****** Object:  UserDefinedFunction [dbo].[tv_CollectEntityData]    Script Date: 2021-12-05 5:07:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
ALTER FUNCTION [dbo].[tv_CollectEntityData] 
(	
	-- Add the parameters for the function here
	@entity_name AS NVARCHAR(MAX),
	@start_date AS DATETIME = NULL,
	@end_date AS DATETIME = NULL
)
RETURNS TABLE 
AS
RETURN 
(
	-- Add the SELECT statement with parameter references here
	SELECT 
		@entity_name AS [Entity Search Pattern],
		SUM([Amount]) AS [Total Spent],
		MAX([Amount]) AS [Max Credit],
		MIN([Amount]) AS [Min Debit],
		AVG([Amount]) AS [Avg Amount],
		COUNT(*) AS [# Transactions],
		MIN([Date]) AS [First Date],
		MAX([Date]) AS [Last Date],
		DATEDIFF(DAY, MIN([Date]), MAX([Date])) AS [# Days],
		SUM([Amount]) / (CASE WHEN DATEDIFF(DAY, MIN([Date]), MAX([Date])) = 0 THEN 1 ELSE DATEDIFF(DAY, MIN([Date]), MAX([Date])) END) AS [$ / Day]
	FROM 
		[ScotiaTransactions]
	WHERE
		LOWER([Entity]) LIKE LOWER('%' + @entity_name + '%')
		AND 1 = 
		(CASE WHEN @start_date IS NULL AND @end_date IS NULL THEN 1 ELSE 
			(CASE WHEN @end_date IS NULL THEN 
				(CASE WHEN [Date] >= @start_date THEN 1 ELSE 0 END) ELSE 
					(CASE WHEN @start_date IS NULL THEN
						(CASE WHEN [Date] <= @end_date THEN 1 ELSE 0 END) ELSE 
							(CASE WHEN [Date] BETWEEN @start_date AND @end_date THEN 1 ELSE 0 END) END) END) END)
--	SET @to_date_amazon = ABS((SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))
--SET @count_amazon = ((SELECT COUNT(*) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))
--SET @first_date_amazon = ((SELECT MIN([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))
--SET @last_date_amazon = ((SELECT MAX([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))
)
