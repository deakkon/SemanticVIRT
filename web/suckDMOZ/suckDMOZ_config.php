<?php

#####################################
#
# Built:07/21/01 -brs-
# Last-Touched:06/24/02 -brs-
# PHPBuild: Apache/1.3.14 (RHLinux7) PHP/4.0.3pl1
# DMOZ parser
#
#####################################

 // the location of this and the rest of the files
DEFINE("SUCKDMOZ_DIR","C:\xampp\htdocs\suckDMOZ");

 // stats will display to the results.txt file every 100,000 rows and every 5% that it chews through the RDF
DEFINE("ECHO_CONTENT_STATS",true);
 // the location of the content RDF file (supplied monthly by DMOZ.org)
DEFINE("CONTENT_RDF",CONSTANT("SUCKDMOZ_DIR")."\content.rdf.u8.gz");

// stats will display to the results.txt file every 100,000 rows and every 5% that it chews through the RDF
DEFINE("ECHO_STRUCTURE_STATS",true);
 // the location of the structure RDF file (supplied monthly by DMOZ.org)
DEFINE("STRUCTURE_RDF",CONSTANT("SUCKDMOZ_DIR")."\structure.rdf.u8.gz");

 // the MySQL database name you want to build the tables in (must already exist)
DEFINE("MY_MYSQL_DB_NAME","dmoz");
 // the server location IP - or 'localhost' if it's on the saem machine
DEFINE("MY_MYSQL_DB_ADDR","localhost");
 // the MySQL user who has create and update privileges on the aforementioned DB
DEFINE("MY_MYSQL_USER","root");
 // the MySQL password for this user
DEFINE("MY_MYSQL_PASS","");

?> 