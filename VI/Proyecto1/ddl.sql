-- Tabla principal de títulos
CREATE TABLE "titles" (
	"tconst"	TEXT,
	"primaryTitle"	TEXT NOT NULL,
	"originalTitle"	TEXT,
	"startYear"	INTEGER,
	"isAdult"	INTEGER,
	"averageRating"	REAL,
	"numVotes"	INTEGER,
	"runtimeMinutes"	INTEGER,
	PRIMARY KEY("tconst")
);

-- Tabla de géneros
CREATE TABLE "genres" (
	"id"	INTEGER,
	"genre_name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

-- Relación muchos-a-muchos títulos-géneros
CREATE TABLE "title_genres" (
	"tconst"	TEXT,
	"genre_id"	INTEGER,
	PRIMARY KEY("tconst","genre_id"),
	FOREIGN KEY("genre_id") REFERENCES "genres"("id") ON DELETE CASCADE,
	FOREIGN KEY("tconst") REFERENCES "titles"("tconst") ON DELETE CASCADE
);

-- Tabla de regiones
CREATE TABLE "regions" (
	"id"	INTEGER,
	"region_code"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

-- Tabla de idiomas
CREATE TABLE "languages" (
	"id"	INTEGER,
	"language_code"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

-- Relación muchos-a-muchos títulos-regiones
CREATE TABLE "title_regions" (
	"tconst"	TEXT,
	"region_id"	INTEGER,
	PRIMARY KEY("tconst","region_id"),
	FOREIGN KEY("region_id") REFERENCES "regions"("id") ON DELETE CASCADE,
	FOREIGN KEY("tconst") REFERENCES "titles"("tconst") ON DELETE CASCADE
);

-- Relación muchos-a-muchos títulos-idiomas
CREATE TABLE "title_languages" (
	"tconst"	TEXT,
	"language_id"	INTEGER,
	PRIMARY KEY("tconst","language_id"),
	FOREIGN KEY("language_id") REFERENCES "languages"("id") ON DELETE CASCADE,
	FOREIGN KEY("tconst") REFERENCES "titles"("tconst") ON DELETE CASCADE
);

-- Tabla de personas (directores, escritores, productores)
CREATE TABLE "people" (
	"nconst"	TEXT,
	"primaryName"	TEXT NOT NULL,
	PRIMARY KEY("nconst")
);

-- Tabla de relación título-persona para directores, escritores y productores
CREATE TABLE "title_roles" (
	"tconst"	TEXT,
	"nconst"	TEXT,
	"category"	TEXT CHECK(category IN ("director", "writer", "producer")),
	PRIMARY KEY("tconst","nconst","category"),
	FOREIGN KEY("nconst") REFERENCES "people"("nconst") ON DELETE CASCADE,
	FOREIGN KEY("tconst") REFERENCES "titles"("tconst") ON DELETE CASCADE
);

-- Tabla de títulos conocidos por persona
CREATE TABLE "known_for" (
	"nconst"	TEXT,
	"tconst"	TEXT,
	PRIMARY KEY("nconst","tconst"),
	FOREIGN KEY("nconst") REFERENCES "titles"("tconst") ON DELETE CASCADE,
	FOREIGN KEY("tconst") REFERENCES "people"("nconst") ON DELETE CASCADE
);
