CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SELECT uuid_generate_v4();

CREATE TABLE applications (
  id uuid DEFAULT uuid_generate_v4 (),
  first_name VARCHAR (50) NOT NULL,
  last_name VARCHAR (50) NOT NULL,
  status VARCHAR (50) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO applications (first_name, last_name, status)
VALUES
    ('Karl', 'Svensson', 'pending'),
    ('Bertil', 'Ahlander', 'pending'),
    ('Rune', 'Hopp', 'completed'),
    ('Hugo', 'Bergius', 'completed'),
    ('Nils', 'Tornquist', 'completed'),
    ('Gabriel', 'Widforss', 'rejected'),
    ('Edvin', 'Carlsson', 'rejected'),
    ('Holvaster', 'Magnusson', 'rejected'),
    ('Mikael', 'Lundmark', 'rejected');

INSERT INTO applications (id, first_name, last_name, status)
VALUES
    ('66cd16f4-2d68-49ae-a15a-71b9de47ac19','Anna', 'Luttu', 'pending');
