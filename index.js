import { Neo4jGraphQL } from "@neo4j/graphql";
import neo4j from 'neo4j-driver'
import express from 'express';
import { graphqlHTTP } from 'express-graphql';
 
const typeDefs = `#graphql
 type participant {
  id: String
  created: String
  crdc_id: String
  uuid: String
  participant_id: String
  race: String
  sex_at_birth: String

  synonym: [synonym!]! @relationship(type: "of_synonym", direction: IN)
  survival: [survival!]! @relationship(type: "of_survival", direction: IN)
  diagnosis: [diagnosis!]! @relationship(type: "of_diagnosis", direction: IN)
  sample: [sample!]! @relationship(type: "of_sample", direction: IN)
  study: study! @relationship(type: "of_participant", direction: OUT)
}

type diagnosis {
  id: String
  created: String
  uuid: String
  diagnosis: String
  diagnosis_id: String
  diagnosis_classification_system: String
  diagnosis_basis: String
  diagnosis_comment: String
  disease_phase: String
  tumor_classification: String
  anatomic_site: String
  age_at_diagnosis: String
  toronto_childhood_cancer_staging: String
  tumor_stage_clinical_t: String
  tumor_stage_clinical_n: String
  tumor_stage_clinical_m: String
  tumor_stage_source: String
  tumor_grade: String
  tumor_grade_source: String
  year_of_diagnosis: String
  laterality: String

  participant: participant @relationship(type: "of_diagnosis", direction: OUT)
}

type sample {
  id: String
  created: String
  crdc_id: String
  uuid: String
  tumor_classification: String
  anatomic_site: String
  sample_id: String
  participant_age_at_collection: String
  sample_tumor_status: String
  sample_description: String

  participant: participant @relationship(type: "of_sample", direction: OUT)
}

type synonym {
  id: String
  created: String
  uuid: String
  synonym_id: String
  repository_of_synonym_id: String
  associated_id: String
  domain_description: String
  domain_category: String
  data_location: String

  participant: participant @relationship(type: "of_synonym", direction: OUT)
}

type survival {
  id: String
  created: String
  uuid: String
  survival_id: String
  last_known_survival_status: String
  age_at_last_known_survival_status: String
  first_event: String
  event_free_survival_status: String
  follow_up_category: String
  follow_up_other: String
  adverse_event: String
  comorbidity: String
  comorbidity_method_of_diagnosis: String
  risk_factor: String
  cause_of_death: String

  participant: participant @relationship(type: "of_survival", direction: OUT)
}

type study {
  id: String
  created: String
  study_id: String
  dbgap_accession: String
  study_name: String
  study_acronym: String
  study_description: String
  consent: String
  consent_number: String
  external_url: String
  experimental_strategy_and_data_subtype: String
  study_status: String
  study_data_types: String
  size_of_data_being_uploaded: String
  crdc_id: String
  uuid: String

  participant: [participant!]! @relationship(type: "of_participant", direction: IN)
  study_admin: [study_admin!]! @relationship(type: "of_study_admin", direction: OUT)
  study_arm: [study_arm!]! @relationship(type: "of_study_arm", direction: OUT)
  clinical_measure_file: [clinical_measure_file!]! @relationship(type: "of_clinical_measure_file", direction: OUT)
  study_personnel: [study_personnel!]! @relationship(type: "of_study_personnel", direction: OUT)
  publication: [publication!]! @relationship(type: "of_publication", direction: OUT)
  study_funding: [study_funding!]! @relationship(type: "of_study_funding", direction: OUT)
}

type study_admin {
  id: String
  created: String
  uuid: String
  study_admin_id: String
  organism_species: String
  adult_or_childhood_study: String
  file_types_and_format: String

  study: study @relationship(type: "of_study_admin", direction: IN)
}

type study_arm {
  id: String
  created: String
  uuid: String
  study_arm_id: String
  study_arm_description: String
  clinical_trial_identifier: String
  clinical_trial_repository: String

  study: study @relationship(type: "of_study_arm", direction: IN)
}

type clinical_measure_file {
  id: String
  created: String
  crdc_id: String
  uuid: String
  clinical_measure_file_id: String
  file_name: String
  data_category: String
  file_type: String
  file_description: String
  file_size: String
  md5sum: String
  file_mapping_level: String
  file_access: String
  acl: String
  authz: String
  file_url: String
  dcf_indexd_guid: String
  checksum_algorithm: String
  checksum_value: String
  participant_list: String

  study: study @relationship(type: "of_clinical_measure_file", direction: IN)
}

type study_personnel {
  id: String
  created: String
  crdc_id: String
  uuid: String
  study_personnel_id: String
  personnel_name: String
  personnel_type: String
  email_address: String
  institution: String
  orcid: String

  study: study @relationship(type: "of_study_personnel", direction: IN)
}

type publication {
  id: String
  created: String
  uuid: String
  publication_id: String
  pubmed_id: String

  study: study @relationship(type: "of_publication", direction: IN)
}

type study_funding {
  id: String
  created: String
  uuid: String
  study_funding_id: String
  funding_agency: String
  grant_id: String
  funding_source_program_name: String

  study: study @relationship(type: "of_study_funding", direction: IN)
}


`;
 
const driver = neo4j.driver(
    "bolt://localhost:7687",
    neo4j.auth.basic("", "")
);
 
const neoSchema = new Neo4jGraphQL({ typeDefs, driver });
 
const app = express();

app.use('/v1/graphiql', graphqlHTTP({
    schema: await neoSchema.getSchema(),
    graphiql: true,
    graphiql: {
    headerEditorEnabled: true,
    defaultQuery: `# Try running a query like:
{
  study {
    study_id
    participant {
      participant_id
    }
  }
}`,
  },
}));

app.listen(9000, () => {
    console.log('🚀 GraphiQL available at http://0.0.0.0:9000/v1/graphiql');
});