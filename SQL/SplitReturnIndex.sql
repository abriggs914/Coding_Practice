--SELECT
--	[Email],
--	SELECT TOP 1 [splited_data] FROM split_string([Name], ' '),
--	[Name],
--	'' AS [Custom Data 1],
--	'' AS [Custom Data 2]
--FROM
--	[ITR Customers]
--WHERE
--	[Name] <> 'UNKNOWN'


--USE [BWSdb]
--GO
--/****** Object:  UserDefinedFunction [dbo].[NBPhonify]    Script Date: 2023-05-02 12:41:35 PM ******/
--SET ANSI_NULLS ON
--GO
--SET QUOTED_IDENTIFIER ON
--GO

--	-- Use this function to quickly alter a phone number.
--	-- Removes country and provincial area codes.

----ALTER FUNCTION [dbo].[SplitReturnIndex](
----	@phrase_in NVARCHAR(MAX)
----	,@delim NVARCHAR(MAX)
----	,@idx INT = -1
----) RETURNS NVARCHAR(MAX)
----AS
----BEGIN

SET ANSI_PADDING OFF;

DECLARE
	@phrase_in NVARCHAR(MAX)
	,@delim NVARCHAR(MAX)
	,@idx INT = -1
;

SELECT
	@phrase_in = 'Avery is the coolest person ever!'
	,@delim = 'er'
	,@idx = 1
;

	--IF @delim COLLATE BINARY = '' COLLATE BINARY
	--BEGIN
	--IF CAST(@delim AS BINARY) = CAST('' AS BINARY)
	IF LEN(@delim + ';') > 1
	BEGIN
	
		DECLARE @lenPhrase AS INTEGER;
		DECLARE @lenDelim AS INTEGER;
		DECLARE @index AS INTEGER;
		DECLARE @isNeg AS BIT;
		DECLARE @x AS INTEGER;
		SELECT @lenDelim = LEN(@delim);
		SELECT @lenPhrase = LEN(@phrase_in);
		DECLARE @t AS TABLE([ID] INT IDENTITY(0, 1), [Word] NVARCHAR(MAX));
		INSERT INTO @t
		SELECT [splited_data] FROM split_string_idx(@phrase_in, @delim)
	
		SELECT @isNeg = (CASE WHEN @idx < 0 THEN 1 ELSE 0 END);
		SELECT @index = COUNT(*) FROM @t;
		IF ABS(@idx) >= @index BEGIN
			SELECT @idx = ABS(@idx) % (CASE WHEN @index = 0 THEN 1 ELSE @index END)
			IF @isNeg = 1 BEGIN
				SELECT @idx = @idx * -1;
			END
		END
		IF @idx < 0 BEGIN 
			SELECT @isNeg = 1;
			SELECT @index = @index + @idx;
		END
		ELSE BEGIN
			SELECT @index = @idx;
		END
		
		SELECT * FROM @t
		SELECT @x = LEN(Word) FROM @t WHERE [ID] = @index;
		IF @x > @lenDelim AND @lenDelim > 0 BEGIN
			SELECT @x = @x - @lenDelim + 1;
		END
		SELECT @x = (CASE WHEN @x < 0 THEN 0 ELSE @x END);
		
		SELECT @index AS [index], @x AS [x]
		SELECT '<' + RIGHT([Word], @x) + '>' AS [Aa] FROM @t WHERE [ID] = @index;
		--RETURN SELECT [Word] FROM @t WHERE [ID] = @index;
	END
	ELSE BEGIN			
		SELECT @phrase_in AS [Bb];
		--RETURN SELECT [Word] FROM @t WHERE [ID] = @index;
	END

SET ANSI_PADDING ON;

	--RETURN 
--END