import uuid
from datetime import datetime
from django.conf import settings
from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    API_VERSION = getattr(settings, 'API_VERSION', '1.0')

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')
        status_code = getattr(response, 'status_code', 200)
        is_success = 200 <= status_code < 400

        # Generate timestamp and traceId
        timestamp = datetime.utcnow().isoformat() + 'Z'
        trace_id = str(uuid.uuid4())

        # Extract meta/links if view already provided them
        meta = data.get('meta') if isinstance(data, dict) and 'meta' in data else None
        links = data.get('links') if isinstance(data, dict) and 'links' in data else None

        # If payload already matches our schema (errors + data keys), enrich it
        if isinstance(data, dict) and 'data' in data and 'errors' in data:
            payload = data
            payload.setdefault('timestamp', timestamp)
            payload.setdefault('traceId', trace_id)
            payload.setdefault('version', self.API_VERSION)
        else:
            # Wrap raw view output
            payload = {
                "timestamp": timestamp,
                "traceId": trace_id,
                "data": data if is_success else None,
                "isSuccess": is_success,
                "errors": data.get('errors') if isinstance(data, dict) and 'errors' in data else [],
                "status": status_code,
                "version": self.API_VERSION,
            }
            if meta is not None:
                payload['meta'] = meta
            if links is not None:
                payload['links'] = links

        return super().render(payload, accepted_media_type, renderer_context)