Select name
FROM songs
Where artist_id =
(
    SELECT ID
    FROM artists
    WHERE name = 'Post Malone'
);
