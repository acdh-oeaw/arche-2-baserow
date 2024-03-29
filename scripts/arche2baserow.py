import json
from config import (jwt_token, BASEROW_DB_ID)
from utils.baserow import (create_database_table, update_table_field_types, update_table_rows_batch, delete_table_field)

vocabs_files = {
    "vocabs_categories": "out/archecategory.json",
    "vocabs_access_restriction": "out/archeaccessrestrictions.json",
    "vocabs_licenses": "out/archelicenses.json",
    "vocabs_lifecyclestatus": "out/archelifecyclestatus.json",
    "vocabs_oaisets": "out/archeoaisets.json",
    "vocabs_oefosdisciplines": "out/oefos_disciplines.json",
    "vocabs_languagecodes": "out/ISO-639-3-languages.json"
}

merged_table = []
for file in vocabs_files.values():
    filename = file.split("/")[-1].split(".")[0]
    # load json files with classes
    with open(file, "r") as f:
        table = json.load(f)
    merged_table.extend(table)

with open("out/Vocabs.json", "w") as f:
    json.dump(merged_table, f, indent=2)

# create table
vocabs = create_database_table(BASEROW_DB_ID, jwt_token, "Vocabs", merged_table)
print("Vocabs uploaded to Baserow...")

# load json files with classes and properites
with open("out/properties_default.json", "r") as f:
    properties_table = json.load(f)
with open("out/classes_default.json", "r") as f:
    classes_table = json.load(f)

# create tables
classes = create_database_table(BASEROW_DB_ID, jwt_token, "Classes", classes_table)
properties = create_database_table(BASEROW_DB_ID, jwt_token, "Properties", properties_table)
persons = create_database_table(BASEROW_DB_ID, jwt_token, "Persons")
places = create_database_table(BASEROW_DB_ID, jwt_token, "Places")
organizations = create_database_table(BASEROW_DB_ID, jwt_token, "Organizations")
project = create_database_table(BASEROW_DB_ID, jwt_token, "Project", "Subject_uri")
print(classes)
print(properties)
print(persons)
print(places)
print(organizations)
print(project)
print("Tables created...")

try:
    class_table = classes["id"]
    properties_table = properties["id"]
except KeyError:
    print("KeyError: tables not found")
    exit()

print("Updating table fields...")

# class table fields
default_fields = [
    {"name": "Notes", "type": "long_text"},
    {"name": "Namespace", "type": "text"},
    {"name": "Label", "type": "text"},
    {"name": "Subclasses", "type": "link_row", "link_row_table_id": classes["id"], "has_related_field": False},
    {"name": "Subclasses_NonLinked", "type": "text"},
    {"name": "Max1", "type": "link_row", "link_row_table_id": properties["id"], "has_related_field": False},
    {"name": "Min1", "type": "link_row", "link_row_table_id": properties["id"], "has_related_field": False}
]
classes_fields = update_table_field_types(
    class_table,
    jwt_token,
    default_fields
)

# properties table fields
default_fields = [
    {"name": "Notes", "type": "long_text"},
    {"name": "Namespace", "type": "text"},
    {"name": "Label", "type": "text"},
    {"name": "Subproperties", "type": "link_row", "link_row_table_id": properties["id"], "has_related_field": False},
    {"name": "Subproperties_NonLinked", "type": "text"},
    {"name": "Domain", "type": "link_row", "link_row_table_id": classes["id"], "has_related_field": False},
    {"name": "Domain_NonLinked", "type": "text"},
    {"name": "Range", "type": "link_row", "link_row_table_id": classes["id"], "has_related_field": False},
    {"name": "Range_NonLinked", "type": "text"},
]
properties_fields = update_table_field_types(
    properties_table,
    jwt_token,
    default_fields
)

# persons table fields
default_fields = [
    {"name": "Name", "type": "text"},
    {"name": "Subject_uri", "type": "text"},
    {"name": "Predicate_uri", "type": "link_row", "link_row_table_id": properties["id"], "has_related_field": False},
    {"name": "Literal", "type": "text"},
    {
        "name": "Object_uri_organizations",
        "type": "link_row",
        "link_row_table_id": organizations["id"],
        "has_related_field": False
    },
    {"name": "Language", "type": "text"}
]
persons_fields = update_table_field_types(
    persons["id"],
    jwt_token,
    default_fields
)
delete_table_field(persons["id"], jwt_token, ["Notes", "Active"])

