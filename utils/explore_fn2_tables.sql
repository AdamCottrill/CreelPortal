
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
update fn123 set rlscnt=0 where rlscnt='' or rlscnt is null;

select * from fn123 where mescnt='';
update fn123 set mescnt=0 where mescnt='' or mescnt is null;
---=================================================
select *  from fn125 where x_scars is not null and x_scars<> '' and x_scars>0 limit 10;
select prj_cd, sam, spc, grp, fish, flen, tlen, rwt, sex, gon, mat, age, agest, clipc, fate from fn125 limit 10; 
select distinct prj_cd from fn125;
select * from fn125 where prj_cd like '%SC13_BSR' and SPC='334';

select * from fn125 where rwt<1;

-- it looks like RWT was reported in kg for *SC13_BSR - RWT should be in grams, and be an integer.
--update fn125 set rwt = round((rwt*1000),0) where prj_cd like '%SC13_BSR'; 
--update fn125 set rwt = round(rwt,0) where prj_cd like '%SC13_BSR'; 
--update fn125 set rwt=replace(rwt,'.0','')  where prj_cd like '%SC13_BSR';
select * from fn125 where prj_cd like '%SC13_BSR';

select * from fn127 limit 10;
select prj_cd, sam, spc, grp, fish, ageid, agea, agemt, conf, edge, nca from fn127 limit 10;

---=================================================
-- effort estimates
select * from fr713 where prj_cd='LSM_SC00_BAS';
select * from fr713 where strat = '++_++_++_++';

select * from fr713;
select count(*), count(prj_cd), count(strat), count(angler_s), count(angler_ss), count(atycnt_s), count(aty_days) from fr713;

select prj_cd, strat, angler_s, angler_ss, atycnt_s, aty_days, aty_nn, chkcnt_s, cif_nn, itvcnt_s, person_s, rod_s, rod_ss, tripno, [run], rec_tp from fr713;
select distinct strat from fr713;
PRAGMA table_info(fr713);

select * from fr714;

SELECT PRJ_CD,
       RUN,
       STRAT,
       REC_TP,
       DATE,
       ANGLER_MN,
       ANGLER_S,
       ANGLER_SS,
       ATY0,
       ATY1,
       ATY1_SE,
       ATY1_VR,
       ATY2,
       ATY2_SE,
       ATY2_VR,
       ATYCNT_S,
       ATY_DAYS,
       ATY_HRS,
       ATY_NN,
       CHKCNT_S,
       CIF_NN,
       EFFAE,
       EFFAE_SE,
       EFFAE_VR,
       EFFAO_S,
       EFFAO_SS,
       EFFPE,
       EFFPE_SE,
       EFFPE_VR,
       EFFPO_S,
       EFFPO_SS,
       EFFRE,
       EFFRE_SE,
       EFFRE_VR,
       EFFRO_S,
       EFFRO_SS,
       ITVCNT_S,
       PERSON_S,
       ROD_MNA,
       ROD_S,
       ROD_SS,
       TRIPNE,
       TRIPNE_SE,
       TRIPNE_VR,
       TRIPNO
  FROM FR713
 ORDER BY PRJ_CD,
          RUN,
          STRAT,
          REC_TP,
          DATE;


select count(*),
Count(PRJ_CD),
Count(ANGLER_MN),
Count(ANGLER_S),
Count(ANGLER_SS),
Count(ATY0),
Count(ATY1),
Count(ATY1_SE),
Count(ATY1_VR),
Count(ATY2),
Count(ATY2_SE),
Count(ATY2_VR),
Count(ATYCNT_S),
Count(ATY_DAYS),
Count(ATY_HRS),
Count(ATY_NN),
Count(CHKCNT_S),
Count(CIF_NN),
Count(DATE),
Count(DBF_FILE),
Count(EFFAE),
Count(EFFAE_SE),
Count(EFFAE_VR),
Count(EFFAO_S),
Count(EFFAO_SS),
Count(EFFPE),
Count(EFFPE_SE),
Count(EFFPE_VR),
Count(EFFPO_S),
Count(EFFPO_SS),
Count(EFFRE),
Count(EFFRE_SE),
Count(EFFRE_VR),
Count(EFFRO_S),
Count(EFFRO_SS),
Count(ITVCNT_S),
Count(PERSON_S),
Count(REC_TP),
Count(ROD_MNA),
Count(ROD_S),
Count(ROD_SS),
Count(RUN),
Count(STRAT),
Count(TRIPNE),
Count(TRIPNE_SE),
Count(TRIPNE_VR),
Count(TRIPNO)
from fr713;




-- catch estimates by species

--delete from Fr714;

select * from fr714 where prj_cd like '%_SC00_BAS';
select * from fr714 where strat = '++_++_++_++';

select prj_cd, strat, spc, sek, rod1_s, angler1_s, catno1_s, catno1_ss, catno_s, catno_ss, cif1_nn, hvsno1_s, hvsno1_ss, hvsno_s, hvsno_ss, mescnt_s, rec_tp, [run] from fr714
order by prj_cd, strat, spc, sek;

PRAGMA table_info(fr714);
select count(*),
Count(PRJ_CD),
Count(SPC),
Count(ANGLER1_S),
Count(CATEA1_XY),
Count(CATEA_XY),
Count(CATEP1_XY),
Count(CATEP_XY),
Count(CATER1_XY),
Count(CATER_XY),
Count(CATNE),
Count(CATNE1),
Count(CATNE1_PC),
Count(CATNE1_SE),
Count(CATNE1_VR),
Count(CATNE_SE),
Count(CATNE_VR),
Count(CATNO1_S),
Count(CATNO1_SS),
Count(CATNO_S),
Count(CATNO_SS),
Count(CIF1_NN),
Count(CUENAE),
Count(CUENAE1),
Count(CUENAO),
Count(CUENAO1),
Count(DATE),
Count(DBF_FILE),
Count(EFFAE1),
Count(EFFAE1_PC),
Count(EFFAE1_SE),
Count(EFFAE1_VR),
Count(EFFAO1_S),
Count(EFFAO1_SS),
Count(EFFPE1),
Count(EFFPE1_SE),
Count(EFFPE1_VR),
Count(EFFPO1_S),
Count(EFFPO1_SS),
Count(EFFRE1),
Count(EFFRE1_SE),
Count(EFFRE1_VR),
Count(EFFRO1_S),
Count(EFFRO1_SS),
Count(HVSCAT_PC),
Count(HVSEA1_XY),
Count(HVSEA_XY),
Count(HVSEP1_XY),
Count(HVSEP_XY),
Count(HVSER1_XY),
Count(HVSER_XY),
Count(HVSNE),
Count(HVSNE1),
Count(HVSNE1_SE),
Count(HVSNE1_VR),
Count(HVSNE_SE),
Count(HVSNE_VR),
Count(HVSNO1_S),
Count(HVSNO1_SS),
Count(HVSNO_S),
Count(HVSNO_SS),
Count(MESCNT_S),
Count(MESWT_S),
Count(REC_TP),
Count(ROD1_S),
Count(RUN),
Count(SEK),
Count(STRAT) from fr714;

---=================================================
-- biosample counts by speceies and strata
select * from fr523 limit 10;