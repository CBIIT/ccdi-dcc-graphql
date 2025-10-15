"""data-model-schema-graphql-mdf.py

Generate a GraphQL SDL schema from one or more CCDI DCC MDF (Model Description Format)
YAML files using the bento-mdf / bento-meta libraries already vendored in
`external/ccdi-dcc-model/bento-mdf`.

Compared to `data-model-schema-graphql.py` (which manually parsed two YAML
files), this version delegates model parsing & validation to
`bento_mdf.MDFReader`, then walks the in‑memory `bento_meta.model.Model` to
emit Neo4j GraphQL compatible SDL.

Features:
  * Creates a GraphQL type for every MDF Node
  * Emits properties (nullable) with a best‑effort mapping from MDF value domains
  * Emits relationship (edge) fields with @relationship directive
  * Provides stable deterministic field naming for edges (keeps duplicates)
  * Supports multiple MDF YAML files merged in order

Usage:
	python data-model-schema-graphql-mdf.py <mdf-yaml> [<mdf-yaml> ...] > schema.graphql

Examples:
	python data-model-schema-graphql-mdf.py external/ccdi-dcc-model/model-desc/ccdi-dcc-model.yml > schema.graphql

Notes / Assumptions:
  * We assume the working directory (or PYTHONPATH) allows importing `bento_mdf`.
	If not, we temporarily append the vendored path.
  * All property fields are nullable (GraphQL optional) – adjust if key semantics desired.
  * MDF value domains -> GraphQL:
		string / regexp / value_set  -> String
		integer / int                -> Int
		float / number / double      -> Float
		boolean / bool               -> Boolean
		list (of primitive)          -> [<MappedType>]
		list (of value_set)          -> [String]
	Unrecognized domains default to String.
  * Composite keys are not currently expressed as @id fields; future enhancement could
	surface them with @unique directives if using neo4j-graphql library extensions.
"""

from __future__ import annotations

import sys
import os
import argparse
from typing import Dict, List, Tuple, Set

# Ensure vendored bento_mdf is importable if not installed in environment
VENDORED_PATH = os.path.join(
	os.path.dirname(__file__),
	"external",
	"ccdi-dcc-model",
	"bento-mdf",
	"python",
	"src",
)
if VENDORED_PATH not in sys.path:
	sys.path.insert(0, VENDORED_PATH)

try:
	from bento_mdf import MDFReader  # type: ignore
except Exception as e:  # pragma: no cover - import diagnostic
	print(
		f"Error importing bento_mdf (looked in '{VENDORED_PATH}'): {e}",
		file=sys.stderr,
	)
	sys.exit(1)

# bento-meta model objects
try:
	from bento_meta.model import Model  # type: ignore
	from bento_meta.objects import Node, Edge, Property  # type: ignore
except Exception as e:  # pragma: no cover
	print(f"Error importing bento_meta: {e}", file=sys.stderr)
	sys.exit(1)


def map_value_domain_to_graphql(prop: Property) -> str:
	"""Map an MDF Property value domain (and item domain) to a GraphQL type.

	Returns a GraphQL SDL type string (without nullability modifier).
	Lists return a wrapped list type `[T]` (nullable wrapper, inner element nullable)
	consistent with making everything optional.
	"""

	domain = (prop.value_domain or "").lower()
	item = (getattr(prop, "item_domain", None) or "").lower()

	scalar_map = {
		"string": "String",
		"regexp": "String",
		"value_set": "String",  # represent enumerated values as plain String for now
		"integer": "Int",
		"int": "Int",
		"float": "Float",
		"number": "Float",
		"double": "Float",
		"boolean": "Boolean",
		"bool": "Boolean",
	}

	if domain == "list":
		# Determine element type from item domain
		elem = scalar_map.get(item, "String") if item else "String"
		return f"[{elem}]"

	return scalar_map.get(domain, "String")


def singularize(name: str) -> str:
	"""Very lightweight singularization similar to original script."""
	if name.endswith("ies"):
		return name[:-3] + "y"
	if name.endswith("ses"):
		return name[:-2]
	if name.endswith("s") and not name.endswith("ss"):
		return name[:-1]
	return name


def build_relationship_fields(model: Model, node: Node) -> List[Tuple[str, str, str]]:
	"""Return list of (field_name, target_node_name, direction) for a node.

	We look at all edges where node is src (OUT) or dst (IN) and build
	deterministic field names similar to the previous script.
	"""
	rels: List[Tuple[str, str, str]] = []
	used: Dict[str, int] = {}

	# OUT edges: node is source
	for edge in model.edges.values():
		if edge.src.handle == node.handle:
			target = edge.dst.handle
			base = f"{singularize(target).lower()}_{edge.handle.lower()}"
			idx = used.get(base, 0)
			used[base] = idx + 1
			fname = base if idx == 0 else f"{base}_{idx+1}"
			rels.append((fname, target, "OUT"))

	# IN edges: node is destination
	for edge in model.edges.values():
		if edge.dst.handle == node.handle:
			source = edge.src.handle
			base = f"{singularize(node.handle).lower()}_{edge.handle.lower()}"
			idx = used.get(base, 0)
			used[base] = idx + 1
			fname = base if idx == 0 else f"{base}_{idx+1}"
			rels.append((fname, source, "IN"))

	# Order OUT before IN
	rels.sort(key=lambda r: (0 if r[2] == "OUT" else 1, r[0]))
	return rels


