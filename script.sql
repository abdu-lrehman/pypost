CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR (255),
    subscription VARCHAR(255),
    role VARCHAR(255)
);

CREATE TABLE album (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    publisher integer references users(id)    
);

CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    lyrics VARCHAR(255),
    album_id integer references album(id),
    publisher integer references users(id)
);

CREATE TABLE tagged (
    id SERIAL PRIMARY KEY,
    song_id integer references songs(id),
    publisher1 integer references users(id)    
);

CREATE TABLE liked_songs (
    id SERIAL PRIMARY KEY,
    song_id integer references songs(id),
    user_id integer references users(id)    
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
    follower_id integer references users(id)
);