CREATE TABLE IF NOT EXISTS users (u_id SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR (100) NOT NULL, 
lastname VARCHAR (100) NOT NULL, othername VARCHAR (100), username VARCHAR (100) NOT NULL, email VARCHAR (100) NOT NULL, 
phone VARCHAR (100) NOT NULL, isAdmin VARCHAR (100) NOT NULL, password VARCHAR (250) NOT NULL, created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS meetups (m_id SERIAL PRIMARY KEY NOT NULL, topic VARCHAR (255) NOT NULL, 
location VARCHAR (100) NOT NULL, happening_on TIMESTAMP, tags VARCHAR (255) NOT NULL, created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS questions (q_id SERIAL PRIMARY KEY NOT NULL, title VARCHAR (255) NOT NULL, body VARCHAR (500) NOT NULL, 
meetup VARCHAR (100) NOT NULL, created_by VARCHAR (100) NOT NULL, created_at TIMESTAMP, votes INTEGER DEFAULT 0);
