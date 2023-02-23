DECLARE @t1 AS TABLE ([Val] INT);
INSERT INTO @t1 ([Val]) VALUES
(6),
(16),
(4),
(-45),
(5)
;
DECLARE @t2 AS TABLE ([Val] INT);
INSERT INTO @t2 ([Val]) VALUES
(3),
(16),
(77),
(-45),
(15)
;


SELECT * FROM @t1 LEFT JOIN @t2 ON [@t1].[Val] = [@t2].[Val]
SELECT * FROM @t1 INNER JOIN @t2 ON [@t1].[Val] = [@t2].[Val]
SELECT * FROM @t1 RIGHT JOIN @t2 ON [@t1].[Val] = [@t2].[Val]