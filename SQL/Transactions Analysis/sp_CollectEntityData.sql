

CREATE PROCEDURE [dbo].[sp_CollectEntityData]
	@entity_name AS NVARCHAR(MAX),
	@start_date AS DATETIME = NULL,
	@end_date AS DATETIME = NULL
AS
BEGIN

	SELECT * FROM [dbo].[tv_CollectEntityData](@entity_name, @start_date, @end_date)

END