-- =====================================================
-- Lenaba Database Schema v1.0
-- PostgreSQL (Supabase)
-- =====================================================
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS names (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Unisex')),
    origin TEXT,
    country VARCHAR(2),
    meaning TEXT,
    variants TEXT,
    popularity INTEGER,
    year_first SMALLINT,
    year_last SMALLINT,
    year_peak SMALLINT,
    biblical BOOLEAN DEFAULT FALSE,
    palindrome BOOLEAN DEFAULT FALSE,
    unisex BOOLEAN DEFAULT FALSE,
    phones TEXT,
    stresses TEXT,
    syllables SMALLINT,
    first_letter CHAR(1),
    slug TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
-- ==========================
-- INDEXES
-- ==========================
CREATE INDEX idx_name ON names(name);
CREATE INDEX idx_slug ON names(slug);
CREATE INDEX idx_gender ON names(gender);
CREATE INDEX idx_origin ON names(origin);
CREATE INDEX idx_country ON names(country);
CREATE INDEX idx_first_letter ON names(first_letter);
CREATE INDEX idx_popularity ON names(popularity DESC);
CREATE INDEX idx_name_search ON names USING GIN (to_tsvector('simple', name));