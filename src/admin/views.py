from src.db.postgres.models import AiModels
from sqladmin import ModelView



class AiModelsAdmin(ModelView, model=AiModels):
    column_list = [AiModels.id, AiModels.name, AiModels.available]
