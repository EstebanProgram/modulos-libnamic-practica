from sqlalchemy import Boolean, String
from app.core.base import Base
from app.core.fields import field


class AssetLocation(Base):
    """
    Modelo que representa una ubicación donde se pueden almacenar
    o gestionar los activos. Incluye nombre, código único y estado.
    """

    __tablename__ = "asset_lending_location"
    __abstract__ = False
    __model__ = "location"
    __service__ = "modules.asset_lending.services.lending.AssetLocationService"

    # Configuración utilizada por los selectores en la interfaz de usuario
    __selector_config__ = {
        "label_field": "name",
        "search_fields": ["name", "code"],
        "columns": [
            {"field": "id", "label": "ID"},
            {"field": "name", "label": "Nombre"},
            {"field": "code", "label": "Código"},
        ],
    }

    # ----------------------------------------------------------------
    # Estado de la ubicación
    # ----------------------------------------------------------------

    is_active = field(
        Boolean,
        required=True,
        public=True,
        editable=True,
        default=True,
        info={"label": {"es": "Activo", "en": "Active"}},
    )

    # ----------------------------------------------------------------
    # Nombre de la ubicación
    # ----------------------------------------------------------------

    name = field(
        String(180),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Ubicación", "en": "Location"}},
    )

    # ----------------------------------------------------------------
    # Código único de la ubicación
    # ----------------------------------------------------------------

    code = field(
        String(50),
        required=True,
        public=True,
        editable=True,
        unique=True,
        info={"label": {"es": "Código de ubicación", "en": "Location Code"}},
    )

