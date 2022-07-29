from typing import Any
import eel
from electionguard_gui.eel_utils import eel_success
from electionguard_gui.components.component_base import ComponentBase
from electionguard_gui.services import (
    DecryptionService,
)


class ViewTallyComponent(ComponentBase):
    """Responsible for functionality related to viewing a tally"""

    _decryption_service: DecryptionService

    def __init__(
        self,
        decryption_service: DecryptionService,
    ) -> None:
        self._decryption_service = decryption_service

    def expose(self) -> None:
        eel.expose(self.get_tally)

    def get_tally(self, decryption_id: str) -> dict[str, Any]:
        try:
            db = self._db_service.get_db()
            self._log.debug(f"retrieving decryption '{decryption_id}'")
            decryption = self._decryption_service.get(db, decryption_id)
            plaintext_tally = decryption.get_plaintext_tally_json()
            return eel_success(plaintext_tally)
        # pylint: disable=broad-except
        except Exception as e:
            return self.handle_error(e)
