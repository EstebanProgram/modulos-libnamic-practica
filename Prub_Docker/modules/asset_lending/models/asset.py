from sqlalchemy import String, Text, ForeignKey, Uuid, Integer
from sqlalchemy.orm import relationship

from app.core.base import Base
from app.core.fields import field


class Asset(Base):
    """
    Modelo que representa un recurso (activo) que puede ser prestado
    dentro del sistema de gestión de préstamos de activos.
    """

    __tablename__ = "asset_lending_asset"
    __abstract__ = False
    __model__ = "asset"
    __service__ = "modules.asset_lending.services.lending.AssetService"

    # Configuración utilizada por los selectores en la interfaz de usuario
    __selector_config__ = {
        "label_field": "name",
        "search_fields": ["name", "asset_code", "status"],
        "columns": [
            {"field": "id", "label": "ID"},
            {"field": "name", "label": "Recurso"},
            {"field": "asset_code", "label": "Código"},
        ],
    }

    # ----------------------------------------------------------------
    # Ubicación del activo
    # ----------------------------------------------------------------

    location_id = field(
        Integer,
        ForeignKey("asset_lending_location.id"),
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Ubicación", "en": "Location"}},
    )

    location = relationship(
        "modules.asset_lending.models.location.AssetLocation",
        foreign_keys=lambda: [Asset.location_id],
        info={"public": True, "recursive": False, "editable": True},
    )

    # ----------------------------------------------------------------
    # Usuario responsable del activo
    # ----------------------------------------------------------------

    responsible_user_id = field(
        Uuid,
        ForeignKey("core_user.id"),
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Usuario responsable", "en": "Responsible User"}},
    )

    # ----------------------------------------------------------------
    # Información básica del activo
    # ----------------------------------------------------------------

    name = field(
        String(180),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Nombre del recurso", "en": "Asset Name"}},
    )

    asset_code = field(
        String(50),
        required=True,
        public=True,
        editable=True,
        unique=True,
        info={"label": {"es": "Código del activo", "en": "Asset Code"}},
    )

    # ----------------------------------------------------------------
    # Información adicional
    # ----------------------------------------------------------------

    notes = field(
        Text,
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Observaciones", "en": "Notes"}},
    )

    # ----------------------------------------------------------------
    # Estado del activo
    # ----------------------------------------------------------------

    status = field(
        String(20),
        required=True,
        public=True,
        editable=True,
        default="available",
        info={"label": {"es": "Estado del activo", "en": "Asset Status"}},
    )