
BEGIN TRAN;

DECLARE @i INT, @c INT;
DECLARE @f AS NVARCHAR(MAX);
SELECT @i = 1;
SELECT @c = COUNT(*) FROM [Projects];

DECLARE @idxThingiverse INT;


	DECLARE   @Details  NVARCHAR(MAX)
            , @Sql      NVARCHAR(MAX);

WHILE @i <= @c BEGIN

	SELECT @f = [Folder] + '\README.txt' FROM [Projects] WHERE [ID] = @i;

	BEGIN TRY
		SET @Sql = N' SELECT @Details = BulkColumn
                  FROM OPENROWSET(BULK ''' + @f + ''',SINGLE_CLOB) JSON;';

		Exec sp_executesql @Sql
			              , N'@Details  NVARCHAR(MAX) OUTPUT'
				          , @Details OUTPUT;
	END TRY
	BEGIN CATCH
		SELECT  
        CONCAT  ('Error Number:',ERROR_NUMBER()
                ,'|Error Message:',ERROR_MESSAGE()
                ,'|Error Procedure:',ERROR_PROCEDURE()) AS 'Error'

		SELECT @Details = '';
	END CATCH

	SELECT @idxThingiverse = CHARINDEX('Thingiverse', @Details);

	IF @idxThingiverse <> 0 BEGIN
		SELECT @Details = LTRIM(RTRIM(RIGHT(@Details, LEN(@Details) - (11 + @idxThingiverse))))
		UPDATE
			[Projects]
		SET
			[URL] = @Details
			WHERE 
				[ID] = @i;
	END
	ELSE BEGIN
		UPDATE
			[Projects]
		SET
			[URL] = NULL
			WHERE 
				[ID] = @i;
	END



	
	--SELECT
	--	@fileText = (SELECT * FROM OPENROWSET(BULK @f, SINGLE_CLOB)
	--	AS Contents)
		

	--UPDATE
	--	[Projects]
	--SET
	--	[URL] =
	--	(SELECT BulkColumn FROM OPENROWSET (BULK [Folder] + '\README.txt', SINGLE_BLOB) a)
	--	FROM [Projects]
	--	WHERE (CriteriaField = @criteria)
		
		
	--	(OPENROWSET(BULK ([Folder] + '\README.txt'), SINGLE_CLOB)	AS Contents)
	--FROM 
	--	[Projects]

	SELECT @i = @i + 1;
END

SELECT
	[Name]
	, [URL]
FROM
	[Projects]

--DECLARE @idxThingiverse INT;
--DECLARE @url NVARCHAR(MAX);
--SELECT @idxThingiverse = CHARINDEX('Thingiverse', @fileText);

--IF @idxThingiverse <> 0 BEGIN
--	SELECT @url = LTRIM(RTRIM(RIGHT(@fileText, LEN(@fileText) - (11 + @idxThingiverse))))
--END

--SELECT @url AS [URL]

ROLLBACK;
COMMIT;