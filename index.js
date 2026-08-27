import { Neo4jGraphQL } from "@neo4j/graphql";
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import neo4j from 'neo4j-driver'
import { ApolloServerPluginLandingPageLocalDefault } from "@apollo/server/plugin/landingPage/default";
import dotenv from 'dotenv';
import { readFileSync } from 'fs';
import { getDatabaseConfig, getServerConfig } from './config.js';

dotenv.config();

const typeDefs = readFileSync('./schema.graphql', 'utf8');

const databaseConfig = getDatabaseConfig();
const serverConfig = getServerConfig();
const driver = neo4j.driver(
    databaseConfig.uri,
    neo4j.auth.basic(databaseConfig.username, databaseConfig.password)
);
 

// Define custom resolvers
const resolvers = {
    Query: {
    }
};
 
const neoSchema = new Neo4jGraphQL({ 
    typeDefs, 
    driver,
    resolvers 
});
 

let plugins = [];
plugins = [
        ApolloServerPluginLandingPageLocalDefault({
                document: `query {
  studyStatusesConnection {
    totalCount
    aggregate {
      count {
        nodes
      }
    }
    edges {
      node {
        guid
        study_status_id
        number_of_files
        number_of_participants
      }
    }
  }
}`
        })
];


const server = new ApolloServer({
    schema: await neoSchema.getSchema(),
    introspection: true,
    debug: true,
    plugins
});

const { url } = await startStandaloneServer(server, {
    context: async ({ req }) => ({ 
        req, 
        sessionConfig: {database: "memgraph"},
        driver: driver  // Pass driver to context for custom resolvers
    }),
    listen: serverConfig,
});
 
console.log(`🚀 Server ready at ${url}`);
