# utils/queries.py

GET_ACTIVITY = """
    SELECT DISTINCT group_param
    FROM individual_care
    ORDER BY group_param
"""

GET_REGIONS = """
    SELECT DISTINCT name, id
    FROM geo_unit
    WHERE type_id = 'Macro-Regiao'
    ORDER BY name
"""

GET_STATES = """
    SELECT DISTINCT name, id
    FROM geo_unit
    WHERE parent_id = ANY(%s) 
    ORDER BY name
"""

GET_CITIES = """
    SELECT DISTINCT name, id
    FROM geo_unit
    WHERE parent_id = ANY(%s) 
    ORDER BY name
"""

GET_CATEGORY_BY_CITY = """
    SELECT distinct(ic.name)
    FROM individual_category ic
        INNER JOIN individual_care_category icc ON ( icc.individual_category_id = ic.id  )
        INNER JOIN individual_care ic1 ON ( ic1.id = icc.individual_care_id  )
    where ic1.geo_unit_id = ANY(%s)
    order by ic.name;
"""
GET_CATEGORY_BY_ACTIVITY = """
select name from materialized_view_category WHERE group_param = ANY(%s) order by name;
"""

GET_CATEGORY_BY_ACTIVITY_OLD = """
select cat.name
from individual_care ic
inner join individual_care_category icc on ic.id = icc.individual_care_id
inner join individual_category cat on cat.id = icc.individual_category_id
inner join geo_unit city on city.id = ic.geo_unit_id
inner join geo_unit state on state.id = city.parent_id
inner join geo_unit region on region.id = state.parent_id
WHERE ic.group_param = ANY(%s)
GROUP BY cat.name
ORDER BY cat.name;
"""

GET_CATEGORY_ALL = """
    SELECT distinct(ic.name)
    FROM individual_category ic
        INNER JOIN individual_care_category icc ON ( icc.individual_category_id = ic.id  )
        INNER JOIN individual_care ic1 ON ( ic1.id = icc.individual_care_id  )
    order by ic.name;
"""

GET_DATA_BY_REGION = """
select name, total, geo_unit, year from materialized_view_region where geo_unit_id = ANY(%s) 
"""
# select cat.name, sum(icc.value) as total, region.name as geo_unit, ic.year
# from individual_care ic
# inner join individual_care_category icc on ic.id = icc.individual_care_id
# inner join individual_category cat on cat.id = icc.individual_category_id
# inner join geo_unit city on city.id = ic.geo_unit_id
# inner join geo_unit state on state.id = city.parent_id
# inner join geo_unit region on region.id = state.parent_id
# where region.id = ANY(%s)
# GROUP BY cat.name, region.name, ic.year
# ORDER BY total;


GET_DATA_BY_REGION_ALL = """
select name, total, geo_unit, year from materialized_view_region
"""
# select cat.name, sum(icc.value) as total, region.name as geo_unit, ic.year
# from individual_care ic
# inner join individual_care_category icc on ic.id = icc.individual_care_id
# inner join individual_category cat on cat.id = icc.individual_category_id
# inner join geo_unit city on city.id = ic.geo_unit_id
# inner join geo_unit state on state.id = city.parent_id
# inner join geo_unit region on region.id = state.parent_id
# GROUP BY cat.name, region.name, ic.year
# ORDER BY total;


GET_DATA_BY_STATE = """
    select name, total, geo_unit, year from materialized_view_state WHERE geo_unit_id = ANY(%s) 
"""

# select cat.name, sum(icc.value) as total, state.name as geo_unit, ic.year
# from individual_care ic
# inner join individual_care_category icc on ic.id = icc.individual_care_id
# inner join individual_category cat on cat.id = icc.individual_category_id
# inner join geo_unit city on city.id = ic.geo_unit_id
# inner join geo_unit state on state.id = city.parent_id
# inner join geo_unit region on region.id = state.parent_id
# WHERE state.id = ANY(%s)
# GROUP BY cat.name, ic.year, state.name
# ORDER BY total;


GET_DATA_BY_CITY = """
    select name, total, geo_unit, year from materialized_view_city WHERE geo_unit_id = ANY(%s) 
"""

# select cat.name, sum(icc.value) as total, city.name as geo_unit, ic.year
# from individual_care ic
# inner join individual_care_category icc on ic.id = icc.individual_care_id
# inner join individual_category cat on cat.id = icc.individual_category_id
# inner join geo_unit city on ic.geo_unit_id = city.id
# WHERE city.id = ANY(%s)
# GROUP BY cat.name, city.name, ic.year
# ORDER BY total;

