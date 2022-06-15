USE [MWBAdb]
GO

BEGIN TRAN;

INSERT INTO	[dbo].[Players] (
	[Name]
	,[Affiliation]
	,[AffiliationsAr]
	,[Team]
	,[TeamsAr]
	,[IsActive]
	,[Number]
	,[NumbersAr])
VALUES 
	('Megan Arseneault', 24, '10;25', 1, '1', 1, 4, '4'),
	('Rahshida Atkinson', 28, '29', 1, '1', 1, 5, '5'),
	('Leah Bowers', 24, '25', 1, '1', 1, 6, '6'),
	('Bailey Black', 24, '25', 1, '1', 1, 7, '7'),
	('Katie Daley', 24, '25', 1, '1', 1, 8, '8'),
	('Robbi Daley', 19, '7;20', 1, '1', 1, 9, '9'),
	('Ashley Bawn', 21, '22', 1, '1', 1, 10, '10'),
	('Katie McAffee', 24, '2;25', 1, '1', 1, 11, '11'),
	('Nicole Esson', 24, '25', 1, '1', 1, 12, '12'),
	('Grace Simpson', 24, '25', 1, '1', 1, 14, '14'),
	('Eva Tumwine', 24, '25', 1, '1', 1, 15, '15'),
	('Torrie Janes', 15, '20;16', 1, '1', 1, 21, '21'),
	('Mackenzie Legere', 15, '16', 1, '1', 1, 31, '31'),
	('Katelyn Mangold', 24, '25', 1, '1', 1, 35, '35'),
	('Kylee Speedy', 24, '25', 1, '1', 1, 44, '44'),
	('Emily MacLeod', 24, '2;25', 1, '1', 1, 51, '51'),
	('Jill Durling', 24, '25', 1, '1', 1, 55, '55'),
	('Emily Shiels()', 0, '1', 2, '2', 1, 2, '2'),
	('Abby Ring-Dineen', 25, '26', 2, '2', 1, 4, '4'),
	('Courtney Thompson', 6, '7', 2, '2', 1, 5, '5'),
	('Bailey Henderson', 25, '26', 2, '2', 1, 6, '6'),
	('Rachel Farwell', 23, '24', 2, '2', 1, 7, '7'),
	('Megan Stewart', 30, '31', 2, '2', 1, 8, '8'),
	('Reese Baxendale', 27, '28', 2, '2', 1, 9, '9'),
	('Emily Briggs', 5, '6', 2, '2', 1, 10, '10'),
	('Janelle Haddad', 3, '4', 2, '2', 1, 11, '11'),
	('Lauren Fleming', 27, '28', 2, '2', 1, 12, '12'),
	('Lauren Harris', 27, '28', 2, '2', 1, 13, '13'),
	('Kaylee Kilpatrick', 29, '18;30', 2, '2', 1, 14, '14'),
	('Emily Thomas', 0, '1', 2, '2', 1, 15, '15'),
	('Amelia Mitchell', 15, '16', 2, '2', 1, 16, '16'),
	('Emily Fitzpatrick', 25, '26', 2, '2', 1, 21, '21'),
	('Maddy Daley', 5, '6', 3, '3', 1, 2, '2'),
	('Anne-Marie Poitras', 14, '15', 3, '3', 1, 3, '3'),
	('Kelsey McLaughlin', 19, '20', 3, '3', 1, 4, '4'),
	('Lindy MacDonald', 8, '22;9', 3, '3', 1, 5, '5'),
	('Maddie Greatorex', 15, '16', 3, '3', 1, 6, '6'),
	('Kelly Vass', 5, '22;6', 3, '3', 1, 7, '7'),
	('Jenna Jones', 27, '28', 3, '3', 1, 9, '9'),
	('Maddy Maillet', 6, '7', 3, '3', 1, 10, '10'),
	('Shannon Youden', 19, '20', 3, '3', 1, 12, '12'),
	('Erika Traikor', 1, '2', 3, '3', 1, 14, '14'),
	('Sarah West', 0, '1', 3, '3', 1, 13, '13'),
	('Emile Turmel', 22, '23', 3, '3', 1, 15, '15'),
	('Abby Miller', 15, '16', 3, '3', 1, 16, '16'),
	('Jodi Whyte', 26, '27', 4, '4', 1, 3, '3'),
	('Sydney Foran', 11, '12', 4, '4', 1, 4, '4'),
	('Jessica Miller', 20, '21', 4, '4', 1, 5, '5'),
	('Cassandra McCormick', 10, '11', 4, '4', 1, 7, '7'),
	('Meghan Keoughan', 5, '6', 4, '4', 1, 8, '8'),
	('Tiffany Reynolds', 9, '10', 4, '4', 1, 9, '9'),
	('Karissa Kajorinne', 9, '3;10', 4, '4', 1, 10, '10'),
	('Chelsea Slawter-Wright', 6, '7', 4, '4', 1, 11, '11'),
	('Lisa Edwards', 8, '9', 4, '4', 1, 12, '12'),
	('Emily MacNeil', 3, '4', 4, '4', 1, 13, '13'),
	('Karla Yepez', 27, '28', 4, '4', 1, 14, '14'),
	('Christina Garon', 10, '11', 4, '4', 1, 15, '15'),
	('Anna von', 6, '7', 4, '4', 1, 16, '16'),
	('Carolina Del', 27, '28', 4, '4', 1, 17, '17'),
	('Jaylnn Skier', 4, '5', 5, '5', 1, 5, '5'),
	('Alaina McMillan', 19, '20', 5, '5', 1, 6, '6'),
	('Chanel Smith', 1, '2', 5, '5', 1, 7, '7'),
	('Jayla Verney', 8, '9', 5, '5', 1, 8, '8'),
	('Aliyah Fraser', 20, '21', 5, '5', 1, 9, '9'),
	('Katherine Khorovets', 16, '17', 5, '5', 1, 10, '10'),
	('Alisha McNeil', 16, '17', 5, '5', 1, 12, '12'),
	('Arianna Macias', 19, '20', 5, '5', 1, 13, '13'),
	('Lucina Beaumont', 19, '20', 5, '5', 1, 14, '14'),
	('Katherine Follis', 26, '27', 5, '5', 1, 15, '15'),
	('Cailin Crosby', 6, '7', 5, '5', 1, 20, '20'),
	('Clara Gascoigne', 19, '20', 5, '5', 1, 21, '21'),
	('Madison Munro', 4, '5', 5, '5', 1, 22, '22'),
	('Leah Martin', 6, '7', 5, '5', 1, 23, '23'),
	('Hannah Brown', 4, '5', 5, '5', 1, 24, '24'),
	('Jasmine Parent', 1, '2', 5, '5', 1, 25, '25'),
	('Ellen Hatt', 1, '2', 6, '6', 1, 1, '1'),
	('Haley McDonald', 7, '2;8', 6, '6', 1, 2, '2'),
	('Gemma Bullard', 18, '19', 6, '6', 1, 3, '3'),
	('Leslie Hawco', 13, '14', 6, '6', 1, 4, '4'),
	('Justine Colley-Leger', 19, '20', 6, '6', 1, 5, '5'),
	('Vanessa Pickard', 12, '21;13', 6, '6', 1, 7, '7'),
	('Katherine Quackenbush', 13, '14', 6, '6', 1, 8, '8'),
	('Jayda Veinot', 1, '2', 6, '6', 1, 9, '9'),
	('Melina Collins', 20, '21', 6, '6', 1, 10, '10'),
	('Abby Duinker', 1, '2', 6, '6', 1, 11, '11'),
	('Marley Curwin', 24, '25', 6, '6', 1, 13, '13'),
	('Grace Wade', 24, '25', 6, '6', 1, 14, '14'),
	('Laura Langille', 19, '20', 6, '6', 1, 15, '15'),
	('Elizabeth Beals-Iseyemi', 1, '2', 6, '6', 1, 22, '22')
GO

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ID]
      ,[Name]
      ,[Affiliation]
      ,[AffiliationsAr]
      ,[Team]
      ,[TeamsAr]
      ,[IsActive]
      ,[DateAdded]
      ,[Number]
      ,[NumbersAr]
  FROM [MWBAdb].[dbo].[Players]


ROLLBACK;
COMMIT;