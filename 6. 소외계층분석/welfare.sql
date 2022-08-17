-- Active: 1659007754281@@127.0.0.1@3306

CREATE DATABASE welfare;
USE welfare;

CREATE TABLE welfare.global_income (
	country CHAR(15) NOT NULL,
	year_2017 DECIMAL(4, 2) NOT NULL,
	year_2018 DECIMAL(4, 2) NOT NULL,
	year_2019 DECIMAL(4, 2) NOT NULL,
	year_2020 DECIMAL(4, 2) NOT NULL,
	year_2021 DECIMAL(4, 2) NOT NULL,
	pk_global_income PRIMARY KEY(country)
);

CREATE TABLE welfare.social_spending (
	country CHAR(15) NOT NULL PRIMARY,
	latest DECIMAL(6, 3) NOT NULL,
	FOREIGN KEY (country) REFERENCES welfare.global_income(country)
);

CREATE TABLE welfare.unemployment_rate (
	country CHAR(15) NOT NULL,
	year_2017 DECIMAL(6, 3) NOT NULL,
	year_2018 DECIMAL(6, 3) NOT NULL,
	year_2019 DECIMAL(6, 3) NOT NULL,
	year_2020 DECIMAL(6, 3) NOT NULL,
	year_2021 DECIMAL(6, 3) NOT NULL,
	PRIMARY KEY(country)
	FOREIGN KEY (country) REFERENCES welfare.global_income(country)
);

ALTER TABLE welfare.unemployment_rate
ADD CONSTRAINT unemployment_rate_FK FOREIGN KEY (country) 
REFERENCES welfare.social_spending(country) 
ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE welfare.social_spending 
ADD CONSTRAINT social_spending_FK FOREIGN KEY (country)
REFERENCES welfare.unemployment_rate(country) 
ON DELETE RESTRICT ON UPDATE RESTRICT;