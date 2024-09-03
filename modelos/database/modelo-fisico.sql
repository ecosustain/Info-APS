CREATE SCHEMA IF NOT EXISTS "public";

CREATE  TABLE "public".auth_group ( 
	id                   integer  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	name                 varchar(150)  NOT NULL  ,
	CONSTRAINT auth_group_pkey PRIMARY KEY ( id ),
	CONSTRAINT auth_group_name_key UNIQUE ( name ) 
 );

CREATE INDEX auth_group_name_a6ea08ec_like ON "public".auth_group USING  btree ( name  varchar_pattern_ops );

CREATE  TABLE "public".auth_user ( 
	id                   integer  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	"password"           varchar(128)  NOT NULL  ,
	last_login           timestamptz    ,
	is_superuser         boolean  NOT NULL  ,
	username             varchar(150)  NOT NULL  ,
	first_name           varchar(150)  NOT NULL  ,
	last_name            varchar(150)  NOT NULL  ,
	email                varchar(254)  NOT NULL  ,
	is_staff             boolean  NOT NULL  ,
	is_active            boolean  NOT NULL  ,
	date_joined          timestamptz  NOT NULL  ,
	CONSTRAINT auth_user_pkey PRIMARY KEY ( id ),
	CONSTRAINT auth_user_username_key UNIQUE ( username ) 
 );

CREATE INDEX auth_user_username_6821ab7c_like ON "public".auth_user USING  btree ( username  varchar_pattern_ops );

CREATE  TABLE "public".auth_user_groups ( 
	id                   bigint  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	user_id              integer  NOT NULL  ,
	group_id             integer  NOT NULL  ,
	CONSTRAINT auth_user_groups_pkey PRIMARY KEY ( id ),
	CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE ( user_id, group_id ) 
 );

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON "public".auth_user_groups USING  btree ( user_id );

CREATE INDEX auth_user_groups_group_id_97559544 ON "public".auth_user_groups USING  btree ( group_id );

CREATE  TABLE "public".django_content_type ( 
	id                   integer  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	app_label            varchar(100)  NOT NULL  ,
	model                varchar(100)  NOT NULL  ,
	CONSTRAINT django_content_type_pkey PRIMARY KEY ( id ),
	CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE ( app_label, model ) 
 );

CREATE  TABLE "public".django_migrations ( 
	id                   bigint  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	app                  varchar(255)  NOT NULL  ,
	name                 varchar(255)  NOT NULL  ,
	applied              timestamptz  NOT NULL  ,
	CONSTRAINT django_migrations_pkey PRIMARY KEY ( id )
 );

CREATE  TABLE "public".django_session ( 
	session_key          varchar(40)  NOT NULL  ,
	session_data         text  NOT NULL  ,
	expire_date          timestamptz  NOT NULL  ,
	CONSTRAINT django_session_pkey PRIMARY KEY ( session_key )
 );

CREATE INDEX django_session_session_key_c0390e0f_like ON "public".django_session USING  btree ( session_key  varchar_pattern_ops );

CREATE INDEX django_session_expire_date_a5c62663 ON "public".django_session USING  btree ( expire_date );

CREATE  TABLE "public".geo_unit_type ( 
	created_at           timestamptz  NOT NULL  ,
	updated_at           timestamptz  NOT NULL  ,
	name                 varchar(50)  NOT NULL  ,
	description          text  NOT NULL  ,
	CONSTRAINT geo_unit_type_pkey PRIMARY KEY ( name )
 );

CREATE INDEX geo_unit_type_name_6f319be1_like ON "public".geo_unit_type USING  btree ( name  varchar_pattern_ops );

CREATE  TABLE "public".individual_category ( 
	created_at           timestamptz  NOT NULL  ,
	updated_at           timestamptz  NOT NULL  ,
	name                 varchar(255)  NOT NULL  ,
	CONSTRAINT individual_category_pkey PRIMARY KEY ( name )
 );

CREATE INDEX individual_category_name_936cab38_like ON "public".individual_category USING  btree ( name  varchar_pattern_ops );

CREATE  TABLE "public".auth_permission ( 
	id                   integer  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	name                 varchar(255)  NOT NULL  ,
	content_type_id      integer  NOT NULL  ,
	codename             varchar(100)  NOT NULL  ,
	CONSTRAINT auth_permission_pkey PRIMARY KEY ( id ),
	CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE ( content_type_id, codename ) 
 );

