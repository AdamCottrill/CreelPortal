
---=================================================
-- fn011 defines attributes of project - top level table in Fishnet project - where project code is declared.
select * from fn011 limit 10;
select distinct prj_cd from fn011;
PRAGMA table_info(fn011);

select prj_cd, count(prj_cd) from fn011 group by prj_cd ;

---=================================================
-- fn021 contains stats about creel design.  it may be re-created from other tables.
-- fk to fn011
select * from fn021 limit 10;

---=================================================
-- fn022 table contain information about seasons used in a creel
-- fk to fn011
select * from fn022 limit 10;
select distinct prj_cd from fn022;
PRAGMA table_info(fn022);
select max(length(SSN_DES)) from fn022 group by length(SSN_DES);
---delete from FN022;

---=================================================
-- fn023 table contain information about daytypes used in a creel
-- fk to fn011
select * from fn023 limit 10;
select distinct prj_cd from fn023;
select prj_cd, ssn, dtp, dtp_nm, dow_lst from fn023 order by prj_cd, ssn, dtp;
PRAGMA table_info(fn023);

---=================================================
-- fn024 table contain information about periods -(am/pm) used in a creel and which period they apply to.
-- fk to fn023
select * from fn024 limit 10;
select distinct prj_cd from fn024;
PRAGMA table_info(fn024);
select prj_cd, ssn, dtp, prd, prdtm0, prdtm1 from fn024;
-- fn025 table contains exception dates that apply to dates other than their the nominal day-type
-- fk to fn011
select * from fn025 limit 10;
PRAGMA table_info(fn025);

---=================================================
-- fn026 table contain information about the spatial strata used in the creel.
-- fk to fn011
select * from fn026 limit 10;
select distinct prj_cd from fn026;
select prj_cd, space, space_des, space_siz, area_cnt, area_lst, area_wt from fn026;


---=================================================
--- FN028 
---contains information on the modes used in the creel
select * from fn028;-- limit 10;
select distinct prj_cd from fn028;
select prj_cd, mode, mode_des, atyunit, itvunit, chkflag from fn028 limit 10;
select distinct itvunit from fn028;
PRAGMA table_info(fn028);
select * from fn028 where prj_cd like '%SC00_SPR';

--
select * from fn028 where prj_cd like '%NIR' or prj_cd like '%NIP';
select * from fn111  where prj_cd like '%NIR' or prj_cd like '%NIP';

select distinct area from fn111 where prj_cd like '%SC12_BSR';
select * from fn026 where prj_cd like '%SC12_BSR';
select * from fn111 where prj_cd like '%SC12_BSR';
select * from fn121 where prj_cd like '%SC12_BSR';

select prj_cd, mode from fn111 group by prj_cd, mode order by prj_cd, mode;

-- information about creel interviews (creel log)
select * from fn111 order by stratum limit 10;
select prj_cd, sama, dow, [date], samtm0, area, mode, stratum, weather, comment1 from fn111 order by prj_cd, sama, area, mode, dow, [date], samtm0; 


---=================================================
select * from fn121 limit 10;
select count(*) as N from fn121;
select distinct prj_cd from fn121;
select prj_cd, sam, sama, itvseq, itvtm0, area, [date], efftm0, efftm1, effcmp, effdur, mode, persons, anglers, rods, angmeth, angvis, angorig, angop1, angop2, angop3 from fn121;
select distinct angop1 from fn121;

select * from fn121 where efftm0 is null or efftm0='';
-- we can't have an empty efftm0 time - it looks like effdur was calcaulated by assuming that efftmo was '00:00'
-- we will make it explicit for now:
update fn121 set efftm0='00:00' where efftm0='';

---=================================================
select * from fn123;
select distinct prj_cd from fn123;
select prj_cd, sam, spc, sek, hvscnt, rlscnt, mescnt, meswt from fn123 order  by prj_cd, sam, spc, sek;

select * from fn123 where rlscnt='';

---=================================================
select *  from fn125 where x_scars is not null and x_scars<> '' and x_scars>0 limit 10;
select prj_cd, sam, spc, grp, fish, flen, tlen, rwt, sex, gon, mat, age, agest, clipc, fate from fn125 limit 10; 
select distinct prj_cd from fn125;
select * from fn125 where prj_cd like '%SC13_BSR' and SPC='334';

select * from fn125 where rwt<1;

-- it looks like RWT was reported in kg for *SC13_BSR - RWT should be in grams, and be an integer.
--update fn125 set rwt = round(rwt*1000),0) where prj_cd like '%SC13_BSR'; 
--update fn125 set rwt = round(rwt,0) where prj_cd like '%SC13_BSR'; 
--update fn125 set rwt=replace(rwt,'.0','')  where prj_cd like '%SC13_BSR';
select * from fn125 where prj_cd like '%SC13_BSR';

select * from fn127 limit 10;
select prj_cd, sam, spc, grp, fish, ageid, agea, agemt, conf, edge, nca from fn127 limit 10;

---=================================================
-- effort estimates
select * from fr713 where prj_cd='LSM_SC00_BAS';
select prj_cd, strat, angler_s, angler_ss, atycnt_s, aty_days, aty_nn, chkcnt_s, cif_nn, itvcnt_s, person_s, rod_s, rod_ss, tripno, [run], rec_tp from fr713;
select distinct strat from fr713;
-- catch estimates by species
select * from fr714 limit 10;
select prj_cd, strat, spc, sek, rod1_s, angler1_s, catno1_s, catno1_ss, catno_s, catno_ss, cif1_nn, hvsno1_s, hvsno1_ss, hvsno_s, hvsno_ss, mescnt_s, rec_tp, [run] from fr714
order by prj_cd, strat, spc, sek;

---=================================================
-- biosample counts by speceies and strata
select * from fr523 limit 10;