USE BWSdb
GO

DECLARE @d AS DATETIME;
DECLARE @t AS DATETIME;

SET @d = '2022-01-18';

-- End of Year
SELECT @d AS [Original], CAST(CAST(YEAR(@d) AS NVARCHAR(4)) + '-12-31 23:59:59' AS DATETIME) AS [End Of Year]
-- First of Year
SELECT @d AS [Original], CAST(CAST(YEAR(@d) AS NVARCHAR(4)) + '-01-01' AS DATETIME) AS [First Of Year]

-- Add 1 Year
DECLARE @inc AS INT;
SET @inc = 365;
SET @d = '2019-02-28';
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

