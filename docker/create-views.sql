-- Run after migrations to create views used by TileStache.
-- docker compose exec db psql -U nycharealtalk nycharealtalk -f /docker-entrypoint-initdb.d/create-views.sql

-- PostGIS 3.x removed ST_Distance_Sphere; Django 1.11's GeoDjango still generates that name.
CREATE OR REPLACE FUNCTION ST_Distance_Sphere(geometry, geometry)
RETURNS float8 AS $$
    SELECT ST_DistanceSphere($1, $2);
$$ LANGUAGE SQL IMMUTABLE STRICT;

CREATE OR REPLACE VIEW visible_centroids AS
    SELECT l.id AS id, l.commons_type, l.bbl, l.centroid, l.owner_id, l.priority,
           l.organizing, l.radpact_converted, l.radpact_planned,
           l.preservation_trust_voting_planned, l.preservation_trust_complete,
           l.private_infill_planned, l.section_8_pre_2014, l.demolition_proposed,
           l.demolition_completed, l.nycha_modernization_planned,
           l.nycha_modernization_complete, l.new_public_housing_built,
           l.new_public_housing_planned, l.private_infill_completed
    FROM lots_lot l
    WHERE l.group_id IS NULL AND l.centroid IS NOT NULL;

CREATE OR REPLACE VIEW visible_polygons AS
    SELECT l.id, l.commons_type, l.bbl, l.polygon, l.owner_id, l.priority,
           l.organizing, l.radpact_converted, l.radpact_planned,
           l.preservation_trust_voting_planned, l.preservation_trust_complete,
           l.private_infill_planned, l.section_8_pre_2014, l.demolition_proposed,
           l.demolition_completed, l.nycha_modernization_planned,
           l.nycha_modernization_complete, l.new_public_housing_built,
           l.new_public_housing_planned, l.private_infill_completed
    FROM lots_lot l
    WHERE l.group_id IS NULL AND l.polygon IS NOT NULL;
