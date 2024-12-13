from src.app.models import APIEntry
from src.app.database import db
import csv
import os


def purge_and_load_csv(csv_path):
    db.drop_all()
    db.create_all()

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = APIEntry(
                name=row.get('name'),
                category=row.get('category'),
                base_url=row.get('base_url'),
                endpoint=row.get('endpoint'),
                description=row.get('description'),
                query_parameters=row.get('query_parameters'),
                example_request=row.get('example_request'),
                example_response=row.get('example_response')
            )
            db.session.add(entry)
        db.session.commit()
