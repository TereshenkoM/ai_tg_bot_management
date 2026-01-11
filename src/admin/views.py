from sqladmin import ModelView

from src.db.postgres.models import AiModels


class AiModelsAdmin(ModelView, model=AiModels):
    column_list = [AiModels.id, AiModels.name, AiModels.available]
