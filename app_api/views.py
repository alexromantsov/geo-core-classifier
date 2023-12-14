# app_api/views.py
import traceback
from http import HTTPStatus

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .handlers.gpt_handler import GptHandler


@method_decorator(csrf_exempt, name='dispatch')
class GptApiView(View):
    async def post(self, request):
        try:
            gpt_handler = GptHandler(request)
            response_data = await gpt_handler.run()
            return JsonResponse(response_data)

        except ValueError as exc:
            # Обработка ошибок валидации
            return JsonResponse(
                {"code": "400", "message": str(exc)},
                status=HTTPStatus.BAD_REQUEST
            )
        except Exception as exc:
            tb = traceback.format_exc()
            message = exc.__class__.__name__ + ": " + str(exc)
            return JsonResponse(
                {"code": "500", "message": message, "details": tb},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
