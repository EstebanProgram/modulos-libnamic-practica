from app.core.base import BaseService
from slugify import slugify


class TagService(BaseService):
    from ..models.tag import Tag

    def create(self, values: dict):
        """Genera automáticamente el slug si no se proporciona."""
        if values.get("name") and not values.get("slug"):
            values["slug"] = slugify(values["name"])
        return super().create(values)