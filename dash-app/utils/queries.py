# utils/queries.py
# utils/queries.py

GET_REGIONS = """
    SELECT DISTINCT name, id
    FROM geo_unit
    WHERE type_id = 'Macro-Regiao'
    ORDER BY name
"""

GET_STATES = """
    SELECT DISTINCT name, id
    FROM geo_unit
    WHERE parent_id = %s 
    ORDER BY name
"""

GET_CITIES = """
    SELECT DISTINCT name, id
    FROM geo_unit
    WHERE parent_id = %s 
    ORDER BY name
"""

GET_CATEGORIES = """
    SELECT distinct(ic.name)
    FROM individual_category ic
        INNER JOIN individual_care_category icc ON ( icc.individual_category_id = ic.name  )
        INNER JOIN individual_care ic1 ON ( ic1.id = icc.individual_care_id  )
    where ic1.geo_unit_id = ANY(%s)
    order by ic.name;
"""

GET_DATA_BY_REGION = """
select cat.name, sum(icc.value) as total, region.name as geo_unit, ic.year
from individual_care ic
inner join public.individual_care_category icc on ic.id = icc.individual_care_id
inner join public.individual_category cat on cat.name = icc.individual_category_id
inner join public.geo_unit city on city.id = ic.geo_unit_id
inner join public.geo_unit state on state.id = city.parent_id
inner join public.geo_unit region on region.id = state.parent_id
where ic.geo_unit_id in (
SELECT gu2.id
FROM "public".geo_unit gu
	INNER JOIN "public".geo_unit gu1 ON ( gu1.parent_id = gu.id  )
	INNER JOIN "public".geo_unit gu2 ON ( gu2.parent_id = gu1.id  )
where gu.id = %s )
GROUP BY cat.name, region.name, ic.year
ORDER BY total;
"""

GET_DATA_BY_STATE = """
select cat.name, sum(icc.value) as total, state.name as geo_unit, ic.year
from individual_care ic
inner join public.individual_care_category icc on ic.id = icc.individual_care_id
inner join public.individual_category cat on cat.name = icc.individual_category_id
inner join public.geo_unit city on city.id = ic.geo_unit_id
inner join public.geo_unit state on state.id = city.parent_id
inner join public.geo_unit region on region.id = state.parent_id
where ic.geo_unit_id in (
SELECT gu2.id
FROM "public".geo_unit gu
	INNER JOIN "public".geo_unit gu1 ON ( gu1.parent_id = gu.id  )
	INNER JOIN "public".geo_unit gu2 ON ( gu2.parent_id = gu1.id  )
where gu1.id = %s )
GROUP BY cat.name, state.name, ic.year
ORDER BY total;
"""

GET_DATA_BY_CITY = """
select cat.name, sum(icc.value) as total, city.name as geo_unit, ic.year
from individual_care ic
inner join public.individual_care_category icc on ic.id = icc.individual_care_id
inner join public.individual_category cat on cat.name = icc.individual_category_id
inner join public.geo_unit city on ic.geo_unit_id = city.id
where ic.geo_unit_id in (
SELECT gu2.id
FROM "public".geo_unit gu
	INNER JOIN "public".geo_unit gu1 ON ( gu1.parent_id = gu.id  )
	INNER JOIN "public".geo_unit gu2 ON ( gu2.parent_id = gu1.id  )
where gu2.id = ANY(%s) )
GROUP BY cat.name, city.name, ic.year
ORDER BY total;
"""

GET_DATA_BY_CATEGORY = """
select cat.name, sum(icc.value) as total, city.name as geo_unit, ic.year
from individual_care ic
inner join public.individual_care_category icc on ic.id = icc.individual_care_id
inner join public.individual_category cat on cat.name = icc.individual_category_id
inner join public.geo_unit city on ic.geo_unit_id = city.id
where ic.geo_unit_id in (
SELECT gu2.id
FROM "public".geo_unit gu
	INNER JOIN "public".geo_unit gu1 ON ( gu1.parent_id = gu.id  )
	INNER JOIN "public".geo_unit gu2 ON ( gu2.parent_id = gu1.id  )
where gu2.id = ANY(%s) )
AND cat.name = ANY(%s)
GROUP BY cat.name, city.name, ic.year
ORDER BY total;
"""
