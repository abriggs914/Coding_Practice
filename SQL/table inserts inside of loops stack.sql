DECLARE @i INT = 0;

WHILE @i < 3
BEGIN
    DECLARE @chartonum TABLE
    (
        [Character] CHAR(1),
        [Number] INT
    );

    INSERT INTO @chartonum
    VALUES ('A', 1), ('B', 2);

    SELECT  'Row count: ' + CAST((SELECT COUNT(*) FROM @chartonum) AS NVARCHAR(10))
    
    SET @i = @i + 1;
END
