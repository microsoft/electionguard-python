import traceback
from typing import Any
import eel
from electionguard_gui.eel_utils import eel_fail, eel_success
from electionguard_gui.components.component_base import ComponentBase
from electionguard_gui.services import (
    ElectionService,
    DecryptionService,
    DbWatcherService,
)
from electionguard_gui.services.decryption_stages import DecryptionS1JoinService


class ViewDecryptionComponent(ComponentBase):
    """Responsible for functionality related to creating decryptions for an election"""

    _decryption_service: DecryptionService
    _election_service: ElectionService
    _decryption_s1_join_service: DecryptionS1JoinService
    _db_watcher_service: DbWatcherService

    def __init__(
        self,
        decryption_service: DecryptionService,
        election_service: ElectionService,
        decryption_s1_join_service: DecryptionS1JoinService,
        db_watcher_service: DbWatcherService,
    ) -> None:
        self._decryption_service = decryption_service
        self._election_service = election_service
        self._decryption_s1_join_service = decryption_s1_join_service
        self._db_watcher_service = db_watcher_service

    def expose(self) -> None:
        eel.expose(self.get_decryption)
        eel.expose(self.watch_decryption)
        eel.expose(self.stop_watching_decryption)
        eel.expose(self.join_decryption)

    def watch_decryption(self, decryption_id: str) -> None:
        db = self._db_service.get_db()
        self._log.debug(f"watching decryption '{decryption_id}'")
        self._db_watcher_service.watch_database(
            db, decryption_id, self.on_decryption_changed
        )

    def stop_watching_decryption(self) -> None:
        self._db_watcher_service.stop_watching()

    def on_decryption_changed(self, _: str, key_ceremony_id: str) -> None:
        try:
            self._log.debug(
                f"on_key_ceremony_changed key_ceremony_id: '{key_ceremony_id}'"
            )
            # pylint: disable=no-member
            eel.refresh_decryption(eel_success())
        # pylint: disable=broad-except
        except Exception as e:
            self._log.error(e)
            traceback.print_exc()
            # pylint: disable=no-member
            eel.refresh_key_ceremony(eel_fail(str(e)))

    def get_decryption(self, decryption_id: str) -> dict[str, Any]:
        try:
            db = self._db_service.get_db()
            decryption = self._decryption_service.get(db, decryption_id)
            return eel_success(decryption.to_dict())
        # pylint: disable=broad-except
        except Exception as e:
            return self.handle_error(e)

    def join_decryption(self, decryption_id: str) -> dict[str, Any]:
        try:
            db = self._db_service.get_db()
            decryption = self._decryption_service.get(db, decryption_id)
            self._decryption_s1_join_service.run(db, decryption)
            return eel_success(decryption.to_dict())
        # pylint: disable=broad-except
        except Exception as e:
            return self.handle_error(e)
