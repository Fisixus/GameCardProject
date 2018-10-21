INSERT INTO CUSTOMER VALUES(1,'jdoe@gmail.com','Empire Street','John','Doe','abcdef');
INSERT INTO CUSTOMER VALUES(2,'kreeves@gmail.com','Washington Street','Keenu','Reeves','abcdef1');
INSERT INTO CUSTOMER VALUES(3,'hledger@hotmail.com','Batman Street','Heath','Ledger','abcdef12');
INSERT INTO CUSTOMER VALUES(4,'akeys@yahoo.com','Panama Street','Alicia','Keys','abcdef123');
INSERT INTO CUSTOMER VALUES(5,'neo07@yahoo.com','Matrix Street','Neo','Anderson','12345');
INSERT INTO CUSTOMER VALUES(6,'ksoze01@yahoo.com','Unusual Street','Kayser','Soze','123456');
INSERT INTO CUSTOMER VALUES(7,'hkojima@gmail.com','Japanese Street','Hideo','Kojima','1234567');
INSERT INTO CUSTOMER VALUES(8,'mhaneke@hotmail.com','Berlin Street','Michael','Haneke','12345678');
INSERT INTO CUSTOMER VALUES(9,'ywenli@yahoo.com','Odin Street','Yang','Wenli','123456789');
INSERT INTO CUSTOMER VALUES(10,'apacino@yahoo.com','Sicilia Street','Al','Pacino','abcde');
INSERT INTO CUSTOMER VALUES(11,'snicks@gmail.com','Fleetwood Street','Stevie','Nicks','01234');

INSERT INTO PRODUCT VALUES(1,'Blue Eyes White Dragon','10.15','This legendary dragon is a powerful engine of destruction. Virtually invincible, very few have faced this awesome creature and lived to tell the tale.','ToysRus',5);
INSERT INTO PRODUCT VALUES(2,'Dark Magician','50.25','The ultimate wizard in terms of attack and defense.','DuelMonsters',2);
INSERT INTO PRODUCT VALUES(3,'Monopoly','26.71','The classic game of buying and selling.','HasbroGaming',15);
INSERT INTO PRODUCT VALUES(4,'Kaiba Starter Deck','143,11','The original Dueling Legends get their Decks updated in Yugi - Reloaded and Kaiba - Reloaded Starter Decks. Each 50-card Deck features that characters favorite cards and is tuned to provide easy learning of the Yu-Gi-Oh!','DuelMonsters',3);
INSERT INTO PRODUCT VALUES(5,'Codebreaker Starter Deck','7.22','Codebreaker introduces the basics of Dueling with cards that are strong and easy to understand. New Duelists can learn the basics of Link Summoning using "Code Talker" Link Monsters, then use this Starter Deck as a base to build their own unique Deck by collecting Cyberse monsters.','DuelMonsters',22);
INSERT INTO PRODUCT VALUES(6,'Taboo','15.50',NULL,'HasbroGaming',22);
INSERT INTO PRODUCT VALUES(7,'Daretti, Ingenious Iconoclast','30.74','Legendary Planeswalker — Daretti.','ToysRus',5);
INSERT INTO PRODUCT VALUES(8,'Gaia The Fierce Knight','8.85','A knight whose horse travels faster than the wind. His battle-charge is a force to be reckoned with.','DuelMonsters',1);

INSERT INTO GAMECARD(Pid,Type,Rarety,BulkOrOne) VALUES (1,'Yugioh','Rare','O');
INSERT INTO GAMECARD(Pid,Type,Rarety,BulkOrOne) VALUES (2,'Yugioh','Very Rare','O');
INSERT INTO GAMECARD(Pid,Type,Rarety,BulkOrOne) VALUES (4,'Yugioh','Rare','B');
INSERT INTO GAMECARD(Pid,Type,Rarety,BulkOrOne) VALUES (5,'Yugioh','Common','B');
INSERT INTO GAMECARD(Pid,Type,Rarety,BulkOrOne) VALUES (7,'Guilds of Ravnica','Common','O');
INSERT INTO GAMECARD(Pid,Type,Rarety,BulkOrOne) VALUES (8,'Yugioh','Rare','O');

INSERT INTO BOARDGAME(Pid,PersonNum,AgeRestrict) VALUES (3,'6','12+');
INSERT INTO BOARDGAME(Pid,PersonNum,AgeRestrict) VALUES (6,'4','14+');

INSERT INTO BUY(Cid,Pid,CargoName,CardType) VALUES (1,4,'Fedex','V');
INSERT INTO BUY(Cid,Pid,CargoName,CardType) VALUES (9,5,'Fedex','M'); 

INSERT INTO REVIEW(Cid,Pid,Comment,Time) VALUES (1,4,'Awesome card!!','2018-10-09 08:23:19.120');
INSERT INTO REVIEW(Cid,Pid,Comment,Time) VALUES (10,4,'Vaov, it is crazy.','2018-10-08 08:23:19.120');
INSERT INTO REVIEW(Cid,Pid,Comment,Time) VALUES (1,4,'Yeah man!!','2018-10-08 08:23:19.120');
INSERT INTO REVIEW(Cid,Pid,Comment,Time) VALUES (5,6,'Where is the Explanation ??','2018-10-08 08:23:19.120');
