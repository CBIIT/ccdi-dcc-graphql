import { Neo4jGraphQL } from "@neo4j/graphql";
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import neo4j from 'neo4j-driver'
import { ApolloServerPluginLandingPageGraphQLPlayground } from "@apollo/server-plugin-landing-page-graphql-playground";
 import {
  ApolloServerPluginLandingPageLocalDefault,
  ApolloServerPluginLandingPageProductionDefault,
} from "@apollo/server/plugin/landingPage/default";
import dotenv from 'dotenv';
import { readFileSync } from 'fs';

dotenv.config();

const typeDefs = readFileSync('./schema.graphql', 'utf8');

console.log(process.env)
const driver = neo4j.driver(
    process.env.NEO4J_URI || "bolt://localhost:7687",
    neo4j.auth.basic(process.env.NEO4J_USERNAME || "", process.env.NEO4J_PASSWORD || "")
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
if (process.env.NODE_ENV !== "production") {
  plugins = [ApolloServerPluginLandingPageGraphQLPlayground({ embed: true, graphRef: "myGraph@prod" })];
} else {
  plugins = [ApolloServerPluginLandingPageGraphQLPlayground({ embed: true })];
}


const server = new ApolloServer({
    schema: await neoSchema.getSchema(),
    plugins
});
const { url } = await startStandaloneServer(server, {
    context: async ({ req }) => ({ 
        req, 
        sessionConfig: {database: "memgraph"},
        driver: driver  // Pass driver to context for custom resolvers
    }),
    listen: { port: 9000 , host: "0.0.0.0"},
});
 
console.log(`🚀 Server ready at ${url}`);