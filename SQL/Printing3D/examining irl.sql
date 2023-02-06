
DECLARE @fileText NVARCHAR(MAX);
SELECT
	@fileText = (SELECT *
FROM
	OPENROWSET(BULK N'D:\3D Prints\Bed Level Test\Test2\README.txt', SINGLE_CLOB)
	AS Contents)

DECLARE @idxThingiverse INT;
DECLARE @url NVARCHAR(MAX);
SELECT @idxThingiverse = CHARINDEX('Thingiverse', @fileText);

IF @idxThingiverse <> 0 BEGIN
	SELECT @url = LTRIM(RTRIM(RIGHT(@fileText, LEN(@fileText) - (11 + @idxThingiverse))))
END

SELECT @url AS [URL]