from io import TextIOWrapper
from os import listdir
from os.path import join
from typing import List
from click import echo
from electionguard import CiphertextElectionContext

from electionguard.ballot import SubmittedBallot
from electionguard.guardian import Guardian, PrivateGuardianRecord
from electionguard.manifest import Manifest
from electionguard.serialize import from_file, from_file_wrapper, from_list_in_file

from .import_ballot_inputs import (
    ImportBallotInputs,
)
from ..cli_steps import (
    InputRetrievalStepBase,
)


class ImportBallotsInputRetrievalStep(InputRetrievalStepBase):
    """Responsible for retrieving and parsing user provided inputs for the CLI's import ballots command."""

    def get_inputs(
        self,
        manifest_file: TextIOWrapper,
        context_file: TextIOWrapper,
        ballots_dir: str,
        guardian_keys: str,
        output_record: str,
    ) -> ImportBallotInputs:

        self.print_header("Retrieving Inputs")
        manifest: Manifest = self._get_manifest(manifest_file)
        context = self._get_context(context_file)
        guardians = ImportBallotsInputRetrievalStep._get_guardians_from_keys(
            guardian_keys, context
        )
        submitted_ballots = ImportBallotsInputRetrievalStep._get_ballots(ballots_dir)

        self.print_value("Ballots Dir", ballots_dir)

        return ImportBallotInputs(
            guardians, manifest, submitted_ballots, context, output_record
        )

    @staticmethod
    def _get_guardians_from_keys(
        guardian_keys: str, context: CiphertextElectionContext
    ) -> List[Guardian]:
        guardian_private_records = from_list_in_file(
            PrivateGuardianRecord, guardian_keys
        )
        return [
            Guardian.from_private_record(g, context.number_of_guardians, context.quorum)
            for g in guardian_private_records
        ]

    @staticmethod
    def _get_context(context_file: TextIOWrapper) -> CiphertextElectionContext:
        return from_file_wrapper(CiphertextElectionContext, context_file)

    @staticmethod
    def _get_ballots(ballots_dir: str) -> List[SubmittedBallot]:
        files = listdir(ballots_dir)

        return [
            ImportBallotsInputRetrievalStep._get_ballot(ballots_dir, f) for f in files
        ]

    @staticmethod
    def _get_ballot(ballots_dir: str, filename: str) -> SubmittedBallot:
        full_file = join(ballots_dir, filename)
        echo(f"importing {filename}")
        return from_file(SubmittedBallot, full_file)
