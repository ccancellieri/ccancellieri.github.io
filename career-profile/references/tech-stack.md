# Carlo Cancellieri — Tech Stack

## Languages & Frameworks

| Technology | Experience | Context |
|-----------|-----------|---------|
| Java | 17+ years (2005–present) | GeoServer, Spring, enterprise backends, Keycloak |
| Python | 8+ years | FastAPI, DynaStore, CKAN extensions, GeoID, data pipelines |
| TypeScript | 8+ years | React frontends, SWS, DynaStore catalog UI |
| JavaScript | 15+ years | CKAN, web mapping, TerriaJS, frontend development |
| C/C++ | GSoC 2009–2010 | OPeNDAP Hyrax SQL Handler (BES module) |
| R | 2015–2017 | Statistical processing pipelines at FAO ESS |
| SQL | 20+ years | PostgreSQL, PostGIS, MySQL, SQLite |
| Pine Script | 2017–2018 | Algo trading (omit from most CVs) |

## Frameworks & Libraries

| Technology | Context |
|-----------|---------|
| FastAPI | DynaStore APIs, Keystone, GeoID |
| React | DynaStore catalog, SWS frontend, data visualization |
| Redux | SWS state management |
| Spring | GeoServer, Java enterprise applications |
| CKAN | Data catalog framework, 5+ extensions authored |
| GeoServer | Core contributor 2010–2014, still maintaining FAO instances |
| GeoNetwork | Metadata catalog, OGC CSW |
| Keycloak | Keystone IAM, OIDC/SAML identity provider |

## Cloud & Infrastructure

| Technology | Context |
|-----------|---------|
| GCP (Google Cloud Platform) | Primary cloud for FAO geospatial services |
| AWS | Secondary cloud experience |
| Kubernetes | Container orchestration for DynaStore services |
| Docker | Containerization of all services |
| Terraform | Infrastructure as Code for GCP resources |
| CI/CD | GitHub Actions, Jenkins, build automation for 75-dev team (Proxima) |

## Data & Databases

| Technology | Context |
|-----------|---------|
| PostgreSQL | Primary relational database |
| PostGIS | Spatial extension, core of geospatial stack |
| asyncpg | Async PostgreSQL driver — per-task pool acquisition pattern in DynaStore routers/tasks |
| pg_cron | PostgreSQL-native scheduler for task reaper and lifecycle enforcement in DynaStore |
| Elasticsearch | DynaStore catalog, STAC search, full-text + geospatial queries |
| OpenSearch | Remote Sensing Portal — STAC-native search backend with date_range indexing |
| DGraph | Graph database for ReBAC in Keystone |
| MongoDB | NoSQL, supported in sql_handler |
| ODBC | Database abstraction in Hyrax SQL Handler |

## Geospatial Standards & Protocols

| Standard | Context |
|---------|---------|
| OGC STAC | SpatioTemporal Asset Catalog — Remote Sensing Portal |
| WMS (Web Map Service) | GeoServer, map rendering |
| WFS (Web Feature Service) | GeoServer, vector data access |
| WCS (Web Coverage Service) | GeoServer, raster data access |
| WMTS (Web Map Tile Service) | Tile serving |
| OGC API Features | Next-gen OGC vector API |
| OGC API Records | Next-gen OGC catalog API |
| OGC API Processes (Parts 1–4) | Process discovery, execution, DRU, workflows, job management — integration plan for DynaStore |
| STAC Datacube Extension | Dimension metadata for datacube collections — gap analysis ongoing (paginated members, non-Gregorian calendars) |
| ISO 19115 | Geospatial metadata standard |
| ISO 19139 | ISO 19115 XML encoding |
| DCAT | Data Catalog Vocabulary (semantic web) |
| SDMX | Statistical Data and Metadata Exchange |
| MVT (Mapbox Vector Tiles) | Vector tile format for web maps |
| netCDF / HDF5 | Scientific data formats (OPeNDAP) |
| OPeNDAP DAP | Data Access Protocol for scientific data |

## AI & Emerging Tech

| Technology | Context |
|-----------|---------|
| Vertex AI | GCP ML platform, explored for FAO applications |
| LLMs | Applied AI research, MCP tooling |
| MCP (Model Context Protocol) | LLM tool integration standard — MCP Skill Hub + career-skill-hub plugin |
| FastMCP | Python MCP server framework used for MCP Skill Hub |
| Ollama | Local LLM runtime (deepseek-r1, nomic-embed-text) powering semantic skill search |
| Claude API / Anthropic SDK | Tool use, prompt caching, structured content generation |
| OPA (Open Policy Agent) | Policy engine for Keystone authorization |

## Tools & Methodologies

| Area | Technologies |
|------|-------------|
| Version Control | Git, GitHub (1,000+ contributions/year) |
| Project Management | Agile, Scrum, Six Sigma Green Belt |
| Testing | JUnit, pytest, load testing (GeoServerStressTest) |
| Build Tools | Maven, Gradle, Autotools, npm |
| Image Processing | JAI (Java Advanced Imaging), GDAL |
| Semantic Web | RDF/OWL, SPARQL, JSON-LD |
