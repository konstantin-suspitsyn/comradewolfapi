import json

from sqlalchemy.orm import Session

from model.base_model import SavedQuery
from model.dto import QueryMetaData


def save_query_meta_data(db: Session, query_info: QueryMetaData, frontend: dict):
    saved_query = SavedQuery(frontend = json.dumps(frontend), query = query_info.sql_query, pages=query_info.pages,
                             items_per_page=query_info.items_per_page)
    db.add(saved_query)
    db.commit()
    db.refresh(saved_query)

    return saved_query