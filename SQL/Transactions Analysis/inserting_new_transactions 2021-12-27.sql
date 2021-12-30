

BEGIN TRAN

SELECT * FROM [ScotiaTransactions] ORDER BY [Date] DESC

INSERT INTO [ScotiaTransactions] ([Date], [Amount], [Notes], [Type], [Entity]) VALUES

('12/24/2021',-129.00,'-','POS Purchase           ','OPOS Starlink Internet   Halif'),
('12/23/2021',-56.94,'-','POS Purchase           ','FPOS FLORENCEVILLE IRVINGWEST '),
('12/23/2021',-2.02,'-','POS Purchase           ','FPOS TIM HORTONS #0919   WOODS'),
('12/23/2021',-30.45,'-','POS Purchase           ','FPOS WOODSTOCK SUPERSTOREWOODS'),
('12/23/2021',-15.98,'-','POS Purchase           ','FPOS ALCOOL NB LIQUOR  #0WOODS'),
('12/23/2021',-142.03,'-','POS Purchase           ','FPOS WALMART STORE #1043 WOODS'),
('12/23/2021',-18.55,'-','POS Purchase           ','FPOS HART - WOODSTOCK    WOODS'),
('12/23/2021',-11.49,'-','POS Purchase           ','SHOPPERS DRUG MART #01   WOODS'),
('12/23/2021',-74.72,'-','POS Purchase           ','FPOS SHOPPERS DRUG MART #WOODS'),
('12/23/2021',-157.23,'-','POS Purchase           ','FPOS CANADIAN TIRE #137  WOODS'),
('12/23/2021',-4.24,'-','POS Purchase           ','FPOS DAIRY QUEEN #12192  WOODS'),
('12/23/2021',-174.82,'-','POS Purchase           ','WALMART STORE #1043      WOODS'),
('12/23/2021',-1.73,'-','POS Purchase           ','FPOS FLORENCEVILLE ESSO  WEST '),
('12/23/2021',613.19,'-','Payroll Deposit        ','BWS MANUFACTURING LTD        '),
('12/22/2021',-54.95,'-','POS Purchase           ','FPOS ULTRAMAR #12659     BATH '),
('12/21/2021',-36.79,'-','Miscellaneous Payment  ','PAYPAL                       ')


SELECT * FROM [ScotiaTransactions] ORDER BY [Date] DESC

ROLLBACK;
COMMIT;