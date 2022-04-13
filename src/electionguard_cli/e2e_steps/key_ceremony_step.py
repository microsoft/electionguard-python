from typing import List
from electionguard.guardian import Guardian
from electionguard.key_ceremony import (
    ElectionJointKey,
)
from electionguard.key_ceremony_mediator import KeyCeremonyMediator
from electionguard.utils import get_optional
from electionguard_tools.helpers.key_ceremony_orchestrator import (
    KeyCeremonyOrchestrator,
)

from .e2e_step_base import E2eStepBase


class KeyCeremonyStep(E2eStepBase):
    """Responsible for running a key ceremony and producing an elgamal public key given a list of guardians."""

    def run_key_ceremony(self, guardians: List[Guardian]) -> ElectionJointKey:
        self.print_header("Performing key ceremony")

        mediator: KeyCeremonyMediator = KeyCeremonyMediator(
            "mediator_1", guardians[0].ceremony_details
        )
        KeyCeremonyOrchestrator.perform_full_ceremony(guardians, mediator)
        KeyCeremonyOrchestrator.perform_round_1(guardians, mediator)
        if not mediator.all_guardians_announced():
            raise ValueError("All guardians failed to announce successfully")
        KeyCeremonyOrchestrator.perform_round_2(guardians, mediator)
        KeyCeremonyOrchestrator.perform_round_3(guardians, mediator)
        joint_key = mediator.publish_joint_key()

        self.print_value("Joint Key", get_optional(joint_key).joint_public_key)
        return get_optional(joint_key)
