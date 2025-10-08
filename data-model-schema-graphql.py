"""
data-model-schema-graphql.py

Generate a GraphQL schema (SDL) from CCDI DCC model YAML files.

What it does:
- Reads ccdi-dcc-model.yml and ccdi-dcc-model-props.yml files
- Emits GraphQL SDL following the Neo4j GraphQL library conventions
- Includes:
  * GraphQL types for each node in the model
  * Properties mapped to appropriate GraphQL field types
  * Relationship fields with @relationship(type:"REL", direction: IN|OUT)
  * Proper handling of key fields and type mappings

Usage:
    python data-model-schema-graphql.py <model-file> <props-file>
    
Example:
    python data-model-schema-graphql.py ccdi-dcc-model.yml ccdi-dcc-model-props.yml > schema.graphql
"""

import yaml
import sys
import re
from typing import Dict, List, Set, Tuple, Any


def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def determine_graphql_type(prop_name: str, prop_def: Dict[str, Any] = None) -> str:
    """Determine GraphQL field type based on property name and definition."""
    
    # If we have property definition, use Type field if available
    if prop_def and 'Type' in prop_def and prop_def['Type'] is not None:
        yaml_type = str(prop_def['Type']).lower()
        type_mapping = {
            'string': 'String',
            'integer': 'Int', 
            'int': 'Int',
            'float': 'Float',
            'number': 'Float',
            'boolean': 'Boolean',
            'date': 'String',  # GraphQL doesn't have native Date type
            'datetime': 'String'
        }
        return type_mapping.get(yaml_type, 'String')
    
    # Common patterns for numeric fields
    numeric_patterns = [
        'age_at_', 'number_of_', '_count', '_size', '_length', 
        'coverage', 'avg_read_length', 'number_of_bp', 'number_of_reads',
        'vaf_numeric', 'test_result_numeric', 'passage_number',
        'magnetic_field_strength', 'repetition_time', 'echo_time',
        'inversion_time', 'flip_angle', 'pixel_spacing', 'slice_thickness',
        'magnification', 'participant_age_', 'year_of_', 'pack_years_',
        'years_', 'cigarettes_per_day', 'alcohol_days_per_week',
        'alcohol_drinks_per_day'
    ]
    
    # ID fields
    if prop_name.endswith('_id') or prop_name == 'id':
        return 'String'
    
    # Check for numeric patterns
    prop_lower = prop_name.lower()
    for pattern in numeric_patterns:
        if pattern in prop_lower:
            return 'Int'
    
    # Boolean patterns
    boolean_patterns = ['indicator', '_flag', 'is_', 'has_']
    for pattern in boolean_patterns:
        if pattern in prop_lower:
            return 'Boolean'
    
    # Default to String
    return 'String'


def build_relationship_map(relationships: Dict[str, Any]) -> Dict[str, List[Tuple[str, str, str]]]:
    """Build a map of relationships for each node type."""
    relationship_map = {}
    
    for rel_name, rel_def in relationships.items():
        if not rel_def or 'Ends' not in rel_def:
            continue
            
        ends = rel_def['Ends']
        for end in ends:
            src_node = end['Src']
            dst_node = end['Dst']
            
            # Add outgoing relationship for source node
            if src_node not in relationship_map:
                relationship_map[src_node] = []
            relationship_map[src_node].append((rel_name, dst_node, "OUT"))
            
            # Add incoming relationship for destination node
            if dst_node not in relationship_map:
                relationship_map[dst_node] = []
            relationship_map[dst_node].append((rel_name, src_node, "IN"))
    
    return relationship_map


def get_property_definition(prop_name: str, prop_definitions: Dict[str, Any]) -> Dict[str, Any]:
    """Get property definition from props file."""
    return prop_definitions.get(prop_name, {})


