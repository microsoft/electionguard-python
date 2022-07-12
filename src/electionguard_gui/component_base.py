from abc import ABC
from electionguard_gui.services.authorization_service import AuthoriationService

from electionguard_gui.services.db_service import DbService


class ComponentBase(ABC):
    """Responsible for common functionality among ell components"""

    db_service: DbService
    auth_service: AuthoriationService

    def init(self, db_service: DbService, auth_service: AuthoriationService) -> None:
        self.db_service = db_service
        self.auth_service = auth_service
        self.expose()

    def expose(self) -> None:
        """Override to expose the component's methods to JavaScript. This technique hides the
        fact that method names exposed must be globally unique."""
