CREATE TABLE CUSTOMER (
    Id INTEGER NOT NULL,
    Email VARCHAR(32) NOT NULL UNIQUE,
    Address VARCHAR(64),
    Fname VARCHAR(32),
    Lname VARCHAR(32),
    Password VARCHAR(32) NOT NULL,
    PRIMARY KEY(Id)
);

CREATE TABLE PRODUCT (
    Id INTEGER NOT NULL,
    Name VARCHAR(64)  NOT NULL UNIQUE,
    Price DECIMAL(5,2),
    Summary VARCHAR(256),
    SourceOfSupply VARCHAR(32),
    NumberOfProduct INTEGER,
    PRIMARY KEY(Id)
);

CREATE TABLE GAMECARD (
    Pid       INTEGER      NOT NULL
                CONSTRAINT Prod_FK_3 REFERENCES PRODUCT (Id) ON DELETE CASCADE
                                                            ON UPDATE SET NULL,
    Type      VARCHAR (16),
    Rarety    VARCHAR (16),
    BulkOrOne CHAR (1)

);


CREATE TABLE BOARDGAME (
    Pid         INTEGER CONSTRAINT Prod_FK_4 REFERENCES PRODUCT (Id) ON DELETE CASCADE
                                                                     ON UPDATE SET NULL
                                                          NOT NULL,
    PersonNum   VARCHAR(4),
    AgeRestrict VARCHAR(4)

);



CREATE TABLE BUY (
    Cid       INTEGER      NOT NULL
                CONSTRAINT Cus_FK_1 REFERENCES CUSTOMER (Id) ON DELETE CASCADE
                                                            ON UPDATE SET NULL,
    Pid       INTEGER      NOT NULL
                           CONSTRAINT Prod_FK_1 REFERENCES PRODUCT (Id) ON DELETE CASCADE
                                                                        ON UPDATE SET NULL,
    CargoName VARCHAR (16),
    CardType  CHAR (1)

);



CREATE TABLE REVIEW (
    Cid     INTEGER      NOT NULL
                         CONSTRAINT Cus_FK_2 REFERENCES CUSTOMER (Id) ON DELETE CASCADE
                                                                      ON UPDATE SET NULL,
    Pid     INTEGER      CONSTRAINT Prod_FK_2 REFERENCES PRODUCT (Id) ON DELETE CASCADE
                                                                      ON UPDATE SET NULL
                         NOT NULL,
    Comment VARCHAR (64),
    Time    DATETIME
);

