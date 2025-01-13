
-- Initial inserts [NHLdb].[dbo].[Divisions]


INSERT INTO [NHLdb].[dbo].[Divisions] ([Name], [InauguralYear], [Description], [Comments])
VALUES
('North Eastern', NULL, NULL, NULL),
('Eastern', NULL, NULL, NULL),
('Western', NULL, NULL, NULL),
('Adams', NULL, 'Eastern Teams', 'Formed from teams in the North Eastern Divsion'),
('Patrick', NULL, 'Eastern Teams', 'Formed from teams in the Eastern Division'),
('Norris', NULL, 'Western Teams', 'Formed from teams in the Western Division'),
('Smythe', NULL, 'Western Teams', 'Formed from teams in the Western Division'),
('Atlantic', 1974, 'Eastern Teams', 'Formed from teams in the Adams Division'),
('Metropolitan', 1974, 'Eastern Teams', 'Formed from teams in the Patrick Division'),
('Central', 1974, 'Western Teams', 'Formed from teams in the Norris Division'),
('Pacific', 1974, 'Western Teams', 'Formed from teams in the Smythe Division')
;