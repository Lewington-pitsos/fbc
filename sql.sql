CREATE TABLE comment_number (
    highest BIGINT NOT NULL DEFAULT 221534646352
);

CREATE TABLE meta_comments (
    id SERIAL,
    comment VARCHAR (1000) NOT NULL,
    info VARCHAR(2000) NOT NULL,
    user_id INTEGER,
    comment_id INTEGER,
    mcid VARCHAR(200),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (comment_id) REFERENCES comments (id),
    UNIQUE(comment, info, user_id, comment_id),
    UNIQUE(mcid)
);

CREATE TABLE comments (
    id SERIAL,
    user_id INTEGER,
    supplier_id INTEGER,
    comment VARCHAR (5000) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    tagged BOOL NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
    UNIQUE(comment, timestamp, user_id)
);

CREATE TABLE users (
    id SERIAL,
    name VARCHAR(200) NOT NULL,
    link VARCHAR(1000) NOT NULL,
    uid BIGINT,
    PRIMARY KEY (id),
    UNIQUE(name, link)
);


INSERT INTO users (name, link) VALUES ({name}, {link})
WHERE NOT EXISTS (
    SELECT id
    FROM users
    WHERE name = {name} AND link = {link}
    )
returning id

CREATE TABLE suppliers (
    id SERIAL, 
    page_id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY (id),
    UNIQUE(name, page_id)
);

CREATE TABLE likes(
    id SERIAL,
    user_id INTEGER,
    supplier_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
    UNIQUE(user_id, supplier_id),
    PRIMARY KEY(id)
);

CREATE TABLE reactions (
    id SERIAL,
    user_id INTEGER,
    kind VARCHAR(10),
    comment_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (comment_id) REFERENCES comments (id),
    PRIMARY KEY(id),
    UNIQUE(user_id, kind, comment_id)
);

CREATE TABLE meta_reactions (
    id SERIAL,
    user_id INTEGER,
    kind VARCHAR(10),
    meta_comment_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (meta_comment_id) REFERENCES meta_comments (id),
    PRIMARY KEY(id),
    UNIQUE(user_id, kind, meta_comment_id)
);