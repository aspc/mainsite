SELECT pg_reload_conf();
DO
$body$
BEGIN
   IF NOT EXISTS (
      SELECT *
      FROM   pg_catalog.pg_user
      WHERE  usename = 'main') THEN

      CREATE ROLE main LOGIN PASSWORD 'dev_password';
   END IF;
   ALTER USER main CREATEDB;
END
$body$