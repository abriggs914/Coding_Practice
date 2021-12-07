USE [master]
GO
/****** Object:  UserDefinedFunction [dbo].[sv_RemoveNumbers]    Script Date: 2021-12-07 12:03:04 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER FUNCTION [dbo].[sv_RemoveSymbols] 
( 
  @BadString nvarchar(MAX) 
) 
RETURNS nvarchar(MAX) 
AS 
BEGIN 

	DECLARE @invalid TABLE ([Sym] NVARCHAR(1));
	INSERT INTO @invalid ([Sym]) VALUES
	('!'),
	('@'),
	('#'),
	('$'),
	('%'),
	('^'),
	('&'),
	('*'),
	('('),
	(')'),
	('_'),
	('-'),
	('+'),
	('='),
	('['),
	(']'),
	('{'),
	('}'),
	(';'),
	(':'),
	(''''),
	('"'),
	(','),
	('<'),
	('.'),
	('>'),
	('?'),
	('/'),
	('\'),
	('|'),
	('`'),
	('~');
 
	DECLARE @NewString AS NVARCHAR(MAX);
	DECLARE @nPos AS INTEGER 
	DECLARE @i AS INTEGER 
	DECLARE @char AS NVARCHAR(1);
	SELECT @nPos = LEN(@BadString) 
	
	SET @NewString = '';
	SET @i = 1;
	WHILE @nPos > @i
	BEGIN 
		SET @char = SUBSTRING(@BadString, @i, @i)
		IF @char NOT IN (SELECT [Sym] FROM @invalid) BEGIN
			SELECT @NewString = @NewString + @char
		END
		SELECT @i = @i + 1
	END 
	
	RETURN @NewString 

END 