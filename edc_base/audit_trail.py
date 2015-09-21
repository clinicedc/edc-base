try:
    from edc_audit.audit_trail import AuditTrail
except ImportError:
    from simple_history.models import HistoricalRecords as AuditTrail