CREATE INDEX auth_permission_content_type_id_2f476e4b ON "public".auth_permission USING  btree ( content_type_id );

CREATE  TABLE "public".auth_user_user_permissions ( 
	id                   bigint  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	user_id              integer  NOT NULL  ,
	permission_id        integer  NOT NULL  ,
	CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY ( id ),
	CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE ( user_id, permission_id ) 
 );

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON "public".auth_user_user_permissions USING  btree ( user_id );

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON "public".auth_user_user_permissions USING  btree ( permission_id );

CREATE  TABLE "public".django_admin_log ( 
	id                   integer  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	action_time          timestamptz  NOT NULL  ,
	object_id            text    ,
	object_repr          varchar(200)  NOT NULL  ,
	action_flag          smallint  NOT NULL  ,
	change_message       text  NOT NULL  ,
	content_type_id      integer    ,
	user_id              integer  NOT NULL  ,
	CONSTRAINT django_admin_log_pkey PRIMARY KEY ( id )
 );

ALTER TABLE "public".django_admin_log ADD CONSTRAINT django_admin_log_action_flag_check CHECK ( (action_flag >= 0) );

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON "public".django_admin_log USING  btree ( content_type_id );

CREATE INDEX django_admin_log_user_id_c564eba6 ON "public".django_admin_log USING  btree ( user_id );

CREATE  TABLE "public".geo_unit ( 
	id                   bigint  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	created_at           timestamptz  NOT NULL  ,
	updated_at           timestamptz  NOT NULL  ,
	name                 varchar(100)  NOT NULL  ,
	description          text  NOT NULL  ,
	parent_id            bigint    ,
	type_id              varchar(50)  NOT NULL  ,
	CONSTRAINT geo_unit_pkey PRIMARY KEY ( id )
 );

CREATE INDEX geo_unit_parent_id_91e1a8f5 ON "public".geo_unit USING  btree ( parent_id );

CREATE INDEX geo_unit_type_id_b053d984 ON "public".geo_unit USING  btree ( type_id );

CREATE INDEX geo_unit_type_id_b053d984_like ON "public".geo_unit USING  btree ( type_id  varchar_pattern_ops );

CREATE  TABLE "public".individual_care ( 
	id                   bigint  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	created_at           timestamptz  NOT NULL  ,
	updated_at           timestamptz  NOT NULL  ,
	group_param          varchar(255)  NOT NULL  ,
	class_param          varchar(255)  NOT NULL  ,
	ibge                 integer    ,
	ine                  integer    ,
	cnes                 integer    ,
	"year"               integer  NOT NULL  ,
	"month"              integer  NOT NULL  ,
	geo_unit_id          bigint  NOT NULL  ,
	CONSTRAINT individual_care_pkey PRIMARY KEY ( id )
 );

CREATE INDEX individual_care_geo_unit_id_0b58ddde ON "public".individual_care USING  btree ( geo_unit_id );

CREATE  TABLE "public".individual_care_category ( 
	id                   bigint  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	created_at           timestamptz  NOT NULL  ,
	updated_at           timestamptz  NOT NULL  ,
	"value"              integer  NOT NULL  ,
	individual_care_id   bigint  NOT NULL  ,
	individual_category_id varchar(255)  NOT NULL  ,
	CONSTRAINT individual_care_category_pkey PRIMARY KEY ( id )
 );

CREATE INDEX individual_care_category_individual_care_id_963f0526 ON "public".individual_care_category USING  btree ( individual_care_id );

CREATE INDEX individual_care_category_individual_category_id_81a964f2 ON "public".individual_care_category USING  btree ( individual_category_id );

CREATE INDEX individual_care_category_individual_category_id_81a964f2_like ON "public".individual_care_category USING  btree ( individual_category_id  varchar_pattern_ops );

CREATE  TABLE "public".auth_group_permissions ( 
	id                   bigint  NOT NULL GENERATED  BY DEFAULT AS IDENTITY ,
	group_id             integer  NOT NULL  ,
	permission_id        integer  NOT NULL  ,
	CONSTRAINT auth_group_permissions_pkey PRIMARY KEY ( id ),
	CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE ( group_id, permission_id ) 
 );

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON "public".auth_group_permissions USING  btree ( group_id );

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON "public".auth_group_permissions USING  btree ( permission_id );

