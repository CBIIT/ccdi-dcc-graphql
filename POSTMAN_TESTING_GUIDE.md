# CCDI DCC GraphQL API - Postman Testing Guide

This document explains the test cases included in the Postman collection for the CCDI DCC GraphQL API.

## Overview

The Postman collection includes comprehensive test cases for:
- **Response validation** (status codes, response structure)
- **GraphQL-specific testing** (error handling, query validation)
- **Data integrity testing** (field validation, type checking)
- **Relationship testing** (nested queries, foreign keys)
- **Performance testing** (response times, load validation)
- **Collection-level metrics** (success rates, API health)

## Test Categories

### 1. Basic Response Tests
Every request includes these fundamental tests:
```javascript
// Status code validation
pm.test('Response status is 200', function () {
    pm.response.to.have.status(200);
});

// GraphQL error checking
pm.test('No GraphQL errors', function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.not.have.property('errors');
});

// Response time validation
pm.test('Response time is acceptable', function () {
    pm.expect(pm.response.responseTime).to.be.below(5000);
});
```

### 2. Data Structure Tests
Validates the structure and types of returned data:
```javascript
// Array validation
pm.test('Data is returned as array', function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.data.participants).to.be.an('array');
});

// Required fields validation
pm.test('Objects have required fields', function () {
    const responseJson = pm.response.json();
    if (responseJson.data.participants.length > 0) {
        const participant = responseJson.data.participants[0];
        pm.expect(participant).to.have.property('participant_id');
        pm.expect(participant).to.have.property('id');
    }
});
```

### 3. Relationship Tests
Tests for GraphQL relationship queries:
```javascript
// Relationship field existence
pm.test('Relationship fields exist', function () {
    const responseJson = pm.response.json();
    if (responseJson.data.cellLines.length > 0) {
        const cellLine = responseJson.data.cellLines[0];
        pm.expect(cellLine).to.have.property('studies');
        pm.expect(cellLine).to.have.property('samples');
        pm.expect(cellLine.studies).to.be.an('array');
    }
});

// Nested relationship validation
pm.test('Nested relationships are valid', function () {
    const responseJson = pm.response.json();
    responseJson.data.study.cell_lines.forEach(cellLine => {
        pm.expect(cellLine).to.have.property('samples');
        pm.expect(cellLine.samples).to.be.an('array');
    });
});
```

### 4. Data Type Validation
Ensures proper data types are returned:
```javascript
pm.test('Field data types are correct', function () {
    const responseJson = pm.response.json();
    responseJson.data.participants.forEach(participant => {
        if (participant.participant_id !== null) {
            pm.expect(participant.participant_id).to.be.a('string');
        }
        if (participant.age_at_diagnosis !== null) {
            pm.expect(participant.age_at_diagnosis).to.be.a('number');
        }
    });
});
```

### 5. Variable and Parameter Tests
For parameterized queries:
```javascript
// Variable validation
pm.test('Variables are properly set', function () {
    const requestBody = JSON.parse(pm.request.body.raw);
    pm.expect(requestBody).to.have.property('variables');
    pm.expect(requestBody.variables).to.have.property('cellLineId');
});

// ID matching validation
pm.test('Returned ID matches requested ID', function () {
    const responseJson = pm.response.json();
    const requestBody = JSON.parse(pm.request.body.raw);
    const requestedId = requestBody.variables.cellLineId;
    
    if (responseJson.data.cellLine !== null) {
        pm.expect(responseJson.data.cellLine.cell_line_id).to.equal(requestedId);
    }
});
```

## Collection-Level Features

### Variables
The collection includes these variables for test configuration:
- `baseUrl`: GraphQL endpoint URL
- `testCellLineId`, `testParticipantId`, etc.: Test IDs for parameterized queries
- `maxResponseTime`: Maximum acceptable response time
- `testRunTimestamp`: When the test run started

### Collection Scripts

#### Pre-request Script
Runs before each request:
- Sets test run timestamp
- Logs request information
- Can add authentication headers

#### Test Script
Runs after each request:
- Tracks API health metrics
- Logs GraphQL errors
- Calculates success rates

### Metrics Tracking
The collection automatically tracks:
- Total requests made
- Successful requests (200 status, no GraphQL errors)
- Error requests
- Success rate percentage

## Test Execution Options