def generate_type_sdl(model: Model, node: Node) -> str:
	"""Generate SDL for a single node (GraphQL type)."""
	lines: List[str] = [f"type {node.handle} {{"]

	# Properties (nullable)
	# node.props is a dict of Property keyed by handle
	for pname, prop in sorted(node.props.items()):
		gql_type = map_value_domain_to_graphql(prop)
		# Remove any illegal chars for GraphQL field names: keep alnum and underscore
		safe_name = "".join(ch if ch.isalnum() or ch == '_' else '_' for ch in pname)
		lines.append(f"  {safe_name}: {gql_type}")

	# Relationships
	for field_name, target, direction in build_relationship_fields(model, node):
		lines.append(
			f"  {field_name}: [{target}!]! @relationship(type: \"{_relationship_type_name(model, field_name, target, direction)}\", direction: {direction})"
		)

	lines.append("}")
	return "\n".join(lines)


def _relationship_type_name(model: Model, field_name: str, target: str, direction: str) -> str:
	"""Return the underlying relationship (edge) type from the Model.

	We map field_name back to an edge handle by re-deriving candidate names.
	Since we embed edge.handle verbatim when constructing field names we can
	just search for an edge that matches source/destination & target.
	"""
	# Fallback: return uppercase of segment after last underscore (edge handle heuristics)
	# but prefer exact edge handle match via scanning edges.
	parts = field_name.split("_")
	guess = parts[-1]
	for edge in model.edges.values():
		# Edge handle is what we built into field_name originally
		if edge.handle.lower() == guess:
			return edge.handle.upper()
	return guess.upper()


def generate_schema(model: Model) -> str:
	"""Generate full SDL for a Model."""
	out: List[str] = ["#graphql", ""]
	out.append("# Auto-generated from MDF using bento_mdf")
	out.append("# Model Handle: {}".format(model.handle))
	out.append("")
	# Optional helper type (mirroring original script)
	out.append("type FieldCount {")
	out.append("  field: String!")
	out.append("  count: Int!")
	out.append("}")
	out.append("")

	# Generate each node type
	for node in sorted(model.nodes.values(), key=lambda n: n.handle):
		out.append(generate_type_sdl(model, node))
		out.append("")
	return "\n".join(out).rstrip() + "\n"


def parse_args(argv: List[str]) -> argparse.Namespace:
	p = argparse.ArgumentParser(description="Generate GraphQL SDL from MDF YAML files")
	p.add_argument(
		"yaml_files",
		nargs="+",
		help="One or more MDF YAML files (merge order left->right)",
	)
	p.add_argument(
		"--debug",
		action="store_true",
		help="Enable debug output (stack traces, intermediate diagnostics)",
	)
	return p.parse_args(argv)


def load_model(yaml_files: List[str]) -> Model:
	try:
		reader = MDFReader(*yaml_files, raise_error=True)
		return reader.model
	except KeyError as ke:  # Common when props file omitted or order wrong
		raise RuntimeError(
			f"KeyError while loading MDF model: {ke}. Hint: Ensure you pass both the core model YAML and the props YAML, e.g.\n"
			"  python data-model-schema-graphql-mdf.py external/ccdi-dcc-model/model-desc/ccdi-dcc-model.yml external/ccdi-dcc-model/model-desc/ccdi-dcc-model-props.yml\n"
			"and that they appear in left-to-right merge order (model first, then props)."
		) from ke
	except Exception:
		# Re-raise so caller can decide how much detail to show based on --debug
		raise


def main(argv: List[str] | None = None) -> int:
	ns = parse_args(argv or sys.argv[1:])
	try:
		model = load_model(ns.yaml_files)
	except Exception as e:  # pragma: no cover - runtime feedback
		if ns.debug:
			import traceback
			print("[DEBUG] Exception while loading model:", file=sys.stderr)
			traceback.print_exc()
		print(f"Error loading MDF model: {e}", file=sys.stderr)
		return 1
	try:
		sdl = generate_schema(model)
		sys.stdout.write(sdl)
	except Exception as e:  # pragma: no cover
		if ns.debug:
			import traceback
			print("[DEBUG] Exception while generating schema:", file=sys.stderr)
			traceback.print_exc()
		print(f"Error generating schema: {e}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":  # pragma: no cover
	raise SystemExit(main())

