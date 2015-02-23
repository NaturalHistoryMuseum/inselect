"""Darwin Core terms
"""
DWC_TERMS = [
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "occurrenceID",
        "Label": "Occurrence ID",
        "URI": "http://rs.tdwg.org/dwc/terms/occurrenceID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "organismID",
        "Label": "Organism ID",
        "URI": "http://rs.tdwg.org/dwc/terms/organismID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "materialSampleID",
        "Label": "Material sample ID",
        "URI": "http://rs.tdwg.org/dwc/terms/materialSampleID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "eventID",
        "Label": "Event ID",
        "URI": "http://rs.tdwg.org/dwc/terms/eventID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "locationID",
        "Label": "Location ID",
        "URI": "http://rs.tdwg.org/dwc/terms/locationID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "geologicalContextID",
        "Label": "Geological context ID",
        "URI": "http://rs.tdwg.org/dwc/terms/geologicalContextID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "identificationID",
        "Label": "Identification ID",
        "URI": "http://rs.tdwg.org/dwc/terms/identificationID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "IdentifierTerms",
        "Group label": "Identifier",
        "Name": "taxonID",
        "Label": "Taxon ID",
        "URI": "http://rs.tdwg.org/dwc/terms/taxonID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "type",
        "Label": "Type",
        "URI": "http://purl.org/dc/terms/type"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "modified",
        "Label": "Modified",
        "URI": "http://purl.org/dc/terms/modified"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "language",
        "Label": "Language",
        "URI": "http://purl.org/dc/terms/language"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "license",
        "Label": "License",
        "URI": "http://purl.org/dc/terms/license"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "rightsHolder",
        "Label": "Rights holder",
        "URI": "http://purl.org/dc/terms/rightsHolder"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "accessRights",
        "Label": "Access rights",
        "URI": "http://purl.org/dc/terms/accessRights"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "bibliographicCitation",
        "Label": "Bibliographic citation",
        "URI": "http://purl.org/dc/terms/bibliographicCitation"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "references",
        "Label": "References",
        "URI": "http://purl.org/dc/terms/references"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "institutionID",
        "Label": "Institution ID",
        "URI": "http://rs.tdwg.org/dwc/terms/institutionID",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "collectionID",
        "Label": "Collection ID",
        "URI": "http://rs.tdwg.org/dwc/terms/collectionID",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "datasetID",
        "Label": "Dataset ID",
        "URI": "http://rs.tdwg.org/dwc/terms/datasetID",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "institutionCode",
        "Label": "Institution code",
        "URI": "http://rs.tdwg.org/dwc/terms/institutionCode",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "collectionCode",
        "Label": "Collection code",
        "URI": "http://rs.tdwg.org/dwc/terms/collectionCode",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "datasetName",
        "Label": "Dataset name",
        "URI": "http://rs.tdwg.org/dwc/terms/datasetName",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "ownerInstitutionCode",
        "Label": "Owner institution code",
        "URI": "http://rs.tdwg.org/dwc/terms/ownerInstitutionCode",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "basisOfRecord",
        "Label": "Basis of record",
        "URI": "http://rs.tdwg.org/dwc/terms/basisOfRecord",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "informationWithheld",
        "Label": "Information withheld",
        "URI": "http://rs.tdwg.org/dwc/terms/informationWithheld",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "dataGeneralizations",
        "Label": "Data generalizations",
        "URI": "http://rs.tdwg.org/dwc/terms/dataGeneralizations",
        "Type": "string"
    },
    {
        "Group": "RecordLevelTerms",
        "Group label": "Record level",
        "Name": "dynamicProperties",
        "Label": "Dynamic properties",
        "URI": "http://rs.tdwg.org/dwc/terms/dynamicProperties",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "catalogNumber",
        "Label": "Catalog number",
        "URI": "http://rs.tdwg.org/dwc/terms/catalogNumber",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "recordNumber",
        "Label": "Record number",
        "URI": "http://rs.tdwg.org/dwc/terms/recordNumber",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "recordedBy",
        "Label": "Recorded by",
        "URI": "http://rs.tdwg.org/dwc/terms/recordedBy",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "individualCount",
        "Label": "Individual count",
        "URI": "http://rs.tdwg.org/dwc/terms/individualCount",
        "Type": "positiveInteger"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "sex",
        "Label": "Sex",
        "URI": "http://rs.tdwg.org/dwc/terms/sex",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "lifeStage",
        "Label": "Life stage",
        "URI": "http://rs.tdwg.org/dwc/terms/lifeStage",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "reproductiveCondition",
        "Label": "Reproductive condition",
        "URI": "http://rs.tdwg.org/dwc/terms/reproductiveCondition",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "behavior",
        "Label": "Behavior",
        "URI": "http://rs.tdwg.org/dwc/terms/behavior",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "establishmentMeans",
        "Label": "Establishment means",
        "URI": "http://rs.tdwg.org/dwc/terms/establishmentMeans",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "occurrenceStatus",
        "Label": "Occurrence status",
        "URI": "http://rs.tdwg.org/dwc/terms/occurrenceStatus",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "preparations",
        "Label": "Preparations",
        "URI": "http://rs.tdwg.org/dwc/terms/preparations",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "disposition",
        "Label": "Disposition",
        "URI": "http://rs.tdwg.org/dwc/terms/disposition",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "associatedMedia",
        "Label": "Associated media",
        "URI": "http://rs.tdwg.org/dwc/terms/associatedMedia",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "associatedReferences",
        "Label": "Associated references",
        "URI": "http://rs.tdwg.org/dwc/terms/associatedReferences",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "associatedSequences",
        "Label": "Associated sequences",
        "URI": "http://rs.tdwg.org/dwc/terms/associatedSequences",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "associatedTaxa",
        "Label": "Associated taxa",
        "URI": "http://rs.tdwg.org/dwc/terms/associatedTaxa",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "otherCatalogNumbers",
        "Label": "Other catalog numbers",
        "URI": "http://rs.tdwg.org/dwc/terms/otherCatalogNumbers",
        "Type": "string"
    },
    {
        "Group": "OccurrenceTerms",
        "Group label": "Occurrence",
        "Name": "occurrenceRemarks",
        "Label": "Occurrence remarks",
        "URI": "http://rs.tdwg.org/dwc/terms/occurrenceRemarks",
        "Type": "string"
    },
    {
        "Group": "OrganismTerms",
        "Group label": "Organism",
        "Name": "organismName",
        "Label": "Organism name",
        "URI": "http://rs.tdwg.org/dwc/terms/organismName",
        "Type": "string"
    },
    {
        "Group": "OrganismTerms",
        "Group label": "Organism",
        "Name": "organismScope",
        "Label": "Organism scope",
        "URI": "http://rs.tdwg.org/dwc/terms/organismScope",
        "Type": "string"
    },
    {
        "Group": "OrganismTerms",
        "Group label": "Organism",
        "Name": "associatedOccurrences",
        "Label": "Associated occurrences",
        "URI": "http://rs.tdwg.org/dwc/terms/associatedOccurrences",
        "Type": "string"
    },
    {
        "Group": "OrganismTerms",
        "Group label": "Organism",
        "Name": "associatedOrganisms",
        "Label": "Associated organisms",
        "URI": "http://rs.tdwg.org/dwc/terms/associatedOrganisms",
        "Type": "string"
    },
    {
        "Group": "OrganismTerms",
        "Group label": "Organism",
        "Name": "previousIdentifications",
        "Label": "Previous identifications",
        "URI": "http://rs.tdwg.org/dwc/terms/previousIdentifications",
        "Type": "string"
    },
    {
        "Group": "OrganismTerms",
        "Group label": "Organism",
        "Name": "organismRemarks",
        "Label": "Organism remarks",
        "URI": "http://rs.tdwg.org/dwc/terms/organismRemarks",
        "Type": "string"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "eventDate",
        "Label": "Event date",
        "URI": "http://rs.tdwg.org/dwc/terms/eventDate",
        "Type": "dateTimeISO"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "eventTime",
        "Label": "Event time",
        "URI": "http://rs.tdwg.org/dwc/terms/eventTime",
        "Type": "time"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "startDayOfYear",
        "Label": "Start day of year",
        "URI": "http://rs.tdwg.org/dwc/terms/startDayOfYear",
        "Type": "dayOfYearDataType"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "endDayOfYear",
        "Label": "End day of year",
        "URI": "http://rs.tdwg.org/dwc/terms/endDayOfYear",
        "Type": "dayOfYearDataType"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "year",
        "Label": "Year",
        "URI": "http://rs.tdwg.org/dwc/terms/year",
        "Type": "gYear"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "month",
        "Label": "Month",
        "URI": "http://rs.tdwg.org/dwc/terms/month",
        "Type": "gMonth"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "day",
        "Label": "Day",
        "URI": "http://rs.tdwg.org/dwc/terms/day",
        "Type": "gDay"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "verbatimEventDate",
        "Label": "Verbatim event date",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimEventDate",
        "Type": "string"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "habitat",
        "Label": "Habitat",
        "URI": "http://rs.tdwg.org/dwc/terms/habitat",
        "Type": "string"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "fieldNumber",
        "Label": "Field number",
        "URI": "http://rs.tdwg.org/dwc/terms/fieldNumber",
        "Type": "string"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "samplingProtocol",
        "Label": "Sampling protocol",
        "URI": "http://rs.tdwg.org/dwc/terms/samplingProtocol",
        "Type": "string"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "samplingEffort",
        "Label": "Sampling effort",
        "URI": "http://rs.tdwg.org/dwc/terms/samplingEffort",
        "Type": "string"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "fieldNotes",
        "Label": "Field notes",
        "URI": "http://rs.tdwg.org/dwc/terms/fieldNotes",
        "Type": "string"
    },
    {
        "Group": "EventTerms",
        "Group label": "Event",
        "Name": "eventRemarks",
        "Label": "Event remarks",
        "URI": "http://rs.tdwg.org/dwc/terms/eventRemarks",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "higherGeographyID",
        "Label": "Higher geography ID",
        "URI": "http://rs.tdwg.org/dwc/terms/higherGeographyID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "higherGeography",
        "Label": "Higher geography",
        "URI": "http://rs.tdwg.org/dwc/terms/higherGeography",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "continent",
        "Label": "Continent",
        "URI": "http://rs.tdwg.org/dwc/terms/continent",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "waterbody",
        "Label": "Waterbody",
        "URI": "http://rs.tdwg.org/dwc/terms/waterbody",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "islandGroup",
        "Label": "Island group",
        "URI": "http://rs.tdwg.org/dwc/terms/islandGroup",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "island",
        "Label": "Island",
        "URI": "http://rs.tdwg.org/dwc/terms/island",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "country",
        "Label": "Country",
        "URI": "http://rs.tdwg.org/dwc/terms/country",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "countryCode",
        "Label": "Country code",
        "URI": "http://rs.tdwg.org/dwc/terms/countryCode",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "stateProvince",
        "Label": "State province",
        "URI": "http://rs.tdwg.org/dwc/terms/stateProvince",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "county",
        "Label": "County",
        "URI": "http://rs.tdwg.org/dwc/terms/county",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "municipality",
        "Label": "Municipality",
        "URI": "http://rs.tdwg.org/dwc/terms/municipality",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "locality",
        "Label": "Locality",
        "URI": "http://rs.tdwg.org/dwc/terms/locality",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimLocality",
        "Label": "Verbatim locality",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimLocality",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "minimumElevationInMeters",
        "Label": "Minimum elevation in meters",
        "URI": "http://rs.tdwg.org/dwc/terms/minimumElevationInMeters",
        "Type": "double"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "maximumElevationInMeters",
        "Label": "Maximum elevation in meters",
        "URI": "http://rs.tdwg.org/dwc/terms/maximumElevationInMeters",
        "Type": "double"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimElevation",
        "Label": "Verbatim elevation",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimElevation",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "minimumDepthInMeters",
        "Label": "Minimum depth in meters",
        "URI": "http://rs.tdwg.org/dwc/terms/minimumDepthInMeters",
        "Type": "double"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "maximumDepthInMeters",
        "Label": "Maximum depth in meters",
        "URI": "http://rs.tdwg.org/dwc/terms/maximumDepthInMeters",
        "Type": "double"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimDepth",
        "Label": "Verbatim depth",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimDepth",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "minimumDistanceAboveSurfaceInMeters",
        "Label": "Minimum distance above surface in meters",
        "URI": "http://rs.tdwg.org/dwc/terms/minimumDistanceAboveSurfaceInMeters",
        "Type": "double"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "maximumDistanceAboveSurfaceInMeters",
        "Label": "Maximum distance above surface in meters",
        "URI": "http://rs.tdwg.org/dwc/terms/maximumDistanceAboveSurfaceInMeters",
        "Type": "double"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "locationRemarks",
        "Label": "Location remarks",
        "URI": "http://rs.tdwg.org/dwc/terms/locationRemarks",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "decimalLatitude",
        "Label": "Decimal latitude",
        "URI": "http://rs.tdwg.org/dwc/terms/decimalLatitude",
        "Type": "decimalLatitudeDataType"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "decimalLongitude",
        "Label": "Decimal longitude",
        "URI": "http://rs.tdwg.org/dwc/terms/decimalLongitude",
        "Type": "decimalLongitudeDataType"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "geodeticDatum",
        "Label": "Geodetic datum",
        "URI": "http://rs.tdwg.org/dwc/terms/geodeticDatum",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "coordinateUncertaintyInMeters",
        "Label": "Coordinate uncertainty in meters",
        "URI": "http://rs.tdwg.org/dwc/terms/coordinateUncertaintyInMeters",
        "Type": "double"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "coordinatePrecision",
        "Label": "Coordinate precision",
        "URI": "http://rs.tdwg.org/dwc/terms/coordinatePrecision",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "pointRadiusSpatialFit",
        "Label": "Point radius spatial fit",
        "URI": "http://rs.tdwg.org/dwc/terms/pointRadiusSpatialFit",
        "Type": "spatialFitDataType"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimCoordinates",
        "Label": "Verbatim coordinates",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimCoordinates",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimLatitude",
        "Label": "Verbatim latitude",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimLatitude",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimLongitude",
        "Label": "Verbatim longitude",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimLongitude",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimCoordinateSystem",
        "Label": "Verbatim coordinate system",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimCoordinateSystem",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "verbatimSRS",
        "Label": "Verbatim srs",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimSRS",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "footprintWKT",
        "Label": "Footprint wkt",
        "URI": "http://rs.tdwg.org/dwc/terms/footprintWKT",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "footprintSRS",
        "Label": "Footprint srs",
        "URI": "http://rs.tdwg.org/dwc/terms/footprintSRS",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "footprintSpatialFit",
        "Label": "Footprint spatial fit",
        "URI": "http://rs.tdwg.org/dwc/terms/footprintSpatialFit",
        "Type": "spatialFitDataType"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "georeferencedBy",
        "Label": "Georeferenced by",
        "URI": "http://rs.tdwg.org/dwc/terms/georeferencedBy",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "georeferencedDate",
        "Label": "Georeferenced date",
        "URI": "http://rs.tdwg.org/dwc/terms/georeferencedDate",
        "Type": "dateTimeISO"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "georeferenceProtocol",
        "Label": "Georeference protocol",
        "URI": "http://rs.tdwg.org/dwc/terms/georeferenceProtocol",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "georeferenceSources",
        "Label": "Georeference sources",
        "URI": "http://rs.tdwg.org/dwc/terms/georeferenceSources",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "georeferenceVerificationStatus",
        "Label": "Georeference verification status",
        "URI": "http://rs.tdwg.org/dwc/terms/georeferenceVerificationStatus",
        "Type": "string"
    },
    {
        "Group": "LocationTerms",
        "Group label": "Location",
        "Name": "georeferenceRemarks",
        "Label": "Georeference remarks",
        "URI": "http://rs.tdwg.org/dwc/terms/georeferenceRemarks",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "earliestEonOrLowestEonothem",
        "Label": "Earliest eon or lowest eonothem",
        "URI": "http://rs.tdwg.org/dwc/terms/earliestEonOrLowestEonothem",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "latestEonOrHighestEonothem",
        "Label": "Latest eon or highest eonothem",
        "URI": "http://rs.tdwg.org/dwc/terms/latestEonOrHighestEonothem",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "earliestEraOrLowestErathem",
        "Label": "Earliest era or lowest erathem",
        "URI": "http://rs.tdwg.org/dwc/terms/earliestEraOrLowestErathem",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "latestEraOrHighestErathem",
        "Label": "Latest era or highest erathem",
        "URI": "http://rs.tdwg.org/dwc/terms/latestEraOrHighestErathem",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "earliestPeriodOrLowestSystem",
        "Label": "Earliest period or lowest system",
        "URI": "http://rs.tdwg.org/dwc/terms/earliestPeriodOrLowestSystem",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "latestPeriodOrHighestSystem",
        "Label": "Latest period or highest system",
        "URI": "http://rs.tdwg.org/dwc/terms/latestPeriodOrHighestSystem",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "earliestEpochOrLowestSeries",
        "Label": "Earliest epoch or lowest series",
        "URI": "http://rs.tdwg.org/dwc/terms/earliestEpochOrLowestSeries",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "latestEpochOrHighestSeries",
        "Label": "Latest epoch or highest series",
        "URI": "http://rs.tdwg.org/dwc/terms/latestEpochOrHighestSeries",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "earliestAgeOrLowestStage",
        "Label": "Earliest age or lowest stage",
        "URI": "http://rs.tdwg.org/dwc/terms/earliestAgeOrLowestStage",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "latestAgeOrHighestStage",
        "Label": "Latest age or highest stage",
        "URI": "http://rs.tdwg.org/dwc/terms/latestAgeOrHighestStage",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "lowestBiostratigraphicZone",
        "Label": "Lowest biostratigraphic zone",
        "URI": "http://rs.tdwg.org/dwc/terms/lowestBiostratigraphicZone",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "highestBiostratigraphicZone",
        "Label": "Highest biostratigraphic zone",
        "URI": "http://rs.tdwg.org/dwc/terms/highestBiostratigraphicZone",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "lithostratigraphicTerms",
        "Label": "Lithostratigraphic terms",
        "URI": "http://rs.tdwg.org/dwc/terms/lithostratigraphicTerms",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "group",
        "Label": "Group",
        "URI": "http://rs.tdwg.org/dwc/terms/group",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "formation",
        "Label": "Formation",
        "URI": "http://rs.tdwg.org/dwc/terms/formation",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "member",
        "Label": "Member",
        "URI": "http://rs.tdwg.org/dwc/terms/member",
        "Type": "string"
    },
    {
        "Group": "GeologicalContextTerms",
        "Group label": "Geological context",
        "Name": "bed",
        "Label": "Bed",
        "URI": "http://rs.tdwg.org/dwc/terms/bed",
        "Type": "string"
    },
    {
        "Group": "IdentificationTerms",
        "Group label": "Identification",
        "Name": "identificationQualifier",
        "Label": "Identification qualifier",
        "URI": "http://rs.tdwg.org/dwc/terms/identificationQualifier",
        "Type": "string"
    },
    {
        "Group": "IdentificationTerms",
        "Group label": "Identification",
        "Name": "typeStatus",
        "Label": "Type status",
        "URI": "http://rs.tdwg.org/dwc/terms/typeStatus",
        "Type": "string"
    },
    {
        "Group": "IdentificationTerms",
        "Group label": "Identification",
        "Name": "identifiedBy",
        "Label": "Identified by",
        "URI": "http://rs.tdwg.org/dwc/terms/identifiedBy",
        "Type": "string"
    },
    {
        "Group": "IdentificationTerms",
        "Group label": "Identification",
        "Name": "dateIdentified",
        "Label": "Date identified",
        "URI": "http://rs.tdwg.org/dwc/terms/dateIdentified",
        "Type": "dateTimeISO"
    },
    {
        "Group": "IdentificationTerms",
        "Group label": "Identification",
        "Name": "identificationReferences",
        "Label": "Identification references",
        "URI": "http://rs.tdwg.org/dwc/terms/identificationReferences",
        "Type": "string"
    },
    {
        "Group": "IdentificationTerms",
        "Group label": "Identification",
        "Name": "identificationVerificationStatus",
        "Label": "Identification verification status",
        "URI": "http://rs.tdwg.org/dwc/terms/identificationVerificationStatus",
        "Type": "string"
    },
    {
        "Group": "IdentificationTerms",
        "Group label": "Identification",
        "Name": "identificationRemarks",
        "Label": "Identification remarks",
        "URI": "http://rs.tdwg.org/dwc/terms/identificationRemarks",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "scientificNameID",
        "Label": "Scientific name ID",
        "URI": "http://rs.tdwg.org/dwc/terms/scientificNameID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "acceptedNameUsageID",
        "Label": "Accepted name usage ID",
        "URI": "http://rs.tdwg.org/dwc/terms/acceptedNameUsageID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "parentNameUsageID",
        "Label": "Parent name usage ID",
        "URI": "http://rs.tdwg.org/dwc/terms/parentNameUsageID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "originalNameUsageID",
        "Label": "Original name usage ID",
        "URI": "http://rs.tdwg.org/dwc/terms/originalNameUsageID",
        "Type": "nonEmptyString"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "nameAccordingToID",
        "Label": "Name according to ID",
        "URI": "http://rs.tdwg.org/dwc/terms/nameAccordingToID",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "namePublishedInID",
        "Label": "Name published in ID",
        "URI": "http://rs.tdwg.org/dwc/terms/namePublishedInID",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "taxonConceptID",
        "Label": "Taxon concept ID",
        "URI": "http://rs.tdwg.org/dwc/terms/taxonConceptID",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "scientificName",
        "Label": "Scientific name",
        "URI": "http://rs.tdwg.org/dwc/terms/scientificName",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "acceptedNameUsage",
        "Label": "Accepted name usage",
        "URI": "http://rs.tdwg.org/dwc/terms/acceptedNameUsage",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "parentNameUsage",
        "Label": "Parent name usage",
        "URI": "http://rs.tdwg.org/dwc/terms/parentNameUsage",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "originalNameUsage",
        "Label": "Original name usage",
        "URI": "http://rs.tdwg.org/dwc/terms/originalNameUsage",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "nameAccordingTo",
        "Label": "Name according to",
        "URI": "http://rs.tdwg.org/dwc/terms/nameAccordingTo",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "namePublishedIn",
        "Label": "Name published in",
        "URI": "http://rs.tdwg.org/dwc/terms/namePublishedIn",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "namePublishedInYear",
        "Label": "Name published in year",
        "URI": "http://rs.tdwg.org/dwc/terms/namePublishedInYear",
        "Type": "gYear"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "higherClassification",
        "Label": "Higher classification",
        "URI": "http://rs.tdwg.org/dwc/terms/higherClassification",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "kingdom",
        "Label": "Kingdom",
        "URI": "http://rs.tdwg.org/dwc/terms/kingdom",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "phylum",
        "Label": "Phylum",
        "URI": "http://rs.tdwg.org/dwc/terms/phylum",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "class",
        "Label": "Class",
        "URI": "http://rs.tdwg.org/dwc/terms/class",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "order",
        "Label": "Order",
        "URI": "http://rs.tdwg.org/dwc/terms/order",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "family",
        "Label": "Family",
        "URI": "http://rs.tdwg.org/dwc/terms/family",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "genus",
        "Label": "Genus",
        "URI": "http://rs.tdwg.org/dwc/terms/genus",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "subgenus",
        "Label": "Subgenus",
        "URI": "http://rs.tdwg.org/dwc/terms/subgenus",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "specificEpithet",
        "Label": "Specific epithet",
        "URI": "http://rs.tdwg.org/dwc/terms/specificEpithet",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "infraspecificEpithet",
        "Label": "Infraspecific epithet",
        "URI": "http://rs.tdwg.org/dwc/terms/infraspecificEpithet",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "taxonRank",
        "Label": "Taxon rank",
        "URI": "http://rs.tdwg.org/dwc/terms/taxonRank",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "verbatimTaxonRank",
        "Label": "Verbatim taxon rank",
        "URI": "http://rs.tdwg.org/dwc/terms/verbatimTaxonRank",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "scientificNameAuthorship",
        "Label": "Scientific name authorship",
        "URI": "http://rs.tdwg.org/dwc/terms/scientificNameAuthorship",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "vernacularName",
        "Label": "Vernacular name",
        "URI": "http://rs.tdwg.org/dwc/terms/vernacularName",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "nomenclaturalCode",
        "Label": "Nomenclatural code",
        "URI": "http://rs.tdwg.org/dwc/terms/nomenclaturalCode",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "taxonomicStatus",
        "Label": "Taxonomic status",
        "URI": "http://rs.tdwg.org/dwc/terms/taxonomicStatus",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "nomenclaturalStatus",
        "Label": "Nomenclatural status",
        "URI": "http://rs.tdwg.org/dwc/terms/nomenclaturalStatus",
        "Type": "string"
    },
    {
        "Group": "TaxonTerms",
        "Group label": "Taxon",
        "Name": "taxonRemarks",
        "Label": "Taxon remarks",
        "URI": "http://rs.tdwg.org/dwc/terms/taxonRemarks",
        "Type": "string"
    }
]
