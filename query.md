# GraphQL Query Examples for CCDI DCC Schema

This document contains example GraphQL queries for all node types in the CCDI DCC GraphQL schema.

## Table of Contents
- [Cell Line Queries](#cell-line-queries)
- [Clinical Measure File Queries](#clinical-measure-file-queries)
- [Consent Group Queries](#consent-group-queries)
- [Cytogenomic File Queries](#cytogenomic-file-queries)
- [Diagnosis Queries](#diagnosis-queries)
- [Exposure Queries](#exposure-queries)
- [Family Relationship Queries](#family-relationship-queries)
- [Genetic Analysis Queries](#genetic-analysis-queries)
- [Medical History Queries](#medical-history-queries)
- [Laboratory Test Queries](#laboratory-test-queries)
- [Methylation Array File Queries](#methylation-array-file-queries)
- [Participant Queries](#participant-queries)
- [Pathology File Queries](#pathology-file-queries)
- [PDX Queries](#pdx-queries)
- [Publication Queries](#publication-queries)
- [Radiology File Queries](#radiology-file-queries)
- [Generic File Queries](#generic-file-queries)
- [Sample Queries](#sample-queries)
- [Sequencing File Queries](#sequencing-file-queries)
- [Study Queries](#study-queries)
- [Study Admin Queries](#study-admin-queries)
- [Study Arm Queries](#study-arm-queries)
- [Study Funding Queries](#study-funding-queries)
- [Study Personnel Queries](#study-personnel-queries)
- [Survival Queries](#survival-queries)
- [Synonym Queries](#synonym-queries)
- [Treatment Queries](#treatment-queries)
- [Treatment Response Queries](#treatment-response-queries)

## Cell Line Queries

### Get all cell lines
```graphql
query GetAllCellLines {
  cellLines {
    cell_line_id
    source
    cell_line_passage_number
    id
  }
}
```

### Get cell lines with related studies and samples
```graphql
query GetCellLinesWithRelations {
  cellLines {
    cell_line_id
    source
    cell_line_passage_number
    id
    studies {
      study_id
      study_name
      study_acronym
    }
    samples {
      sample_id
      anatomic_site
      sample_description
    }
  }
}
```

### Get specific cell line by ID
```graphql
query GetCellLineById($cellLineId: String!) {
  cellLine(cell_line_id: $cellLineId) {
    cell_line_id
    source
    cell_line_passage_number
    id
    studies {
      study_id
      study_name
    }
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Clinical Measure File Queries

### Get all clinical measure files
```graphql
query GetAllClinicalMeasureFiles {
  clinicalMeasureFiles {
    clinical_measure_file_id
    file_name
    data_category
    file_type
    file_size
    md5sum
    file_access
    id
    crdc_id
  }
}
```

### Get clinical measure files with relationships
```graphql
query GetClinicalMeasureFilesWithRelations {
  clinicalMeasureFiles {
    clinical_measure_file_id
    file_name
    data_category
    file_type
    file_size
    studies {
      study_id
      study_name
    }
    participants {
      participant_id
      race
      sex_at_birth
    }
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Consent Group Queries

### Get all consent groups
```graphql
query GetAllConsentGroups {
  consentGroups {
    consent_group_id
    consent_group_name
    consent_group_suffix
    id
  }
}
```

### Get consent groups with related studies and participants
```graphql
query GetConsentGroupsWithRelations {
  consentGroups {
    consent_group_id
    consent_group_name
    consent_group_suffix
    id
    studies {
      study_id
      study_name
    }
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Cytogenomic File Queries

### Get all cytogenomic files
```graphql
query GetAllCytogenomicFiles {
  cytogenomicFiles {
    cytogenomic_file_id
    file_name
    data_category
    file_type
    file_size
    cytogenomic_platform
    id
    crdc_id
  }
}
```

### Get cytogenomic files with samples
```graphql
query GetCytogenomicFilesWithSamples {
  cytogenomicFiles {
    cytogenomic_file_id
    file_name
    cytogenomic_platform
    samples {
      sample_id
      anatomic_site
      sample_description
    }
  }
}
```

## Diagnosis Queries

### Get all diagnoses
```graphql
query GetAllDiagnoses {
  diagnoses {
    diagnosis_id
    submitted_diagnosis
    diagnosis
    diagnosis_category
    age_at_diagnosis
    tumor_grade
    year_of_diagnosis
    id
  }
}
```

### Get diagnoses with participants and samples
```graphql
query GetDiagnosesWithRelations {
  diagnoses {
    diagnosis_id
    diagnosis
    diagnosis_category
    age_at_diagnosis
    participants {
      participant_id
      race
      sex_at_birth
    }
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Exposure Queries

### Get all exposures
```graphql
query GetAllExposures {
  exposures {
    exposure_id
    age_at_exposure
    pack_years_smoked
    years_smoked
    tobacco_smoking_status
    smoking_frequency
    id
  }
}
```

### Get exposures with participants
```graphql
query GetExposuresWithParticipants {
  exposures {
    exposure_id
    tobacco_smoking_status
    smoking_frequency
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Family Relationship Queries

### Get all family relationships
```graphql
query GetAllFamilyRelationships {
  familyRelationships {
    family_relationship_id
    relationship
    family_id
    id
  }
}
```

### Get family relationships with participants
```graphql
query GetFamilyRelationshipsWithParticipants {
  familyRelationships {
    family_relationship_id
    relationship
    family_id
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Genetic Analysis Queries

### Get all genetic analyses
```graphql
query GetAllGeneticAnalyses {
  geneticAnalyses {
    genetic_analysis_id
    age_at_genetic_analysis
    test
    method
    result
    gene_symbol
    alteration
    alteration_type
    id
  }
}
```

### Get genetic analyses with samples and participants
```graphql
query GetGeneticAnalysesWithRelations {
  geneticAnalyses {
    genetic_analysis_id
    test
    result
    gene_symbol
    samples {
      sample_id
      anatomic_site
    }
    participants {
      participant_id
      race
    }
  }
}
```

## Medical History Queries

### Get all medical histories
```graphql
query GetAllMedicalHistories {
  medicalHistories {
    medical_history_id
    medical_history_category
    medical_history_condition
    id
  }
}
```

### Get medical histories with participants
```graphql
query GetMedicalHistoriesWithParticipants {
  medicalHistories {
    medical_history_id
    medical_history_category
    medical_history_condition
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Laboratory Test Queries

### Get all laboratory tests
```graphql
query GetAllLaboratoryTests {
  laboratoryTests {
    laboratory_test_id
    age_at_laboratory_test
    laboratory_test_method
    laboratory_test_name
    specimen
    test_result_text
    test_result_numeric
    id
  }
}
```

### Get laboratory tests with participants and samples
```graphql
query GetLaboratoryTestsWithRelations {
  laboratoryTests {
    laboratory_test_id
    laboratory_test_name
    test_result_text
    participants {
      participant_id
      race
    }
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Methylation Array File Queries

### Get all methylation array files
```graphql
query GetAllMethylationArrayFiles {
  methylationArrayFiles {
    methylation_array_file_id
    file_name
    data_category
    file_type
    file_size
    methylation_platform
    reporter_label
    id
    crdc_id
  }
}
```

### Get methylation array files with samples
```graphql
query GetMethylationArrayFilesWithSamples {
  methylationArrayFiles {
    methylation_array_file_id
    file_name
    methylation_platform
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Participant Queries

### Get all participants
```graphql
query GetAllParticipants {
  participants {
    participant_id
    race
    sex_at_birth
    id
    crdc_id
  }
}
```

### Get participants with all relationships
```graphql
query GetParticipantsWithAllRelations {
  participants {
    participant_id
    race
    sex_at_birth
    consent_groups {
      consent_group_id
      consent_group_name
    }
    diagnosis {
      diagnosis_id
      diagnosis
    }
    samples {
      sample_id
      anatomic_site
    }
    treatments {
      treatment_id
      treatment_type
    }
  }
}
```

## Pathology File Queries

### Get all pathology files
```graphql
query GetAllPathologyFiles {
  pathologyFiles {
    pathology_file_id
    file_name
    data_category
    file_type
    file_size
    image_modality
    magnification
    staining_method
    id
    crdc_id
  }
}
```

### Get pathology files with samples
```graphql
query GetPathologyFilesWithSamples {
  pathologyFiles {
    pathology_file_id
    file_name
    image_modality
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## PDX Queries

### Get all PDX models
```graphql
query GetAllPdxModels {
  pdxModels {
    pdx_id
    model_id
    mouse_strain
    implantation_type
    implantation_site
    passage_number
    validation_technique
    id
  }
}
```

### Get PDX models with studies and samples
```graphql
query GetPdxModelsWithRelations {
  pdxModels {
    pdx_id
    model_id
    mouse_strain
    studies {
      study_id
      study_name
    }
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Publication Queries

### Get all publications
```graphql
query GetAllPublications {
  publications {
    publication_id
    pubmed_id
    id
  }
}
```

### Get publications with studies
```graphql
query GetPublicationsWithStudies {
  publications {
    publication_id
    pubmed_id
    studies {
      study_id
      study_name
      study_description
    }
  }
}
```

## Radiology File Queries

### Get all radiology files
```graphql
query GetAllRadiologyFiles {
  radiologyFiles {
    radiology_file_id
    file_name
    data_category
    file_type
    file_size
    anatomic_site
    participant_age_at_imaging
    image_modality
    scanner_manufacturer
    id
    crdc_id
  }
}
```

### Get radiology files with participants
```graphql
query GetRadiologyFilesWithParticipants {
  radiologyFiles {
    radiology_file_id
    file_name
    image_modality
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Generic File Queries

### Get all generic files
```graphql
query GetAllGenericFiles {
  genericFiles {
    generic_file_id
    file_name
    data_category
    file_type
    file_description
    file_size
    md5sum
    file_access
    id
    crdc_id
  }
}
```

### Get generic files with all relationships
```graphql
query GetGenericFilesWithRelations {
  genericFiles {
    generic_file_id
    file_name
    data_category
    studies {
      study_id
      study_name
    }
    participants {
      participant_id
      race
    }
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Sample Queries

### Get all samples
```graphql
query GetAllSamples {
  samples {
    sample_id
    anatomic_site
    participant_age_at_collection
    sample_tumor_status
    sample_description
    percent_tumor
    id
    crdc_id
  }
}
```

### Get samples with all relationships
```graphql
query GetSamplesWithAllRelations {
  samples {
    sample_id
    anatomic_site
    sample_tumor_status
    participants {
      participant_id
      race
      sex_at_birth
    }
    cell_lines {
      cell_line_id
      source
    }
    diagnosis {
      diagnosis_id
      diagnosis
    }
    sequencing_files {
      sequencing_file_id
      platform
    }
  }
}
```

## Sequencing File Queries

### Get all sequencing files
```graphql
query GetAllSequencingFiles {
  sequencingFiles {
    sequencing_file_id
    file_name
    data_category
    file_type
    file_size
    library_strategy
    platform
    instrument_model
    number_of_reads
    coverage
    id
    crdc_id
  }
}
```

### Get sequencing files with samples
```graphql
query GetSequencingFilesWithSamples {
  sequencingFiles {
    sequencing_file_id
    file_name
    platform
    library_strategy
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Study Queries

### Get all studies
```graphql
query GetAllStudies {
  studies {
    study_id
    dbgap_accession
    study_name
    study_acronym
    study_description
    study_status
    experimental_strategy_and_data_subtype
    id
    crdc_id
  }
}
```

### Get studies with all relationships
```graphql
query GetStudiesWithAllRelations {
  studies {
    study_id
    study_name
    study_acronym
    cell_lines {
      cell_line_id
      source
    }
    publications {
      publication_id
      pubmed_id
    }
    study_admins {
      study_admin_id
      organism_species
    }
    study_personnels {
      study_personnel_id
      personnel_name
      institution
    }
  }
}
```

## Study Admin Queries

### Get all study admins
```graphql
query GetAllStudyAdmins {
  studyAdmins {
    study_admin_id
    organism_species
    adult_or_childhood_study
    number_of_participants
    number_of_samples
    id
  }
}
```

### Get study admins with studies
```graphql
query GetStudyAdminsWithStudies {
  studyAdmins {
    study_admin_id
    organism_species
    number_of_participants
    studies {
      study_id
      study_name
    }
  }
}
```

## Study Arm Queries

### Get all study arms
```graphql
query GetAllStudyArms {
  studyArms {
    study_arm_id
    study_arm_description
    clinical_trial_identifier
    clinical_trial_repository
    id
  }
}
```

### Get study arms with studies
```graphql
query GetStudyArmsWithStudies {
  studyArms {
    study_arm_id
    study_arm_description
    clinical_trial_identifier
    studies {
      study_id
      study_name
    }
  }
}
```

## Study Funding Queries

### Get all study fundings
```graphql
query GetAllStudyFundings {
  studyFundings {
    study_funding_id
    funding_agency
    grant_id
    funding_source_program_name
    id
  }
}
```

### Get study fundings with studies
```graphql
query GetStudyFundingsWithStudies {
  studyFundings {
    study_funding_id
    funding_agency
    grant_id
    studies {
      study_id
      study_name
    }
  }
}
```

## Study Personnel Queries

### Get all study personnel
```graphql
query GetAllStudyPersonnel {
  studyPersonnels {
    study_personnel_id
    personnel_name
    personnel_type
    email_address
    institution
    orcid
    id
    crdc_id
  }
}
```

### Get study personnel with studies
```graphql
query GetStudyPersonnelWithStudies {
  studyPersonnels {
    study_personnel_id
    personnel_name
    personnel_type
    institution
    studies {
      study_id
      study_name
    }
  }
}
```

## Survival Queries

### Get all survivals
```graphql
query GetAllSurvivals {
  survivals {
    survival_id
    last_known_survival_status
    age_at_last_known_survival_status
    first_event
    event_free_survival_status
    cause_of_death
    id
  }
}
```

### Get survivals with participants
```graphql
query GetSurvivalsWithParticipants {
  survivals {
    survival_id
    last_known_survival_status
    age_at_last_known_survival_status
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Synonym Queries

### Get all synonyms
```graphql
query GetAllSynonyms {
  synonyms {
    synonym_id
    repository_of_synonym_id
    associated_id
    domain_description
    domain_category
    data_location
    id
  }
}
```

### Get synonyms with all relationships
```graphql
query GetSynonymsWithRelations {
  synonyms {
    synonym_id
    repository_of_synonym_id
    domain_description
    studies {
      study_id
      study_name
    }
    participants {
      participant_id
      race
    }
    samples {
      sample_id
      anatomic_site
    }
  }
}
```

## Treatment Queries

### Get all treatments
```graphql
query GetAllTreatments {
  treatments {
    treatment_id
    age_at_treatment_start
    age_at_treatment_end
    treatment_type
    treatment_agent
    dose
    dose_unit
    id
  }
}
```

### Get treatments with participants
```graphql
query GetTreatmentsWithParticipants {
  treatments {
    treatment_id
    treatment_type
    treatment_agent
    dose
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Treatment Response Queries

### Get all treatment responses
```graphql
query GetAllTreatmentResponses {
  treatmentResponses {
    treatment_response_id
    response
    age_at_response
    response_category
    response_system
    id
  }
}
```

### Get treatment responses with participants
```graphql
query GetTreatmentResponsesWithParticipants {
  treatmentResponses {
    treatment_response_id
    response
    response_category
    participants {
      participant_id
      race
      sex_at_birth
    }
  }
}
```

## Complex Queries

### Get comprehensive study information
```graphql
query GetComprehensiveStudyInfo($studyId: String!) {
  study(study_id: $studyId) {
    study_id
    study_name
    study_description
    study_status
    publications {
      publication_id
      pubmed_id
    }
    study_personnels {
      personnel_name
      personnel_type
      institution
    }
    study_admins {
      organism_species
      number_of_participants
      number_of_samples
    }
    cell_lines {
      cell_line_id
      source
      samples {
        sample_id
        anatomic_site
      }
    }
  }
}
```

### Get participant with complete medical profile
```graphql
query GetParticipantMedicalProfile($participantId: String!) {
  participant(participant_id: $participantId) {
    participant_id
    race
    sex_at_birth
    diagnosis {
      diagnosis_id
      diagnosis
      age_at_diagnosis
    }
    treatments {
      treatment_id
      treatment_type
      treatment_agent
    }
    treatment_responses {
      treatment_response_id
      response
      age_at_response
    }
    survivals {
      survival_id
      last_known_survival_status
      age_at_last_known_survival_status
    }
    exposures {
      exposure_id
      tobacco_smoking_status
      pack_years_smoked
    }
  }
}
```

### Get sample with all associated files
```graphql
query GetSampleWithFiles($sampleId: String!) {
  sample(sample_id: $sampleId) {
    sample_id
    anatomic_site
    sample_tumor_status
    sample_description
    sequencing_files {
      sequencing_file_id
      file_name
      platform
      library_strategy
    }
    pathology_files {
      pathology_file_id
      file_name
      image_modality
      staining_method
    }
    cytogenomic_files {
      cytogenomic_file_id
      file_name
      cytogenomic_platform
    }
    methylation_array_files {
      methylation_array_file_id
      file_name
      methylation_platform
    }
  }
}
```