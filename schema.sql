PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

CREATE TABLE USERS(
    USERNAME VARCHAR PRIMARY KEY, 
    EMAIL VARCHAR NOT NULL, 
    PASSWORD VARCHAR NOT NULL
);
INSERT INTO USERS VALUES('A','A@A.COM','pbkdf2:sha256:150000$3eq2d560$bca38a47dc52ba90932997ae4bc22bb8c0508c0c03930c703540042857b48bdc');
INSERT INTO USERS VALUES('G','G@GGNORE.COM','pbkdf2:sha256:150000$KkGLIfVQ$a1c8f83635c8d1cd0ad954c92e47e26992be671d22ae8c5840b0ffa1f3eec622');
INSERT INTO USERS VALUES('X','X@X.COM','pbkdf2:sha256:150000$kkM0XWhu$d315b80730c0b95023c4afb8eb5a0928132df35249cb1bcaa907b9e20447fba4');
INSERT INTO USERS VALUES('B','B@B.COM','pbkdf2:sha256:150000$nCS2GVuw$843bb080a4cf605da7681119da82e17d4119fb7ee070365b76d09d253186d07f');
INSERT INTO USERS VALUES('C','C@C.COM','pbkdf2:sha256:150000$eJitVkjR$0b37be0553c347671ae791345f9040789bd66b87e10803799c16f4319c274242');
INSERT INTO USERS VALUES('D','D@D.COM','pbkdf2:sha256:150000$hXpfoUmL$e73ce8e2ee38e74536b7e0427c97e3f2fc15172b392972c39be20fab7bc5a2f4');
INSERT INTO USERS VALUES('F','F@F.COM','pbkdf2:sha256:150000$HEVBT8yR$f92b4b5e62cd75f9fef95970695935e200649cc97cc13421fe4833786d497de8');


CREATE TABLE FOLLOWERS(
    FOLLOWING VARCHAR NOT NULL, 
    USER VARCHAR NOT NULL,
    FOREIGN KEY(USER) REFERENCES USERS(USERNAME)
);
INSERT INTO FOLLOWERS VALUES('G','A');
INSERT INTO FOLLOWERS VALUES('X','A');
INSERT INTO FOLLOWERS VALUES('F','A');
INSERT INTO FOLLOWERS VALUES('C','B');
INSERT INTO FOLLOWERS VALUES('F','B');
INSERT INTO FOLLOWERS VALUES('A','D');
INSERT INTO FOLLOWERS VALUES('X','G');
INSERT INTO FOLLOWERS VALUES('G','X');
INSERT INTO FOLLOWERS VALUES('A','X');


CREATE TABLE TWEETS(
    TWEET TEXT NOT NULL, 
    TIME_STAMP VARCHAR NOT NULL,
    AUTHOR VARCHAR NOT NULL,
    FOREIGN KEY(AUTHOR) REFERENCES USERS(USERNAME)
);
INSERT INTO TWEETS VALUES('Andromeda','2020-10-05 19:05:13','A');
INSERT INTO TWEETS VALUES('GG NO RE','2020-10-05 20:05:13','G');
INSERT INTO TWEETS VALUES('XANDER CAGE','2020-10-05 21:05:13','X');
INSERT INTO TWEETS VALUES('JUST BO-LIEVE','2020-10-05 22:05:13','B');
INSERT INTO TWEETS VALUES('C WHAT I DID THERE','2020-10-05 07:05:13','C');
INSERT INTO TWEETS VALUES('DINOSAURS ARE DOPE','2020-10-05 06:05:13','D');
INSERT INTO TWEETS VALUES('FANTASTIC','2020-10-05 05:05:13','F');
INSERT INTO TWEETS VALUES('APPLES AND PIE','2020-10-06 03:12:34','A');
INSERT INTO TWEETS VALUES('GEE GEE GEE','2020-10-06 02:12:34','G');
INSERT INTO TWEETS VALUES('X-PAC','2020-10-07 02:21:43','X');
INSERT INTO TWEETS VALUES('KENNY V OKADA II 6.5/5','2020-10-07 04:43:43','F');
INSERT INTO TWEETS VALUES('KENNY V OKADA IV 7/5','2020-10-07 12:41:33','C');
COMMIT;
