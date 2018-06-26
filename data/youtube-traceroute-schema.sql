DROP TABLE IF EXISTS msmpoint;
CREATE TABLE "msmpoint" (
  skunitid        TEXT,
  msmid           TEXT,
  mac             TEXT,
  name            TEXT,
  hardware        TEXT
);

DROP TABLE IF EXISTS traceroute;
CREATE TABLE "traceroute" (
  unit_id         INT,
  dtime           TEXT,
  version         TEXT,
  source          TEXT,
  destination     TEXT,
  method          TEXT,
  status          TEXT,
  ttl             INT,
  endpoint        TEXT,
  rtt             TEXT,
  location_id     INT
);
