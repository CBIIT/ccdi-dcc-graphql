import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { Neo4jGraphQL } from '@neo4j/graphql';
import neo4j from 'neo4j-driver';

const typeDefs = readFileSync(new URL('../schema.graphql', import.meta.url), 'utf8');

test('schema compiles with Neo4j GraphQL built-in scalars', async () => {
  const driver = neo4j.driver('bolt://localhost:7687');

  try {
    const neoSchema = new Neo4jGraphQL({ typeDefs, driver });
    const schema = await neoSchema.getSchema();

    assert.equal(schema.getType('BigInt')?.name, 'BigInt');
    assert.equal(schema.getType('DateTime')?.name, 'DateTime');
    assert.equal(schema.getType('JSON')?.name, 'JSON');
  } finally {
    await driver.close();
  }
});
