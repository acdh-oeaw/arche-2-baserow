# Baserow Project table template
PROJECT = [
    "hasTitle",
    "hasDescription",
    "hasContact",
    "hasMetadataCreator",
    "hasRelatedDiscipline",
    "hasSubject",
    "hasRelatedCollection"
]
TOPCOLLECTION = [
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
COLLECTION = [
    "hasTitle",
    "hasMetadataCreator",
    "hasRelatedDiscipline",
    "hasOwner",
    "hasRightsHolder",
    "hasLicensor",
    "hasDepositor"
]
RESOURCE = [
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
METADATA = [
    "hasTitle",
    "hasMetadataCreator",
    "hasOwner",
    "hasRightsHolder",
    "hasLicensor",
    "hasDepositor",
    "hasLicense",
    "hasCategory"
]
PUBLICATION = [
    "hasTitle"
]
# export object can be extentent with more tables
BASEROW_PROJECT_TABLE = {
    "Project": PROJECT,
    "TopCollection": TOPCOLLECTION,
    "Collection": COLLECTION,
    "Resource": RESOURCE,
    "Metadata": METADATA,
    "Publication": PUBLICATION
}
