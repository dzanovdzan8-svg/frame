-- ==========================================
-- Путевые заметки: SQL-запросы проекта
-- Проверка: sqlite3 data/travelnotes.sqlite
-- Длительность поездки в днях считается как
-- julianday(end_date) - julianday(start_date) + 1
-- ==========================================


-- ---------- ВЫБОРКА СПИСКОВ ----------

-- Q1. Список всех поездок по дате начала (страница «Поездки»)
SELECT
    id,
    title,
    country,
    start_date,
    end_date,
    CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1
        AS duration_days
FROM trips
ORDER BY start_date;

-- Q2. Список путешественников по имени
SELECT
    id,
    name,
    email
FROM travelers
ORDER BY name;


-- ---------- ФИЛЬТРАЦИЯ (WHERE) ----------

-- Q3. Поездки в России длительностью не менее 5 дней
SELECT
    id,
    title,
    country,
    CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1
        AS duration_days
FROM trips
WHERE country = 'Россия'
  AND CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1
      >= 5
ORDER BY duration_days DESC;

-- Q4. Только активные заметки (архивные не учитываются)
SELECT
    id,
    trip_id,
    traveler_id,
    note_date
FROM notes
WHERE is_archived = 0
ORDER BY note_date;

-- Q5. Заметки, сделанные в июле 2026 года
SELECT
    id,
    trip_id,
    note_date,
    text
FROM notes
WHERE note_date BETWEEN '2026-07-01' AND '2026-07-31'
  AND is_archived = 0
ORDER BY note_date;


-- ---------- СОЕДИНЕНИЕ ТАБЛИЦ (JOIN) ----------

-- Q6. Полная информация об активных заметках (страница «Заметки»)
SELECT
    notes.id,
    notes.note_date,
    notes.text,
    trips.title AS trip_title,
    trips.country,
    travelers.name AS traveler_name,
    travelers.email
FROM notes
JOIN trips
    ON notes.trip_id = trips.id
JOIN travelers
    ON notes.traveler_id = travelers.id
WHERE notes.is_archived = 0
ORDER BY notes.note_date;

-- Q7. Все заметки одной поездки с авторами (страница поездки)
SELECT
    notes.id,
    notes.note_date,
    notes.text,
    notes.is_archived,
    travelers.name AS traveler_name
FROM notes
JOIN travelers
    ON notes.traveler_id = travelers.id
WHERE notes.trip_id = 1
ORDER BY notes.note_date;


-- ---------- ПОДЗАПРОС ----------

-- Q8. Поездки, у которых выбранный день входит в период поездки,
-- но заметки на этот день ещё нет (страница «Дни без заметок»)
SELECT
    trips.id,
    trips.title,
    trips.country
FROM trips
WHERE '2026-07-15' BETWEEN trips.start_date AND trips.end_date
  AND trips.id NOT IN (
      SELECT notes.trip_id
      FROM notes
      WHERE notes.note_date = '2026-07-15'
        AND notes.is_archived = 0
  )
ORDER BY trips.title;


-- ---------- АГРЕГАТНЫЕ ФУНКЦИИ ----------

-- Q9. Количество активных заметок
SELECT
    COUNT(*) AS notes_count
FROM notes
WHERE is_archived = 0;

-- Q10. Сводка по длительности поездок: количество, минимум,
-- максимум и среднее значение
SELECT
    COUNT(*) AS trips_count,
    CAST(MIN(julianday(end_date) - julianday(start_date)) AS INTEGER) + 1
        AS min_days,
    CAST(MAX(julianday(end_date) - julianday(start_date)) AS INTEGER) + 1
        AS max_days,
    ROUND(AVG(julianday(end_date) - julianday(start_date) + 1), 1)
        AS avg_days
FROM trips;


-- ---------- ГРУППИРОВКА (GROUP BY, HAVING) ----------

-- Q11. Количество активных заметок по поездкам, включая поездки
-- без заметок (страница «Статистика»)
SELECT
    trips.title AS trip_title,
    COUNT(notes.id) AS notes_count
FROM trips
LEFT JOIN notes
    ON trips.id = notes.trip_id
    AND notes.is_archived = 0
GROUP BY trips.id, trips.title
ORDER BY notes_count DESC, trips.title;

-- Q12. Количество поездок и суммарная длительность по странам
SELECT
    country,
    COUNT(*) AS trips_count,
    SUM(CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1)
        AS total_days
FROM trips
GROUP BY country
ORDER BY trips_count DESC, country;

-- Q13. Поездки с более чем одной активной заметкой (HAVING)
SELECT
    trips.title AS trip_title,
    COUNT(notes.id) AS notes_count
FROM trips
JOIN notes
    ON trips.id = notes.trip_id
WHERE notes.is_archived = 0
GROUP BY trips.id, trips.title
HAVING COUNT(notes.id) > 1
ORDER BY notes_count DESC;

-- Q14. Количество активных заметок по авторам
SELECT
    travelers.name AS traveler_name,
    COUNT(notes.id) AS notes_count
FROM travelers
LEFT JOIN notes
    ON travelers.id = notes.traveler_id
    AND notes.is_archived = 0
GROUP BY travelers.id, travelers.name
ORDER BY notes_count DESC, travelers.name;


-- ---------- ОГРАНИЧЕНИЕ ВЫБОРКИ ----------

-- Q15. Три последние активные заметки (LIMIT)
SELECT
    notes.id,
    notes.note_date,
    trips.title AS trip_title
FROM notes
JOIN trips
    ON notes.trip_id = trips.id
WHERE notes.is_archived = 0
ORDER BY notes.note_date DESC
LIMIT 3;
