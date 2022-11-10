create table ftbl (
	c_code char(6) Not Null,
    f_date DATE Not Null,
    sales BIGINT NOT Null,
    gm BIGINT NOT Null,
    ni BIGINT NOT Null,
    asset BIGINT NOT Null,
    ca BIGINT NOT Null,
    cl BIGINT NOT Null,
    issued_shares BIGINT NOT Null,
    bps INT NOT Null,
    EPS INT NOT Null,
    PRIMARY KEY (c_code, f_date),
    FOREIGN KEY (c_code) REFERENCES comtbl (c_code)
);