# places table fields
default_fields = [
    {"name": "Name", "type": "text"},
    {"name": "Subject_uri", "type": "text"},
    {"name": "Predicate_uri", "type": "link_row", "link_row_table_id": properties["id"], "has_related_field": False},
    {"name": "Literal", "type": "text"},
    {"name": "Language", "type": "text"}
]
places_fields = update_table_field_types(
    places["id"],
    jwt_token,
    default_fields
)
delete_table_field(places["id"], jwt_token, ["Notes", "Active"])

# organizations table fields
default_fields = [
    {"name": "Name", "type": "text"},
    {"name": "Subject_uri", "type": "text"},
    {"name": "Predicate_uri", "type": "link_row", "link_row_table_id": properties["id"], "has_related_field": False},
    {"name": "Literal", "type": "text"},
    {"name": "Language", "type": "text"}
]
organizations_fields = update_table_field_types(
    organizations["id"],
    jwt_token,
    default_fields
)
delete_table_field(organizations["id"], jwt_token, ["Notes", "Active"])

# project table fields
default_fields = [
    {"name": "Subject_uri", "type": "text"},
    {"name": "Class", "type": "link_row", "link_row_table_id": classes["id"], "has_related_field": False},
    {"name": "Predicate_uri", "type": "link_row", "link_row_table_id": properties["id"], "has_related_field": False},
    {"name": "Object_uri_persons", "type": "link_row", "link_row_table_id": persons["id"], "has_related_field": False},
    {"name": "Object_uri_places", "type": "link_row", "link_row_table_id": places["id"], "has_related_field": False},
    {
        "name": "Object_uri_organizations",
        "type": "link_row",
        "link_row_table_id": organizations["id"],
        "has_related_field": False
    },
    {
        "name": "Object_uri_resource",
        "type": "link_row",
        "link_row_table_id": project["id"],
        "has_related_field": False
    },
    {
        "name": "Object_uri_vocabs",
        "type": "link_row",
        "link_row_table_id": vocabs["id"],
        "has_related_field": False
    },
    {"name": "Literal", "type": "text"},
    {"name": "Language", "type": "text"},
    {"name": "Date", "type": "date"},
    {"name": "Number", "type": "number"},
    {"name": "Inherit", "type": "link_row", "link_row_table_id": classes["id"], "has_related_field": False}
]
project_fields = update_table_field_types(
    project["id"],
    jwt_token,
    default_fields
)
delete_table_field(project["id"], jwt_token, ["Notes", "Active"])

# Upading Baserow table rows
with open("out/properties.json", "r") as f:
    properties = json.load(f)
with open("out/classes.json", "r") as f:
    classes = json.load(f)

update_table_rows_batch(properties_table, properties)
update_table_rows_batch(class_table, classes)

