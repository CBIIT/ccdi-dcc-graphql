# Use Cases

Below are practical, role‑oriented GraphQL query examples you can adapt. Start with a small `limit`, verify fields, then expand.

---
## Researcher: Early Diagnosis Neuroblastoma (Abdomen)
**Goal:** Participants diagnosed before age 5 with neuroblastoma in the abdomen, newest diagnosis first.

```graphql
query EarlyNeuroblastomaAbdomen {
  participants(
    where: {
      diagnoses_SOME: {
        diagnosis_CONTAINS: "neuroblastoma"
        anatomic_site_CONTAINS: "abdomen"
        age_at_diagnosis_LT: 5
      }
    }
    options: {
      sort: [{ diagnoses: { year_of_diagnosis_DESC: true } }]
      limit: 10
    }
  ) {
    participant_id
    sex_at_birth
    diagnoses {
      diagnosis
      year_of_diagnosis
      age_at_diagnosis
      anatomic_site
    }
  }
}
```

---
## Data Scientist: Sequencing File Stats by Platform
**Goal:** Total files + average/min/max size, grouped by platform.

```graphql
query SeqFileStatsByPlatform {
  sequencing_filesAggregate {
    count
    file_size { average min max }
    platform { groupBy { platform count } }
  }
}
```
> Adjust naming if your schema uses a different aggregate root or field names.

---
## Cohort Analyst: Female Asian Participants with >3 Samples
**Goal:** Filter by sex, race, and sample count.

```graphql
query FemaleAsianSampleRich {
  participants(
    where: {
      sex_at_birth: "Female"
      race_CONTAINS: "Asian"
      samplesAggregate: { count_GT: 3 }
    }
    options: { sort: [{ participant_id_ASC: true }], limit: 20 }
  ) {
    participant_id
    race
    sex_at_birth
    samples { sample_id }
  }
}
```

---
## Genomics: TP53 Alterations & Survival
**Goal:** Participants with TP53 mutation and deceased status + average survival age.

```graphql
query TP53DeceasedSurvivalAvg {
  participants(
    where: {
      samples_SOME: { genetic_analyses_SOME: { gene_symbol: "TP53" } }
      survivals_SOME: { last_known_survival_status_CONTAINS: "Deceased" }
    }
  ) {
    participant_id
    survivalsAggregate { age_at_last_known_survival_status { average } }
  }
}
```

---
## Epidemiologist: High Smoking + Asbestos Exposure
**Goal:** Smokers (>20 cigarettes/day) with asbestos exposure, ordered by years smoked.

```graphql
query HighRiskExposure {
  participants(
    where: {
      exposures_SOME: {
        cigarettes_per_day_GT: 20
        asbestos_exposure_CONTAINS: "Yes"
      }
    }
    options: { sort: [{ exposures: { years_smoked_DESC: true } }], limit: 15 }
  ) {
    participant_id
    exposures { cigarettes_per_day asbestos_exposure years_smoked }
  }
}
```

---
## Bioinformatics: High Coverage Tumor Samples
**Goal:** Tumor samples with average coverage > 30x.

```graphql
query HighCoverageTumorSamples {
  samples(
    where: {
      sequencing_filesAggregate: { coverage_AVERAGE_GT: 30 }
      sample_tumor_status_CONTAINS: "tumor"
    }
    options: { sort: [{ sequencing_filesAggregate: { coverage_AVERAGE_DESC: true } }], limit: 10 }
  ) {
    sample_id
    anatomic_site
    sequencing_filesAggregate { coverage { average } }
  }
}
```

---
## Researcher: Osteosarcoma + Complete Response
**Goal:** Participants with osteosarcoma diagnosis and complete treatment response.

```graphql
query OsteosarcomaCompleteResponse {
  participants(
    where: {
      diagnoses_SOME: { diagnosis_CONTAINS: "osteosarcoma" }
      treatment_responses_SOME: { response_CONTAINS: "Complete" }
    }
  ) {
    participant_id
    diagnoses { diagnosis age_at_diagnosis }
    treatment_responses { response response_system }
    survivals { last_known_survival_status age_at_last_known_survival_status }
  }
}
```

