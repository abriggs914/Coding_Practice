select CONVERT(VARCHAR,GETDATE(),1) + ' ' + RIGHT(CONVERT(VARCHAR,GETDATE(),9), 14)


DECLARE @TimeZone VARCHAR(50)
EXEC MASTER.dbo.xp_regread 'HKEY_LOCAL_MACHINE',
'SYSTEM\CurrentControlSet\Control\TimeZoneInformation',
'TimeZoneKeyName',@TimeZone OUT


select CONVERT(VARCHAR,GETDATE(),1) + ' ' + RIGHT(CONVERT(VARCHAR,GETDATE(),9), 14) + ' ' + @TimeZone