GET_DATA_BY_CATEGORY = """
select cat.name, sum(icc.value) as total, city.name as geo_unit, ic.year
from individual_care ic
inner join individual_care_category icc on ic.id = icc.individual_care_id
inner join individual_category cat on cat.id = icc.individual_category_id
inner join geo_unit city on ic.geo_unit_id = city.id
WHERE 
city.id = ANY(%s) AND 
cat.name = ANY(%s)
GROUP BY cat.name, city.name, ic.year
ORDER BY total;
"""

GET_DATA_BY_ACTIVITY = """
SELECT 
    name, 
    total, 
    geo_unit, 
    year
FROM 
    materialized_view_activity
WHERE 
    group_param = ANY(%s) AND  -- Este é o único parâmetro obrigatório
    (region_id = ANY(%s) OR %s IS NULL) AND 
    (state_id = ANY(%s) OR %s IS NULL) AND 
    (city_id = ANY(%s) OR %s IS NULL) AND 
    (name = ANY(%s) OR %s IS NULL)
"""

# SELECT
#     cat.name,
#     SUM(icc.value) AS total,
#     city.name AS geo_unit,
#     ic.year
# FROM
#     individual_care ic
# INNER JOIN
#     individual_care_category icc ON ic.id = icc.individual_care_id
# INNER JOIN
#     individual_category cat ON cat.id = icc.individual_category_id
# INNER JOIN
#     geo_unit city ON ic.geo_unit_id = city.id
# INNER JOIN
#     geo_unit state ON state.id = city.parent_id
# INNER JOIN
#     geo_unit region ON region.id = state.parent_id
# WHERE
#     ic.group_param = ANY(%s) AND  -- Este é o único parâmetro obrigatório
#     (region.id = ANY(%s) OR %s IS NULL) AND
#     (state.id = ANY(%s) OR %s IS NULL) AND
#     (city.id = ANY(%s) OR %s IS NULL) AND
#     (cat.name = ANY(%s) OR %s IS NULL)
# GROUP BY
#     cat.name, city.name, ic.year
# ORDER BY
#     total;


GET_MAP_REGION_DATA_INIT = """
    select name,latitude,longitude,total, parent_id, geo_unit from search_max_by_region
"""

GET_MAP_REGION_DATA = """
    select name,latitude,longitude,total, parent_id, geo_unit from search_max_by_state where parent_id = ANY(%s)
"""

GET_MAP_STATE_DATA = """
    select name,latitude,longitude,total, parent_id, geo_unit from search_max_by_city where parent_id = %s
"""

GET_MAP_CITY_DATA = """
    select name,latitude,longitude,total, parent_id, geo_unit from search_max_by_city where geo_unit_id = ANY (%s)
"""

GET_MAP_ALL_CATEGORY_DATA = """
SELECT 
    name,
    latitude, longitude, 
    total, 
    geo_unit, 
    parent_id
FROM materialized_view_map_category
"""

GET_ALL_YEAR = """
select distinct year
    from individual_care order by year desc;
"""

GET_MAP_CATEGORY_DATA = """
SELECT 
    name,
    latitude, longitude, 
    total, 
    geo_unit, 
    parent_id
FROM materialized_view_map_category
WHERE
    group_param = ANY(%s) AND 
    (name = ANY(%s) OR %s IS NULL) AND
    (year = ANY(%s) OR %s IS NULL)
"""

# SELECT
#     cat.name,
#     city.latitude, city.longitude,
#     SUM(icc.value) AS total,
#     city.name AS geo_unit,
#     city.parent_id AS parent_id
# FROM
#     individual_care ic
# INNER JOIN
#     individual_care_category icc ON ic.id = icc.individual_care_id
# INNER JOIN
#     individual_category cat ON cat.id = icc.individual_category_id
# INNER JOIN
#     geo_unit city ON ic.geo_unit_id = city.id
# INNER JOIN
#     geo_unit state ON state.id = city.parent_id
# INNER JOIN
#     geo_unit region ON region.id = state.parent_id
# WHERE
#     ic.group_param = ANY(%s) AND
#     (cat.name = ANY(%s) OR %s IS NULL) AND
#     (ic.year = ANY(%s) OR %s IS NULL)
# GROUP BY
#     cat.name,
#     city.latitude, city.longitude,
#     city.name,
#     city.parent_id
# ORDER BY
#     total;

