

SET ANSI_PADDING OFF;
SELECT
	(CASE WHEN ' ' = '' THEN 1 ELSE 0 END) AS [A],
	(CASE WHEN '' = '' THEN 1 ELSE 0 END) AS [B],
	(CASE WHEN ' ' = ' ' THEN 1 ELSE 0 END) AS [C],
	(CASE WHEN ';' = ' ' THEN 1 ELSE 0 END) AS [D]

SET ANSI_PADDING ON;
SELECT
	(CASE WHEN ' ' = '' THEN 1 ELSE 0 END) AS [A],
	(CASE WHEN '' = '' THEN 1 ELSE 0 END) AS [B],
	(CASE WHEN ' ' = ' ' THEN 1 ELSE 0 END) AS [C],
	(CASE WHEN ';' = ' ' THEN 1 ELSE 0 END) AS [D]
	

SET ANSI_PADDING ON;
SELECT
	LEN('k ') AS [A]
	,LEN('k  ') AS [B]
	,LEN('k   ') AS [C]
	,LEN('k    ') AS [D]
	,LEN('k     ') AS [E]
	,LEN(' ') AS [F]
	,LEN('  ') AS [G]
	,LEN('   ') AS [H]
	,LEN('    ') AS [I]
	,LEN('     ') AS [J]
	,LEN(' k') AS [K]
	,LEN('  k') AS [L]
	,LEN('   k') AS [M]
	,LEN('    k') AS [N]
	,LEN('     k') AS [O]