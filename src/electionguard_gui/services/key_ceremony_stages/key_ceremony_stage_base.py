from abc import ABC
from pymongo.database import Database

from electionguard_gui.models.key_ceremony_dto import KeyCeremonyDto
from electionguard_gui.services.authorization_service import AuthorizationService
from electionguard_gui.services.db_service import DbService
from electionguard_gui.services.eel_log_service import EelLogService
from electionguard_gui.services.key_ceremony_service import KeyCeremonyService
from electionguard_gui.services.key_ceremony_state_service import (
    KeyCeremonyStateService,
)


class KeyCeremonyStageBase(ABC):
    """Responsible for shared functionality across all key ceremony stages"""

    log: EelLogService
    _db_service: DbService
    _key_ceremony_service: KeyCeremonyService
    _auth_service: AuthorizationService
    _key_ceremony_state_service: KeyCeremonyStateService

    def __init__(
        self,
        log_service: EelLogService,
        db_service: DbService,
        key_ceremony_service: KeyCeremonyService,
        auth_service: AuthorizationService,
        key_ceremony_state_service: KeyCeremonyStateService,
    ):
        self._db_service = db_service
        self._key_ceremony_service = key_ceremony_service
        self._auth_service = auth_service
        self._key_ceremony_state_service = key_ceremony_state_service
        self.log = log_service

    def run(self, db: Database, key_ceremony: KeyCeremonyDto) -> None:
        pass
