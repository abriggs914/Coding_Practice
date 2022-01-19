USE BWSdb
GO

--	EndOf AND FirstOf AND Add AND Sub
--		Day
--		Week
--		Month
--		Year

DECLARE @d AS DATETIME;
DECLARE @t AS DATETIME;

SET @d = '2022-01-18';

-- End of Day
SELECT @d AS [Original], CAST(CAST(YEAR(@d) AS NVARCHAR(4)) + '-' + CAST(MONTH(@d) AS NVARCHAR(2)) + '-' + CAST(DAY(@d) AS NVARCHAR(2)) + ' 23:59:59' AS DATETIME) AS [End Of Day]

-- End of Week
SET @d = '2019-03-03';
SET @t = @d;
WHILE DATEPART(WEEK, @d) = DATEPART(WEEK, DATEADD(DAY, 1, @t)) BEGIN
	SET @t = DATEADD(DAY, 1, @t)
END
SET @t = DATEADD(HOUR, 23, DATEADD(MINUTE, 59, DATEADD(SECOND, 59, CAST(CAST(YEAR(@t) AS NVARCHAR(4)) + '-' + CAST(MONTH(@t) AS NVARCHAR(2)) + '-' + CAST(DAY(@t) AS NVARCHAR(2)) AS DATETIME))))
SELECT @d AS [Original], @t AS [End Of Week]

-- End of Month
SET @t = DATEADD(MONTH, 1, @d);
WHILE DATEPART(MONTH, DATEADD(DAY, 1, @t)) = DATEPART(MONTH, @t) BEGIN
	SET @t = DATEADD(DAY, 1, @t);
END
SELECT @d AS [Original], @t AS [End Of Month], 'IsSP' AS [IsSP]

-- End of Year
SELECT @d AS [Original], CAST(CAST(YEAR(@d) AS NVARCHAR(4)) + '-12-31 23:59:59' AS DATETIME) AS [End Of Year]

-- First of Year
SELECT @d AS [Original], CAST(CAST(YEAR(@d) AS NVARCHAR(4)) + '-01-01' AS DATETIME) AS [First Of Year]

-- Add 1 Day
SET @t = DATEADD(DAY, 1, @d);
SELECT @d AS [Original], @t AS [Add 1 Day]

-- Add 1 Month
SET @d = '2020-01-29';
SET @t = DATEADD(DAY, 27, @d);
--WHILE MONTH(@d) = MONTH(@t) OR (MONTH(@d) <> MONTH(@t) AND DAY(@t) < DAY(@d)) BEGIN
WHILE MONTH(@d) = MONTH(@t) OR (MONTH(@d) < MONTH(@t) AND DAY(@t) < DAY(@d) ) BEGIN
	PRINT 'month: ' + CAST(@t AS NVARCHAR(MAX))
	SET @t = DATEADD(DAY, 1, @t)
END
SELECT @d AS [Original], @t AS [Add 1 Month]

-- Add 1 Year
DECLARE @inc AS INT;
SET @inc = 365;
SET @d = '2020-01-29';
SET @t = DATEADD(DAY, 363, @d);
WHILE DATEDIFF(DAY, @d, @t) < @inc BEGIN
	SET @t = DATEADD(DAY, 1, @t)
	IF MONTH(@d) = MONTH(@t) AND DAY(@t) < (DAY(@d) - 1) BEGIN
		SET @t = DATEADD(DAY, 1, @t)
		SET @inc = @inc + 1;
	END
END
SELECT @d AS [Original], @t AS [Add 1 Year]

--

SELECT DATEPART(WEEK, @d)

