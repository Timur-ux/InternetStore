insert into
  access(name, privileges)
values
  (
    'user'
  ),
  (
    'administrator'
  );

insert into
 users(access_level, login, password)
values
  (
    (select id from access where name = 'administrator'),
    'admin',
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
  );
