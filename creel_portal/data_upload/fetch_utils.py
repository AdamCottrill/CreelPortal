"""
=============================================================
~\fn_portal\data_upload\fetch_utils.py
Created: Aug-12-2021 09:43
DESCRIPTION:

    fetch FN011
    fetch FN013
    fetch FN014
    fetch FN022
    fetch FN026
    fetch FN028
    fetch FN121


A. Cottrill
=============================================================
"""


# an example of connecting to MS Access with SQL Alchemy
# and reflecting it to get the tables and columns and running a simple
# query.

from datetime import datetime
import pyodbc


def strip_date(value):
    """pyodbc treats times as datetimes. we need to strip the date off if
    it is there."""
    if isinstance(value, datetime):
        return value.time()
    return value


def get_mdb_connection(mdb):
    """

    Arguments:
    - `mdb`: path to either a *.mdb or *.accdb file.

    """
    constring = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s"
    con = pyodbc.connect(constring % mdb)
    return con


def execute_select(con, stmt):

    dat = []
    with con.cursor() as cursor:
        cursor.execute(stmt)
        rs = cursor.fetchall()
        colnames = [x[0].lower() for x in cursor.description]
        for row in rs:
            row_dict = {k: v for k, v in zip(colnames, row)}
            dat.append(row_dict)
    return dat


def get_fn011_stmt():
    """Some day soon nuke fiedls after FOF_LOC.  ADD LAKE!"""

    stmt = """SELECT YEAR,
                 PRJ_CD,
                 CONTMETH,
                 PRJ_DATE0,
                 PRJ_DATE1,
                 PRJ_LDR,
                 PRJ_NM,
                 COMMENT0
        FROM FN011;"""

    return stmt


def get_fn022_stmt():

    stmt = """select
                PRJ_CD,
                SSN,
                SSN_DES,
                SSN_DATE0,
                SSN_DATE1
         from FN022"""

    return stmt


def get_fn023_stmt():

    stmt = """SELECT
    PRJ_CD,
    SSN,
    DTP,
    UCASE([FN023].[DTP_NM]) as DTP_NM,
    DOW_LST
    FROM FN023;
    """
    return stmt


def get_fn024_stmt():

    stmt = """SELECT PRJ_CD,
                SSN,
                DTP,
                PRD,
                PRDTM0,
                PRD_DUR,
                PRDTM1,
                TIME_WT
            FROM FN024"""

    return stmt


def get_fn025_stmt():

    stmt = """SELECT PRJ_CD,
                SSN,
                [DATE],
                DTP1,
                DESCRIPTION
            FROM FN025"""

    return stmt


def get_fn026_stmt():

    stmt = """SELECT
                PRJ_CD,
                SPACE,
                SPACE_DES,
                COMMENT6,
                AREA_CNT,
                AREA_LST,
                AREA_WT,
                SPACE_SIZ,
                GRID5,
                DD_LAT,
                DD_LON
    FROM FN026;"""
    return stmt


def get_fn028_stmt():

    stmt = """SELECT
                 PRJ_CD,
                 MODE,
                 MODE_DES,
                 ATYUNIT,
                 ITVUNIT,
                 CHKFLAG,
                 COMMENT8
              FROM FN028;"""
    return stmt


def get_fn111_stmt():

    stmt = """SELECT
                 PRJ_CD,
                 SAMA,
                 STRATUM,
                 MODE,
                 [DATE],
                 SAMTM0,
                 COMMENT1,
                 SPACE,
                 WEATHER,
                 ATYDATA,
                 CREW,
                 AIRTEM0,
                 SITEM0,
                 WIND,
                 CLOUD_PC,
                 PRECIP
              FROM FN111;"""
    return stmt


def get_fn112_stmt():

    stmt = """SELECT
                PRJ_CD,
                SAMA,
                ATYTM0,
                ATYTM1,
                Round(24*([ATYTM1]-[ATYTM0]),2) AS ATYDUR,
                ATYCNT,
                ITVCNT,
                CHKCNT,
                COMMENT2
              FROM FN112;"""
    return stmt


def get_fn121_stmt():

    stmt = """SELECT
                PRJ_CD,
                SAM,
                SAMA,
                ITVSEQ,
                [DATE],
                DOW,
                ITVTM0,
                EFFTM0,
                EFFTM1,
                EFFCMP,
                EFFDUR,
                PERSONS,
                ANGLERS,
                RODS,
                ANGMETH,
                ANGGUID,
                ANGORIG,
                ANGVIS,
                ANGOP1,
                ANGOP2,
                ANGOP3,
                COMMENT1
              FROM FN121
              order by
                PRJ_CD,
                SAM,
                SAMA,
                ITVSEQ
"""
    return stmt


def get_fn123_stmt():

    stmt = """SELECT
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                SEK,
                HVSCNT,
                RLSCNT,
                MESCNT,
                MESWT
                FROM FN123;
                """
    return stmt


def get_fn124_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                SIZ,
                SIZCNT
         from FN124"""
    return stmt


def get_fn125_stmt():

    stmt = """SELECT
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                FLEN,
                TLEN,
                RWT,
                SEX,
                MAT,
                GON,
                CLIPC,
                GIRTH,
                AGEST,
                NODC,
                COMMENT5,
                TISSUE,
                AGE_FLAG,
                LAM_FLAG,
                STOM_FLAG,
                TAG_FLAG
               FROM FN125;"""
    return stmt


def get_fn125tags_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                FISH_TAG_ID,
                TAGID,
                TAGDOC,
                TAGSTAT,
                XCWTSEQ,
                COMMENT_TAG
         from FN125_tags"""
    return stmt


def get_fn125lamprey_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                LAMID,
                XLAM,
                LAMIJC_TYPE,
                LAMIJC_SIZE,
                COMMENT_LAM
         from FN125_lamprey"""
    return stmt


def get_fn126_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                FOOD,
                TAXON,
                FDCNT,
                FDMES,
                FDVAL,
                LF,
                COMMENT6
         from FN126"""
    return stmt


def get_fn127_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                AGEID,
                PREFERRED,
                AGEA,
                AGEMT,
                EDGE,
                CONF,
                NCA,
                COMMENT7
         from FN127"""
    return stmt
