CREATE DATABASE IF NOT EXISTS power KEEP 365 DURATION 10 BUFFER 16 WAL_LEVEL 1;
USE power;

CREATE STABLE IF NOT EXISTS meters (ts timestamp, current float, voltage int, phase float) TAGS (location TINYINT, groupId int, remarks NCHAR(128));
CREATE TABLE IF NOT EXISTS meters_airflow_csv_import_test USING meters TAGS (1, 1, "Test only.");
