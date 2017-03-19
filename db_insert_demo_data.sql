USE CSE305;


REPLACE INTO Actors VALUES(1,"Al Pacino","M",63,5);
REPLACE INTO Actors VALUES(2,"Tim Robbins","M",53,2);


REPLACE INTO Customers VALUES(4,111111111,"Yang","Shang","123 Success Street","Stony Brook","NY","11790","5166328959","syang@cs.sunysb.edu","Limited",TIMESTAMP("2017-03-15"),"1234567812345670",1);
REPLACE INTO Customers VALUES(2,222222222,"Du","Victor","456 Fortune Road","Stony Brook","NY","11790","5166324360","vicdu@cs.sunysb.edu","Limited",TIMESTAMP("2006-10-15"),"5678123456781230",1);
REPLACE INTO Customers VALUES(3,333333333,"Smith","John","789 Peace Blvd","Los Angeles","CA","93536","3154434321","jsmith@ic.sunysb.edu","Limited",TIMESTAMP("2017-03-15"),"2345678923456780",1);
REPLACE INTO Customers VALUES(1,444444444,"Philip","Lewis","135 Knowledge Lane","Stony Brook","NY","11790","5166668888","pml@cs.sunysb.edu","unlimited-2",TIMESTAMP("2006-10-01"),"6789234567892340",1);


REPLACE INTO Employees VALUES(1,123456789,"Smith","David","123 College road","Stony Brook","NY","11790","5162152345","2005-11-01",60.00,"Employee");
REPLACE INTO Employees VALUES(2,789123456,"Warren","David","456 Sunken Street","Stony Brook","NY","11794","6316329987","2006-02-02",50.00,"Employer");


REPLACE INTO Movies VALUES(1,"The Godfather","Drama",10000,3,5);
REPLACE INTO Movies VALUES(2,"Shawshank Redemption","Drama",1000,2,4);
REPLACE INTO Movies VALUES(3,"Borat","Comedy",500,1,3);


REPLACE INTO Orders VALUES(1,TIMESTAMP("2009-11-11 10:00:00"),1,1,1);
REPLACE INTO Orders VALUES(2,TIMESTAMP("2009-11-11 18:15:00"),3,2,1);
REPLACE INTO Orders VALUES(3,TIMESTAMP("2009-11-12 09:30:00"),3,1,1);
REPLACE INTO Orders VALUES(4,TIMESTAMP("2009-11-21 22:22:00"),2,2,1);


REPLACE INTO Historys VALUES(1,1);
REPLACE INTO Historys VALUES(2,2);
REPLACE INTO Historys VALUES(1,3);
REPLACE INTO Historys VALUES(2,4);


REPLACE INTO Perform VALUES(1,1);
REPLACE INTO Perform VALUES(1,3);
REPLACE INTO Perform VALUES(2,1);
