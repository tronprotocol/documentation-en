#!/usr/bin/env python3
"""Generate machine-readable API specs from java-tron source plus docs metadata."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
HTTP_INDEX = DOCS / "api" / "http" / "index.md"
JSON_RPC_INDEX = DOCS / "api" / "json-rpc" / "index.md"
OPENAPI_OUT = DOCS / "api" / "openapi.yaml"
OPENRPC_OUT = DOCS / "api" / "openrpc.json"
HTTP_SPECS_DIR = DOCS / "api" / "specs" / "http"
JSON_RPC_SPECS_DIR = DOCS / "api" / "specs" / "json-rpc"


def find_java_tron_root() -> Path:
    candidates = [
        Path(os.environ["JAVA_TRON_SOURCE"]) if os.environ.get("JAVA_TRON_SOURCE") else None,
        ROOT.parent / "java-tron",
    ]
    for candidate in candidates:
        if candidate and (candidate / "framework/src/main/java").is_dir():
            return candidate
    raise FileNotFoundError(
        "java-tron source tree not found. Set JAVA_TRON_SOURCE to the java-tron checkout."
    )


JAVA_TRON = find_java_tron_root()
JAVA_MAIN = JAVA_TRON / "framework/src/main/java"
JAVA_SOURCE_ROOTS = [path for path in JAVA_TRON.glob("*/src/main/java") if path.is_dir()]
PROTO_ROOTS = [
    JAVA_TRON / "protocol/src/main/protos",
    JAVA_TRON / "framework/src/main/protos",
]


TYPE_MAP = {
    "bool": "boolean",
    "boolean": "boolean",
    "int": "integer",
    "int32": "integer",
    "int64": "integer",
    "long": "integer",
    "number": "number",
    "object": "object",
    "json object": "object",
    "array": "array",
    "string[]": "array",
    "object[]": "array",
}


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")


def clean_inline(value: str) -> str:
    value = value.replace("\\|", "|")
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "")
    value = value.replace("`", "")
    return value.strip()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_java_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return "\n".join(line for line in text.splitlines() if not line.strip().startswith("//"))


def extract_index_entries(index_path: Path, base_dir: Path, link_pattern: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current_section = ""
    for line in read(index_path).splitlines():
        heading = re.match(r"^##\s+(.+)", line)
        if heading:
            current_section = clean_inline(heading.group(1))
            continue
        match = re.match(rf"^\|\s*\[`?({link_pattern})`?\]\(([^)]+)\)\s*\|\s*(.*?)\s*\|", line)
        if not match:
            continue
        name, rel, description = match.groups()
        entries.append(
            {
                "name": clean_inline(name),
                "description": clean_inline(description),
                "section": current_section,
                "doc": str((base_dir / rel).resolve().relative_to(ROOT)),
            }
        )
    return entries


def extract_bullet(markdown: str, label: str) -> str | None:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", markdown, flags=re.MULTILINE)
    return clean_inline(match.group(1)) if match else None


def doc_entry_map(entries: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {entry["name"]: entry for entry in entries}


def servlet_class_files() -> dict[str, Path]:
    files: dict[str, Path] = {}
    for root in JAVA_SOURCE_ROOTS:
        for path in root.rglob("*.java"):
            files.setdefault(path.stem, path)
    return files


CLASS_FILES = servlet_class_files()


def parse_autowired_fields(java_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in re.finditer(r"private\s+([A-Za-z0-9_]+)\s+([A-Za-z0-9_]+)\s*;", java_text):
        class_name, field_name = match.groups()
        fields[field_name] = class_name
    return fields


def extract_servlet_registrations(service_file: Path) -> list[dict[str, str]]:
    java = strip_java_comments(read(service_file))
    fields = parse_autowired_fields(java)
    registrations: list[dict[str, str]] = []
    pattern = re.compile(
        r"\.?\s*addServlet\s*\(\s*new\s+ServletHolder\s*\(\s*([A-Za-z0-9_]+)\s*\)"
        r"\s*,\s*\"([^\"]+)\"\s*\)",
        re.S,
    )
    for match in pattern.finditer(java):
        field_name, path = match.groups()
        servlet_class = fields.get(field_name, field_name)
        registrations.append(
            {
                "path": path,
                "servlet": servlet_class,
                "field": field_name,
                "source": str(service_file.relative_to(JAVA_TRON)),
            }
        )
    return registrations


def source_http_registrations() -> dict[str, dict[str, Any]]:
    fullnode_file = JAVA_MAIN / "org/tron/core/services/http/FullNodeHttpApiService.java"
    solidity_file = (
        JAVA_MAIN
        / "org/tron/core/services/interfaceOnSolidity/http/solidity/HttpApiOnSolidityService.java"
    )
    registrations: dict[str, dict[str, Any]] = {}
    for item in extract_servlet_registrations(fullnode_file):
        if not item["path"].startswith("/wallet/"):
            continue
        registrations[item["path"]] = {**item, "service": "FullNode HTTP"}
    for item in extract_servlet_registrations(solidity_file):
        if not item["path"].startswith("/walletsolidity/"):
            continue
        wallet_path = "/wallet/" + item["path"].removeprefix("/walletsolidity/")
        if wallet_path in registrations:
            registrations[wallet_path]["solidityEndpoint"] = item["path"]
            registrations[wallet_path]["solidityServlet"] = item["servlet"]
    return registrations


def java_class_text(class_name: str) -> str:
    path = CLASS_FILES.get(class_name)
    return read(path) if path else ""


def class_extends(java: str) -> str | None:
    match = re.search(r"\bclass\s+[A-Za-z0-9_]+\s+extends\s+([A-Za-z0-9_]+)", java)
    return match.group(1) if match else None


def java_method_body(java: str, method_name: str) -> str | None:
    match = re.search(rf"\b{method_name}\s*\([^)]*\)\s*(?:throws\s+[^\{{]+)?\{{", java)
    if not match:
        return None
    start = match.end()
    depth = 1
    idx = start
    while idx < len(java) and depth:
        if java[idx] == "{":
            depth += 1
        elif java[idx] == "}":
            depth -= 1
        idx += 1
    return java[start : idx - 1]


def java_class_body(java: str, class_name: str | None = None) -> str:
    if class_name:
        match = re.search(rf"\bclass\s+{re.escape(class_name)}\b[^\{{]*\{{", java)
    else:
        match = re.search(r"\bclass\s+[A-Za-z0-9_]+\b[^\{]*\{", java)
    if not match:
        return java
    start = match.end()
    depth = 1
    idx = start
    while idx < len(java) and depth:
        if java[idx] == "{":
            depth += 1
        elif java[idx] == "}":
            depth -= 1
        idx += 1
    return java[start : idx - 1]


def remove_nested_class_bodies(java_body: str) -> str:
    result = []
    idx = 0
    nested = re.compile(r"\b(?:public|private|protected|static|\s)*class\s+[A-Za-z0-9_]+\b[^\{]*\{")
    while idx < len(java_body):
        match = nested.search(java_body, idx)
        if not match:
            result.append(java_body[idx:])
            break
        result.append(java_body[idx : match.start()])
        depth = 1
        pos = match.end()
        while pos < len(java_body) and depth:
            if java_body[pos] == "{":
                depth += 1
            elif java_body[pos] == "}":
                depth -= 1
            pos += 1
        idx = pos
    return "".join(result)


def servlet_http_methods(class_name: str, seen: set[str] | None = None) -> list[str]:
    seen = seen or set()
    if class_name in seen:
        return ["post"]
    seen.add(class_name)
    java = strip_java_comments(java_class_text(class_name))
    methods = []
    do_get = java_method_body(java, "doGet")
    do_post = java_method_body(java, "doPost")
    if do_get and do_get.strip():
        methods.append("get")
    if do_post and do_post.strip():
        methods.append("post")
    if methods:
        return methods
    parent = class_extends(java)
    return servlet_http_methods(parent, seen) if parent else ["post"]


def method_delegates_to(class_name: str, method_name: str, target_method: str) -> bool:
    java = strip_java_comments(java_class_text(class_name))
    body = java_method_body(java, method_name) or ""
    return bool(
        re.fullmatch(
            rf"\s*{re.escape(target_method)}\s*\(\s*request\s*,\s*response\s*\)\s*;?\s*",
            body,
            re.S,
        )
    )


def imports_by_simple_name(java: str) -> dict[str, str]:
    imports: dict[str, str] = {}
    for match in re.finditer(r"^import\s+([A-Za-z0-9_.]+)\.([A-Za-z0-9_]+);", java, re.M):
        package, simple = match.groups()
        imports[simple] = f"{package}.{simple}"
    return imports


def servlet_request_type(class_name: str, seen: set[str] | None = None) -> tuple[str | None, str | None]:
    seen = seen or set()
    if class_name in seen:
        return None, None
    seen.add(class_name)
    java = strip_java_comments(java_class_text(class_name))
    imports = imports_by_simple_name(java)
    match = re.search(r"\b([A-Za-z0-9_]+)\.Builder\s+[A-Za-z0-9_]+\s*=", java)
    if not match:
        match = re.search(r"\b([A-Za-z0-9_]+)\.newBuilder\s*\(", java)
    if match:
        simple = match.group(1)
        return simple, imports.get(simple)
    if "Util.packTransaction" in java:
        return "Transaction", imports.get("Transaction", "org.tron.protos.Protocol.Transaction")
    parent = class_extends(java)
    return servlet_request_type(parent, seen) if parent else (None, None)


def source_field_schema(name: str) -> dict[str, Any]:
    integer_names = {
        "fee_limit",
        "call_value",
        "consume_user_resource_percent",
        "origin_energy_limit",
        "call_token_value",
        "token_id",
        "timestamp",
        "num",
        "offset",
        "limit",
        "Permission_id",
        "count",
        "burnTrxAmount",
        "brokerage",
        "reward",
    }
    boolean_names = {"visible", "approved", "result"}
    array_names = {"signature", "votes"}
    object_names = {"raw_data", "abi", "new_contract", "transaction"}
    if name in integer_names or name.endswith("_count") or name.endswith("_amount") or name.endswith("Size"):
        return {"type": "integer"}
    if name in boolean_names:
        return {"type": "boolean"}
    if name in array_names:
        return {"type": "array", "items": {"type": "object"}}
    if name in object_names:
        return {"type": "object", "additionalProperties": True}
    return {"type": "string"}


def transaction_json_request_schema(source_shape: str = "transaction-json") -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "raw_data": {"type": "object", "additionalProperties": True},
            "raw_data_hex": {"type": "string"},
            "signature": {"type": "array", "items": {"type": "string"}},
            "visible": {"type": "boolean"},
        },
        "oneOf": [
            {"required": ["raw_data"]},
            {"required": ["raw_data_hex"]},
        ],
        "x-source-shape": source_shape,
    }


def transaction_response_schema(
    source_shape: str = "transaction-json",
    java_response: str = "protocol.Transaction rendered by Util.printCreateTransaction",
) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "txID": {"type": "string"},
            "raw_data": {"type": "object", "additionalProperties": True},
            "raw_data_hex": {"type": "string"},
            "signature": {"type": "array", "items": {"type": "string"}},
            "visible": {"type": "boolean"},
            "contract_address": {"type": "string"},
        },
        "x-java-response": java_response,
        "x-source-shape": source_shape,
    }


def proto_response_schema(message_name: str, description: str | None = None) -> dict[str, Any]:
    schema = proto_message_schema(message_name) or {
        "type": "object",
        "additionalProperties": True,
        "properties": {},
    }
    schema["x-java-response"] = description or f"{message_name} rendered by java-tron JSON printer"
    return schema


def array_response_schema(item_schema: dict[str, Any], description: str) -> dict[str, Any]:
    return {
        "type": "array",
        "items": item_schema,
        "x-java-response": description,
    }


def address_visible_request_schema(source_shape: str = "servlet-effective-input") -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "address": {"type": "string"},
            "visible": {"type": "boolean"},
        },
        "x-source-shape": source_shape,
    }


def transaction_sign_weight_response_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "result": {"type": "object", "additionalProperties": True},
            "approved_list": {"type": "array", "items": {"type": "string"}},
            "current_weight": {"type": "integer"},
            "transaction": transaction_response_schema("nested-transaction-json"),
            "permission": {"type": "object", "additionalProperties": True},
        },
        "x-java-response": "TransactionSignWeight rendered by Util.printTransactionSignWeight",
    }


def transaction_approved_list_response_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "result": {"type": "object", "additionalProperties": True},
            "approved_list": {"type": "array", "items": {"type": "string"}},
            "transaction": transaction_response_schema("nested-transaction-json"),
        },
        "x-java-response": "TransactionApprovedList rendered by Util.printTransactionApprovedList",
    }


def broadcast_response_schema(include_transaction: bool = False) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "result": {"type": "boolean"},
        "code": {"type": "string"},
        "message": {"type": "string"},
        "txid": {"type": "string"},
    }
    if include_transaction:
        properties["transaction"] = {"type": "string"}
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": properties,
        "x-java-response": "Return/GrpcAPI.Return plus transaction id fields",
    }


def return_result_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "result": {"type": "boolean"},
            "code": {"type": "string"},
            "message": {"type": "string"},
        },
    }


def transaction_extention_response_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "transaction": transaction_response_schema("nested-transaction-json"),
            "txid": {"type": "string"},
            "constant_result": {"type": "array", "items": {"type": "string"}},
            "result": return_result_schema(),
            "energy_used": {"type": "integer"},
            "logs": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
            "internal_transactions": {
                "type": "array",
                "items": {"type": "object", "additionalProperties": True},
            },
            "energy_penalty": {"type": "integer"},
        },
        "x-java-response": "TransactionExtention rendered by Util.printTransactionExtention",
    }


def estimate_energy_response_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "result": return_result_schema(),
            "energy_required": {"type": "integer"},
        },
        "x-java-response": "EstimateEnergyMessage rendered by Util.printEstimateEnergyMessage",
    }


UTIL_CONSTANTS = {
    "PERMISSION_ID": "Permission_id",
    "S_VALUE": "value",
    "VISIBLE": "visible",
    "TRANSACTION": "transaction",
    "VALUE": "value",
    "VALUE_FIELD_NAME": "value",
    "CONTRACT_TYPE": "contractType",
    "EXTRA_DATA": "extra_data",
    "OWNER_ADDRESS": "owner_address",
    "CONTRACT_ADDRESS": "contract_address",
    "FUNCTION_SELECTOR": "function_selector",
    "FUNCTION_PARAMETER": "parameter",
    "CALL_DATA": "data",
}


def java_string_constants(java: str) -> dict[str, str]:
    constants = dict(UTIL_CONSTANTS)
    for match in re.finditer(
        r"\b(?:public|private|protected)?\s*(?:static\s+)?final\s+String\s+([A-Za-z0-9_]+)\s*=\s*\"([^\"]+)\"",
        java,
    ):
        name, value = match.groups()
        constants[name] = value
    return constants


def literal_json_fields(java: str) -> list[str]:
    fields: list[str] = []
    patterns = [
        r"\.getString\s*\(\s*\"([A-Za-z0-9_]+)\"\s*\)",
        r"\.getInteger\s*\(\s*\"([A-Za-z0-9_]+)\"\s*\)",
        r"\.getBoolean\s*\(\s*\"([A-Za-z0-9_]+)\"\s*\)",
        r"\.getLong\s*\(\s*\"([A-Za-z0-9_]+)\"\s*\)",
        r"\.getBigDecimal\s*\(\s*\"([A-Za-z0-9_]+)\"\s*\)",
        r"\.containsKey\s*\(\s*\"([A-Za-z0-9_]+)\"\s*\)",
        r"Util\.getJsonLongValue\s*\([^,]+,\s*\"([A-Za-z0-9_]+)\"",
    ]
    for pattern in patterns:
        fields.extend(re.findall(pattern, java))
    for constant, field_name in UTIL_CONSTANTS.items():
        if re.search(rf"\bUtil\.{constant}\b|\b{constant}\b", java):
            fields.append(field_name)
    return list(dict.fromkeys(fields))


def source_post_fields(class_name: str, seen: set[str] | None = None) -> list[str]:
    seen = seen or set()
    if class_name in seen:
        return []
    seen.add(class_name)
    java = strip_java_comments(java_class_text(class_name))
    body = java_method_body(java, "doPost") or ""
    fields = literal_json_fields(body)
    if "Util.getVisiblePost" in body or "params.isVisible()" in body:
        fields.append("visible")
    if "setTransactionPermissionId" in body:
        fields.append("Permission_id")
    if "setTransactionExtraData" in body:
        fields.append("extra_data")
    if "Util.packTransaction" in body:
        fields.extend(["raw_data", "raw_data_hex", "signature"])
    parent = class_extends(java)
    if parent:
        fields.extend(source_post_fields(parent, seen))
    return list(dict.fromkeys(fields))


def post_body_uses_direct_json(class_name: str) -> bool:
    java = strip_java_comments(java_class_text(class_name))
    body = java_method_body(java, "doPost") or ""
    if "JsonFormat.merge" not in body:
        return bool(literal_json_fields(body))
    return False


def servlet_get_parameters(class_name: str, seen: set[str] | None = None) -> list[str]:
    seen = seen or set()
    if class_name in seen:
        return []
    seen.add(class_name)
    java = strip_java_comments(java_class_text(class_name))
    if class_name == "GetBlockServlet":
        return ["id_or_num", "detail", "visible"]
    body = java_method_body(java, "doGet") or ""
    if method_delegates_to(class_name, "doGet", "doPost"):
        body += "\n" + (java_method_body(java, "doPost") or "")
    constants = java_string_constants(java)
    params = []
    for match in re.finditer(r"\.getParameter\s*\(\s*(?:\"([A-Za-z0-9_]+)\"|([A-Za-z0-9_]+))\s*\)", body):
        literal, identifier = match.groups()
        if literal:
            params.append(literal)
        elif identifier in constants:
            params.append(constants[identifier])
    if "Util.getAddress(request)" in body:
        params.append("address")
    suppress_visible = {
        "GetBrokerageServlet",
        "GetRewardServlet",
        "GetTransactionCountByBlockNumServlet",
        "ValidateAddressServlet",
    }
    if "Util.getVisible(request)" in body or (params and class_name not in suppress_visible):
        params.append("visible")
    if params:
        return list(dict.fromkeys(params))
    parent = class_extends(java)
    return servlet_get_parameters(parent, seen) if parent else []


def proto_type_to_schema(proto_type: str, repeated: bool) -> dict[str, Any]:
    mapping = {
        "string": {"type": "string"},
        "bytes": {"type": "string"},
        "bool": {"type": "boolean"},
        "double": {"type": "number"},
        "float": {"type": "number"},
        "int32": {"type": "integer"},
        "int64": {"type": "integer"},
        "uint32": {"type": "integer"},
        "uint64": {"type": "integer"},
        "sint32": {"type": "integer"},
        "sint64": {"type": "integer"},
        "fixed32": {"type": "integer"},
        "fixed64": {"type": "integer"},
    }
    schema = mapping.get(proto_type.lstrip("."), {"type": "object", "additionalProperties": True})
    if repeated:
        return {"type": "array", "items": schema}
    return schema


def remove_proto_nested_blocks(body: str) -> str:
    result = []
    idx = 0
    nested = re.compile(r"^\s*(?:message|enum)\s+[A-Za-z0-9_]+\s*\{", re.M)
    while idx < len(body):
        match = nested.search(body, idx)
        if not match:
            result.append(body[idx:])
            break
        result.append(body[idx : match.start()])
        depth = 1
        pos = match.end()
        while pos < len(body) and depth:
            if body[pos] == "{":
                depth += 1
            elif body[pos] == "}":
                depth -= 1
            pos += 1
        idx = pos
    return "".join(result)


def proto_message_schema(message_name: str | None) -> dict[str, Any] | None:
    if not message_name:
        return None
    for root in PROTO_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.proto"):
            text = read(path)
            match = re.search(rf"\bmessage\s+{re.escape(message_name)}\s*\{{", text)
            if not match:
                continue
            start = match.end()
            depth = 1
            idx = start
            while idx < len(text) and depth:
                if text[idx] == "{":
                    depth += 1
                elif text[idx] == "}":
                    depth -= 1
                idx += 1
            body = remove_proto_nested_blocks(re.sub(r"//.*", "", text[start : idx - 1]))
            properties: dict[str, Any] = {}
            for field in re.finditer(
                r"^\s*(?:(optional|required|repeated)\s+)?([.\w]+)\s+([A-Za-z0-9_]+)\s*=",
                body,
                re.M,
            ):
                label, proto_type, name = field.groups()
                properties[name] = proto_type_to_schema(proto_type, label == "repeated")
            return {
                "type": "object",
                "additionalProperties": True,
                "properties": properties,
                "x-proto-message": message_name,
                "x-proto-file": str(path.relative_to(JAVA_TRON)),
            }
    return None


def java_path_for_fqn(fqn: str) -> Path | None:
    rel = Path(*fqn.split(".")).with_suffix(".java")
    for root in JAVA_SOURCE_ROOTS:
        path = root / rel
        if path.exists():
            return path
    return None


def java_field_schema(java_type: str) -> dict[str, Any]:
    java_type = java_type.strip()
    if java_type.startswith("List<"):
        inner = java_type.removeprefix("List<").removesuffix(">")
        return {"type": "array", "items": java_field_schema(inner)}
    if java_type.startswith("Map<"):
        return {"type": "object", "additionalProperties": True}
    return java_type_schema(java_type)


def java_pojo_schema(fqn: str) -> dict[str, Any] | None:
    path = java_path_for_fqn(fqn)
    if not path:
        return None
    text = remove_nested_class_bodies(java_class_body(strip_java_comments(read(path)), path.stem))
    properties: dict[str, Any] = {}
    for match in re.finditer(
        r"private\s+(?:final\s+)?([A-Za-z0-9_<>, ?\[\]]+)\s+([A-Za-z0-9_]+)\s*(?:=|;)",
        text,
    ):
        java_type, name = match.groups()
        properties[name] = java_field_schema(java_type)
    if not properties:
        return None
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": properties,
        "x-java-response-type": fqn,
        "x-java-response-source": str(path.relative_to(JAVA_TRON)),
    }


def schema_for_printed_proto(body: str, imports: dict[str, str]) -> dict[str, Any] | None:
    printed_vars = re.findall(
        r"(?:JsonFormat\.printToString|Util\.print[A-Za-z0-9_]*)\s*\(\s*([A-Za-z0-9_]+)\b",
        body,
    )
    for var_name in printed_vars:
        declaration = re.search(
            rf"\b([A-Za-z0-9_.]+(?:\.Builder)?)\s+{re.escape(var_name)}\s*(?:=|;)",
            body,
        )
        if not declaration:
            continue
        java_type = declaration.group(1).removesuffix(".Builder")
        simple_type = java_type.split(".")[-1]
        schema = proto_message_schema(simple_type)
        if schema:
            schema["x-java-response-type"] = imports.get(simple_type, java_type)
            schema["x-java-response"] = f"{simple_type} rendered by java-tron JSON printer"
            return schema
    return None


def source_request_schema(class_name: str, request_type: str | None, request_fqn: str | None) -> dict[str, Any]:
    explicit_fields = source_post_fields(class_name)
    java = strip_java_comments(java_class_text(class_name))
    post_body = java_method_body(java, "doPost") or ""
    if class_name in {
        "GetAccountServlet",
        "GetAccountNetServlet",
        "GetAssetIssueByAccountServlet",
    }:
        schema = address_visible_request_schema()
        if request_type:
            schema["x-java-request-type"] = request_fqn or request_type
        return schema
    if class_name == "BroadcastHexServlet":
        return {
            "type": "object",
            "additionalProperties": True,
            "properties": {"transaction": {"type": "string"}},
            "required": ["transaction"],
            "x-source-shape": "servlet-json-fields",
        }
    if "Util.packTransaction" in post_body:
        schema = transaction_json_request_schema()
        if request_type:
            schema["x-java-request-type"] = request_fqn or request_type
        return schema
    if re.search(r"\bdoGet\s*\(\s*request\s*,\s*response\s*\)", post_body):
        explicit_fields.extend(servlet_get_parameters(class_name))
        request_type = request_type if request_type != "Transaction" else request_type
    proto_schema = proto_message_schema(request_type)
    if post_body_uses_direct_json(class_name):
        schema: dict[str, Any] = {
            "type": "object",
            "additionalProperties": True,
            "properties": {name: source_field_schema(name) for name in explicit_fields},
            "x-source-shape": "servlet-json-fields",
        }
    else:
        schema = proto_schema or {
            "type": "object",
            "additionalProperties": True,
            "properties": {},
        }
        schema.setdefault("properties", {})
        for name in explicit_fields:
            schema["properties"].setdefault(name, source_field_schema(name))
        schema["x-source-shape"] = "protobuf-json-plus-servlet-fields" if proto_schema else "servlet-json-fields"
    if request_type:
        schema["x-java-request-type"] = request_fqn or request_type
    return schema


def source_response_schema(class_name: str, seen: set[str] | None = None) -> dict[str, Any]:
    seen = seen or set()
    if class_name in seen:
        return {"type": "object", "additionalProperties": True}
    seen.add(class_name)
    java = strip_java_comments(java_class_text(class_name))
    imports = imports_by_simple_name(java)
    body = java_class_body(java, class_name)
    if class_name == "BroadcastServlet":
        return broadcast_response_schema()
    if class_name == "BroadcastHexServlet":
        return broadcast_response_schema(include_transaction=True)
    if "Util.printCreateTransaction" in body:
        return transaction_response_schema()
    if "Util.printTransactionExtention" in body:
        return transaction_extention_response_schema()
    if "Util.printEstimateEnergyMessage" in body:
        return estimate_energy_response_schema()
    if "Util.printTransactionSignWeight" in body:
        return transaction_sign_weight_response_schema()
    if "Util.printTransactionApprovedList" in body:
        return transaction_approved_list_response_schema()
    if "convertLogAddressToTronAddress(reply" in body:
        return proto_response_schema(
            "TransactionInfo",
            "TransactionInfo rendered through convertLogAddressToTronAddress",
        )
    if "printTransactionInfoList(reply" in body:
        return array_response_schema(
            proto_response_schema(
                "TransactionInfo",
                "TransactionInfo rendered through convertLogAddressToTronAddress",
            ),
            "Array of TransactionInfo rendered by printTransactionInfoList",
        )
    if "Util.printTransaction(reply.getInstance()" in body:
        return transaction_response_schema(
            java_response="protocol.Transaction rendered by Util.printTransaction"
        )
    if "wallet.getChainParameters()" in body:
        return proto_response_schema("ChainParameters")
    json_response = re.search(
        r"\b([A-Za-z0-9_]+)\s+([A-Za-z0-9_]+)\s*=.*?;\s*.*?JSON\.toJSONString\s*\(\s*\2\s*\)",
        body,
        re.S,
    )
    if json_response:
        simple_type = json_response.group(1)
        pojo = java_pojo_schema(imports.get(simple_type, simple_type))
        if pojo:
            return pojo
    proto_print = schema_for_printed_proto(body, imports)
    if proto_print:
        return proto_print
    properties: dict[str, Any] = {}
    for field in re.findall(r'\{\s*\\?"([A-Za-z0-9_]+)\\?"\s*:', body):
        properties[field] = source_field_schema(field)
    for field in re.findall(r"\.put\s*\(\s*\"([A-Za-z0-9_]+)\"", body):
        properties[field] = source_field_schema(field)
    for constant, field_name in UTIL_CONSTANTS.items():
        if re.search(rf"\.put\s*\(\s*(?:Util\.)?{constant}\b", body):
            properties[field_name] = source_field_schema(field_name)
    util_prints = {
        "Util.printCreateTransaction": "protocol.Transaction plus txID/raw_data_hex/visible",
        "Util.printTransactionExtention": "TransactionExtention with expanded transaction",
        "Util.printEstimateEnergyMessage": "EstimateEnergyMessage",
        "Util.printTransactionSignWeight": "TransactionSignWeight",
        "Util.printTransactionApprovedList": "TransactionApprovedList",
        "JsonFormat.printToString": "protobuf JSON",
    }
    schema: dict[str, Any] = {"type": "object", "additionalProperties": True}
    if properties:
        schema["properties"] = properties
    for marker, description in util_prints.items():
        if marker in body:
            schema["x-java-response"] = description
            break
    parent = class_extends(java)
    if not properties and parent:
        return source_response_schema(parent, seen)
    return schema


def documented_http_entries() -> dict[str, dict[str, str]]:
    return doc_entry_map(extract_index_entries(HTTP_INDEX, HTTP_INDEX.parent, r"/wallet/[A-Za-z0-9/_-]+"))


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [clean_inline(part) for part in re.split(r"(?<!\\)\|", stripped)]


def extract_request_rows(markdown: str) -> list[dict[str, str]]:
    marker = re.search(r"^## Request parameters\s*$", markdown, flags=re.MULTILINE)
    if not marker:
        return []
    lines = markdown[marker.end() :].splitlines()
    table: list[str] = []
    in_table = False
    for line in lines:
        if line.startswith("|"):
            table.append(line)
            in_table = True
        elif in_table:
            break
    if len(table) < 3:
        return []
    headers = [h.lower() for h in split_table_row(table[0])]
    rows = []
    for line in table[2:]:
        cells = split_table_row(line)
        if len(cells) < len(headers):
            continue
        item = dict(zip(headers, cells))
        rows.append(item)
    return rows


def schema_for_type(type_text: str) -> dict[str, Any]:
    lowered = type_text.lower().replace(" ", "")
    if lowered.endswith("[]") or "array" in lowered or lowered.startswith("repeated"):
        return {"type": "array", "items": {"type": "object"}}
    if lowered in TYPE_MAP:
        schema_type = TYPE_MAP[lowered]
        if schema_type == "array":
            return {"type": "array", "items": {"type": "object"}}
        return {"type": schema_type}
    if any(token in lowered for token in ["int", "uint", "long"]):
        return {"type": "integer"}
    if any(token in lowered for token in ["bool"]):
        return {"type": "boolean"}
    if any(token in lowered for token in ["object", "map", "json"]):
        return {"type": "object", "additionalProperties": True}
    return {"type": "string"}


def required_value(value: str) -> bool:
    return value.strip().lower() in {"yes", "true", "required"}


def http_request_schema(rows: list[dict[str, str]]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    required: list[str] = []
    for row in rows:
        field = row.get("field", "")
        if not field:
            continue
        name = field.split("/")[0].strip()
        schema = schema_for_type(row.get("type", "string"))
        description = row.get("description")
        if description:
            schema["description"] = description
        properties[name] = schema
        if required_value(row.get("required", "")):
            required.append(name)
    schema: dict[str, Any] = {"type": "object", "additionalProperties": True}
    if properties:
        schema["properties"] = properties
    if required:
        schema["required"] = required
    return schema


def build_openapi() -> dict[str, Any]:
    entries = documented_http_entries()
    source_paths = source_http_registrations()
    missing_in_source = sorted(set(entries) - set(source_paths))
    if missing_in_source:
        raise RuntimeError(
            "Documented HTTP endpoints are not registered in java-tron source: "
            + ", ".join(missing_in_source)
        )
    paths: dict[str, Any] = {}
    for endpoint, entry in entries.items():
        source = source_paths[endpoint]
        markdown = read(ROOT / entry["doc"])
        method_names = servlet_http_methods(source["servlet"])
        request_type, request_fqn = servlet_request_type(source["servlet"])
        request_schema = source_request_schema(source["servlet"], request_type, request_fqn)
        response_schema = source_response_schema(source["servlet"])
        operation_base = {
            "tags": [entry["section"]],
            "summary": entry["description"],
            "description": f"Endpoint registration, HTTP method, servlet, and request type are derived from java-tron source. See `{entry['doc']}` for examples and detailed behavior.",
            "operationId": slug(entry["name"]),
            "externalDocs": {"url": entry["doc"]},
            "responses": {
                "200": {
                    "description": "java-tron response. Most business errors are returned with HTTP 200 and an error object in the body.",
                    "content": {
                        "application/json": {
                            "schema": response_schema,
                        },
                        "text/plain": {"schema": {"type": "string"}},
                    },
                },
                "404": {"description": "Endpoint disabled by node configuration."},
            },
            "x-source-derived": True,
            "x-java-service": source["service"],
            "x-java-servlet": source["servlet"],
            "x-java-source": source["source"],
        }
        if source.get("solidityEndpoint"):
            operation_base["x-solidity-endpoint"] = source["solidityEndpoint"]
            operation_base["x-solidity-servlet"] = source.get("solidityServlet")

        path_item: dict[str, Any] = {}
        for method in method_names:
            operation = json.loads(json.dumps(operation_base))
            operation["operationId"] = f"{slug(entry['name'])}_{method}"
            if method == "get":
                get_params = servlet_get_parameters(source["servlet"])
                operation["parameters"] = [
                    {
                        "name": name,
                        "in": "query",
                        "required": False,
                        "schema": request_schema.get("properties", {}).get(name, source_field_schema(name)),
                        "x-source-derived": True,
                    }
                    for name in get_params
                ]
            else:
                if method_delegates_to(source["servlet"], "doPost", "doGet") or source[
                    "servlet"
                ] == "GetTransactionListFromPendingServlet":
                    post_params = servlet_get_parameters(source["servlet"])
                    operation["parameters"] = [
                        {
                            "name": name,
                            "in": "query",
                            "required": False,
                            "schema": source_field_schema(name),
                            "x-source-derived": True,
                        }
                        for name in post_params
                    ]
                elif request_schema.get("properties") or request_schema.get("x-java-request-type"):
                    operation["requestBody"] = {
                        "required": method == "post",
                        "content": {
                            "application/json": {
                                "schema": request_schema,
                            }
                        },
                    }
            path_item[method] = operation
        paths[endpoint] = path_item
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "java-tron HTTP API",
            "version": "1.0.0",
            "description": "Machine-readable definition generated from java-tron source code, with human-facing metadata linked to the markdown API documentation.",
        },
        "servers": [
            {"url": "https://nile.trongrid.io", "description": "Nile testnet TronGrid"},
            {"url": "http://127.0.0.1:8090", "description": "Local FullNode HTTP API"},
        ],
        "paths": paths,
        "components": {
            "schemas": {
                "JavaTronError": {
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {"Error": {"type": "string"}},
                }
            }
        },
    }


def http_fragment_name(endpoint: str) -> str:
    return endpoint.removeprefix("/wallet/").replace("/", "-") + ".yaml"


def json_rpc_fragment_name(method: str) -> str:
    return method + ".json"


def clean_generated_files(directory: Path, suffix: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for path in directory.glob(f"*{suffix}"):
        path.unlink()


def write_http_fragments(paths: dict[str, Any]) -> None:
    clean_generated_files(HTTP_SPECS_DIR, ".yaml")
    for endpoint, path_item in paths.items():
        out = HTTP_SPECS_DIR / http_fragment_name(endpoint)
        out.write_text(
            "# This file is generated by scripts/generate_api_specs.py. Do not edit by hand.\n"
            + dump_yaml({endpoint: path_item})
            + "\n",
            encoding="utf-8",
        )


def write_json_rpc_fragments(methods: list[dict[str, Any]]) -> None:
    clean_generated_files(JSON_RPC_SPECS_DIR, ".json")
    for method in methods:
        out = JSON_RPC_SPECS_DIR / json_rpc_fragment_name(method["name"])
        out.write_text(json.dumps(method, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def java_type_schema(java_type: str) -> dict[str, Any]:
    cleaned = java_type.strip()
    if cleaned.endswith("[]"):
        return {"type": "array", "items": java_type_schema(cleaned[:-2])}
    if cleaned.startswith("List<"):
        inner = cleaned.removeprefix("List<").removesuffix(">")
        return {"type": "array", "items": java_type_schema(inner)}
    mapping = {
        "String": {"type": "string"},
        "Object": {},
        "Boolean": {"type": "boolean"},
        "boolean": {"type": "boolean"},
        "int": {"type": "integer"},
        "Integer": {"type": "integer"},
        "long": {"type": "integer"},
        "Long": {"type": "integer"},
    }
    return mapping.get(cleaned, {"type": "object", "additionalProperties": True})


def extract_source_jsonrpc_methods() -> dict[str, dict[str, Any]]:
    java = strip_java_comments(read(JAVA_MAIN / "org/tron/core/services/jsonrpc/TronJsonRpc.java"))
    methods: dict[str, dict[str, Any]] = {}
    pattern = re.compile(
        r"@JsonRpcMethod\(\"([^\"]+)\"\)(?P<body>.*?);",
        re.S,
    )
    signature_re = re.compile(
        r"(?:public\s+)?([A-Za-z0-9_<>, ?\[\]]+)\s+([A-Za-z0-9_]+)\s*\((.*?)\)"
    )
    for match in pattern.finditer(java):
        rpc_name = match.group(1)
        body = match.group("body")
        signature = signature_re.search(body)
        if not signature:
            continue
        return_type, java_method, params_text = signature.groups()
        params = []
        if params_text.strip():
            for idx, param in enumerate(re.split(r"\s*,\s*", params_text.strip())):
                pieces = param.rsplit(" ", 1)
                if len(pieces) != 2:
                    continue
                java_type, name = pieces
                params.append(
                    {
                        "name": name,
                        "required": True,
                        "schema": java_type_schema(java_type),
                        "x-java-type": java_type,
                        "x-position": idx,
                    }
                )
        errors = []
        for error in re.finditer(
            r"@JsonRpcError\(exception\s*=\s*([A-Za-z0-9_]+)\.class,\s*code\s*=\s*(-?\d+)",
            body,
        ):
            exception, code = error.groups()
            errors.append({"code": int(code), "message": exception, "x-java-exception": exception})
        methods[rpc_name] = {
            "name": rpc_name,
            "x-java-method": java_method,
            "x-java-source": "framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpc.java",
            "params": params,
            "result": {
                "name": "result",
                "schema": {
                    **java_type_schema(return_type),
                    "x-java-type": return_type.strip(),
                },
            },
            "errors": errors,
        }
    return methods


def openrpc_params(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    params = []
    for row in rows:
        position = row.get("position", "")
        name = position.replace("params[", "param").replace("]", "")
        params.append(
            {
                "name": name,
                "required": required_value(row.get("required", "")),
                "description": row.get("description", ""),
                "schema": schema_for_type(row.get("type", "string")),
            }
        )
    return params


def build_openrpc() -> dict[str, Any]:
    entries = extract_index_entries(JSON_RPC_INDEX, JSON_RPC_INDEX.parent, r"[A-Za-z0-9_]+")
    source_methods = extract_source_jsonrpc_methods()
    missing_in_source = sorted(entry["name"] for entry in entries if entry["name"] not in source_methods)
    if missing_in_source:
        raise RuntimeError(
            "Documented JSON-RPC methods are not declared in java-tron source: "
            + ", ".join(missing_in_source)
        )
    methods = []
    for entry in entries:
        markdown = read(ROOT / entry["doc"])
        ports = extract_bullet(markdown, "Ports")
        source = source_methods[entry["name"]]
        method: dict[str, Any] = {
            "name": entry["name"],
            "tags": [{"name": entry["section"]}],
            "summary": entry["description"],
            "description": f"Method name, Java signature, parameters, return type, and declared errors are derived from java-tron source. See `{entry['doc']}` for examples and detailed behavior.",
            "params": source["params"],
            "result": source["result"],
            "errors": source["errors"],
            "externalDocs": {"url": entry["doc"]},
            "x-source-derived": True,
            "x-java-method": source["x-java-method"],
            "x-java-source": source["x-java-source"],
        }
        if ports:
            method["x-ports"] = ports
        methods.append(method)
    return {
        "openrpc": "1.2.6",
        "info": {
            "title": "java-tron JSON-RPC API",
            "version": "1.0.0",
            "description": "Machine-readable definition generated from java-tron source code, with human-facing metadata linked to the markdown API documentation.",
        },
        "servers": [
            {"name": "Nile testnet", "url": "https://nile.trongrid.io/jsonrpc"},
            {"name": "Local FullNode", "url": "http://127.0.0.1:8545/jsonrpc"},
            {"name": "Local Solidity", "url": "http://127.0.0.1:8555/jsonrpc"},
        ],
        "methods": methods,
    }


def dump_yaml(value: Any, indent: int = 0) -> str:
    space = "  " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            yaml_key = json.dumps(str(key))
            if isinstance(item, (dict, list)):
                lines.append(f"{space}{yaml_key}:")
                lines.append(dump_yaml(item, indent + 1))
            else:
                lines.append(f"{space}{yaml_key}: {json.dumps(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return f"{space}[]"
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{space}-")
                lines.append(dump_yaml(item, indent + 1))
            else:
                lines.append(f"{space}- {json.dumps(item)}")
        return "\n".join(lines)
    return f"{space}{json.dumps(value)}"


def main() -> None:
    openapi = build_openapi()
    openrpc = build_openrpc()
    write_http_fragments(openapi["paths"])
    write_json_rpc_fragments(openrpc["methods"])
    OPENAPI_OUT.write_text(
        "# This file is generated by scripts/generate_api_specs.py. Do not edit by hand.\n"
        + dump_yaml(openapi)
        + "\n",
        encoding="utf-8",
    )
    OPENRPC_OUT.write_text(json.dumps(openrpc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
