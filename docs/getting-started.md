# Getting Started

This guide walks you through cloning, configuring, and running the CCDI DCC GraphQL API locally.

## Prerequisites
- Node.js 20+
- Python 3.8+ (schema generation utilities)
- Neo4j or Memgraph running locally or remotely
- Docker (optional for container deployment)

## Clone & Install
```bash
git clone https://github.com/CBIIT/ccdi-dcc-graphql.git
cd ccdi-dcc-graphql
npm install
```

## Environment Configuration
Copy and edit environment variables:
```bash
cp .env.example .env
```
Key variables:

| Name | Purpose | Default |
|------|---------|---------|
| DB_URI | Graph DB URI | bolt://localhost:7687 |
| DB_USERNAME | DB user | memgraphdb |
| DB_PASSWORD | DB password | (required) |
| PORT | Server port | 9000 |

## Run the Server
```bash
node index.js
```
Then open: http://localhost:9000

## Generate Schema (Optional)
From CCDI model YAML:
```bash
python data-model-schema-graphql.py \
  external/ccdi-dcc-model/model-desc/ccdi-dcc-model.yml \
  external/ccdi-dcc-model/model-desc/ccdi-dcc-model-props.yml \
  > schema-from-model.graphql
```

## Explore with GraphQL Playground
Run queries like:
```graphql
query ListStudies { studies(options: { limit: 3 }) { study_id study_name } }
```

## Docker Flow
```bash
docker build -t ccdi-dcc-graphql .
docker run -p 9000:9000 ccdi-dcc-graphql
```

