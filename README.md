# CCDI DCC GraphQL API

## Overview
A GraphQL API service for the Childhood Cancer Data Initiative (CCDI) Data Coordinating Center (DCC). This service provides a unified GraphQL interface for accessing complex biomedical research data stored in a Neo4j/Memgraph graph database. The API supports flexible querying of participants, samples, studies, and their interconnected relationships.

## Features
- **GraphQL API**: Auto-generated schema from graph database with custom resolvers
- **Graph Database Integration**: Neo4j/Memgraph connectivity with relationship-based querying  
- **Schema Generation**: Python utilities to generate GraphQL schema from (a) Memgraph JSON, and (b) CCDI DCC MDF model YAML via the vendored Bento MDF/Meta libraries (`data-model-schema-graphql-mdf.py`)
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
- Python 3.7+ (for schema generation utilities)
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

5. **Set up Python environment (for schema generation)**
   ```bash
   # Create Python virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   
   # Install Python dependencies
   pip install PyYAML
   
   # Deactivate when done
   deactivate
   ```

6. **Access GraphQL Playground**
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

### Option 1: From CCDI DCC Model YAML Files (Legacy Script)
Generate GraphQL schema from CCDI DCC model definition files using the original, lightweight parser:

```bash
# Prerequisites: Set up Python virtual environment and install dependencies
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required Python packages
pip install PyYAML

# Generate schema from YAML model files
python data-model-schema-graphql.py external/ccdi-dcc-model/model-desc/ccdi-dcc-model.yml external/ccdi-dcc-model/model-desc/ccdi-dcc-model-props.yml > schema-from-model.graphql

# Deactivate virtual environment when done
deactivate
```

**Features of `data-model-schema-graphql.py`:**
- Parses CCDI DCC model YAML files (`ccdi-dcc-model.yml` and `ccdi-dcc-model-props.yml`)
- Converts node definitions to GraphQL types
- Maps properties to appropriate GraphQL field types based on property definitions
- Generates relationship fields with `@relationship` directives
- Handles proper type inference (String, Int, Boolean, Float)
- Supports complex biomedical data model relationships
- Includes field count aggregation types

### Option 2: Using Bento MDF / Meta Libraries (Preferred)
`data-model-schema-graphql-mdf.py` leverages the vendored Bento MDF / Meta libraries (`external/ccdi-dcc-model/bento-mdf`) to fully parse, validate, and merge one or more MDF YAML model description files, then emits a deterministic Neo4j GraphQL–compatible SDL schema.

#### Why this script?
- Re-uses the canonical MDF parser/validator instead of maintaining custom YAML parsing logic
- Merges multiple MDF YAML files in left→right order (later files can extend/override)
- Deterministic relationship field naming; preserves duplicates with numeric suffixes
- Best‑effort mapping from MDF value domains to GraphQL scalars (all fields nullable by default)
- Produces stable output suited for version control diffs

#### Prerequisites
Python 3.8+ (the vendored libraries are included; no extra pip installs required for basic use). If you already created a virtual environment, just activate it—no additional dependencies should be necessary. If you prefer to install the libraries yourself rather than rely on the vendored copy, consult `external/ccdi-dcc-model/bento-mdf/python/pyproject.toml`.

#### Basic Usage
```bash
python data-model-schema-graphql-mdf.py external/ccdi-dcc-model/model-desc/ccdi-dcc-model.yml > schema.graphql
```

#### Merging Multiple MDF Files
You can supply multiple YAML files. They are read and merged in order (left to right):
```bash
python data-model-schema-graphql-mdf.py \
  external/ccdi-dcc-model/model-desc/ccdi-dcc-model.yml \
  external/ccdi-dcc-model/model-desc/ccdi-dcc-model-props.yml \
  > schema.graphql
```

#### Output
- Writes GraphQL SDL to stdout (redirect or pipe as needed)
- Adds a `FieldCount` helper type
- Generates one `type <Node>` per MDF node with property fields (nullable) and relationship fields annotated with `@relationship(type: "EDGE_HANDLE", direction: OUT|IN)`

#### Value Domain Mapping (Summary)
| MDF Domain | GraphQL |
|------------|---------|
| string / regexp / value_set | String |
| integer / int | Int |
| float / number / double | Float |
| boolean / bool | Boolean |
| list (primitive) | [MappedType] |
| list (value_set) | [String] |
| (unrecognized) | String |

All list and scalar fields are nullable; list elements are also nullable. Adjust nullability post‑generation if your application requires stricter constraints.

#### Comparison vs Legacy Script
| Aspect | Legacy (`data-model-schema-graphql.py`) | MDF (`data-model-schema-graphql-mdf.py`) |
|--------|----------------------------------------|------------------------------------------|
| Parsing | Manual YAML traversal | Canonical MDF parser (`MDFReader`) |
| Validation | Minimal | Full MDF validation |
| Multiple Files | Two specific files | Arbitrary N YAML files (merge) |
| Determinism | Basic | Stable deterministic field naming |
| Extensibility | Harder | Leverages model object graph |

#### Future Enhancements
- Express composite keys as `@unique` or `@id` where appropriate
- Optionally generate enum types for `value_set` domains
- Configurable nullability & scalar overrides

**Common Features (Both Scripts):**
- Convert MDF / model node labels to GraphQL `type`s
- Map properties to appropriate GraphQL field types  
- Generate relationship fields with `@relationship` directives
- Provide a helper aggregation type (`FieldCount`)


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
├── index.js                      # Main Apollo Server application
├── schema.graphql               # GraphQL type definitions
├── memgraph-schema-graphql.py   # Schema generation from Memgraph JSON
├── data-model-schema-graphql.py       # Legacy schema generation from CCDI model YAML
├── data-model-schema-graphql-mdf.py   # Preferred schema generation using Bento MDF/Meta parser
├── package.json                 # Node.js dependencies
├── Dockerfile                   # Container configuration  
├── docker-compose.yml           # Multi-container setup
├── .env.example                 # Environment template
├── venv/                        # Python virtual environment (created locally)
├── external/                    # External model definitions
│   └── ccdi-dcc-model/         # CCDI DCC model YAML files
└── README.md                    # This file
```


