USE [master]
GO


-- Stored Procedure Demos
-- 2022-07-14


DECLARE @t AS DATETIME;			-- today
DECLARE @en AS NVARCHAR(MAX);	-- entity name
DECLARE @sd AS DATETIME;		-- start date
DECLARE @ed AS DATETIME;		-- end date
DECLARE @pd AS DATETIME;		-- prediction date
DECLARE @m AS NVARCHAR(MAX);	-- mode
DECLARE @ua AS BIT;				-- use absolutes


SET @t = GETDATE();
SET @en = 'BWS';
SET @sd = (SELECT TOP 1 [Date] FROM [ScotiaTransactions] ORDER BY [Date]);
SET @ed = DATEADD(YEAR, 5, @t);
SET @pd = DATEADD(YEAR, 1, @t);
SET @m = 'm';


SELECT
	* 
FROM
	[ScotiaTransactions]
WHERE
	[ScotiaTransactions].[Entity] LIKE '%' + @en + '%'
ORDER BY
	[Date] DESC
;

-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------


EXEC [sp_BalanceAsOf]
	@d=@t
;

EXEC [sp_AllBalancesAsOf]
	@date=@t
;

EXEC [sp_CollectEntityData]
	@entity_name=@en
	, @start_date=@sd
	, @end_date=@ed
;

EXEC [sp_EntityTransactionsAnalysis]
	@entity_name=@en
	, @start_date=@sd
	, @end_date=@ed
	, @mode=@m
	, @use_absolutes=@ua
;

EXEC [sp_GroupEntities]
	@nameIn=@en
;

EXEC [sp_ProjectBalanceAsOf]
	@date=@pd
	, @entity_name=@en
	, @mode=@m
	, @start_date=@sd
	, @end_date=@ed
;
