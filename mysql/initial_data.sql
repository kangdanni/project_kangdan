use django-app-db;

set foreign_key_checks = 0;

DROP TABLE IF EXISTS project_category;
DROP TABLE IF EXISTS project_coupon;
DROP TABLE IF EXISTS project_product;

CREATE TABLE project_category
(
    id int         NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '상품 아이디',
    name varchar(100) NOT NULL COMMENT '카테고리명',
    UNIQUE KEY uk (name)
);

INSERT INTO project_category(name)
VALUES ('교양'),('자기계발'),('경제경영'),('수필');


CREATE TABLE project_coupon
(
    id  int         NOT NULL AUTO_INCREMENT  PRIMARY KEY COMMENT '아이디',
    code varchar(255) NOT NULL COMMENT '쿠폰코드',
    discount_rate float  NULL COMMENT '할인율',
    UNIQUE KEY uk (code)
);

INSERT INTO project_coupon(code,discount_rate)
VALUES ('A',0.1),('B',0.5),('C',0.3);

CREATE TABLE project_product
(
    id  int         NOT NULL AUTO_INCREMENT COMMENT '상품 아이디',
    name varchar(255) NOT NULL COMMENT '상품명',
    description text NULL COMMENT '설명',
    price int  NULL COMMENT '가격',
    category varchar(100)  NULL COMMENT '카테고리',
    discount_rate float NULL COMMENT '할인율',
    coupon_applicable BOOL COMMENT '쿠폰적용여부',
    CONSTRAINT CUSTOMER_PK PRIMARY KEY (id),
    FOREIGN KEY (category) REFERENCES project_category (name) ON UPDATE CASCADE
) ;

INSERT INTO project_product(name,description,price,category,discount_rate,coupon_applicable)
VALUES ('채식주의자','채식주의자 2007년도',20000,'교양',0.1,1),
       ('소년이온다','소년이온다 2014년도',22000,'교양',0.5,1),
       ('흰','흰 2016년도',10000,'자기계발',0.2,0),
       ('작별하지않는다','작별하지않는다 2021년도',15000,'수필',0.3,0),
       ('희랍어시간','희랍어 시간 2011년도',17000,'경제경영',0.1,0)
;
SET foreign_key_checks = 1;
