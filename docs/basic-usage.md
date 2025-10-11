# Basic Usage

## Listing Entities
```graphql
query FirstParticipants { participants(options: { limit: 5 }) { participant_id race sex_at_birth } }
```

## Filtering
```graphql
query BrainSamples {
  samples(where: { anatomic_site: "Brain" }, options: { limit: 5 }) {
    sample_id anatomic_site tumor_classification
  }
}
```

## Nested Traversal
```graphql
query ParticipantSamples {
  participants(where: { participant_id: "CCDI_00001" }) {
    participant_id
    participant_of_sample { sample_id anatomic_site }
  }
}
```

## Counting (Custom Aggregation)
```graphql
query SampleCounts { samplesByTumorClassification { field count } }
```

## Selecting File Metadata
```graphql
query FilesForSample {
  samples(where: { sample_id: "SAMPLE_001" }) {
    sample_id
    sample_of_sequencing_file { file_name platform library_strategy }
  }
}
```

## Pagination
Use `options: { limit, offset, sort: [{ field: ASC|DESC }] }`.
```graphql
query PageParticipants {
  participants(options: { limit: 10, offset: 10, sort: [{ participant_id: ASC }] }) {
    participant_id
  }
}
```
