from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from app_db.handlers.excel_file import ExcelProcessor
from app_db.models.core_description_example import CoreDescriptionExample
import random
import json


@require_http_methods(["POST"])
@csrf_exempt
def random_core_description(request):
    try:
        data = json.loads(request.body)
        language = data['language']

        descriptions = list(CoreDescriptionExample.objects.filter(language=language))
        if not descriptions:
            return JsonResponse(
                {"code": "404", "message": "Описания на указанном языке не найдены"},
                status=404
            )

        random_description = random.choice(descriptions)
        return JsonResponse(
            data={
            "description": random_description.description,
            "language": random_description.language
            },
            status=HTTPStatus.OK

        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"code": "400", "message": "Неверный формат JSON"},
            status=400
        )
    except KeyError:
        return JsonResponse(
            {"code": "400", "message": "Отсутствует обязательный параметр: language"},
            status=400
        )
    except Exception as exc:
        return JsonResponse(
            {"code": "500", "message": str(exc)},
            status=500
        )


@require_http_methods(["POST"])
@csrf_exempt
def handle_excel_file(request):
    """Ручка для обработки Excel файлов."""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)

        excel_file = request.FILES['file']
        excel_file_name = excel_file.name
        processor = ExcelProcessor()

        if not processor.is_excel_extension(excel_file_name):
            return JsonResponse({'error': 'Uploaded file is not an Excel file.'}, status=400)

        processor = ExcelProcessor()
        success = processor.read_excel_file(excel_file.read())

        if success:
            process_desc = processor.process_descriptions(request)
            if process_desc:
                processor.save_dataframe_to_excel(excel_file_name)

        print(processor.dataframe)
        # Дополнительные действия, например, сохранение обработанно


        return JsonResponse(
            data={
                "code": HTTPStatus.OK,
                'message': success
            },
            status=HTTPStatus.OK
        )
    except Exception as exc:
        return JsonResponse(
            data={
                "code": "500",
                "message": str(exc)
            },
            status=500
        )
