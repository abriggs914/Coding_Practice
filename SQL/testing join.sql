CREATE TABLE [Logons] (
  [Id] INT,
  [Logon] DATETIME,
  [Time_Float] BIGINT,
  [LocationID] INT
);
INSERT INTO [Logons] ([Id], [Logon], [Time_Float], [LocationID]) VALUES
  (8, '12:26:00 AM', 1560, 1),
  (9, '2:53:00 PM', 53580, 1),
  (10, '2:52:00 PM', 53520, 1),
  (11, '1:18:00 PM', 47880, 1),
  (12, '5:41:00 PM', 63660, 1),
  (13, '5:16:00 PM', 86400, 1),
  (14, '2:13:00 PM', 86400, 1),
  (15, '12:01:00 PM', 86400, 1),
  (16, '9:40:00 AM', 34800, 3),
  (17, '4:30:00 AM', 16200, 4),
  (18, '7:30:00 AM', 27000, 1),
  (19, '9:17:00 PM', 76620, 1),
  (20, '9:50:00 PM', 78600, 2),
  (21, '9:18:00 PM', 76680, 4),
  (22, '9:11:00 PM', 76260, 2),
  (23, '2:30:00 PM', 52200, 1)
;

CREATE TABLE [Locations] (
  [ID] INT,
  [Location] VARCHAR(50)
);
INSERT INTO [Locations] ([ID], [Location]) VALUES
  (1, 'Main Office'),
  (2, 'Reception'),
  (3, 'Server Room'),
  (4, 'Conference Room')
;


-----------------------------------------------------------------------------------------------------------------------

SELECT
  Locations.[Location],
  *
FROM (
  SELECT
    Logons.[LocationID],
    Count(Logons.[LocationID]) AS CountOfLocationID
  FROM
    Logons
  GROUP BY
    Logons.[LocationID]
)  AS SrcTable
INNER JOIN 
  Locations 
ON
  Locations.[LocationID] = SrcTable.[LocationID];
