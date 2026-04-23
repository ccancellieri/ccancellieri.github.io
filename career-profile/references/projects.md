# Carlo Cancellieri — Projects

## DynaStore
**Role:** Creator & Technical Lead | **Timeline:** 2020–Present
**URL:** data.apps.fao.org

FAO's multi-tenant geospatial data infrastructure: catalog API, maps/tiles API, dual GeoServer clusters, and
vector tiles. Powers the Organisation's geospatial web presence in support of the Hand-in-Hand Initiative.

### Components

| Component | URL | Technology |
|-----------|-----|-----------|
| Data Catalog | data.apps.fao.org/catalog | Python, FastAPI, OpenSearch/Elasticsearch, React |
| Catalog API | data.apps.fao.org/geospatial/v2/api/catalog/ | FastAPI, OpenSearch |
| Maps/Tiles API | data.apps.fao.org/geospatial/v2/api/maps/ | FastAPI, PostGIS, MVT |
| GeoServer (read) | data.apps.fao.org/map/gsrv/gsrv1/web/ | Java, GeoServer, PostGIS |
| GeoServer (edit) | data.apps.fao.org/map/gsrv/edit/web/ | Java, GeoServer, PostGIS |
| GeoID Service | un-fao/GeoID on GitHub | Python, FastAPI, PostGIS |
| Admin UI | data.apps.fao.org/admin | React — operator console for catalogs, tasks, configs |

### Tech Stack
Python, FastAPI, React, TypeScript, OpenSearch, Elasticsearch, PostgreSQL, PostGIS, asyncpg, pg_cron,
GCP, Terraform, Kubernetes, Docker, GeoServer, OGC API Records, OGC API Processes.

### 2026 Operational Hardening
- Async PostgreSQL connection handling (asyncpg) with per-task pool acquisition to eliminate shared-connection deadlocks
- pg_cron-driven task reaper enforcing PENDING → ACTIVE → FAILED lifecycle invariants with no leader election required
- GCP provisioning resilience: async Cloud Run Jobs/Services client lazy-binding, retry classification, Forbidden/Conflict reclassification
- Separated metadata tables, decorator-to-protocol refactor, STAC-capability checks, tenant-scoped schema DDL
- Catalog-ready guard: fail-fast 409 on STAC mutations against provisioning or failed catalogs

### Key Numbers
- Designed to scale to thousands of tenants and millions of records via pluggable storage drivers (Iceberg, DuckDB, Parquet)
- OGC-compliant metadata (ISO 19115, OGC API Records)
- Serves 50+ countries through the Hand-in-Hand Initiative
- Cloud-native on GCP with Infrastructure as Code (Terraform)

---

## Remote Sensing Portal
**Role:** Creator & Lead | **Timeline:** 2022–Present
**URL:** data.apps.fao.org/remote-sensing-portal

FAO's STAC-native earth observation discovery and access platform. A distinct runtime from the DynaStore
catalog, co-deployed on the same Keystone IAM and GCP substrate. OGC STAC standard end-to-end, from
collection metadata through catalog search to item retrieval.

### Components

| Component | Technology |
|-----------|-----------|
| STAC API | stac-fastapi-elasticsearch (OGC STAC) |
| Search backend | OpenSearch / Elasticsearch with date_range indexing |
| Item ingestion | FastAPI workers with JSON-safe STAC pydantic serialisation |
| Frontend | React + MapLibre |

### Tech Stack
Python, FastAPI, STAC, stac-pydantic, OpenSearch, Elasticsearch, OGC API, GCP, React, MapLibre.

### Differentiators vs. DynaStore Catalog
- STAC-first, not retrofitted — every endpoint follows the STAC specification exactly
- Handles very large dimension spaces: agricultural indicators (thousands of codes), dekadal time series (36 periods/year), administrative hierarchies (sub-national levels)
- Custom OpenSearch serialiser that keeps STAC pydantic models (HttpUrl, datetime, UUID, Decimal) deterministic on ingest — preventing the class of "not JSON serializable" failures common in STAC ingestion pipelines
- Separate data plane from DynaStore so EO workloads don't compete with catalog writes

---

## Keystone
**Role:** Creator & Architect | **Timeline:** 2020–Present

Unified Identity and Access Management platform for FAO's geospatial services.

