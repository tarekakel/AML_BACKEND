# aml_core/utils/exceptions.py
from rest_framework.views import exception_handler
from .response import standard_response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        errors = []
        detail = response.data
        if isinstance(detail, dict):
            for field, msgs in detail.items():
                if isinstance(msgs, list):
                    errors += [f"{field}: {m}" for m in msgs]
                else:
                    errors.append(f"{field}: {msgs}")
        else:
            errors = [str(detail)]

        return standard_response(
            data=None,
            is_success=False,
            errors=errors,
            status_code=response.status_code
        )
    return response