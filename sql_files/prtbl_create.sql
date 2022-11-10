create table prtbl(
	c_code char(6) Not Null,
	p_date DATE Not Null,
    price int not null,
    PRIMARY KEY (c_code, p_date),
    FOREIGN KEY (c_code) REFERENCES comtbl (c_code)
);