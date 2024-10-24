USE [master]
GO
/****** Object:  UserDefinedFunction [dbo].[RemoveNumbers]    Script Date: 2021-12-06 11:59:27 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- https://social.msdn.microsoft.com/forums/sqlserver/en-US/cbfe653f-7de6-4043-9258-e3a3f8822442/replacing-numbers-from-a-string

ALTER FUNCTION [dbo].[RemoveNumbers] 
( 
  @BadString nvarchar(MAX) 
) 
RETURNS nvarchar(MAX) 
AS 
BEGIN 
 
      DECLARE @nPos INTEGER 
      SELECT @nPos = PATINDEX('%[0-9]%', @BadString) 
 
      WHILE @nPos > 0 
      BEGIN 
            SELECT @BadString = STUFF(@BadString, @nPos, 1, '') 
            SELECT @nPos = PATINDEX('%[0-9]%', @BadString) 
      END 
 
      RETURN @BadString 
END 