import json
from config import (jwt_token, BASEROW_DB_ID)
from utils.baserow import (create_database_table, update_table_field_types, update_table_rows_batch)

# load json files with classes and properites
with open("out/properties_default.json", "r") as f:
    properties = json.load(f)
with open("out/classes_default.json", "r") as f:
    classes = json.load(f)
# create tables
classes = create_database_table(BASEROW_DB_ID, jwt_token, "Classes", classes)
properties = create_database_table(BASEROW_DB_ID, jwt_token, "Properties", properties)
print(classes)
print(properties)
print("Tables created...")

default_fields = [
    {"name": "Notes", "type": "long_text"},
    {"name": "Namespace", "type": "text"},
    {"name": "Label", "type": "text"},
    {"name": "Subclasses_NonLinked", "type": "text"}
]
try:
    class_table = classes["id"]
    properties_table = properties["id"]
except KeyError:
    print("KeyError: tables not found")
    exit()

print("Updating table fields...")
classes_fields = update_table_field_types(
    class_table,
    jwt_token,
    default_fields,
    {"name": "Subclasses", "id": classes["id"]},
    {"name": "Max1", "id": properties["id"]},
    {"name": "Min1", "id": properties["id"]}
)
default_fields = [
    {"name": "Notes", "type": "long_text"},
    {"name": "Namespace", "type": "text"},
    {"name": "Label", "type": "text"},
    {"name": "Subproperties_NonLinked", "type": "text"},
    {"name": "Domain_NonLinked", "type": "text"},
    {"name": "Range_NonLinked", "type": "text"}
]
properties_fields = update_table_field_types(
    properties_table,
    jwt_token,
    default_fields,
    {"name": "Subproperties", "id": properties["id"]},
    {"name": "Domain", "id": classes["id"]},
    {"name": "Range", "id": classes["id"]}
)

# Upading Baserow table rows
with open("out/properties.json", "r") as f:
    properties = json.load(f)
with open("out/classes.json", "r") as f:
    classes = json.load(f)

update_table_rows_batch(properties_table, properties)
update_table_rows_batch(class_table, classes)
