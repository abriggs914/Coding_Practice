EXEC [dbo].[sp_GroupEntities];
EXEC [dbo].[sp_GroupEntities] @nameIn='amz';

SELECT [dbo].[sv_RemoveNumbers]('amz')
SELECT [dbo].[sv_RemoveSymbols]('amazon')