CREATE TABLE IF NOT EXISTS users (
    u_id SERIAL PRIMARY KEY NOT NULL, 
    firstname VARCHAR (100) NOT NULL, 
    lastname VARCHAR (100) NOT NULL, 
    othername VARCHAR (100), 
    username VARCHAR (100) NOT NULL, 
    email VARCHAR (100) NOT NULL, 
    phone VARCHAR (100) NOT NULL, 
    isAdmin INTEGER, 
    password VARCHAR (250) NOT NULL, 
    created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS meetups (
    m_id SERIAL PRIMARY KEY NOT NULL, 
    topic VARCHAR (255) NOT NULL, 
    description VARCHAR (2048) NOT NULL, 
    location VARCHAR (100) NOT NULL, 
    happening_on TIMESTAMP, 
    created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS questions (
    q_id SERIAL PRIMARY KEY NOT NULL, 
    title VARCHAR (255) NOT NULL, 
    body VARCHAR (500) NOT NULL, 
    meetup INTEGER REFERENCES meetups(m_id) ON DELETE CASCADE, 
    created_by INTEGER REFERENCES users(u_id) ON DELETE CASCADE, 
    created_at TIMESTAMP, votes INTEGER DEFAULT 0);

CREATE TABLE IF NOT EXISTS comments (
    c_id SERIAL PRIMARY KEY NOT NULL, 
    question_id INTEGER REFERENCES questions(q_id) ON DELETE CASCADE, 
    u_id INTEGER REFERENCES users(u_id) ON DELETE CASCADE, 
    comment VARCHAR (500) NOT NULL, 
    created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS rsvp (
    r_id SERIAL PRIMARY KEY NOT NULL, 
    meetup_id INTEGER REFERENCES meetups(m_id) ON DELETE CASCADE, 
    rsvp VARCHAR (50) NOT NULL, 
    u_id INTEGER REFERENCES users(u_id) ON DELETE CASCADE, 
    created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS tags (
    t_id SERIAL PRIMARY KEY NOT NULL, 
    meetup_id INTEGER REFERENCES meetups(m_id) ON DELETE CASCADE, 
    tags VARCHAR ARRAY NOT NULL, 
    created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS voters (
    v_id SERIAL PRIMARY KEY NOT NULL, 
    q_id INTEGER NOT NULL, 
    u_id INTEGER NOT NULL, 
    voted INTEGER NOT NULL, 
    created_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS blascklist (
    b_id SERIAL PRIMARY KEY NOT NULL, 
    token VARCHAR (500) NOT NULL, 
    created_at TIMESTAMP);