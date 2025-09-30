# CCDI DCC GraphQL API

## Overview
A GraphQL API service for the Childhood Cancer Data Initiative (CCDI) Data Coordinating Center (DCC). This service provides a unified GraphQL interface for accessing complex biomedical research data stored in a Neo4j/Memgraph graph database. The API supports flexible querying of participants, samples, studies, and their interconnected relationships.

## Features
- **GraphQL API**: Auto-generated schema from graph database with custom resolvers
- **Graph Database Integration**: Neo4j/Memgraph connectivity with relationship-based querying  
- **Schema Generation**: Python utility to generate GraphQL schema from Memgraph JSON schema
- **Biomedical Data Types**: Support for participants, samples, studies, diagnoses, treatments, and more
- **Custom Queries**: Specialized aggregation queries for sample grouping and counting
- **GraphQL Playground**: Interactive query interface for development and testing

## Architecture

### Core Components
- **Apollo Server 4**: GraphQL server with Neo4j GraphQL library integration
- **Neo4j GraphQL Library**: Auto-generates CRUD operations and relationship resolvers
- **Graph Database**: Neo4j or Memgraph for storing interconnected biomedical data
- **Schema Generator**: Python script to convert database schema to GraphQL SDL

### Data Model
The GraphQL schema includes types for:
- Research participants and their demographics
- Biological samples and specimen data  
- Clinical diagnoses and medical histories
- Laboratory tests and genetic analyses
- Study metadata and administrative data
- File attachments (sequencing, pathology, radiology)
- Complex relationships between all entities

## Tech Stack
- **Apollo Server 4** - GraphQL server and middleware
- **@neo4j/graphql** - Neo4j GraphQL library for auto-generated resolvers
- **Neo4j/Memgraph** - Graph database for biomedical data storage
- **Node.js 20+** - Runtime environment with ES modules
- **Docker** - Containerization for deployment

## Installation & Setup

### Prerequisites
- Node.js 20 or higher
- Neo4j or Memgraph database instance
- NPM or Yarn package manager

### Local Development
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ccdi-dcc-graphql
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

4. **Start the server**
   ```bash
   node index.js
   ```

5. **Access GraphQL Playground**
   - Development: `http://localhost:9000`
   - Production endpoints as configured

### Docker Deployment
```bash
# Build the container
docker build -t ccdi-dcc-graphql .

# Run with environment variables
docker run -p 9000:9000 -e DB_URI=bolt://your-db:7687 ccdi-dcc-graphql
```

## Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `NEO4J_URI` | Database connection string | `bolt://localhost:7687` |
| `NEO4J_USERNAME` | Database username | `neo4j` |
| `NEO4J_PASSWORD` | Database password | _(required)_ |
| `NODE_ENV` | Environment mode | `development` |
| `PORT` | Server port | `9000` |

## Schema Management

### GraphQL Schema Generation
The project includes a Python utility to generate GraphQL schema from Memgraph schema JSON:

```bash
python memgraph-schema-graphql.py schema.json > schema.graphql
```

This tool:
- Converts node labels to GraphQL types
- Maps properties to appropriate GraphQL field types  
- Generates relationship fields with `@relationship` directives
- Includes custom query types for data aggregation


## API Usage

### Example Queries

These queries are ready to run in the GraphQL Playground at `http://localhost:9000` after starting the server.

#### 1. List All Participants (Simple)
```graphql
query ListParticipants {
  participants(options: { limit: 10 }) {
    participant_id
    race
    sex_at_birth
  }
}
```

#### 2. Get Participant by ID
```graphql
query GetParticipant {
  participants(where: { participant_id: "CCDI_00001" }) {
    participant_id
    race
    sex_at_birth
    samples {
      sample_id
      anatomic_site
      tumor_classification
    }
  }
}
```

#### 3. List All Samples
```graphql
query ListSamples {
  samples(options: { limit: 10 }) {
    sample_id
    anatomic_site
    tumor_classification
    sample_tumor_status
  }
}
```

#### 4. Count Samples by Tumor Type
```graphql
query SampleCounts {
  samplesByTumorClassification {
    field
    count
  }
}
```

#### 5. Search Samples by Anatomic Site
```graphql
query SamplesByBrain {
  samples(
    where: { anatomic_site: "Brain" }
    options: { limit: 5 }
  ) {
    sample_id
    anatomic_site
    tumor_classification
    participants {
      participant_id
      race
    }
  }
}
```

#### 6. List Studies
```graphql
query ListStudies {
  studies(options: { limit: 5 }) {
    study_id
    study_name
    study_description
  }
}
```

#### 7. Get Files for a Sample
```graphql
query FilesForSample {
  samples(where: { sample_id: "SAMPLE_001" }) {
    sample_id
    sequencing_files {
      file_name
      file_type
      data_category
    }
  }
}
```

**Pro tip:** Copy any query above directly into the GraphQL Playground and click the play button to run it. No variables needed for these basic examples!

## Development

### Project Structure
```
├── index.js                 # Main Apollo Server application
├── schema.graphql          # GraphQL type definitions
├── memgraph-schema-graphql.py # Schema generation utility
├── package.json            # Node.js dependencies
├── Dockerfile             # Container configuration  
├── .env.example           # Environment template
└── README.md              # This file
```


