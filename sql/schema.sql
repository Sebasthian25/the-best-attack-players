
-- SCHEMA: football_analysis

CREATE TABLE attackers (
    id                SERIAL          PRIMARY KEY,
    player            TEXT            NOT NULL,
    squad             TEXT            NOT NULL,
    competition       TEXT            NOT NULL,         -- 'eng Premier League', 'es La Liga', etc.
    position          TEXT            NOT NULL,         -- 'FW', 'MF,FW', 'FW,MF'
    minutes           INT             NOT NULL,
    goals             INT             NOT NULL DEFAULT 0,
    assists           INT             NOT NULL DEFAULT 0,
    shots             INT             NOT NULL DEFAULT 0,
    shots_on_target   INT             NOT NULL DEFAULT 0,
    goals_per_90      FLOAT           NOT NULL DEFAULT 0,
    assists_per_90    FLOAT           NOT NULL DEFAULT 0,
    shots_per_90      FLOAT           NOT NULL DEFAULT 0,
    sot_per_90        FLOAT           NOT NULL DEFAULT 0,  -- shots on target per 90
    shot_accuracy     FLOAT           NOT NULL DEFAULT 0,  -- SoT / Sh  (0–1)
    goal_efficiency   FLOAT           NOT NULL DEFAULT 0,  -- Gls / Sh  (0–1)
    contribution      INT             NOT NULL DEFAULT 0,  -- goals + assists
    score             FLOAT           NOT NULL DEFAULT 0   -- composite 0–1
);

-- Índices para queries frecuentes
CREATE INDEX idx_attackers_score       ON attackers (score DESC);
CREATE INDEX idx_attackers_competition ON attackers (competition);
CREATE INDEX idx_attackers_squad       ON attackers (squad);
CREATE INDEX idx_attackers_goals       ON attackers (goals DESC);
CREATE INDEX idx_attackers_minutes     ON attackers (minutes);