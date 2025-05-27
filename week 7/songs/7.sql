Select AVG(energy)
FROM songs
Where artist_id =
(
    SELECT ID
    FROM artists
    WHERE name = 'Drake'
);