---
## Data Curator: Paginated Studies + Participant Count
**Goal:** Page 2 (offset 10) of studies with participant counts.

```graphql
query PaginatedStudies {
  studies(options: { offset: 10, limit: 10, sort: [{ study_name_ASC: true }] }) {
    study_name
    dbgap_accession
    participantsAggregate { count }
  }
}
```

---
## Genetic Counselor: Family History + Leukemia
**Goal:** Participants with family cancer history AND leukemia diagnosis.

```graphql
query FamilyHistoryLeukemia {
  participants(
    where: {
      AND: [
        { medical_histories_SOME: { medical_history_condition_CONTAINS: "cancer" } }
        { diagnoses_SOME: { diagnosis_CONTAINS: "leukemia" } }
      ]
    }
  ) {
    participant_id
    sex_at_birth
    family_relationships { relationship related_to_participant_id }
    diagnoses { diagnosis age_at_diagnosis diagnosis_category }
  }
}
```

---
## Data Quality: Average Lab Test Result
**Goal:** Per-participant summary stats of laboratory tests.

```graphql
query LabResultAverages {
  participants {
    participant_id
    laboratory_testsAggregate {
      test_result_numeric { average max min }
    }
  }
}
```

---
## Bioinformatics Engineer: RNA-Seq Rich Samples
**Goal:** Samples with >5 sequencing files and at least one RNA‑Seq file.

```graphql
query RNASeqRichSamples {
  samples(
    where: {
      sequencing_filesAggregate: { count_GT: 5 }
      sequencing_files_SOME: { library_strategy_CONTAINS: "RNA-Seq" }
    }
    options: { sort: [{ sample_id_ASC: true }] }
  ) {
    sample_id
    sequencing_filesAggregate { count }
    sequencing_files { file_name library_strategy }
  }
}
```

---
## Multimodal: Pathology + Radiology Availability
**Goal:** Samples that have both pathology (H&E) and MRI radiology files.

```graphql
query MultimodalSamples {
  samples(
    where: {
      AND: [
        { pathology_files_SOME: { image_modality_CONTAINS: "H&E" } }
        { radiology_files_SOME: { image_modality_CONTAINS: "MRI" } }
      ]
    }
  ) {
    sample_id
    pathology_files { file_name staining_method magnification }
    radiology_files { file_name image_modality magnetic_field_strength slice_thickness }
  }
}
```

---
## Translational: PDX Models with Treatments
**Goal:** Traverse PDX → Sample → Participant → Treatments.

```graphql
query PDXWithTreatments {
  pdxes {
    pdx_id
    implantation_site
    validation_technique
    sample {
      sample_id
      sample_tumor_status
      participant {
        participant_id
        treatments { treatment_agent dose dose_unit treatment_type }
      }
    }
  }
}
```

---
## Grants: Study Publications & Funding
**Goal:** Publications count + funding per study.

```graphql
query StudyPubFunding {
  studies(options: { sort: [{ study_name_ASC: true }], limit: 10 }) {
    study_name
    dbgap_accession
    study_fundings { funding_agency grant_id }
    publicationsAggregate { count }
    publications { pubmed_id }
  }
}
```

---
## Clinical Review: Vincristine & Survivors
**Goal:** Alive participants treated with vincristine, youngest survivors first.

```graphql
query VincristineAliveParticipants {
  participants(
    where: {
      AND: [
        { treatments_SOME: { treatment_agent_CONTAINS: "vincristine" } }
        { survivals_SOME: { last_known_survival_status_CONTAINS: "Alive" } }
      ]
    }
    options: {
      sort: [{ survivals: { age_at_last_known_survival_status_ASC: true } }]
      limit: 10
      offset: 0
    }
  ) {
    participant_id
    treatments { treatment_agent dose treatment_type }
    survivals { last_known_survival_status age_at_last_known_survival_status }
  }
}
```

---
### Adaptation Tips
| Need | Tweak |
|------|-------|
| Fewer rows | Lower `limit` |
| Next page | Increase `offset` |
| Narrow filter | Add more `*_CONTAINS` or numeric comparisons |
| Performance | Retrieve fewer nested collections first |

Use these as templates—swap field names or filters to fit your dataset.
