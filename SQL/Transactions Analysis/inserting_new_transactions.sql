

BEGIN TRAN

SELECT * FROM [ScotiaTransactions] ORDER BY [Date] DESC

INSERT INTO [ScotiaTransactions] ([Date], [Amount], [Notes], [Type], [Entity]) VALUES
('12/17/2021',-92.24,'-','POS Purchase           ','FPOS FLORENCEVILLE IRVINGWEST '),
('12/16/2021',-28.29,'-','POS Purchase           ','FPOS ULTRAMAR #(12659     BATH '),
('12/16/2021',613.19,'-','Payroll Deposit        ','BWS MANUFACTURING LTD        '),
('12/14/2021',-5.74,'-','POS Purchase           ','OPOS PrimeVideo.ca       www.a'),
('12/10/2021',-21.74,'-','POS Purchase           ','OPOS AMZN Mktp CA        WWW.A'),
('12/10/2021',-36.16,'-','POS Purchase           ','OPOS AMZN Mktp CA        WWW.A'),
('12/10/2021',-56.34,'-','POS Purchase           ','OPOS AMZN Mktp CA        WWW.A'),
('12/10/2021',-62.77,'-','POS Purchase           ','FPOS FLORENCEVILLE IRVINGWEST '),
('12/10/2021',21.74,'-','Correction             ','OPOS AMAZON.COM   PMTS - WWW.A'),
('12/10/2021',34.49,'-','Correction             ','581338007523605               '),
('12/9/2021',-4.59,'-','Miscellaneous Payment  ','PAYPAL                       '),
('12/9/2021',-5.74,'-','POS Purchase           ','OPOS PrimeVideo.ca       www.a'),
('12/9/2021',-32.02,'-','POS Purchase           ','FPOS FLORENCEVILLE IRVINGWEST '),
('12/9/2021',-21.74,'-','POS Purchase           ','OPOS AMZN Mktp CA        WWW.A'),
('12/9/2021',-34.49,'-','POS Purchase           ','OPOS Amazon.ca           AMAZO'),
('12/9/2021',-55.34,'-','POS Purchase           ','OPOS AMZN Mktp CA        WWW.A'),
('12/9/2021',613.19,'-','Payroll Deposit        ','BWS MANUFACTURING LTD        '),
('12/8/2021',-149.49,'-','POS Purchase           ','OPOS AMZN Mktp CA        WWW.A'),
('12/7/2021',-28.29,'-','POS Purchase           ','FPOS ULTRAMAR #(12659     BATH '),
('12/7/2021',-2.02,'-','POS Purchase           ','FPOS TIM HORTONS #3567   PERTH'),
('12/7/2021',-200.00,'-','POS Purchase           ','CNB #018                 PERTH'),
('12/7/2021',-121.50,'-','POS Purchase           ','CNB #018                 PERTH'),
('12/7/2021',-12.28,'-','POS Purchase           ','CO-OP #9283              FLORE'),
('12/3/2021',-34.49,'-','POS Purchase           ','OPOS Amazon.ca           AMAZO'),
('12/3/2021',-32.19,'-','POS Purchase           ','OPOS Amazon.ca           AMAZO'),
('12/3/2021',-92.35,'-','POS Purchase           ','FPOS FLORENCEVILLE IRVINGWEST '),
('12/3/2021',320.00,'-','DEPOSIT                ','FREE INTERAC E-TRANSFER'),
('12/2/2021',613.19,'-','Payroll Deposit        ','BWS MANUFACTURING LTD        '),
('12/1/2021',-5.74,'-','POS Purchase           ','FPOS MARK''S THE SPOT     BEECH'),
('11/30/2021',-530.01,'-','Miscellaneous Payment  ','NSLSC                        '),
('11/30/2021',-64.40,'-','POS Purchase           ','OPOS Amazon.ca           AMAZO'),
('11/30/2021',-31.05,'-','POS Purchase           ','OPOS Amazon.ca           AMAZO'),
('11/29/2021',-3.44,'-','POS Purchase           ','OPOS PrimeVideo.ca       www.a')

SELECT * FROM [ScotiaTransactions] ORDER BY [Date] DESC

ROLLBACK;
COMMIT;