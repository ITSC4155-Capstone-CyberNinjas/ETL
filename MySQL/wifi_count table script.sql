SET GLOBAL local_infile = 1;

CREATE DATABASE IF NOT EXISTS `CyberNinjas`;
USE `CyberNinjas`;

/*'wifi_count' table*/
DROP TABLE IF EXISTS `wifi_count`;

CREATE TABLE `wifi_count` (
  `timestamp` DATETIME NOT NULL,
  `Atki` int(4) NOT NULL,
  `Auxi` int(4) NOT NULL,
  `BaTF` int(4) NOT NULL,
  `Band` int(4) NOT NULL,
  `Barn` int(4) NOT NULL,
  `BelG` int(4) NOT NULL,
  `BelH` int(4) NOT NULL,
  `Bioi` int(4) NOT NULL,
  `Burs` int(4) NOT NULL,
  `Cafe` int(4) NOT NULL,
  `Came` int(4) NOT NULL,
  `Cato` int(4) NOT NULL,
  `Ceda` int(4) NOT NULL,
  `CoEd` int(4) NOT NULL,
  `Colv` int(4) NOT NULL,
  `Cone` int(4) NOT NULL,
  `Coun` int(4) NOT NULL,
  `Denn` int(4) NOT NULL,
  `Duke` int(4) NOT NULL,
  `EPIC` int(4) NOT NULL,
  `FOPS` int(4) NOT NULL,
  `Faci` int(4) NOT NULL,
  `Foun` int(4) NOT NULL,
  `Fret` int(4) NOT NULL,
  `Frid` int(4) NOT NULL,
  `Gage` int(4) NOT NULL,
  `Gari` int(4) NOT NULL,
  `Grig` int(4) NOT NULL,
  `Harr` int(4) NOT NULL,
  `Heal` int(4) NOT NULL,
  `Hick` int(4) NOT NULL,
  `Hous` int(4) NOT NULL,
  `HunH` int(4) NOT NULL,
  `Irwi` int(4) NOT NULL,
  `JBui` int(4) NOT NULL,
  `Kenn` int(4) NOT NULL,
  `King` int(4) NOT NULL,
  `Laur` int(4) NOT NULL,
  `Levi` int(4) NOT NULL,
  `Lync` int(4) NOT NULL,
  `MSII` int(4) NOT NULL,
  `Macy` int(4) NOT NULL,
  `Mart` int(4) NOT NULL,
  `McCo` int(4) NOT NULL,
  `McMi` int(4) NOT NULL,
  `Memo` int(4) NOT NULL,
  `MilH` int(4) NOT NULL,
  `Milt` int(4) NOT NULL,
  `NERF` int(4) NOT NULL,
  `PORT` int(4) NOT NULL,
  `Phil` int(4) NOT NULL,
  `Pros` int(4) NOT NULL,
  `Rece` int(4) NOT NULL,
  `Rees` int(4) NOT NULL,
  `Robi` int(4) NOT NULL,
  `Rowe` int(4) NOT NULL,
  `SVDH` int(4) NOT NULL,
  `Scot` int(4) NOT NULL,
  `Smit` int(4) NOT NULL,
  `SoTF` int(4) NOT NULL,
  `Stor` int(4) NOT NULL,
  `StuA` int(4) NOT NULL,
  `StuH` int(4) NOT NULL,
  `StuU` int(4) NOT NULL,
  `Syca` int(4) NOT NULL,
  `Tenn` int(4) NOT NULL,
  `UREC` int(4) NOT NULL,
  `Unio` int(4) NOT NULL,
  `Wach` int(4) NOT NULL,
  `Wall` int(4) NOT NULL,
  `Winn` int(4) NOT NULL,
  `With` int(4) NOT NULL,
  `Wood` int(4) NOT NULL,
  PRIMARY KEY (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `wifi_count`, file path will be different from your computer*/
LOAD DATA LOCAL INFILE 'C:/Users/Willy/Downloads/wifi_counts_combined.csv'
INTO TABLE wifi_count
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM wifi_count;