#DROP TABLES
#Dimension
DimCity_Table_Drop = "DROP TABLE IF EXISTS DimCity"
DimYear_Table_Drop = "DROP TABLE IF EXISTS DimYear"

#Staging area
ForestSourceDataStaging_Table_Drop = "DROP TABLE IF EXISTS ForestSourceDataStaging"
ClimateSourceDataStaging_Table_Drop = "DROP TABLE IF EXISTS ClimateSourceDataStaging"
PopulationSourceDataStaging_Table_Drop = "DROP TABLE IF EXISTS PopulationSourcDataStaging"
IndustrySourceDataStaging_Table_Drop = "DROP TABLE IF EXISTS IndustrySourceDataStaging"

#FACT TABLES
FactForest_Table_Drop = "DROP TABLE IF EXISTS FactForest"
FactClimate_Table_Drop = "DROP TABLE IF EXISTS FactClimate"
FactPopulation_Table_Drop = "DROP TABLE IF EXISTS FactPopulation"
FactIndustry_Table_Drop = "DROP TABLE IF EXISTS FactIndustry"



#CREATE TABLE
#Dimention
DimCity_Table_Create = ("""CREATE TABLE IF NOT EXISTS DimCity(
        CityID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,  
        City VARCHAR NULL
    );""")

DimYear_Table_Create = ("""CREATE TABLE IF NOT EXISTS DimYear(
        YearID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
        Year INT NULL        
    );""")

#Staging area
ForestSourceDataStaging = ("""CREATE TABLE IF NOT EXISTS ForestSourceDataStaging(
        Source_StagingID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL, 
        City VARCHAR null,
        CityID int null,
        Year int null,
        YearID int null,
        Afforestation double precision null,
        ForestCover double precision null
    );""")

ClimateSourceDataStaging = ("""CREATE TABLE IF NOT EXISTS ClimateSourceDataStaging(
        Source_StagingID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL, 
        City VARCHAR null,
        CityID int null,
        Year int null,
        YearID int null,
        Humidity double precision null,
        Rainfall double precision null,
        Temperature double precision null
    );""")

PopulationSourceDataStaging = ("""CREATE TABLE IF NOT EXISTS PopulationSourceDataStaging(
        Source_StagingID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL, 
        City VARCHAR null,
        CityID int null,
        Year int null,
        YearID int null,
        Population double precision null 
    );""")


IndustrySourceDataStaging = ("""CREATE TABLE IF NOT EXISTS IndustrySourceDataStaging(
        Source_StagingID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL, 
        City VARCHAR null,
        CityID int null,
        Year int null,
        YearID int null,
        Industry double precision null 
    );""")



#FACT TABLES
FactForest = ("""CREATE TABLE IF NOT EXISTS FactForest(
        ForestID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
        CityID int null,
        YearID int null,
        Afforestation double precision null,
        ForestCover double precision null,
        FOREIGN KEY (CityID) REFERENCES DimCity(CityID),
        FOREIGN KEY (YearID) REFERENCES DimYear(YearID)
    );""")

FactClimate = ("""CREATE TABLE IF NOT EXISTS FactClimate(
        ClimateID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
        CityID int null,
        YearID int null,
        Humidity double precision null,
        Rainfall double precision null,
        Temperature double precision null,
        FOREIGN KEY (CityID) REFERENCES DimCity(CityID),
        FOREIGN KEY (YearID) REFERENCES DimYear(YearID)
    );""")

FactPopulation = ("""CREATE TABLE IF NOT EXISTS FactPopulation(
        PopulationID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
        CityID int null,
        YearID int null,
        Population double precision null,
        FOREIGN KEY (CityID) REFERENCES DimCity(CityID),
        FOREIGN KEY (YearID) REFERENCES DimYear(YearID)
    );""")

FactIndustry = ("""CREATE TABLE IF NOT EXISTS FactIndustry(
        IndustryID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
        CityID int null,
        YearID int null,
        Industry double precision null,
        FOREIGN KEY (CityID) REFERENCES DimCity(CityID),
        FOREIGN KEY (YearID) REFERENCES DimYear(YearID)
    );""")



#INSERT INTO TABLES
ForestSourceDataStaging_table_insert = ("""INSERT INTO ForestSourceDataStaging(City, Year, Afforestation)
            VALUES(%s, %s, %s);
        """)

ForestCover_insert_table = ("""UPDATE ForestSourceDataStaging SET ForestCover = %s WHERE (City = %s) AND (Year = %s);
        """)



ClimateSourceDataStaging_table_insert = ("""INSERT INTO ClimateSourceDataStaging(City, Year, Humidity) 
           VALUES(%s, %s, %s);
        """)
Rainfall_insert_table = ("""UPDATE ClimateSourceDataStaging SET Rainfall = %s WHERE (City = %s) AND (Year = %s);
        """)

        
Temperature_insert_table = ("""UPDATE ClimateSourceDataStaging SET Temperature = %s WHERE (City = %s) AND (Year = %s);
        """)

        





PopulationSourceDataStaging_table_insert = ("""INSERT INTO PopulationSourceDataStaging(City, Year, Population)
            VALUES(%s, %s, %s);
        """)

IndustrySourceDataStaging_table_insert = ("""INSERT INTO IndustrySourceDataStaging(City, Year, Industry)
            VALUES(%s, %s, %s);
        """)



