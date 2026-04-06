from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.core.config import settings


def build_sqlalchemy_url() -> str:
    return (
        f"mssql+pyodbc://{settings.mssql_user}:{settings.mssql_password}"
        f"@{settings.mssql_host}:{settings.mssql_port}/{settings.mssql_db}"
        f"?driver={settings.mssql_driver.replace(' ', '+')}&TrustServerCertificate=yes"
    )


def get_engine() -> Engine:
    return create_engine(build_sqlalchemy_url(), pool_pre_ping=True, future=True)


class SQLServerRepo:
    def __init__(self):
        self.engine = get_engine()

    def fetch_pricing_base(self, since_days: int = 90):
        sql = text("""
            SELECT
                product_id,
                sale_date,
                unit_price,
                quantity,
                revenue,
                cost,
                channel,
                region
            FROM dbo.fact_sales
            WHERE sale_date >= DATEADD(day, -:since_days, CAST(GETDATE() AS date))
        """)
        with self.engine.begin() as conn:
            rows = conn.execute(sql, {"since_days": since_days}).mappings().all()
        return [dict(r) for r in rows]

    def fetch_policy_rules(self):
        sql = text("SELECT rule_key, rule_value FROM dbo.business_rules")
        with self.engine.begin() as conn:
            rows = conn.execute(sql).mappings().all()
        return {r["rule_key"]: r["rule_value"] for r in rows}

    def insert_audit(self, payload: dict):
        sql = text("""
            INSERT INTO dbo.audit_log
            (event_ts, actor, action, entity_type, entity_id, status, reason_code, request_json, response_json)
            VALUES
            (GETUTCDATE(), :actor, :action, :entity_type, :entity_id, :status, :reason_code, :request_json, :response_json)
        """)
        with self.engine.begin() as conn:
            conn.execute(sql, payload)
