USE [NHLdb]
GO

/****** Object:  Table [dbo].[Games]    Script Date: 2025-01-12 10:05:49 PM ******/


-- 2025-01-13 1147 YET TO RUN

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

--CREATE TABLE [dbo].[Games](
	[ID] [int] IDENTITY(0,1) NOT NULL,
	[DateCreated] [datetime] NULL,
	[LastModified] [datetime] NULL,
	[Active] [bit] NULL,
	[DateActive] [datetime] NULL,
	[DateInActive] [datetime] NULL,

	[NHLAPI_ID] [nvarchar](10) NULL,

	[Name] [nvarchar](255) NULL,
	[Description] [nvarchar](max) NULL,
	[Comments] [nvarchar](max) NULL,
 CONSTRAINT [PK_Games] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Games] ADD  CONSTRAINT [DF_Games_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO

ALTER TABLE [dbo].[Games] ADD  CONSTRAINT [DF_Games_Active]  DEFAULT ((1)) FOR [Active]
GO


