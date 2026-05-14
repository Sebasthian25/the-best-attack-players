
-- 1. TOP 10 POR SCORE COMPUESTO
SELECT
    player,
    squad,
    competition,
    goals,
    assists,
    ROUND(score::NUMERIC, 4) AS score
FROM attackers
ORDER BY score DESC
LIMIT 10;
-- Resultado esperado: Kane, Dembélé, Mbappé, Malen, Undav, Haaland…



-- 2. TOP 10 GOLES POR 90 MINUTOS
SELECT
    player,
    squad,
    competition,
    goals,
    minutes,
    ROUND(goals_per_90::NUMERIC, 4) AS goals_per_90
FROM attackers
WHERE minutes >= 900
ORDER BY goals_per_90 DESC
LIMIT 10;
-- Kane (1.38), Dembélé (0.97), Mbappé (0.90), Malen (0.88)…



-- 3. TOP 10 ASISTIDORES POR 90 MINUTOS
SELECT
    player,
    squad,
    competition,
    assists,
    minutes,
    ROUND(assists_per_90::NUMERIC, 4) AS assists_per_90
FROM attackers
WHERE minutes >= 900
ORDER BY assists_per_90 DESC
LIMIT 10;



-- 4. JUGADORES MÁS EFICIENTES
SELECT
    player,
    squad,
    competition,
    goals,
    shots,
    shots_on_target,
    ROUND((goal_efficiency * 100)::NUMERIC, 1) AS goal_efficiency_pct,
    ROUND((shot_accuracy  * 100)::NUMERIC, 1) AS shot_accuracy_pct
FROM attackers
WHERE shots >= 20
ORDER BY goal_efficiency DESC
LIMIT 10;
-- Demirovič 30.3%, Kane 29.7%, Burkardt 27.8%…



-- 5. COMPARACIÓN POR LIGA
SELECT
    competition,
    COUNT(*)                                        AS total_players,
    SUM(goals)                                      AS total_goals,
    SUM(assists)                                    AS total_assists,
    ROUND(AVG(goals_per_90)::NUMERIC, 4)            AS avg_goals_per_90,
    ROUND(AVG(assists_per_90)::NUMERIC, 4)          AS avg_assists_per_90,
    ROUND(AVG(score)::NUMERIC, 4)                   AS avg_score,
    MAX(goals)                                      AS max_goals,
    MAX(player) FILTER (WHERE goals = MAX(goals)
                        OVER (PARTITION BY competition))
                                                    AS top_scorer
FROM attackers
GROUP BY competition
ORDER BY avg_goals_per_90 DESC;
-- Bundesliga lidera en promedio (0.30 G/90)



-- 5b. COMPARACIÓN POR LIGA 
SELECT
    competition,
    COUNT(*)                                AS total_players,
    SUM(goals)                              AS total_goals,
    SUM(assists)                            AS total_assists,
    ROUND(AVG(goals_per_90)::NUMERIC, 4)   AS avg_goals_per_90,
    ROUND(AVG(score)::NUMERIC, 4)          AS avg_score
FROM attackers
GROUP BY competition
ORDER BY avg_goals_per_90 DESC;



-- 6. TOP JUGADOR POR EQUIPO
SELECT DISTINCT ON (squad)
    squad,
    player,
    goals,
    assists,
    contribution,
    ROUND(score::NUMERIC, 4) AS score
FROM attackers
ORDER BY squad, score DESC;



-- 7. DISTRIBUCIÓN DE SCORE POR LIGA (deciles)
SELECT
    competition,
    ROUND(percentile_cont(0.50) WITHIN GROUP (ORDER BY score)::NUMERIC, 4) AS mediana_score,
    ROUND(percentile_cont(0.90) WITHIN GROUP (ORDER BY score)::NUMERIC, 4) AS p90_score,
    ROUND(MAX(score)::NUMERIC, 4)                                           AS max_score
FROM attackers
GROUP BY competition
ORDER BY p90_score DESC;



-- 8. JUGADORES CON ALTA CONTRIBUCIÓN Y BUENA

SELECT
    player,
    squad,
    competition,
    goals,
    assists,
    contribution,
    ROUND(goals_per_90::NUMERIC,   3) AS g90,
    ROUND(assists_per_90::NUMERIC, 3) AS a90,
    ROUND(goal_efficiency::NUMERIC, 3) AS eff,
    ROUND(score::NUMERIC, 4)           AS score
FROM attackers
WHERE contribution >= 10
  AND goal_efficiency >= 0.15
  AND minutes >= 900
ORDER BY score DESC
LIMIT 15;


-- 9. ANÁLISIS DE VOLUMEN DE TIRO

SELECT
    player,
    squad,
    competition,
    shots,
    minutes,
    ROUND(shots_per_90::NUMERIC, 2) AS shots_per_90,
    ROUND(sot_per_90::NUMERIC,   2) AS sot_per_90,
    ROUND(shot_accuracy::NUMERIC * 100, 1) AS accuracy_pct
FROM attackers
WHERE minutes >= 900
ORDER BY shots_per_90 DESC
LIMIT 10;
