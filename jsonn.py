import json

def toJson(record_start, record_end, record_count, records, UUID, client_id):
    data = {
        "record_start": record_start,
        "record_end": record_end,
        "record_format": "csv",
        "record_count": record_count,
        "records": records,
        "id": UUID,
        "id_client": "168E62D0-4E61-4144-8069-0D7784C59776"
    }

    json_data = json.dumps(data, indent=4)
    return json_data
print(toJson())