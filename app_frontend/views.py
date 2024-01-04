import json
import traceback
from http import HTTPStatus

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from app_db.handlers.user_action import UserActionHandler
from app_frontend.handlers.rock_sample.core_analysis import CoreAnalysis
from server.settings import USER_UNDEFINED


def index(request):
    template = 'en/index.html'
    context = {
    }
    return render(request, template, context)


def rock_sample(request):
    analysis = CoreAnalysis(request)

    # Определяем текст для кнопки и её статус
    if analysis.available_requests > 0:
        button_text = f"Remaining requests: {analysis.available_requests}"
        button_disabled = False
    else:
        button_text = "Daily request limit exhausted"
        button_disabled = True

    # Подготовка контекста для шаблона
    context = {
        'user_ip': analysis.user_ip,
        'button_text': button_text,
        'button_disabled': button_disabled,
    }

    template = 'en/tools/rock_sample.html'
    return render(request, template, context)


@require_http_methods(["POST"])
@csrf_exempt
def core_analysis(request):
    try:
        analysis = CoreAnalysis(request)
        result = analysis.run()
        return JsonResponse(result)
    except (ValueError, LookupError) as exc:
        return JsonResponse(
            data={
                "code": "501",
                "message": str(exc),
                "details": "",
                "data": {
                    "response_data": {}
                }
            },
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except Exception as exc:
        tb = traceback.format_exc()
        message = exc.__class__.__name__ + ": " + str(exc)
        return JsonResponse(
            {"code": "500", "message": message, "details": tb},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
