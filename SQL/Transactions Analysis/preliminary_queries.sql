SELECT  * FROM [ScotiaTransactions]ORDER BY [Date] DESC
SELECT  * FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%cnb%' ORDER BY [Date] DESC
SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%cnb%'
SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%cnb%' AND YEAR([Date]) = 2021
SELECT SUM(Amount) AS [Total Earned] FROM [ScotiaTransactions] WHERE [Amount] > 0
SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE [Amount] < 0
SELECT SUM(Amount) AS [Total Money] FROM [ScotiaTransactions]
SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%bws%'

SELECT * FROM [ScotiaTransactions] ORDER BY [Amount] DESC
SELECT * FROM [ScotiaTransactions] WHERE [Entity] = 'BKR Management Inc.' ORDER BY [Date] DESC

------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------

DECLARE @today AS DATETIME;
SET @today = GETDATE();

-- CNB
DECLARE @to_date_cnb AS FLOAT;
DECLARE @count_cnb AS INT;
DECLARE @first_date_cnb AS DATETIME;
DECLARE @last_date_cnb AS DATETIME;
SET @to_date_cnb = ABS((SELECT SUM([Amount]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%cnb%'))
SET @count_cnb = ((SELECT COUNT(*) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%cnb%'))
SET @first_date_cnb = ((SELECT MIN([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%cnb%'))
SET @last_date_cnb = ((SELECT MAX([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%cnb%'))


-- BWS
DECLARE @to_date_bws AS FLOAT;
DECLARE @count_bws AS INT;
DECLARE @first_date_bws AS DATETIME;
DECLARE @last_date_bws AS DATETIME;
SET @to_date_bws = ABS((SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%bws%'))
SET @count_bws = ((SELECT COUNT(*) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%bws%'))
SET @first_date_bws = ((SELECT MIN([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%bws%'))
SET @last_date_bws = ((SELECT MAX([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%bws%'))


-- Irving
DECLARE @to_date_irving AS FLOAT;
DECLARE @count_irving AS INT;
DECLARE @first_date_irving AS DATETIME;
DECLARE @last_date_irving AS DATETIME;
SET @to_date_irving = ABS((SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%irving%'))
SET @count_irving = ((SELECT COUNT(*) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%irving%'))
SET @first_date_irving = ((SELECT MIN([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%irving%'))
SET @last_date_irving = ((SELECT MAX([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%irving%'))


-- BK
DECLARE @to_date_bk AS FLOAT;
DECLARE @count_bk AS INT;
DECLARE @first_date_bk AS DATETIME;
DECLARE @last_date_bk AS DATETIME;
SET @to_date_bk = ABS((SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE [Entity] = 'BKR Management Inc.'))
SET @count_bk = ((SELECT COUNT(*) AS [Total Spent] FROM [ScotiaTransactions] WHERE [Entity] = 'BKR Management Inc.'))
SET @first_date_bk = ((SELECT MIN([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE [Entity] = 'BKR Management Inc.'))
SET @last_date_bk = ((SELECT MAX([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE [Entity] = 'BKR Management Inc.'))


-- Irving
DECLARE @to_date_amazon AS FLOAT;
DECLARE @count_amazon AS INT;
DECLARE @first_date_amazon AS DATETIME;
DECLARE @last_date_amazon AS DATETIME;
SET @to_date_amazon = ABS((SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))
SET @count_amazon = ((SELECT COUNT(*) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))
SET @first_date_amazon = ((SELECT MIN([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))
SET @last_date_amazon = ((SELECT MAX([Date]) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%amaz%'))



--DECLARE @to_date_bws AS FLOAT;
--SET @to_date_bws = ABS((SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%bws%'))

--DECLARE @to_date_irving AS FLOAT;
--SET @to_date_irving = ABS((SELECT SUM(Amount) AS [Total Spent] FROM [ScotiaTransactions] WHERE LOWER([Entity]) LIKE '%irving%'))

--DECLARE @to_date_bk AS FLOAT;
--SET @to_date_bk = ABS((SELECT SUM([Amount]) FROM [ScotiaTransactions] WHERE [Entity] = 'BKR Management Inc.'))

-- Print Statements
PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' I have spent $ ' + CAST(CAST(@to_date_cnb AS MONEY) AS NVARCHAR(MAX)) + ' at CNB - Over ' + CAST(@count_cnb AS NVARCHAR(MAX)) + ' transactions - Between: ' + CAST(@first_date_cnb AS NVARCHAR(MAX)) + ' and ' + CAST(@last_date_cnb AS NVARCHAR(MAX)) + '.';
PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' I have spent $ ' + CAST(CAST(@to_date_irving AS MONEY) AS NVARCHAR(MAX)) + ' at CNB - Over ' + CAST(@count_irving AS NVARCHAR(MAX)) + ' transactions - Between: ' + CAST(@first_date_irving AS NVARCHAR(MAX)) + ' and ' + CAST(@last_date_irving AS NVARCHAR(MAX)) + '.';
PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' I have spent $ ' + CAST(CAST(@to_date_amazon AS MONEY) AS NVARCHAR(MAX)) + ' at Amazon - Over ' + CAST(@count_amazon AS NVARCHAR(MAX)) + ' transactions - Between: ' + CAST(@first_date_amazon AS NVARCHAR(MAX)) + ' and ' + CAST(@last_date_amazon AS NVARCHAR(MAX)) + '.';
PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' BWS has paid me $ ' + CAST(CAST(@to_date_bws AS MONEY) AS NVARCHAR(MAX)) + ' - Over ' + CAST(@count_bws AS NVARCHAR(MAX)) + ' transactions - Between: ' + CAST(@first_date_bws AS NVARCHAR(MAX)) + ' and ' + CAST(@last_date_bws AS NVARCHAR(MAX)) + '.';
PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' BWS has paid me $ ' + CAST(CAST(@to_date_bk AS MONEY) AS NVARCHAR(MAX)) + ' - Over ' + CAST(@count_bk AS NVARCHAR(MAX)) + ' transactions - Between: ' + CAST(@first_date_bk AS NVARCHAR(MAX)) + ' and ' + CAST(@last_date_bk AS NVARCHAR(MAX)) + '.';

SELECT * FROM [dbo].[tv_CollectEntityData]('bws', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('bkr', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('irving', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('amaz', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('amz', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('cnb', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('canada', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('sobeys', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('greco', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('wendy', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('mcd', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('goodlife', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('wal-mart', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('liquor', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('cineplex', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('cellar', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('unb', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('nslsc', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('horton', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('a&w', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('burger', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('dairy', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('jungle', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('spotify', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('domino', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('papa', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('energienb', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('skyfall', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('bell', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('ringo', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('manchu', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('paypal', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('colp', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('mark', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('fred', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('bath', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('flor', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('hart', DEFAULT, DEFAULT)
SELECT * FROM [dbo].[tv_CollectEntityData]('flor', DEFAULT, DEFAULT)

SELECT * FROM [dbo].[tv_CollectEntityData]('irving', '2021-01-01', '2021-12-31')



--PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' I have spent $ ' + CAST(CAST(@to_date_irving AS MONEY) AS NVARCHAR(MAX)) + ' at Irvings.';
--PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' BWS has paid me $ ' + CAST(CAST(@to_date_bws AS MONEY) AS NVARCHAR(MAX)) + '.';
--PRINT 'As of ''' + CAST(@today AS NVARCHAR(MAX)) + ''' BK has paid me $ ' + CAST(CAST(@to_date_bk AS MONEY) AS NVARCHAR(MAX)) + '.';