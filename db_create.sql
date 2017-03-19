DROP DATABASE IF EXISTS CSE305;
CREATE DATABASE CSE305;
USE CSE305;

DROP TABLE IF EXISTS `Movie`;
CREATE TABLE `Movie` (
  `Movie_ID` int(12) AUTO_INCREMENT,
  `Movie_Name` varchar(50) NOT NULL,
  `Movie_Type` varchar(12) NOT NULL CHECK(Movie_Type IN('Comedy','Drama','Action','Foreign', 'N/A')),
  `Distribution_Fee` decimal(8,2) NOT NULL,
  `Number_of_Copies` int DEFAULT 0 CHECK(Number_of_Copies >= 0),
  `Rating` int NOT NULL CHECK(Rating>=1&&Rating<=5),
  PRIMARY KEY (`Movie_ID`)
);

DROP TABLE IF EXISTS `Actor`;
CREATE TABLE `Actor` (
  `Actor_ID` int AUTO_INCREMENT,
  `Actor_Name` varchar(50),
  `Actor_Sex` varchar(6),
  `Age` int,
  `Rating` int,
  PRIMARY KEY (`Actor_ID`)
);


DROP TABLE IF EXISTS `Customer`;
CREATE TABLE `Customer` (
  `Account_Id` int AUTO_INCREMENT,
  `Customer_Id` varchar(20) NOT NULL, -- log in name
  `Last_Name` varchar(20),
  `First_Name` varchar(20),
  `Address` varchar(50),
  `City` varchar(20),
  `State` varchar(20),
  `Zip_Code` varchar(10),
  `Telephone` varchar(20),
  `Email` varchar(50) NOT NULL,
  `Account_Type` varchar(12) DEFAULT 'Limited' CHECK(Account_Type IN('Limited','unlimited-1','unlimited-2','unlimited-3')),
  `Account_Creation_Date` timestamp NOT NULL,
  `Credit_Card_Number` varchar(20) ,
  `Rating` int CHECK(Rating>=1&&Rating<=5),
  PRIMARY KEY (`Account_Id`),
  UNIQUE KEY(`Customer_Id`)
);


DROP TABLE IF EXISTS `Employee`;
CREATE TABLE `Employee` (
  `Employee_ID` int NOT NULL auto_increment,
  `SSN` varchar(20) NOT NULL,
  `Last_Name` varchar(30) NOT NULL,
  `First_Name` varchar(30) NOT NULL,
  `Address` varchar(50) NOT NULL,
  `City` varchar(20) NOT NULL,
  `State` varchar(20) NOT NULL,
  `Zip_Code` varchar(10) NOT NULL,
  `Telephone` varchar(20) NOT NULL,
  `Start_Date` timestamp NOT NULL,
  `HOURLY_Rating` decimal(6,2) NOT NULL,
  `Type` varchar(8) NOT NULL CHECK(Type IN('Employer','Employee')),
  PRIMARY KEY (`Employee_ID`)
) ;

DROP TABLE IF EXISTS `Order`;
CREATE TABLE `Order` (
  `Order_ID` int AUTO_INCREMENT,
  `Order_Date` timestamp NOT NULL,
  `Movie_ID` int NOT NULL,
  `Account_Id` int NOT NULL,
  `Employee_ID` int NOT NULL,
  PRIMARY KEY (`Order_ID`),
  FOREIGN KEY (`Movie_ID`) REFERENCES `Movie` (`Movie_ID`),
  FOREIGN KEY (`Account_Id`) REFERENCES `Customer` (`Account_Id`),
  FOREIGN KEY (`Employee_ID`) REFERENCES `Employee` (`Employee_ID`)
) ;

DROP TABLE IF EXISTS `Perform`;
CREATE TABLE `Perform` (
  `Actor` int NOT NULL,
  `Movie` int NOT NULL,
  UNIQUE KEY  (`Actor`,`Movie`),
  FOREIGN KEY (`Actor`) REFERENCES `Actor` (`Actor_ID`),
  FOREIGN KEY (`Movie`) REFERENCES `Movie` (`Movie_ID`)
) ;

DROP TABLE IF EXISTS `Queue`;
CREATE TABLE `Queue` (
  `Account_Id` int NOT NULL,
  `Movie` int NOT NULL,
  UNIQUE KEY (`Account_Id`,`Movie`),
  FOREIGN KEY (`Account_Id`) REFERENCES `Customer` (`Account_Id`),
  FOREIGN KEY (`Movie`) REFERENCES `Movie` (`Movie_ID`)
) ;

DROP TABLE IF EXISTS `History`;
CREATE TABLE `History` (
  `Account_Id` int NOT NULL,
  `Order` int NOT NULL,
  UNIQUE KEY (`Account_Id`,`Order`),
  FOREIGN KEY (`Account_Id`) REFERENCES `Customer` (`Account_Id`),
  FOREIGN KEY (`Order`) REFERENCES `Order` (`Order_ID`)
) ;
