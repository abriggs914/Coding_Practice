import tkinter

from tkinter_utility import *
from pyodbc_connection import connect


if __name__ == '__main__':

    app = tkinter.Tk()
    w, h = 500, 500
    app.geometry(f"{w}x{h}")

    sql_req = """
    SELECT
        CAST([RequestDate] AS DATE) AS [RequestDate],
        [RequestedBy],
        COUNT(*) AS [RequestedToday]
    FROM
        [Calendar]
    LEFT JOIN
        [IT Requests]
    ON
        CAST([RequestDate] AS DATE) = [Date]
    GROUP BY
        CAST([RequestDate] AS DATE),
        [RequestedBy]
    ;
    """


    new_sql = """
        USE BWSdb
GO

DECLARE @d1 AS DATETIME;
DECLARE @d2 AS DATETIME;

SELECT @d1 = MIN([RequestDate]), @d2 = MAX([RequestDate]) FROM [IT Requests]

DECLARE @people AS TABLE ([ID] INT IDENTITY(0, 1), [Name] NVARCHAR(MAX), [Count] INT);
DECLARE @dates AS TABLE ([ID] INT IDENTITY(0, 1), [Date] DATETIME DEFAULT(0));

INSERT INTO @people
SELECT DISTINCT [RequestedBy], 0 FROM [IT Requests]

INSERT INTO @dates
SELECT [Date] FROM [Calendar] WHERE [Date] BETWEEN @d1 AND @d2

DECLARE @data AS TABLE ([ID] INT IDENTITY(0, 1), [RequestDate] DATETIME, [RequestedBy] NVARCHAR(MAX), [RequestedToday] INT);

INSERT INTO @data
SELECT
        [Date] AS [RequestDate],
        [Name] AS [RequestedBy],
        COUNT(*) - 1 AS [RequestedToday]
	FROM (
		SELECT
			[Date],
			[Name]
		FROM
			@dates
		CROSS JOIN
			@people
	) AS [A]
	LEFT JOIN
		[IT Requests]
	ON
		[Date] = CAST([RequestDate] AS DATE)
		AND [Name] = [RequestedBy]
	GROUP BY
        [Date],
        [Name]
	ORDER BY
        [Date],
        [Name]

	

--SELECT
--        [Date] AS [RequestDate],
--        [RequestedBy],
--        COUNT(*) AS [RequestedToday]
--    FROM
--        [Calendar]
--    LEFT JOIN
--        [IT Requests]
--    ON
--        CAST([RequestDate] AS DATE) = [Date]
--    GROUP BY
--        [Date],
--        [RequestedBy]
--    ;

SELECT * FROM @data

DECLARE @i AS INT;
DECLARE @c AS INT;
DECLARE @rd AS NVARCHAR(MAX);
DECLARE @rb AS NVARCHAR(MAX);

SELECT @i = 0, @c = COUNT(*) FROM @data

WHILE @i < @c BEGIN
	
	SELECT @rd = [RequestDate], @rb = [RequestedBy] FROM @data WHERE [ID] = @i;

	UPDATE
		@people
	SET
		[Count] = [Count] + 1
	FROM
		@people
	WHERE
		[Name] = @rb
	;
	SELECT @i = @i + 1;

	UPDATE
		@data
	SET
		[RequestedToday] = [Count]
	FROM
		@data
	INNER JOIN
		@people
	ON
		[Name] = @rb
	WHERE
		[RequestDate] = @rd 

		

END

SELECT * FROM @people
SELECT * FROM @data

    """


    sql_result = connect(sql=sql_req)
    print(sql_result)

    app.mainloop()