### 1. Individual Request Testing
- Select any request in the collection
- Click "Send" to execute with tests
- View test results in the "Test Results" tab

### 2. Folder Testing
- Right-click on a folder (e.g., "Cell Line Queries")
- Select "Run folder"
- Execute all requests in that folder with tests

### 3. Full Collection Testing
- Click "Runner" in Postman
- Select the entire collection
- Configure iterations and delays
- Run comprehensive test suite

### 4. Automated Testing
- Use Newman (Postman CLI) for CI/CD integration
- Export collection and environment
- Run automated tests in your pipeline

## Advanced Test Scenarios

### Performance Testing
```javascript
// Load testing simulation
pm.test('API handles concurrent requests', function () {
    // This would be implemented with multiple iterations
    pm.expect(pm.response.responseTime).to.be.below(10000);
});

// Memory usage validation
pm.test('Response size is reasonable', function () {
    const responseSize = pm.response.responseSize;
    pm.expect(responseSize).to.be.below(10000000); // 10MB limit
});
```

### Data Consistency Tests
```javascript
// Cross-reference validation
pm.test('Participant count matches samples', function () {
    // Validate that participant counts in different queries match
    const participantCount = pm.collectionVariables.get('participantCount');
    const sampleParticipantCount = pm.collectionVariables.get('sampleParticipantCount');
    
    if (participantCount && sampleParticipantCount) {
        pm.expect(Math.abs(participantCount - sampleParticipantCount)).to.be.below(10);
    }
});
```

### Security Tests
```javascript
// Input validation
pm.test('API handles invalid input gracefully', function () {
    // Test with malformed variables
    const responseJson = pm.response.json();
    if (responseJson.errors) {
        pm.expect(responseJson.errors[0].message).to.include('validation');
    }
});
```

## Environment Setup

### Development Environment
```json
{
  "baseUrl": "http://localhost:4000/graphql",
  "authToken": "dev-token",
  "maxResponseTime": "5000"
}
```

### Staging Environment
```json
{
  "baseUrl": "https://staging-api.ccdi-dcc.org/graphql",
  "authToken": "staging-token",
  "maxResponseTime": "3000"
}
```

### Production Environment
```json
{
  "baseUrl": "https://api.ccdi-dcc.org/graphql",
  "authToken": "prod-token",
  "maxResponseTime": "2000"
}
```

## Best Practices

### 1. Test Organization
- Group related tests in folders
- Use descriptive test names
- Include both positive and negative test cases

### 2. Data Management
- Use collection variables for reusable test data
- Set up test data in pre-request scripts
- Clean up test data when needed

### 3. Error Handling
- Test both successful and error scenarios
- Validate GraphQL error messages
- Check for proper HTTP status codes

### 4. Performance
- Set appropriate response time limits
- Test with realistic data volumes
- Monitor resource usage

### 5. Maintenance
- Update test data regularly
- Review and update assertions
- Keep documentation current

## Troubleshooting

### Common Issues

1. **GraphQL Syntax Errors**
   - Check query syntax in GraphQL playground first
   - Validate field names against schema
   - Ensure proper variable definitions

2. **Authentication Failures**
   - Verify auth tokens in environment
   - Check token expiration
   - Validate permission levels

3. **Network Issues**
   - Check baseUrl configuration
   - Verify network connectivity
   - Review proxy settings

4. **Test Failures**
   - Review console logs
   - Check variable assignments
   - Validate test logic

### Debugging Tips

1. Use `console.log()` in test scripts for debugging
2. Check the Postman Console for detailed logs
3. Use the GraphQL playground for query validation
4. Review network traffic in browser dev tools

## Integration with CI/CD

### Newman Command Examples
```bash
# Run entire collection
newman run collection.json -e environment.json

# Run specific folder
newman run collection.json -e environment.json --folder "Cell Line Queries"

# Generate reports
newman run collection.json -e environment.json --reporters cli,html --reporter-html-export report.html

# Set timeout and iterations
newman run collection.json -e environment.json --timeout 10000 --iteration-count 5
```

### GitHub Actions Integration
```yaml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Newman
        run: npm install -g newman
      - name: Run Postman tests
        run: newman run CCDI-DCC-GraphQL-Collection.postman_collection.json -e environment.json
```

This comprehensive testing setup ensures your GraphQL API is reliable, performant, and maintains data integrity across all operations.