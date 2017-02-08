-- fn011 defines attributes of project - top level table in Fishnet project - where project code is declared.
select * from fn011 limit 10;
PRAGMA table_info(fn011);

-- fn021 contains stats about creel design.  it may be re-created from other tables.
-- fk to fn011
select * from fn021 limit 10;

-- fn022 table contain information about seasons used in a creel
-- fk to fn011
select * from fn022 limit 10;
PRAGMA table_info(fn022);

-- fn02 table contain information about daytypes used in a creel
-- fk to fn011
select * from fn023 limit 10;
PRAGMA table_info(fn023);

-- fn024 table contain information about periods -(am/pm) used in a creel and which period they apply to.
-- fk to fn023
select * from fn024 limit 10;

-- fn025 table contains exception dates that apply to dates other than their the nominal day-type
-- fk to fn011
select * from fn025 limit 10;

-- fn026 table contain information about the spatial strata used in the creel.
-- fk to fn011
select * from fn026 limit 10;


select * from fn028 limit 10;
