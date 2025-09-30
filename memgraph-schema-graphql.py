"""
memgraph-schema-graphql.py (JSON-driven)

Generate a GraphQL schema (SDL) from a *Memgraph schema JSON file*, not from a live DB.

What it does:
- Reads a JSON file describing node labels, their properties, and relationship types.
- Emits GraphQL SDL following the provided template style, including:
  * Custom Query types for sample grouping/counting
  * One GraphQL type per node label (lowercase names to match template)
  * Fields for node properties (default to String unless overridden)
  * Relationship fields with @relationship(type:"REL", direction: IN|OUT)
"""

import json
import sys
from typing import Dict, List, Set, Tuple


def extract_node_label(labels: List[str]) -> str:
    """Extract the primary node label from a list of labels."""
    return labels[0] if labels else "unknown"


def determine_field_type(property_key: str, types: List) -> str:
    """Determine GraphQL field type based on property name and types."""
    # Common numeric fields
    numeric_fields = {
        'count', 'number', 'size', 'length', 'age', 'year', 'coverage',
        'avg_read_length', 'number_of_bp', 'number_of_reads', 'number_of_participants',
        'number_of_samples', 'vaf_numeric', 'test_result_numeric'
    }
    
    # # Check if field name suggests numeric type
    # for numeric_key in numeric_fields:
    #     if numeric_key in property_key.lower():
    #         return "Int"
    
    # Default to String
    return "String"


def build_relationship_map(edges: List[Dict]) -> Dict[str, List[Tuple[str, str, str]]]:
    """Build a map of relationships for each node type."""
    relationships = {}
    
    for edge in edges:
        rel_type = edge.get("type", "")
        start_labels = edge.get("start_node_labels", [])
        end_labels = edge.get("end_node_labels", [])
        
        if not start_labels or not end_labels:
            continue
            
        start_label = extract_node_label(start_labels)
        end_label = extract_node_label(end_labels)
        
        # Add outgoing relationship
        if start_label not in relationships:
            relationships[start_label] = []
        relationships[start_label].append((rel_type, end_label, "OUT"))
        
        # Add incoming relationship
        if end_label not in relationships:
            relationships[end_label] = []
        relationships[end_label].append((rel_type, start_label, "IN"))
    
    return relationships


def generate_custom_queries() -> str:
    """Generate custom Query types for sample grouping/counting."""
    return '''# Custom Query types


'''


def generate_node_type(node_label: str, properties: List[Dict], relationships: List[Tuple[str, str, str]]) -> str:
    """Generate GraphQL type definition for a node."""
    lines = [f"type {node_label} {{"]
    
    # Add property fields
    for prop in properties:
        prop_key = prop.get("key", "")
        prop_types = prop.get("types", [])
        field_type = determine_field_type(prop_key, prop_types)
        lines.append(f"  {prop_key}: {field_type}")
    
    # Add relationship fields
    added_relationships = set()
    for rel_type, target_label, direction in relationships:
        # Skip duplicate relationships
        rel_key = f"{rel_type}_{target_label}_{direction}"
        if rel_key in added_relationships:
            continue
        added_relationships.add(rel_key)
        
        # All relationship fields must be arrays to avoid deprecation warning
        field_name = target_label
        
        # Generate appropriate field name (make plural for arrays)
        if not field_name.endswith('s') and target_label != node_label:
            # Make plural for collections, but be careful about self-references
            if target_label.endswith('y'):
                field_name = target_label[:-1] + 'ies'
            elif target_label.endswith('s'):
                field_name = target_label
            else:
                field_name = target_label + 's'
        
        # Always use arrays for @relationship directive to avoid deprecation warning
        lines.append(f"  {field_name}: [{target_label}!]! @relationship(type: \"{rel_type}\", direction: {direction})")
    
    lines.append("}")
    lines.append("")
    
    return "\n".join(lines)


def process_schema_json(schema_data: Dict) -> str:
    """Process the schema JSON and generate GraphQL SDL."""
    output_lines = []
    
    # Add GraphQL schema directive
    output_lines.append("#graphql")
    output_lines.append("")
    
    # Extract nodes and edges
    nodes = schema_data.get("schema", {}).get("nodes", [])
    edges = schema_data.get("schema", {}).get("edges", [])
    
    # Build relationship map
    relationship_map = build_relationship_map(edges)
    
    # Generate GraphQL types for each node
    for node in nodes:
        labels = node.get("labels", [])
        properties = node.get("properties", [])
        
        if not labels:
            continue
            
        node_label = extract_node_label(labels)
        node_relationships = relationship_map.get(node_label, [])
        
        type_def = generate_node_type(node_label, properties, node_relationships)
        output_lines.append(type_def)
    
    return "\n".join(output_lines)


def main():
    """Main function to read JSON and generate GraphQL schema."""
    if len(sys.argv) != 2:
        print("Usage: python memgraph-schema-graphql.py <schema.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            schema_data = json.load(f)
        
        graphql_schema = process_schema_json(schema_data)
        
        # Output to stdout
        print(graphql_schema)
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{input_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()