project_properties = [
    "hasTitle",
    "hasDescription",
    "hasContact",
    "hasMetadataCreator",
    "hasRelatedDiscipline",
    "hasSubject",
    "hasRelatedCollection"
]
topCol_properties = [
    "hasTitle",
    "hasDescription",
    "hasContact",
    "hasMetadataCreator",
    "hasRelatedDiscipline",
    "hasSubject",
    "hasOwner",
    "hasRightsHolder",
    "hasLicensor",
    "hasDepositor",
    "hasCurator"
]
collection_properties = [
    "hasTitle",
    "hasMetadataCreator",
    "hasRelatedDiscipline",
    "hasOwner",
    "hasRightsHolder",
    "hasLicensor",
    "hasDepositor"
]
resource_properties = [
    "hasTitle",
    "hasMetadataCreator",
    "hasRelatedDiscipline",
    "hasOwner",
    "hasRightsHolder",
    "hasLicensor",
    "hasDepositor",
    "hasLicense",
    "hasCategory",
    "isPartOf"
]
metadata_properties = [
    "hasTitle",
    "hasMetadataCreator",
    "hasOwner",
    "hasRightsHolder",
    "hasLicensor",
    "hasDepositor",
    "hasLicense",
    "hasCategory"
]
publication_properties = [
    "hasTitle"
]
# Create Initial Project Template
ids = 1
project_template = []
for prop in project_properties:
    project_template.append({
        "id": ids,
        "order": f"{ ids }.00000000000000000000",
        "Subject_uri": "your-project",
        "Class": [x["id"] for x in classes if x["Name"] == "Project" and
                  x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Predicate_uri": [x["id"] for x in properties if x["Name"] == prop and
                          x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Object_uri_persons": [],
        "Object_uri_places": [],
        "Object_uri_organizations": [],
        "Object_uri_resource": [],
        "Literal": None,
        "Language": None,
        "Date": None,
        "Number": None,
        "Inherit": []
    })
    ids += 1
topCol_template = []
for prop in topCol_properties:
    topCol_template.append({
        "id": ids,
        "order": f"{ ids }.00000000000000000000",
        "Subject_uri": "your-top-collection",
        "Class": [x["id"] for x in classes if x["Name"] == "TopCollection" and
                  x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Predicate_uri": [x["id"] for x in properties if x["Name"] == prop and
                          x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Object_uri_persons": [],
        "Object_uri_places": [],
        "Object_uri_organizations": [],
        "Object_uri_resource": [],
        "Literal": None,
        "Language": None,
        "Date": None,
        "Number": None,
        "Inherit": []
    })
    ids += 1
collection_template = []
for prop in collection_properties:
    collection_template.append({
        "id": ids,
        "order": f"{ ids }.00000000000000000000",
        "Subject_uri": "your-collection",
        "Class": [x["id"] for x in classes if x["Name"] == "Collection" and
                  x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Predicate_uri": [x["id"] for x in properties if x["Name"] == prop and
                          x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Object_uri_persons": [],
        "Object_uri_places": [],
        "Object_uri_organizations": [],
        "Object_uri_resource": [],
        "Literal": None,
        "Language": None,
        "Date": None,
        "Number": None,
        "Inherit": []
    })
    ids += 1
resource_template = []
for prop in resource_properties:
    resource_template.append({
        "id": ids,
        "order": f"{ ids }.00000000000000000000",
        "Subject_uri": "your-resource",
        "Class": [x["id"] for x in classes if x["Name"] == "Resource" and
                  x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Predicate_uri": [x["id"] for x in properties if x["Name"] == prop and
                          x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Object_uri_persons": [],
        "Object_uri_places": [],
        "Object_uri_organizations": [],
        "Object_uri_resource": [],
        "Literal": None,
        "Language": None,
        "Date": None,
        "Number": None,
        "Inherit": []
    })
    ids += 1
metadata_template = []
for prop in metadata_properties:
    metadata_template.append({
        "id": ids,
        "order": f"{ ids }.00000000000000000000",
        "Subject_uri": "your-metadata",
        "Class": [x["id"] for x in classes if x["Name"] == "Metadata" and
                  x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Predicate_uri": [x["id"] for x in properties if x["Name"] == prop and
                          x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Object_uri_persons": [],
        "Object_uri_places": [],
        "Object_uri_organizations": [],
        "Object_uri_resource": [],
        "Literal": None,
        "Language": None,
        "Date": None,
        "Number": None,
        "Inherit": []
    })
    ids += 1
publication_template = []
for prop in publication_properties:
    metadata_template.append({
        "id": ids,
        "order": f"{ ids }.00000000000000000000",
        "Subject_uri": "your-publication",
        "Class": [x["id"] for x in classes if x["Name"] == "Publication" and
                  x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Predicate_uri": [x["id"] for x in properties if x["Name"] == prop and
                          x["Namespace"] == "https://vocabs.acdh.oeaw.ac.at/schema#"],
        "Object_uri_persons": [],
        "Object_uri_places": [],
        "Object_uri_organizations": [],
        "Object_uri_resource": [],
        "Literal": None,
        "Language": None,
        "Date": None,
        "Number": None,
        "Inherit": []
    })
    ids += 1

print(f"Updating {ids} Project table rows...")
update_table_rows_batch(project["id"], project_template)
update_table_rows_batch(project["id"], topCol_template)
update_table_rows_batch(project["id"], collection_template)
update_table_rows_batch(project["id"], resource_template)
update_table_rows_batch(project["id"], metadata_template)
update_table_rows_batch(project["id"], publication_template)
print("Done...")
