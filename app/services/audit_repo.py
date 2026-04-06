import json
from app.services.sqlserver_repo import SQLServerRepo


class AuditRepository:
    def __init__(self, repo: SQLServerRepo):
        self.repo = repo

    def log(self, actor: str, action: str, entity_type: str, entity_id: str, status: str,
            reason_code: str, request_obj, response_obj):
        self.repo.insert_audit(
            {
                "actor": actor,
                "action": action,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "status": status,
                "reason_code": reason_code,
                "request_json": json.dumps(request_obj, ensure_ascii=False),
                "response_json": json.dumps(response_obj, ensure_ascii=False),
            }
        )
