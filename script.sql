CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR (255),
    google_id integer,
    facebook_id integer,
    apple_id integer
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    followers INTEGER,
    subscription VARCHAR(255),
    role VARCHAR(255) CHECK (role IN ('singer', 'podcaster', 'user')),
    google_id INTEGER,
    facebook_id INTEGER,
    apple_id INTEGER
);


CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    picture VARCHAR(255),
    year DATE,
    likes INTEGER,
    singer_id INTEGER REFERENCES users(id)
);

CREATE TABLE podcasts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    picture VARCHAR(255),
    year date,
    likes integer,
    podcaster_id integer references users(id)
);

CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    lyrics VARCHAR(255),
    picture VARCHAR(255),
    likes integer,
    listented_to integer,
    duration time,
    genre VARCHAR(255),
    year date,
    language VARCHAR(255),
    country VARCHAR(255),
    album_id integer references albums(id),
    singer_id INTEGER REFERENCES users(id)
);

CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    lyrics VARCHAR(255),
    picture VARCHAR(255),
    listented_to integer,
    likes integer,
    duration time,
    genre VARCHAR(255),
    year date,
    language VARCHAR(255),
    country VARCHAR(255),
    podcast_id integer references podcasts(id),
    podcaster_id integer references users(id)
);

CREATE TABLE tagged_episodes (
    id SERIAL PRIMARY KEY,
    episode_id integer references episodes(id),
    podcaster_id integer references users(id)
);

CREATE TABLE tagged_songs (
    id SERIAL PRIMARY KEY,
    song_id integer references songs(id),
    singer_id INTEGER REFERENCES users(id)
);

CREATE TABLE playlists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    user_id integer references users(id)        
);

CREATE TABLE playlist_songs (
    id SERIAL PRIMARY KEY,
    song_id integer references songs(id),
    playlist_id integer references playlists(id)
);

CREATE TABLE followers (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    follower_id integer references users(id),
    UNIQUE (user_id, follower_id)
);

CREATE TABLE history_songs (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    song_id integer references songs(id)
);

CREATE TABLE history_albums (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    album_id integer references albums(id)
);

CREATE TABLE history_playlists (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    playlist_id integer references playlists(id)
);

CREATE TABLE history_episodes (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    episode_id integer references episodes(id)
);

CREATE TABLE history_podcasts (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    podcast_id integer references podcasts(id)
);

CREATE TABLE liked_podcasts (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    podcast_id integer references podcasts(id),
    UNIQUE (user_id, podcast_id)
);

CREATE TABLE liked_episodes (
    id SERIAL PRIMARY KEY,
    user_id integer references users(id),
    episode_id integer references episodes(id),
    UNIQUE (user_id, episode_id)
);

CREATE TABLE liked_songs (
    id SERIAL PRIMARY KEY,
    song_id integer references songs(id),
    user_id integer references users(id),
    UNIQUE (user_id, song_id)
);

CREATE TABLE liked_albums (
    id SERIAL PRIMARY KEY,
    album_id integer references albums(id),
    user_id integer references users(id),
    UNIQUE (user_id, album_id)
);

CREATE TABLE liked_playlists (
    id SERIAL PRIMARY KEY,
    playlist_id integer references playlists(id),
    user_id integer references users(id),
    UNIQUE (user_id, playlist_id)
);


ALTER TABLE users 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE admins 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE albums 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE episodes 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE followers 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE history_albums 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE history_episodes 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE history_playlists 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE history_podcasts 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE history_songs 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE liked_albums 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE liked_episodes 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE liked_playlists 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE liked_podcasts 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE liked_songs 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE playlist_songs 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE playlists 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE podcasts 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE songs 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE tagged_episodes 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE tagged_songs 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;