#DIM TABLES INSERT
DimCity_table_insert = ("""
        INSERT INTO DimCity (City)
        SELECT DISTINCT City From climatesourcedatastaging a
        WHERE NOT EXISTS (SELECT City FROM DimCity WHERE a.City = City)
        ORDER BY City ASC;

        INSERT INTO DimCity (City)
        SELECT DISTINCT City From forestsourcedatastaging a
        WHERE NOT EXISTS (SELECT City FROM DimCity WHERE a.City = City)
        ORDER BY City ASC;
        
        INSERT INTO DimCity (City)
        SELECT DISTINCT City From industrysourcedatastaging a
        WHERE NOT EXISTS (SELECT City FROM DimCity WHERE a.City = City)
        ORDER BY City ASC;


        INSERT INTO DimCity (City)
        SELECT DISTINCT City From populationsourcedatastaging a
        WHERE NOT EXISTS (SELECT City FROM DimCity WHERE a.City = City)
        ORDER BY City ASC;
        """)

DimYear_table_insert = ("""
        INSERT INTO DimYear (Year)
        SELECT DISTINCT Year From climatesourcedatastaging a
        WHERE NOT EXISTS (SELECT Year FROM DimYear WHERE a.Year = Year)
        ORDER BY Year ASC;

        INSERT INTO DimYear (Year)
        SELECT DISTINCT Year From forestsourcedatastaging a
        WHERE NOT EXISTS (SELECT Year FROM DimYear WHERE a.Year = Year)
        ORDER BY Year ASC;

        INSERT INTO DimYear (Year)
        SELECT DISTINCT Year From industrysourcedatastaging a
        WHERE NOT EXISTS (SELECT Year FROM DimYear WHERE a.Year = Year)
        ORDER BY Year ASC;

        INSERT INTO DimYear (Year)
        SELECT DISTINCT Year From populationsourcedatastaging a
        WHERE NOT EXISTS (SELECT Year FROM DimYear WHERE a.Year = Year)
        ORDER BY Year ASC;
        """)


update_staging_tables = ("""
        UPDATE climatesourcedatastaging AS c
        SET YearID = d.YearID
        FROM DimYear AS d
        WHERE c.Year = d.Year;

        UPDATE climatesourcedatastaging AS c
        SET CityID = d.CityID
        FROM DimCity AS d
        WHERE c.City = d.City;

        UPDATE forestsourcedatastaging AS c
        SET YearID = d.YearID
        FROM DimYear AS d
        WHERE c.Year = d.Year;

        UPDATE forestsourcedatastaging AS c
        SET CityID = d.CityID
        FROM DimCity AS d
        WHERE c.City = d.City;
    
        UPDATE industrysourcedatastaging AS c
        SET YearID = d.YearID
        FROM DimYear AS d
        WHERE c.Year = d.Year;

        UPDATE industrysourcedatastaging AS c
        SET CityID = d.CityID
        FROM DimCity AS d
        WHERE c.City = d.City;

        UPDATE populationsourcedatastaging AS c
        SET YearID = d.YearID
        FROM DimYear AS d
        WHERE c.Year = d.Year;

        UPDATE populationsourcedatastaging AS c
        SET CityID = d.CityID
        FROM DimCity AS d
        WHERE c.City = d.City;
        
    """)

insert_fact_tables = ("""
        INSERT INTO FactClimate(CityID, YearID, Humidity, Rainfall, Temperature)
        SELECT CityID, YearID, Humidity, Rainfall, Temperature FROM ClimateSourceDataStaging;

        INSERT INTO FactForest(CityID, YearID, Afforestation, Forestcover)
        SELECT CityID, YearID, Afforestation, Forestcover FROM ForestSourceDataStaging;

        INSERT INTO FactIndustry(CityID, YearID, Industry)
        SELECT CityID, YearID, Industry FROM IndustrySourceDataStaging;

        INSERT INTO FactPopulation(CityID, YearID, Population)
        SELECT CityID, YearID, Population FROM PopulationSourceDataStaging;
    """)










#QUERY LISTS
create_table_queries = [DimCity_Table_Create, DimYear_Table_Create, 
            ForestSourceDataStaging, ClimateSourceDataStaging, PopulationSourceDataStaging, IndustrySourceDataStaging,
            FactForest, FactClimate, FactPopulation, FactIndustry]



drop_table_queries = [DimCity_Table_Drop, DimYear_Table_Drop, 
                    ForestSourceDataStaging_Table_Drop, ClimateSourceDataStaging_Table_Drop
                    ,PopulationSourceDataStaging_Table_Drop, IndustrySourceDataStaging_Table_Drop,
                    FactForest_Table_Drop, FactClimate_Table_Drop, FactPopulation_Table_Drop, FactIndustry_Table_Drop]



insert_table_queries = [ForestSourceDataStaging_table_insert, ClimateSourceDataStaging_table_insert, PopulationSourceDataStaging_table_insert,
                        IndustrySourceDataStaging_table_insert ]


insert_domain = [Rainfall_insert_table, Temperature_insert_table, ForestCover_insert_table]

insert_tables = [DimCity_table_insert, DimYear_table_insert, update_staging_tables, insert_fact_tables]



