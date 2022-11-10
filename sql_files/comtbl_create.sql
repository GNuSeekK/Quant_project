create table comtbl (
	c_code char(6) Not Null,
    c_name varchar(20) Not Null,
    c_kindlarge char(2) Not Null,
    c_kindsmall char(4) Not Null,
    PRIMARY KEY (c_code),
    FOREIGN KEY (c_kindlarge) REFERENCES ktbl (kind),
    FOREIGN KEY (c_kindsmall) REFERENCES ktbl (kind)
);