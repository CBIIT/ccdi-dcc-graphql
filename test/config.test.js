import test from 'node:test';
import assert from 'node:assert/strict';
import { getDatabaseConfig, getServerConfig } from '../config.js';

test('uses safe database defaults when variables are absent', () => {
  assert.deepEqual(getDatabaseConfig({}), {
    uri: 'bolt://localhost:7687',
    username: '',
    password: ''
  });
});

test('uses configured database values', () => {
  assert.deepEqual(getDatabaseConfig({
    DB_URI: 'bolt://db.example:7687',
    DB_USERNAME: 'neo4j',
    DB_PASSWORD: 'secret'
  }), {
    uri: 'bolt://db.example:7687',
    username: 'neo4j',
    password: 'secret'
  });
});

test('uses default server settings', () => {
  assert.deepEqual(getServerConfig({}), { port: 9000, host: '0.0.0.0' });
});

test('uses configured server settings', () => {
  assert.deepEqual(getServerConfig({ PORT: '9100', HOST: '127.0.0.1' }), {
    port: 9100,
    host: '127.0.0.1'
  });
});