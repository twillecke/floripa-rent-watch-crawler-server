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

CREATE TABLE IF NOT EXISTS mailing_list(
    mail_id BIGSERIAL NOT NULL,
    email BYTEA NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY(email)
);

CREATE TABLE IF NOT EXISTS overview(
    job_ids BIGINT[],
    week BIGINT,
    total_count BIGINT,
    total_avg NUMERIC(15,2),
    total_avg_monthly_count BIGINT,
    total_avg_monthly NUMERIC(15,2),
    total_avg_daily_count BIGINT,
    total_avg_daily NUMERIC(15,2),
    apartamento_monthly_count BIGINT,
    apartamento_monthly_avg NUMERIC(15,2),
    apartamento_daily_count BIGINT,
    apartamento_daily_avg NUMERIC(15,2),
    casa_monthly_count BIGINT,
    casa_monthly_avg NUMERIC(15,2),
    casa_daily_count BIGINT,
    casa_daily_avg NUMERIC(15,2),
    chacara_monthly_count BIGINT,
    chacara_monthly_avg NUMERIC(15,2),
    chacara_daily_count BIGINT,
    chacara_daily_avg NUMERIC(15,2),
    cobertura_monthly_count BIGINT,
    cobertura_monthly_avg NUMERIC(15,2),
    cobertura_daily_count BIGINT,
    cobertura_daily_avg NUMERIC(15,2),
    condominio_monthl_count BIGINT,
    condominio_monthly_avg NUMERIC(15,2),
    condominio_daily_count BIGINT,
    condominio_daily_avg NUMERIC(15,2),
    flat_monthly_count BIGINT,
    flat_monthly_avg NUMERIC(15,2),
    flat_daily_count BIGINT,
    flat_daily_avg NUMERIC(15,2),
    loft_monthly_count BIGINT,
    loft_monthly_avg NUMERIC(15,2),
    loft_daily_count BIGINT,
    loft_daily_avg NUMERIC(15,2),
    quitinete_monthly_count BIGINT,
    quitinete_monthly_avg NUMERIC(15,2),
    quitinete_daily_count BIGINT,
    quitinete_daily_avg NUMERIC(15,2),
    sobrado_monthly_count BIGINT,
    sobrado_monthly_avg NUMERIC(15,2),
    sobrado_daily_count BIGINT,
    sobrado_daily_avg NUMERIC(15,2),
    studio_monthly_count BIGINT,
    studio_monthly_avg NUMERIC(15,2),
    studio_daily_count BIGINT,
    studio_daily_avg NUMERIC(15,2),
    vila_monthly_count BIGINT,
    vila_monthly_avg NUMERIC(15,2),
    vila_daily_count BIGINT,
    vila_daily_avg NUMERIC(15,2),
    PRIMARY KEY(job_ids, week)
);

CREATE OR REPLACE FUNCTION update_job_id_after_job_finish()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE rent_data SET job_id = NEW.job_id WHERE job_id < 0;
    RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_job_id
    BEFORE INSERT ON job_stats
    FOR EACH ROW
    EXECUTE FUNCTION update_job_id_after_job_finish();

CREATE OR REPLACE FUNCTION insert_overview()
RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO overview
        SELECT ARRAY_AGG (DISTINCT j.job_id ORDER BY j.job_id) job_ids,
            DATE_PART('week',j.start_time) as week,
            COUNT (*),
            AVG (r.price),
            COUNT (CASE WHEN r.rent_type = 'monthly' THEN r.price END) as d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' THEN r.price END) as d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' THEN r.price END) as m_count,
            AVG (CASE WHEN r.rent_type = 'daily' THEN r.price END) as m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'apartamento' THEN r.price END) as apart_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'apartamento' THEN r.price END) as apart_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'apartamento' THEN r.price END) as apart_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'apartamento' THEN r.price END) as apart_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'casa' THEN r.price END) as casa_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'casa' THEN r.price END) as casa_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'casa' THEN r.price END) as casa_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'casa' THEN r.price END) as casa_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'chacara' THEN r.price END) as chacara_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'chacara' THEN r.price END) as chacara_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'chacara' THEN r.price END) as chacara_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'chacara' THEN r.price END) as chacara_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'cobertura' THEN r.price END) as cobertura_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'cobertura' THEN r.price END) as cobertura_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'cobertura' THEN r.price END) as cobertura_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'cobertura' THEN r.price END) as cobertura_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'condominio' THEN r.price END) as condominio_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'condominio' THEN r.price END) as condominio_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'condominio' THEN r.price END) as condominio_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'condominio' THEN r.price END) as condominio_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'flat' THEN r.price END) as flat_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'flat' THEN r.price END) as flat_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'flat' THEN r.price END) as flat_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'flat' THEN r.price END) as flat_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'loft' THEN r.price END) as loft_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'loft' THEN r.price END) as loft_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'loft' THEN r.price END) as loft_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'loft' THEN r.price END) as loft_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'quitinete' THEN r.price END) as quitinete_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'quitinete' THEN r.price END) as quitinete_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'quitinete' THEN r.price END) as quitinete_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'quitinete' THEN r.price END) as quitinete_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'sobrado' THEN r.price END) as sobrado_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'sobrado' THEN r.price END) as sobrado_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'sobrado' THEN r.price END) as sobrado_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'sobrado' THEN r.price END) as sobrado_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'studio' THEN r.price END) as studio_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'studio' THEN r.price END) as studio_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'studio' THEN r.price END) as studio_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'studio' THEN r.price END) as studio_m_avg,
            COUNT (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'vila' THEN r.price END) as vila_d_count,
            AVG (CASE WHEN r.rent_type = 'monthly' AND r.housing_type = 'vila' THEN r.price END) as vila_d_avg,
            COUNT (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'vila' THEN r.price END) as vila_m_count,
            AVG (CASE WHEN r.rent_type = 'daily' AND r.housing_type = 'vila' THEN r.price END) as vila_m_avg
        FROM rent_data r
        JOIN job_stats j USING (job_id)
        WHERE DATE_PART('week',j.start_time) = DATE_PART('week',NEW.start_time)
        GROUP BY week
        ORDER BY week;
    RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_overview
    AFTER INSERT ON job_stats
    FOR EACH ROW
    EXECUTE FUNCTION insert_overview();

CREATE EXTENSION IF NOT EXISTS pgcrypto;
