import datetime as dt
from fastapi import HTTPException

from app.core.base import BaseService
from app.core.services import exposed_action
from app.core.serializer import serialize


# Servicio para gestionar ubicaciones de activos
class AssetLocationService(BaseService):
    from ..models import AssetLocation


# Servicio para gestionar los recursos (activos)
class AssetService(BaseService):
    from ..models import Asset

    # Mueve un recurso a estado maintenance
    @exposed_action("write", groups=["asset_lending_group_manager", "asset_lending_group_tech", "core_group_superadmin"])
    def mark_maintenance(self, id: int, note: str | None = None) -> dict:
        asset = self.repo.session.get(self.Asset, int(id))
        if asset is None:
            raise HTTPException(404, "Asset not found")
        
        asset.status = "maintenance"

        # Agregar nota de mantenimiento si existe
        if note:
            base = (asset.notes or "").strip()
            asset.notes = f"{base}\n\n[Mantenimiento] {note}".strip()
            
        self.repo.session.add(asset)
        self.repo.session.commit()
        self.repo.session.refresh(asset)
        return serialize(asset)


    # Devuelve un recurso de mantenimiento a disponible
    @exposed_action("write", groups=["asset_lending_group_manager", "asset_lending_group_tech", "core_group_superadmin"])
    def release_maintenance(self, id: int) -> dict:
        asset = self.repo.session.get(self.Asset, int(id))
        if asset is None:
            raise HTTPException(404, "Asset not found")
            
        asset.status = "available"
        self.repo.session.add(asset)
        self.repo.session.commit()
        self.repo.session.refresh(asset)
        return serialize(asset)

# Servicio para gestionar los préstamos de recursos
class AssetLoanService(BaseService):
    from ..models import AssetLoan
    from ..models import Asset

    # Marca un préstamo como devuelto y libera el recurso
    @exposed_action("write", groups=["asset_lending_group_manager", "core_group_superadmin"])
    def return_asset(self, id: int, note: str | None = None) -> dict:
        loan = self.repo.session.get(self.AssetLoan, int(id))
        if loan is None:
            raise HTTPException(404, "Loan not found")
        
        if loan.status != "open":
            raise HTTPException(400, "Este préstamo ya no está abierto.")

        # Actualizar el préstamo
        loan.status = "returned"
        loan.returned_at = dt.datetime.now(dt.timezone.utc)
        if note:
            loan.return_note = note

        # Actualizar el recurso asociado para que vuelva a estar disponible
        asset = self.repo.session.get(self.Asset, loan.asset_id)
        if asset:
            asset.status = "available"
            self.repo.session.add(asset)

        self.repo.session.add(loan)
        self.repo.session.commit()
        self.repo.session.refresh(loan)
        return serialize(loan)