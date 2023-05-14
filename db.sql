CREATE TABLE IF NOT EXISTS spiders(
    id BIGSERIAL NOT NULL,
    spider_name VARCHAR(255) UNIQUE NOT NULL,
    schedule TIMESTAMP NOT NULL,
    website VARCHAR(255) NOT NULL,
    lib VARCHAR(255) NOT NULL,
    project_number BIGINT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS job_stats(
    job_id BIGSERIAL NOT NULL,
    spider_name VARCHAR(255) NOT NULL,
    item_count BIGINT NOT NULL,
    item_drop_count BIGINT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    finish_time TIMESTAMP NOT NULL,
    duration NUMERIC NOT NULL,
    request_count BIGINT NOT NULL,
    response_count BIGINT NOT NULL,
    finish_reason VARCHAR(255) NOT NULL,
    max_depth BIGINT NOT NULL,
    PRIMARY KEY(job_id),
    CONSTRAINT job_stats_spider_name_foreign FOREIGN KEY(spider_name) REFERENCES spiders(spider_name) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS rent_data(
    job_id BIGINT,
    rent_id BIGINT NOT NULL,
    address VARCHAR(255),
    region VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    housing_type VARCHAR(255) NOT NULL,
    rent_type VARCHAR(255) NOT NULL,
    price BIGINT NOT NULL,
    cond_price BIGINT,
    iptu_price BIGINT,
    size_m2 BIGINT,
    bedroom_count BIGINT,
    parking_count BIGINT,
    bathroom_count BIGINT,
    datetime TIMESTAMP,
    PRIMARY KEY(job_id, rent_id)
);