ALTER TABLE "public".auth_group_permissions ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY ( group_id ) REFERENCES "public".auth_group( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".auth_group_permissions ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY ( permission_id ) REFERENCES "public".auth_permission( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".auth_permission ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY ( content_type_id ) REFERENCES "public".django_content_type( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".auth_user_groups ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY ( user_id ) REFERENCES "public".auth_user( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".auth_user_groups ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY ( group_id ) REFERENCES "public".auth_group( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".auth_user_user_permissions ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY ( user_id ) REFERENCES "public".auth_user( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".auth_user_user_permissions ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY ( permission_id ) REFERENCES "public".auth_permission( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".django_admin_log ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY ( content_type_id ) REFERENCES "public".django_content_type( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".django_admin_log ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY ( user_id ) REFERENCES "public".auth_user( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".geo_unit ADD CONSTRAINT geo_unit_parent_id_91e1a8f5_fk_geo_unit_id FOREIGN KEY ( parent_id ) REFERENCES "public".geo_unit( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".geo_unit ADD CONSTRAINT geo_unit_type_id_b053d984_fk_geo_unit_type_name FOREIGN KEY ( type_id ) REFERENCES "public".geo_unit_type( name )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".individual_care ADD CONSTRAINT individual_care_geo_unit_id_0b58ddde_fk_geo_unit_id FOREIGN KEY ( geo_unit_id ) REFERENCES "public".geo_unit( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".individual_care_category ADD CONSTRAINT individual_care_cate_individual_care_id_963f0526_fk_individua FOREIGN KEY ( individual_care_id ) REFERENCES "public".individual_care( id )   DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "public".individual_care_category ADD CONSTRAINT individual_care_cate_individual_category__81a964f2_fk_individua FOREIGN KEY ( individual_category_id ) REFERENCES "public".individual_category( name )   DEFERRABLE INITIALLY DEFERRED;

CREATE OR REPLACE FUNCTION public.akeys(hstore)
 RETURNS text[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_akeys$function$
;

CREATE OR REPLACE FUNCTION public.avals(hstore)
 RETURNS text[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_avals$function$
;

CREATE OR REPLACE FUNCTION public.defined(hstore, text)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_defined$function$
;

CREATE OR REPLACE FUNCTION public.delete(hstore, text)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_delete$function$
;

CREATE OR REPLACE FUNCTION public.delete(hstore, text[])
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_delete_array$function$
;

CREATE OR REPLACE FUNCTION public.delete(hstore, hstore)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_delete_hstore$function$
;

CREATE OR REPLACE FUNCTION public.each(hs hstore, OUT key text, OUT value text)
 RETURNS SETOF record
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_each$function$
;

CREATE OR REPLACE FUNCTION public.exist(hstore, text)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_exists$function$
;

CREATE OR REPLACE FUNCTION public.exists_all(hstore, text[])
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_exists_all$function$
;

CREATE OR REPLACE FUNCTION public.exists_any(hstore, text[])
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_exists_any$function$
;

CREATE OR REPLACE FUNCTION public.fetchval(hstore, text)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_fetchval$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_compress(internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_compress$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_consistent(internal, hstore, smallint, oid, internal)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_consistent$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_decompress(internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_decompress$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_in(cstring)
 RETURNS ghstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_in$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_options(internal)
 RETURNS void
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE
AS '$libdir/hstore', $function$ghstore_options$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_out(ghstore)
 RETURNS cstring
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_out$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_penalty(internal, internal, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_penalty$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_picksplit(internal, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_picksplit$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_same(ghstore, ghstore, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_same$function$
;

CREATE OR REPLACE FUNCTION public.ghstore_union(internal, internal)
 RETURNS ghstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$ghstore_union$function$
;

CREATE OR REPLACE FUNCTION public.gin_consistent_hstore(internal, smallint, hstore, integer, internal, internal)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$gin_consistent_hstore$function$
;

CREATE OR REPLACE FUNCTION public.gin_extract_hstore(hstore, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$gin_extract_hstore$function$
;

CREATE OR REPLACE FUNCTION public.gin_extract_hstore_query(hstore, internal, smallint, internal, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$gin_extract_hstore_query$function$
;

CREATE OR REPLACE FUNCTION public.hs_concat(hstore, hstore)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_concat$function$
;

CREATE OR REPLACE FUNCTION public.hs_contained(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_contained$function$
;

CREATE OR REPLACE FUNCTION public.hs_contains(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_contains$function$
;

CREATE OR REPLACE FUNCTION public.hstore(text, text)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE
AS '$libdir/hstore', $function$hstore_from_text$function$
;

CREATE OR REPLACE FUNCTION public.hstore(text[], text[])
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE
AS '$libdir/hstore', $function$hstore_from_arrays$function$
;

CREATE OR REPLACE FUNCTION public.hstore(text[])
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_from_array$function$
;

CREATE OR REPLACE FUNCTION public.hstore(record)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE
AS '$libdir/hstore', $function$hstore_from_record$function$
;

CREATE OR REPLACE FUNCTION public.hstore_cmp(hstore, hstore)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_cmp$function$
;

CREATE OR REPLACE FUNCTION public.hstore_eq(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_eq$function$
;

CREATE OR REPLACE FUNCTION public.hstore_ge(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_ge$function$
;

CREATE OR REPLACE FUNCTION public.hstore_gt(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_gt$function$
;

CREATE OR REPLACE FUNCTION public.hstore_hash(hstore)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_hash$function$
;

CREATE OR REPLACE FUNCTION public.hstore_hash_extended(hstore, bigint)
 RETURNS bigint
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_hash_extended$function$
;

CREATE OR REPLACE FUNCTION public.hstore_in(cstring)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_in$function$
;

CREATE OR REPLACE FUNCTION public.hstore_le(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_le$function$
;

CREATE OR REPLACE FUNCTION public.hstore_lt(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_lt$function$
;

CREATE OR REPLACE FUNCTION public.hstore_ne(hstore, hstore)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_ne$function$
;

CREATE OR REPLACE FUNCTION public.hstore_out(hstore)
 RETURNS cstring
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_out$function$
;

CREATE OR REPLACE FUNCTION public.hstore_recv(internal)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_recv$function$
;

CREATE OR REPLACE FUNCTION public.hstore_send(hstore)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_send$function$
;

CREATE OR REPLACE FUNCTION public.hstore_subscript_handler(internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_subscript_handler$function$
;

CREATE OR REPLACE FUNCTION public.hstore_to_array(hstore)
 RETURNS text[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_to_array$function$
;

CREATE OR REPLACE FUNCTION public.hstore_to_json(hstore)
 RETURNS json
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_to_json$function$
;

CREATE OR REPLACE FUNCTION public.hstore_to_json_loose(hstore)
 RETURNS json
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_to_json_loose$function$
;

CREATE OR REPLACE FUNCTION public.hstore_to_jsonb(hstore)
 RETURNS jsonb
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_to_jsonb$function$
;

CREATE OR REPLACE FUNCTION public.hstore_to_jsonb_loose(hstore)
 RETURNS jsonb
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_to_jsonb_loose$function$
;

CREATE OR REPLACE FUNCTION public.hstore_to_matrix(hstore)
 RETURNS text[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_to_matrix$function$
;

CREATE OR REPLACE FUNCTION public.hstore_version_diag(hstore)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_version_diag$function$
;

CREATE OR REPLACE FUNCTION public.isdefined(hstore, text)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_defined$function$
;

CREATE OR REPLACE FUNCTION public.isexists(hstore, text)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_exists$function$
;

CREATE OR REPLACE FUNCTION public.populate_record(anyelement, hstore)
 RETURNS anyelement
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE
AS '$libdir/hstore', $function$hstore_populate_record$function$
;

CREATE OR REPLACE FUNCTION public.skeys(hstore)
 RETURNS SETOF text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_skeys$function$
;

CREATE OR REPLACE FUNCTION public.slice(hstore, text[])
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_slice_to_hstore$function$
;

CREATE OR REPLACE FUNCTION public.slice_array(hstore, text[])
 RETURNS text[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_slice_to_array$function$
;

CREATE OR REPLACE FUNCTION public.svals(hstore)
 RETURNS SETOF text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/hstore', $function$hstore_svals$function$
;

CREATE OR REPLACE FUNCTION public.tconvert(text, text)
 RETURNS hstore
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE
AS '$libdir/hstore', $function$hstore_from_text$function$
;

