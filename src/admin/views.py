from sqladmin import ModelView

from src.db.postgres.models import AiModels, ModelResponses


class AiModelsAdmin(ModelView, model=AiModels):
    column_list = [AiModels.id, AiModels.name, AiModels.available]


class ModelResponsesAdmin(ModelView, model=ModelResponses):
    column_list = [ModelResponses.id, ModelResponses.data]