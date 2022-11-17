SET GLOBAL local_infile=1;

CREATE DATABASE IF NOT EXISTS `CyberNinjas`;
USE `CyberNinjas`;

/*'coordinates' table*/
DROP TABLE IF EXISTS `coordinates`;

CREATE TABLE `coordinates` (
  `Building abbreviation` char(4) NOT NULL,
  `Building Name` VARCHAR(20),
  `Id` INT(2) NOT NULL,
  `Latitude` FLOAT(7),
  `Longitude` FLOAT(7),
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `coordinates`, file path will be different from your computer*/
LOAD DATA LOCAL INFILE 'C:/Users/Willy/Downloads/UNCC Building Abbreviations - UNCC Buildings INFO.csv'
INTO TABLE coordinates
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM coordinates;