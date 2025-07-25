import uuid
from datetime import datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status as drf_status

API_VERSION = getattr(settings, 'API_VERSION', '1.0')

def standard_response(
    data=None,
    is_success=True,
    errors=None,
    status_code=drf_status.HTTP_200_OK,
    meta=None,
    links=None,
    version=None,
    trace_id=None,
    timestamp=None,
    **extra
):
    """
    Wrap any payload in the standard schema with extra tracing and pagination.
    """
    # Generate timestamp and traceId if not provided
    timestamp = timestamp or datetime.utcnow().isoformat() + 'Z'
    trace_id = trace_id or str(uuid.uuid4())
    version = version or API_VERSION

    payload = {
        "timestamp": timestamp,
        "traceId": trace_id,
        "data": data,
        "isSuccess": is_success,
        "errors": errors or [],
        "status": status_code,
        "version": version,
    }

    # Include optional sections only when supplied
    if meta is not None:
        payload["meta"] = meta
    if links is not None:
        payload["links"] = links

    # Merge any additional custom fields
    payload.update(extra)

    return Response(payload, status=status_code)