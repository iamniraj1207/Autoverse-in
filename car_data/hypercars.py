# Hypercars & Megacars — Full specs
# (brand, model, year, engine, horsepower, torque, fuel_type, acceleration, image_url)

HYPERCARS = [
    # ── Pagani ────────────────────────────────────────────────────────
    ("Pagani","Zonda C12",       2000,"6.0L AMG V12",          550, 553,"Petrol", 3.7,None),
    ("Pagani","Zonda F",         2006,"7.3L AMG V12",          602, 479,"Petrol", 3.6,None),
    ("Pagani","Zonda Cinque",    2009,"7.3L AMG V12",          669, 575,"Petrol", 3.4,None),
    ("Pagani","Huayra",          2013,"6.0L AMG Biturbo V12",  730, 738,"Petrol", 3.3,None),
    ("Pagani","Huayra BC",       2017,"6.0L AMG Biturbo V12",  789, 811,"Petrol", 2.9,None),
    ("Pagani","Huayra Roadster", 2017,"6.0L AMG Biturbo V12",  764, 738,"Petrol", 3.1,None),
    ("Pagani","Imola",           2020,"6.0L AMG Biturbo V12",  827, 811,"Petrol", 2.8,None),
    ("Pagani","Utopia",          2022,"6.0L AMG Biturbo V12",  852, 811,"Petrol", 2.8,None),
    # ── Koenigsegg ────────────────────────────────────────────────────
    ("Koenigsegg","CC8S",            2002,"4.7L Supercharged V8",    655, 753,"Petrol", 3.5,None),
    ("Koenigsegg","CCX",             2006,"4.7L Twin-Supercharged V8",806, 920,"Petrol", 3.2,None),
    ("Koenigsegg","CCXR Trevita",    2009,"4.7L Twin-Supercharged V8",1018,1060,"E85",   2.9,None),
    ("Koenigsegg","Agera R",         2013,"5.0L Twin-Turbo V8",     1140,1200,"E85",   2.8,None),
    ("Koenigsegg","One:1",           2014,"5.0L Twin-Turbo V8",     1341,1011,"E85",   2.8,None),
    ("Koenigsegg","Regera",          2016,"5.0L Twin-Turbo V8+Elec",1500,2000,"Hybrid",2.7,None),
    ("Koenigsegg","Agera RS",        2017,"5.0L Twin-Turbo V8",     1360,1280,"E85",   2.6,None),
    ("Koenigsegg","Jesko",           2020,"5.0L Twin-Turbo V8",     1600,1500,"E85",   2.5,None),
    ("Koenigsegg","Jesko Absolut",   2020,"5.0L Twin-Turbo V8",     1600,1106,"E85",   2.5,None),
    ("Koenigsegg","Gemera",          2021,"3cyl+3 Electric Motors",  1700,3500,"Hybrid",1.9,None),
    ("Koenigsegg","CC850",           2022,"5.0L Twin-Turbo V8",     1385,1385,"E85",   3.0,None),
    # ── Bugatti ───────────────────────────────────────────────────────
    ("Bugatti","EB110",              1992,"3.5L Quad-Turbo V12",    553, 457,"Petrol", 3.2,None),
    ("Bugatti","Veyron",             2005,"8.0L Quad-Turbo W16",   1001, 922,"Petrol", 2.5,None),
    ("Bugatti","Veyron SS",          2010,"8.0L Quad-Turbo W16",   1200,1106,"Petrol", 2.4,None),
    ("Bugatti","Grand Sport",        2012,"8.0L Quad-Turbo W16",   1001, 922,"Petrol", 2.6,None),
    ("Bugatti","Chiron",             2017,"8.0L Quad-Turbo W16",   1479,1180,"Petrol", 2.4,None),
    ("Bugatti","Chiron Sport",       2018,"8.0L Quad-Turbo W16",   1479,1180,"Petrol", 2.4,None),
    ("Bugatti","Divo",               2018,"8.0L Quad-Turbo W16",   1479,1180,"Petrol", 2.4,None),
    ("Bugatti","Centodieci",         2020,"8.0L Quad-Turbo W16",   1577,1180,"Petrol", 2.4,None),
    ("Bugatti","Bolide",             2021,"8.0L Quad-Turbo W16",   1825,1364,"Petrol", 2.1,None),
    ("Bugatti","Chiron Super Sport", 2021,"8.0L Quad-Turbo W16",   1578,1180,"Petrol", 2.4,None),
    ("Bugatti","Mistral",            2022,"8.0L Quad-Turbo W16",   1578,1180,"Petrol", 2.4,None),
    ("Bugatti","Tourbillon",         2024,"8.3L NA V16+HEV",       1800,1800,"Hybrid", 2.0,None),
    # ── Rimac ─────────────────────────────────────────────────────────
    ("Rimac","Concept One",          2016,"Electric Quad Motor",    1073,1600,"Electric",2.6,None),
    ("Rimac","C_Two",                2020,"Electric Quad Motor",    1888,2300,"Electric",1.85,None),
    ("Rimac","Nevera",               2021,"Electric Quad Motor",    1914,2360,"Electric",1.8,None),
    # ── SSC ───────────────────────────────────────────────────────────
    ("SSC","Ultimate Aero",          2007,"6.3L Twin-Turbo V8",    1046, 921,"Petrol", 2.7,None),
    ("SSC","Ultimate Aero TT",       2009,"6.3L Twin-Turbo V8",    1287,1112,"Petrol", 2.78,None),
    ("SSC","Tuatara",                2020,"5.9L Twin-Turbo V8",    1750,1735,"E85",   2.5,None),
    # ── Hennessey ─────────────────────────────────────────────────────
    ("Hennessey","Venom GT",         2013,"7.0L Twin-Turbo V8",    1244,1155,"Petrol", 2.7,None),
    ("Hennessey","Venom F5",         2021,"6.6L Twin-Turbo V8",    1817,1617,"Petrol", 2.6,None),
    # ── Other Hypercars ───────────────────────────────────────────────
    ("Zenvo","TSR-S",                2019,"5.8L Twin-Supercharged V8",1177,1100,"Petrol",2.8,None),
    ("Zenvo","Aurora",               2023,"5.8L Biturbo V8",       1100,1100,"Petrol",3.0,None),
    ("Lykan","HyperSport",           2014,"3.7L Twin-Turbo F6",    780, 708,"Petrol", 2.8,None),
    ("Cizeta","V16T",                1991,"6.0L V16",              540, 406,"Petrol", 4.5,None),
    ("W Motors","Lykan HyperSport",  2017,"3.7L Twin-Turbo F6",    780, 708,"Petrol", 2.8,None),
    ("9ff","GT9-R",                  2010,"5.0L Flat-6",           987, 771,"Petrol", 2.9,None),
    ("Mosler","MT900S",              2006,"7.0L LS7 V8",           449, 486,"Petrol", 3.4,None),
    ("Ultima","GTR720",              2006,"6.3L V8",               720, 660,"Petrol", 2.6,None),
    ("Ultima","RS",                  2015,"6.2L Supercharged V8",  1020, 775,"Petrol", 2.3,None),
]
