/* ========================================================= */
/* 0. NETTOYAGE ET LIBNAME                                   */
/* ========================================================= */
/* On utilise ton identifiant partout u64403318 */
libname tarif "/home/u64403318";

/* IMPORT 1 : BASE COUT */
PROC IMPORT Datafile ="/home/u64403318/base_cout.csv"
    out = tarif.base_cout
    DBMS=CSV REPLACE; /* DBMS=CSV utilise la virgule par défaut */
    Getnames=yes;
    GUESSINGROWS=MAX; /* Aide SAS à ne pas tronquer les noms */
Run;

/* IMPORT 2 : BASE FREQUENCE */
PROC IMPORT Datafile ="/home/u64403318/base_freq.csv"
    out = tarif.base_freq
    DBMS=CSV REPLACE;
    Getnames=yes;
    GUESSINGROWS=MAX;
Run;

/* VERIFICATION : On s'assure que les colonnes sont bien là */
/* Si log_RA plante encore, c'est que l'import a échoué */
data tarif.base_freq;
    set tarif.base_freq;
    /* On crée log_RA proprement */
    if RA > 0 then log_RA = log(RA);
    else log_RA = 0; 
run;

/* ========================================================= */
/* ETAPE 1 : ANALYSES DESCRIPTIVES                           */
/* ========================================================= */
title "1.1 Statistiques globales";
proc means data=tarif.base_freq n sum;
    var RA ns_bg;
run;
proc means data=tarif.base_cout sum mean;
    var cs_bg;
run;

title "1.2 Distribution des variables";
proc freq data = tarif.base_freq;
    /* Correction : Formule avec un F majuscule comme dans tes captures */
    tables age_cl anc_perm_cl anveh_cl franchise zone_bg Formule / nocum;
run;

title "1.3 Colinéarité - V de Cramér";
proc freq data = tarif.base_freq;
    tables age_cl * anc_perm_cl / chisq measures;
run;

/* ========================================================= */
/* ETAPE 2 : MODELE DE FREQUENCE                             */
/* ========================================================= */
title "ETAPE 2 : Modèle de Fréquence GLM";
PROC GENMOD DATA = tarif.base_freq ; 
    CLASS age_cl anveh_cl franchise Formule zone_bg / PARAM=GLM DESC ORDER=FREQ; 
    MODEL ns_bg = age_cl anveh_cl franchise Formule zone_bg / 
        OFFSET = log_RA
        DIST = poisson
        LINK = log
        TYPE3 ; 
    ODS OUTPUT ParameterEstimates = tarif.coef_frequence;
RUN ;

/* ========================================================= */
/* ETAPE 3 : MODELE DE COUT                                  */
/* ========================================================= */
title "ETAPE 3 : Modèle de Coût GLM";
PROC GENMOD DATA = tarif.base_cout ; 
    CLASS age_cl anveh_cl franchise Formule zone_bg / PARAM=GLM DESC ORDER=FREQ; 
    MODEL cs_bg = age_cl anveh_cl franchise Formule zone_bg / 
        DIST = gamma
        LINK = log
        TYPE3 ; 
    ODS OUTPUT ParameterEstimates = tarif.coef_cout;
RUN ;

/* ========================================================= */
/* ETAPE EXTRA : EXPORT CSV (AVEC TON CHEMIN u64403318)      */
/* ========================================================= */
proc export data=tarif.coef_frequence
    outfile="/home/u64403318/Betas_Frequence.csv"
    dbms=csv replace;
run;

proc export data=tarif.coef_cout
    outfile="/home/u64403318/Betas_Cout.csv"
    dbms=csv replace;
run;
