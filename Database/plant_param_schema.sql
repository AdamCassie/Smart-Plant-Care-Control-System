-- This schema defines the ideal target values for soil moisture, Nitrogen(N),
-- Phosphorous (P) and Potassium (K) for common houseplants found in North America.
-- Soil Moisture target is given as a percentage value (range from 0% to 100%).
-- N, P and K target values are given as the mass of the respective nutrient present 
-- in every kilogram of soil (range from 0mg/kg to 255mg/kg).

drop schema if exists plant_param cascade;
create schema plant_param;
set search_path to plant_param;

-- A row in this table indicates the ideal parameter target values for a specific
-- plant type.
create table IdealPlantParams (
	plantType varchar(50) primary key,
	moistureTarget int not null,
	nitrogenTarget int not null,
	phosphorousTarget int not null,
	potassiumTarget int not null,
	constraint validMoistureRange 
		check (moistureTarget >= 0 and moistureTarget <= 100),
	constraint validNitrogenRange 
		check (nitrogenTarget >= 0 and nitrogenTarget <= 1999),
	constraint validPhosphorousRange 
		check (phosphorousTarget >= 0 and phosphorousTarget <= 1999),
	constraint validPotassiumRange 
		check (potassiumTarget >= 0 and potassiumTarget <= 1999)
);