def generate_node_type(node_name: str, node_def: Dict[str, Any], 
                      relationship_map: Dict[str, List[Tuple[str, str, str]]],
                      prop_definitions: Dict[str, Any]) -> str:
    """Generate GraphQL type definition for a node."""
    
    lines = [f"type {node_name} {{"]
    
    # Add property fields (all optional/nullable)
    if 'Props' in node_def and node_def['Props']:
        for prop_name in node_def['Props']:
            prop_def = get_property_definition(prop_name, prop_definitions)
            field_type = determine_graphql_type(prop_name, prop_def)
            # Make all properties optional (nullable) by not adding the ! suffix
            lines.append(f"  {prop_name}: {field_type}")
    
    # Add relationship fields
    node_relationships = relationship_map.get(node_name, [])
    added_relationships = set()
    added_field_names = set()
    
    # First pass: process OUT relationships first to prioritize them
    for rel_type, target_node, direction in node_relationships:
        if direction != "OUT":
            continue
            
        # Create unique key for this relationship to avoid duplicates
        rel_key = f"{rel_type}_{target_node}_{direction}"
        if rel_key in added_relationships:
            continue
        added_relationships.add(rel_key)
        
        # Generate field name - use plural form for arrays
        field_name = target_node
        if not field_name.endswith('s') and target_node != node_name:
            # Make plural for collections
            if target_node.endswith('y'):
                field_name = target_node[:-1] + 'ies'
            elif target_node.endswith('s'):
                field_name = target_node
            else:
                field_name = target_node + 's'
        
        # Track field names to avoid duplicates
        added_field_names.add(field_name)
        
        # Always use arrays for @relationship directive
        lines.append(f"  {field_name}: [{target_node}!]! @relationship(type: \"{rel_type}\", direction: {direction})")
    
    # Second pass: process IN relationships, but skip if field name already exists
    for rel_type, target_node, direction in node_relationships:
        if direction != "IN":
            continue
            
        # Create unique key for this relationship to avoid duplicates
        rel_key = f"{rel_type}_{target_node}_{direction}"
        if rel_key in added_relationships:
            continue
        added_relationships.add(rel_key)
        
        # Generate field name - use plural form for arrays
        field_name = target_node
        if not field_name.endswith('s') and target_node != node_name:
            # Make plural for collections
            if target_node.endswith('y'):
                field_name = target_node[:-1] + 'ies'
            elif target_node.endswith('s'):
                field_name = target_node
            else:
                field_name = target_node + 's'
        
        # Skip if field name already exists (prioritize OUT relationships)
        if field_name in added_field_names:
            continue
            
        added_field_names.add(field_name)
        
        # Always use arrays for @relationship directive
        lines.append(f"  {field_name}: [{target_node}!]! @relationship(type: \"{rel_type}\", direction: {direction})")
    
    lines.append("}")
    lines.append("")
    
    return "\n".join(lines)


def process_ccdi_model(model_data: Dict[str, Any], props_data: Dict[str, Any]) -> str:
    """Process the CCDI model files and generate GraphQL SDL."""
    output_lines = []
    
    # Add GraphQL schema directive
    output_lines.append("#graphql")
    output_lines.append("")
    
    # Add custom field count type for aggregations
    output_lines.append("# Type for field count results")
    output_lines.append("type FieldCount {")
    output_lines.append("  field: String!")
    output_lines.append("  count: Int!")
    output_lines.append("}")
    output_lines.append("")
    
    # Extract nodes and relationships
    nodes = model_data.get('Nodes', {})
    relationships = model_data.get('Relationships', {})
    prop_definitions = props_data.get('PropDefinitions', {})
    
    # Build relationship map
    relationship_map = build_relationship_map(relationships)
    
    # Generate GraphQL types for each node
    for node_name, node_def in nodes.items():
        type_def = generate_node_type(node_name, node_def, relationship_map, prop_definitions)
        output_lines.append(type_def)
    
    return "\n".join(output_lines)


def main():
    """Main function to read YAML files and generate GraphQL schema."""
    if len(sys.argv) != 3:
        print("Usage: python data-model-schema-graphql.py <model-file> <props-file>")
        print("Example: python data-model-schema-graphql.py ccdi-dcc-model.yml ccdi-dcc-model-props.yml")
        sys.exit(1)
    
    model_file = sys.argv[1]
    props_file = sys.argv[2]
    
    try:
        # Load YAML files
        model_data = load_yaml_file(model_file)
        props_data = load_yaml_file(props_file)
        
        # Generate GraphQL schema
        graphql_schema = process_ccdi_model(model_data, props_data)
        
        # Output to stdout
        print(graphql_schema)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()