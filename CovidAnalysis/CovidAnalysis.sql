SELECT * 
FROM covidAnalysis..['covid deaths$']

--SELECTING DATA TO BE USED
SELECT location, date, total_cases, total_deaths, population
FROM covidAnalysis..['covid deaths$']
ORDER BY 1, 2

--ASSESSING TOTAL CASE WITH POPULATION
SELECT location, date, total_cases, population, (total_cases/population)*100 AS death_percentage
FROM covidAnalysis..['covid deaths$']
WHERE location = 'Pakistan' AND total_deaths IS NOT NULL
ORDER BY 1, 2

--ASSESSING LIKELYHOOD OF DEATH IF CAUGHT COVID
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage
FROM covidAnalysis..['covid deaths$']
WHERE location = 'Pakistan' AND total_deaths IS NOT NULL
ORDER BY 1, 2

--MOST AFFECTED COUNTRIES W.R.T POPULATION
SELECT location, MAX(total_cases) AS highest_count, MAX((total_deaths/population)*100) AS death_percentage
FROM covidAnalysis..['covid deaths$']
GROUP BY location
ORDER BY 2 desc

--SHOWING ONLY COUNTRIES WITH HIGHTEST DEATH COUNT
SELECT location, MAX(CAST(total_deaths AS INT)) AS highest_count
FROM covidAnalysis..['covid deaths$']
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY 2 desc

-- GLOBAL NUMBERS
SELECT date, total_deaths, total_cases, total_deaths*100/total_cases AS global_death_percentage
FROM covidAnalysis..['covid deaths$']
ORDER BY date

--ASSESSING TOTAL POPULATION VS VACCINATIONS
WITH PopVSVac (continent, location, date, population, new_vaccinations, RollingPeopleVacc) AS
(
SELECT d.continent, d.location, d.date, d.population, v.new_vaccinations, 
	   SUM(CAST(v.new_vaccinations AS BIGINT)) OVER (PARTITION BY d.location ORDER BY d.location, d.date) AS RollingPeopleVacc
FROM covidAnalysis..['covid deaths$'] d
INNER JOIN covidAnalysis..['covid deaths$'] v
ON d.location = v.location AND d.date = v.date
WHERE d.continent IS NOT NULL
--ORDER BY 2, 3
)
SELECT *, RollingPeopleVacc*100/population
FROM PopVSVac

DROP TABLE IF EXISTS #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
Continent nvarchar(255),
location nvarchar(255),
date datetime,
popluation numeric,
new_vaccincations numeric,
RollingPeopleVaccinated numeric
)
INSERT INTO #PercentPopulationVaccinated
SELECT d.continent, d.location, d.date, d.population, v.new_vaccinations, 
	   SUM(CAST(v.new_vaccinations AS BIGINT)) OVER (PARTITION BY d.location ORDER BY d.location, d.date) AS RollingPeopleVacc
FROM covidAnalysis..['covid deaths$'] d
INNER JOIN covidAnalysis..['covid deaths$'] v
ON d.location = v.location AND d.date = v.date
WHERE d.continent IS NOT NULL