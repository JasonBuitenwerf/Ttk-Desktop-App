DROP DATABASE IF EXISTS travelq;
CREATE DATABASE travelq;

USE travelq;

DROP TABLE IF EXISTS travel_records;
CREATE TABLE travel_records (
	ref_number VARCHAR(63) PRIMARY KEY, 
    title_en VARCHAR(255), 
    purpose_en VARCHAR(255), 
    start_date DATE, 
    end_date DATE, 
    airfare DECIMAL(7,2), 
    other_transport DECIMAL(7,2), 
    lodging DECIMAL(7,2), 
    meals DECIMAL(7,2), 
    other_expenses DECIMAL(7,2), 
    total DECIMAL(7,2)
)

select * from travel_records;