### Architecture
- **Keycloak** — Identity provider with OIDC/SAML
- **GCP IAM** — Cloud identity integration, organization-level sync
- **RBAC** — Role-based access control for application-level permissions
- **ReBAC** — Relationship-based access control using DGraph/OPA for fine-grained data-level permissions
- **Multi-tenant** — Isolated realms per FAO division and external partners

### Tech Stack
Keycloak, Java, GCP IAM, OIDC, Terraform, DGraph, OPA (Open Policy Agent)

### Key Numbers
- Designed to scale to millions of users per realm (Keycloak-based)
- Multi-tenant across FAO divisions and external partners
- Integrates with GCP organization structure

---

## GeoID Service
**Role:** Creator & Lead | **Timeline:** 2020–Present
**Repository:** github.com/un-fao/GeoID

Persistent geospatial identifier service for standardised geographic references.

### Features
- Resolvable URIs for geographic entities (countries, regions, administrative boundaries, thematic taxonomies)
- OGC and ISO-TC211 aligned (OGC API Records, ISO 19115 metadata)
- RDF/OWL ontologies for geographic relationships
- Multi-language support for geographic entity names
- REST + SPARQL endpoints
- Integrated with the DynaStore catalog as the canonical identifier authority

### Tech Stack
Python, FastAPI, PostGIS, asyncpg, OGC API Records, GCP, RDF/OWL

---

## Hyrax SQL Handler
**Role:** Original Author | **Timeline:** GSoC 2009–2010
**Repository:** github.com/OPENDAP/sql_handler

C++ BES module for OPeNDAP Hyrax server enabling SQL/ODBC database access through the OPeNDAP data access protocol. Created during Google Summer of Code under mentorship of Patrick West.

### Features
- Multi-database support: PostgreSQL, MySQL, SQLite, MongoDB via ODBC
- Exposes tabular data through netCDF, HDF5, FITS, ASCII formats
- Configurable via XML/INI for connection management
- Still actively maintained and used in production

### Deployments
FAO, NATO, NURC (NATO Undersea Research Centre), LaMMa (Environmental Monitoring Lab, Tuscany)

### Tech Stack
C++, ODBC, OPeNDAP DAP protocol, Autotools

---

## CKAN Extensions
**Role:** Creator & Maintainer | **Timeline:** 2012–Present

Suite of open-source CKAN extensions for metadata management and geospatial visualization.

| Extension | Purpose | Stars |
|-----------|---------|-------|
| ckanext-jsonschema | JSON Schema-based metadata editing and validation | 5 |
| ckanext-publisher | Publishing workflow management for datasets | — |
| ckanext-terriajs | TerriaJS map visualization integration | — |
| ckanext-scheming_dcat | DCAT metadata schema for semantic web interoperability | — |
| ckanext-cloudstorage | Cloud storage backend for resource files | — |

### Tech Stack
Python, CKAN, JavaScript, JSON Schema, DCAT/RDF

---

## GeoServer Contributions
**Role:** Core Contributor | **Timeline:** 2010–2014, ongoing maintenance

### Contributions
- **GetLegendGraphic JSON Output** — community-adopted feature for JSON-based map legends
- **JMX monitoring interfaces** — enhanced operational visibility
- **REST API improvements** — extended management capabilities
- **JMS integration** — message-based clustering support
- **WPS interfaces** — geoprocessing service enhancements
- **GeoServerStressTest** — load testing tool (5 GitHub stars)

### Production Deployments
FAO, NATO, NURC, LaMMa research institutions

### Tech Stack
Java, Spring, GeoServer, PostGIS, JAI (Java Advanced Imaging)

---

## SWS (Statistical Working System)
**Role:** Full-Stack Engineer | **Timeline:** Jul 2015 – Dec 2017
**Organization:** FAO Statistics Division (ESS)

FAO's corporate statistics platform for Food Balance Sheets and Supply Utilization Accounts.

### Contributions
- React/Redux/TypeScript frontend for statistical data entry and validation
- R-based statistical processing pipelines
- Reusable React component library for statistical visualization
- CI/CD pipeline implementation

### Tech Stack
React, Redux, TypeScript, R, Java, PostgreSQL

---

## TAP/SMAI Monitoring System
**Role:** Head of R&D | **Timeline:** Oct 2018 – Sep 2019
**Organization:** SIGEO S.r.l.

Real-time environmental monitoring system for the Trans Adriatic Pipeline.

### Tech Stack
Various (IoT, real-time data, monitoring, alerting)

**Note:** Include only in certain CV variants — see cv-strategy.md
