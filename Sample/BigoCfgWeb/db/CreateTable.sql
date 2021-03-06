
/*
创建日期：2012/12/18
创建人  ：Leon
创建内容：创建Bigo配置管理系统后台配置表
 */

 --创建用户表
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
);

--创建用户权限关联表
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);

CREATE INDEX "auth_user_groups_403f60f" ON "auth_user_groups" ("user_id");

CREATE INDEX "auth_user_groups_425ae3c4" ON "auth_user_groups" ("group_id");

--
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);

CREATE INDEX "auth_permission_1bb8f392" ON "auth_permission" ("content_type_id");

--
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);

CREATE INDEX "auth_user_user_permissions_1e014c8f" ON "auth_user_user_permissions" ("permission_id");

CREATE INDEX "auth_user_user_permissions_403f60f" ON "auth_user_user_permissions" ("user_id");


--
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);

CREATE INDEX "auth_group_permissions_1e014c8f" ON "auth_group_permissions" ("permission_id");

CREATE INDEX "auth_group_permissions_425ae3c4" ON "auth_group_permissions" ("group_id");

--
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);


insert into auth_permission values(1,'Can add group',2,'add_group')
insert into auth_permission values(2,'Can add permission',1,'add_permission')
insert into auth_permission values(3,'Can add user',3,'add_user')
insert into auth_permission values(4,'Can change group',2,'change_group')
insert into auth_permission values(5,'Can change permission',1,'change_permission')
insert into auth_permission values(6,'Can change user',3,'change_user')
insert into auth_permission values(7,'Can delete group',2,'delete_group')
insert into auth_permission values(8,'Can delete permission',1,'delete_permission')
insert into auth_permission values(9,'Can delete user',3,'delete_user')
insert into auth_permission values(10,'Can add content type',4,'add_contenttype')
insert into auth_permission values(11,'Can change content type',4,'change_contenttype')
insert into auth_permission values(12,'Can delete content type',4,'delete_contenttype')
insert into auth_permission values(13,'Can add session',5,'add_session')
insert into auth_permission values(14,'Can change session',5,'change_session')
insert into auth_permission values(15,'Can delete session',5,'delete_session')
insert into auth_permission values(16,'Can add site',6,'add_site')
insert into auth_permission values(17,'Can change site',6,'change_site')
insert into auth_permission values(18,'Can delete site',6,'delete_site')
insert into auth_permission values(19,'Can add log entry',7,'add_logentry')
insert into auth_permission values(20,'Can change log entry',7,'change_logentry')
insert into auth_permission values(21,'Can delete log entry',7,'delete_logentry')