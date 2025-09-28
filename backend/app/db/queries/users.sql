-- users.sql

-- name: get_all_users
SELECT id, username, email, created_at, updated_at
FROM users
ORDER BY id;

-- name: get_user_by_id
SELECT id, username, email,password_hash, created_at, updated_at
FROM users
WHERE id = $1;

-- name: get_password_hash_by_email
SELECT password_hash
FROM users
WHERE email = $1;


-- name: create_user
INSERT INTO users (username, email, password_hash)
VALUES ($1, $2, $3)
RETURNING id, username, email, created_at, updated_at;

-- name: update_user
UPDATE users
SET username = $1,
    email = $2
WHERE id = $3
RETURNING id, username, email, created_at, updated_at;

-- name: delete_user
DELETE FROM users
WHERE id = $1
RETURNING id, username, email;

-- name: count_users
SELECT COUNT(*) AS total_users
FROM users;
