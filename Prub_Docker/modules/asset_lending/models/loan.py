from sqlalchemy import String, Text, ForeignKey, Uuid, DateTime, Integer
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.core.fields import field


class AssetLoan(Base):
    """
    Modelo que representa el préstamo de un activo a un usuario.
    Permite registrar cuándo se entrega el recurso, cuándo debe devolverse
    y cuándo se ha devuelto realmente.
    """

    __tablename__ = "asset_lending_loan"
    __abstract__ = False
    __model__ = "loan"
    __service__ = "modules.asset_lending.services.lending.AssetLoanService"

    # Configuración para los selectores en la interfaz
    __selector_config__ = {
        "label_field": "id",
        "search_fields": ["status"],
        "columns": [
            {"field": "id", "label": "ID"},
            {"field": "status", "label": "Estado"},
        ],
    }

    # ----------------------------------------------------------------
    # Recurso prestado
    # ----------------------------------------------------------------
    asset_id = field(
        Integer,
        ForeignKey("asset_lending_asset.id"),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Recurso", "en": "Asset"}},
    )

    # ----------------------------------------------------------------
    # Usuario que recibe el préstamo
    # ----------------------------------------------------------------
    borrower_user_id = field(
        Uuid,
        ForeignKey("core_user.id"),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Usuario prestatario", "en": "Borrower"}},
    )

    # ----------------------------------------------------------------
    # Estado del préstamo
    # ----------------------------------------------------------------
    status = field(
        String(20),
        required=True,
        public=True,
        editable=True,
        default="open",
        info={"label": {"es": "Estado del préstamo", "en": "Loan Status"}},
    )

    # ----------------------------------------------------------------
    # Fechas del préstamo
    # ----------------------------------------------------------------
    checkout_at = field(
        DateTime(timezone=True),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Fecha de entrega", "en": "Checkout Date"}},
    )

    due_at = field(
        DateTime(timezone=True),
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Fecha límite de devolución", "en": "Due Date"}},
    )

    returned_at = field(
        DateTime(timezone=True),
        required=False,
        public=True,
        editable=False,
        info={"label": {"es": "Fecha de devolución", "en": "Returned At"}},
    )

    # ----------------------------------------------------------------
    # Notas del préstamo
    # ----------------------------------------------------------------
    checkout_note = field(
        Text,
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Observaciones de entrega", "en": "Checkout Notes"}},
    )

    return_note = field(
        Text,
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Observaciones de devolución", "en": "Return Notes"}},
    )