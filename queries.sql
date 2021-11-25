select region_name, count(name) from Characteristics natural join Generation group by region_name;
select count(distinct pokedex_number) from Characteristics;
select name from Characteristics where name not like "% %" and pokedex_number in (select pokedex_number from Characteristics where name like "% %");
select name, Max(attack) from Characteristics natural join Stats group by name order by Max(attack) desc limit 1;
select distinct type_primary from Typing;
select type_primary, count(name) from Typing natural join Characteristics group by type_primary;
select name from characteristics where weight_kg = 0;
select name from characteristics where percentage_male = '0.0' or percentage_male = 'None';
select name from Characteristics natural join Abilities where ability_1 = 'Intimidate' or ability_2 = 'Intimidate' or ability_hidden = "Intimidate";
select name from Characteristics natural join Species where species = 'Shadow Pokemon';