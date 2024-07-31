CREATE DATABASE power KEEP 365 DURATION 10 BUFFER 16 WAL_LEVEL 1;
USE power;

CREATE STABLE meters (
  ts timestamp, 
  current float, 
  voltage int, 
  phase float
) TAGS (
  location TINYINT, 
  groupId int, 
  remarks NCHAR(128)
);
