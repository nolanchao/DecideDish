
drop table if exists groupnames;
create table groupnames (
	group_id integer primary key,
	groupnames text not null,
	name text not null,
	city text not null,
	state text not null
);

drop table if exists preferences;
create table preferences (
	preferences_id integer primary key,
	groupnames text not null,
	name text not null,
	cuisine text,
	priceInput text,
	radius integer,
	chinese integer,
	pizza integer, 
	mexican integer, 
	italian integer, 
	ethiopian integer, 
	sandwiches integer, 
	steak integer, 
	french integer, 
	diners integer, 
	burgers integer, 
	barbecue integer,
	ramen integer
);






