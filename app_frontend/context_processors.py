# context = {
#     "PROJECT_NAME": {
#         "name": "GeoCoreClassifier",
#         "description": "Название проекта."
#     },
#     "ROCK_SAMPLE": {
#         "name": "Описание керна",
#         "description": ""
#     },
#     "INDEX_HTML": {
#         "name": "GeoCoreClassifier — это передовое решение для геологов и специалистов в области исследования данных. Платформа предоставляет мощные инструменты для классификации и анализа геологических данных, обеспечивая точность и эффективность в ваших исследованиях.",
#         "description": "Возможности платформы включают в себя сбор данных, интеграцию документации, визуализацию, аналитику и многое другое. GeoCoreClassifier помогает преобразовать сложные геологические данные в понятные и легко управляемые результаты, делая вашу работу проще и продуктивнее."
#     }
# }

context = {
    "PROJECT_NAME": {
        "name": "GeoCoreClassifier",
        "description": "Project name."
    },
    "ROCK_SAMPLE": {
        "name": "Core Sample Description",
        "description": ""
    },
    "INDEX_HTML": {
        "name": "GeoCoreClassifier is an advanced solution for geologists and data research specialists. The platform offers powerful tools for the classification and analysis of geological data, ensuring accuracy and efficiency in your research.",
        "description": "Platform capabilities include data collection, documentation integration, visualization, analytics, and much more. GeoCoreClassifier helps to transform complex geological data into understandable and easily manageable results, making your work simpler and more productive."
    }
}


# Глобальные константы
def global_constants(request):
    return context
