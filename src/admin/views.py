from sqladmin import ModelView
from src.db.postgres.models import AiModels, ModelResponses


class AiModelsAdmin(ModelView, model=AiModels):
    name = AiModels.Meta.admin_title
    icon = AiModels.Meta.admin_icon
    column_list = [getattr(AiModels, c) for c in AiModels.Meta.admin_columns]
    column_default_sort = AiModels.Meta.admin_default_order


class ModelResponsesAdmin(ModelView, model=ModelResponses):
    name = ModelResponses.Meta.admin_title
    icon = ModelResponses.Meta.admin_icon
    column_list = [getattr(ModelResponses, c) for c in ModelResponses.Meta.admin_columns]
    column_default_sort = ModelResponses.Meta.admin_default_order
