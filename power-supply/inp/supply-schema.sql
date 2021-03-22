CREATE TABLE External_Supply(
    id       integer primary key,
    name       text,
    make       text,
    connected_systems text,
    interface   text,
    prog_voltage real,
    prog_current real
);

INSERT into External_Supply (id, name, make, interface, connected_systems, prog_voltage, prog_current) values(1, "PS-1", "LAMBDA", "legacy", "INS_OBC, Avionics, Seeker Electronics", 28.0, 10.0);
INSERT into External_Supply (id, name, make, interface, connected_systems, prog_voltage, prog_current) values(2, "PS-2", "LAMBDA", "legacy", "EMA_SERVO", 50.0, 20.0);
INSERT into External_Supply (id, name, make, interface, connected_systems, prog_voltage, prog_current) values(3, "PS-3", "LAMBDA", "legacy", "Seeker Tx+Heater", 50.0, 20.0);


CREATE TABLE Internal_Supply(
    id       integer primary key,
    name       text,
    make       text,
    connected_systems text,
    interface   text,
    prog_voltage real,
    prog_current real
);
INSERT into Internal_Supply (id, name, make, interface, connected_systems, prog_voltage, prog_current) values(4, "PS-1", "LAMBDA", "legacy", "INS_OBC, Avionics, Seeker Electronics", 28.0, 10.0);
INSERT into Internal_Supply (id, name, make, interface, connected_systems, prog_voltage, prog_current) values(5, "PS-2", "LAMBDA", "legacy", "EMA_SERVO", 50, 20.0);
INSERT into Internal_Supply (id, name, make, interface, connected_systems, prog_voltage, prog_current) values(6, "PS-3", "LAMBDA", "legacy", "Seeker Tx+Heater", 50.0, 20.0);


CREATE TABLE Logtable(
    id integer primary key autoincrement not null,
    log text
);

CREATE TABLE EVENTS(
    id integer primary key autoincrement not null,
    event text
);
