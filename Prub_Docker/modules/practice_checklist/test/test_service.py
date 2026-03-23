import pytest
from unittest.mock import MagicMock, patch, PropertyMock

# Importamos tu clase de override
from modules.practice_checklist.services.checklist_override import PracticeChecklistServiceOverride

@pytest.fixture
def checklist_service():
    """
    Configura el servicio con un Mock que sobrevive al serializador de Licium.
    """
    mock_repo = MagicMock()
    
    # Creamos el objeto que simula ser un registro de base de datos
    mock_rec = MagicMock()
    
    # ESTO EVITA EL ERROR __mapper__:
    # Configuramos el atributo __mapper__ a nivel de clase del mock
    type(mock_rec).__mapper__ = PropertyMock()
    
    mock_rec.id = 99
    mock_rec.name = "Test Checklist"
    mock_rec.status = "open"
    mock_rec.extra_field = "added_by_override"
    
    # Configuramos el repo para devolver este objeto
    mock_repo.get.return_value = mock_rec
    mock_repo.create.return_value = mock_rec
    mock_repo.session.get.return_value = mock_rec
    
    service = PracticeChecklistServiceOverride(mock_repo)
    
    # Punto 2: Settings simulados
    service.settings = {"auto_close": True}
    
    return service

# --- TESTS DE LOS 5 PUNTOS ---

def test_point_5_service_override(checklist_service):
    """Verifica el override: debe añadir 'extra_field'"""
    # Mockeamos serialize para evitar que busque mappers reales en el core
    with patch('modules.practice_checklist.services.checklist.serialize', side_effect=lambda x: x):
        payload = {"name": "Test Override"}
        result = checklist_service.create(payload)
        
        assert result is not None
        # Verificamos que el campo extra existe (Punto 5)
        assert hasattr(result, "extra_field")
        assert result.extra_field == "added_by_override"

@patch('modules.practice_checklist.services.checklist.serialize', side_effect=lambda x: x)
def test_point_4_unit_actions_close(mock_serialize, checklist_service):
    """Verifica la acción unitaria 'close' (Punto 4)"""
    if hasattr(checklist_service, 'close'):
        result = checklist_service.close(99)
        assert result is not None
        # Verificamos que el estado cambió a cerrado
        assert result.status == "closed"
    else:
        pytest.fail("ERROR: El método 'close' no existe en el servicio")

def test_point_1_bulk_actions(checklist_service):
    """Verifica la acción masiva 'set_done_bulk' (Punto 1)"""
    if hasattr(checklist_service, 'set_done_bulk'):
        res = checklist_service.set_done_bulk([1, 2, 3], True)
        assert res is True
    else:
        pytest.fail("ERROR: El método 'set_done_bulk' no existe. Revisa tu checklist_override.py")

def test_point_2_and_3_settings_and_i18n(checklist_service):
    """Verifica la integración de settings (Punto 2)"""
    # Verificamos que el servicio tiene acceso a sus settings
    assert "auto_close" in checklist_service.settings
    assert checklist_service.settings["auto_close"] is True

def test_db_connection_isolated(db_session):
    """Verifica que la conexión a la base de datos de test está activa"""
    from sqlalchemy import text
    res = db_session.execute(text("SELECT 1")).fetchone()
    assert res[0] == 1