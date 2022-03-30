CONTMETH_CHOICES = (
    ("A2", "Access; Same days"),
    ("R0", "Roving; No interviews"),
    ("R1", "Roving; Not same days"),
    ("R2", "Roving; Same days"),
)

REC_TP_CHOICES = ((1, "creel log (daily)"), (2, "stratum"), (3, "multi-stratum"))

ANG_FN_CHOICES = [
    ("agnvis", "ANGVIS"),
    ("angorig", "ANGORIG"),
    ("angmeth", "ANGMETH"),
    ("angguid", "ANGGUID"),
    ("angop1", "ANGOP1"),
    ("angop2", "ANGOP2"),
    ("angop3", "ANGOP3"),
    ("angop4", "ANGOP4"),
    ("angop5", "ANGOP5"),
]


ANGMETH_CHOICES = [
    (1, "Still"),
    (2, "Jig"),
    (3, "Drift"),
    (4, "Troll"),
    (5, "Down rig"),
    (6, "Spin cast"),
    (7, "Fly cast"),
    (8, "Other/combination"),
]

ANGVIZ_CHOICES = [
    (1, "Permanent resident"),
    (2, "Non-permanent resident"),
    (3, "Day tripper"),
    (4, "Camp-provincial park"),
    (5, "Camp-commercial park"),
    (6, "Camp-crown land"),
    (7, "Other-paid"),
    (8, "Other-non-paid"),
]

ANGORIG_CHOICES = [
    (1, "Local"),
    (2, "Ontario"),
    (3, "Canada"),
    (4, "US"),
    (5, "Other"),
]


SEX_CHOICES = ((1, "Male"), (2, "Female"), (3, "Hermaphrodite"), (9, "Unknown"))
MAT_CHOICES = ((1, "Immature"), (2, "Mature"), (9, "Unknown"))


LAMIJC_TYPE_CHOICES = (
    ["0", "0"],
    ["a1", "A1"],
    ["a2", "A2"],
    ["a3", "A3"],
    ["a4", "A4"],
    ["b1", "B1"],
    ["b2", "B2"],
    ["b3", "B3"],
    ["b4", "B4"],
)


FDMES_CHOICES = (
    (None, "No Data"),
    ("L", "Length"),
    ("W", "Weight"),
    ("V", "Volume"),
)
LIFESTAGE_CHOICES = (
    (None, "No Data"),
    ("10", "10"),
    ("20", "20"),
    ("30", "30"),
    ("40", "40"),
    ("50", "50"),
    ("60", "60"),
)
