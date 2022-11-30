CREATE DATABASE IF NOT EXISTS 'NINER_TRANSIT';
USE 'NINER_TRANSIT';

/*'coordinates' table*/
CREATE OR REPLACE TABLE PUBLIC."Coordinates" (
  "Building_Abbreviation" char(4) NOT NULL,
  "Building_Name" VARCHAR(100),
  "Id" INT NOT NULL,
  "Latitude" FLOAT(7),
  "Longitude" FLOAT(7),
  "File_Name" VARCHAR(800),
  PRIMARY KEY ("Id")
);

/* RUN THIS LINE */
SELECT * FROM "Coordinates";
ls @MY_STAGE;

/* Copies from CSV*/  
/*copy into PUBLIC."Coordinates" (
    "Building_Abbreviation",
    "Building_Name",
    "Id",
    "Latitude",
    "Longitude" 
)

from (
select
    c.$1,
    c.$2,
    c.$3,
    c.$4,
    c.$5
from @NINER_TRANSIT.PUBLIC.MY_STAGE/UNCC_Building_Abbreviations.csv.gz(file_format => CSV_FORMAT) c
    ); */
    
/* Selects from CSV*/  
select
  c.$1,
  c.$2,
  c.$3,
  c.$4,
  c.$5,
  metadata$filename
from @NINER_TRANSIT.PUBLIC.MY_STAGE/UNCC_Building_Abbreviations.csv.gz(file_format => CSV_FORMAT) c;

select * from PUBLIC."Coordinates";