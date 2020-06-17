from dataclasses import dataclass
from typing import Dict, Tuple

from .chaum_pedersen import ChaumPedersenProof
from .election_object_base import ElectionObjectBase

from .group import ElementModP, ElementModQ

from .types import BALLOT_ID, CONTEST_ID, GUARDIAN_ID, SELECTION_ID


@dataclass
class CiphertextDecryptionSelection(ElectionObjectBase):
    """
    A Guardian's Partial Decryption of a selection
    """

    description_hash: ElementModQ
    """
    The SelectionDescription hash
    """

    # M_i in the spec
    share: ElementModP
    """
    The Share of the selection
    """

    proof: ChaumPedersenProof
    """
    The Proof that the share was decrypted correctly
    """


@dataclass
class CiphertextCompensatedDecryptionSelection(ElectionObjectBase):
    """
    A Compensated Partial Decryption Selection
    """

    #
    description_hash: ElementModQ
    """
    The SelectionDescription hash
    """

    # M_i in the spec
    partial_share: ElementModP

    # Proof that the share was decrypted correctly
    proof: ChaumPedersenProof


@dataclass
class CiphertextDecryptionContest(ElectionObjectBase):
    """
    A Guardian's Partial Decryption of a contest
    """

    description_hash: ElementModQ
    """
    The ContestDescription Hash
    """

    selections: Dict[SELECTION_ID, CiphertextDecryptionSelection]
    """
    the collection of decryption shares for this contest's selections
    """


@dataclass
class CiphertextCompensatedDecryptionContest(ElectionObjectBase):
    """
    A Compensated Partial Decryption contest
    """

    # The ContestDescription Hash
    description_hash: ElementModQ

    # the collection of decryption shares for this contest's selections
    selections: Dict[SELECTION_ID, CiphertextCompensatedDecryptionSelection]


@dataclass
class BallotDecryptionShare:
    """
    A Guardian's Partial Decryption Share of a specific ballot (e.g. of a spoiled ballot)
    """

    guardian_id: GUARDIAN_ID
    """
    The Available Guardian that this share belongs to
    """

    public_key: ElementModP
    """
    The election public key for the guardian
    """

    ballot_id: BALLOT_ID
    """
    The Ballot Id that this Decryption Share belongs to
    """

    contests: Dict[CONTEST_ID, CiphertextDecryptionContest]
    """
    The collection of all contests in the ballot
    """


@dataclass
class DecryptionShare:
    """
    A Guardian's Partial Decryption Share of an election tally
    """

    guardian_id: GUARDIAN_ID
    """
    The Available Guardian that this share belongs to
    """

    public_key: ElementModP
    """
    The election public key for the guardian
    """

    contests: Dict[CONTEST_ID, CiphertextDecryptionContest]
    """
    The collection of decryption shares for all contests in the election
    """

    spoiled_ballots: Dict[BALLOT_ID, BallotDecryptionShare]
    """
    The collection of decryption shares for all spoiled ballots in the election
    """


@dataclass
class CompensatedDecryptionShare:
    """
    A Compensated Partial Decryption Share generated by 
    an available guardian on behalf of a missing guardian
    """

    # The Available Guardian that this partial share belongs to
    available_guardian_id: GUARDIAN_ID

    # The Missing Guardian for whom this share is calculated on behalf of
    missing_guardian_id: GUARDIAN_ID

    # The collection of all contests in the election
    contests: Dict[CONTEST_ID, CiphertextCompensatedDecryptionContest]

    lagrange_coefficient: ElementModQ


def get_tally_shares_for_selection(
    selection_id: str, shares: Dict[GUARDIAN_ID, DecryptionShare],
) -> Dict[GUARDIAN_ID, Tuple[ElementModP, CiphertextDecryptionSelection]]:
    """
    Get all of the cast shares for a specific selection
    """
    cast_shares: Dict[
        GUARDIAN_ID, Tuple[ElementModP, CiphertextDecryptionSelection]
    ] = {}
    for share in shares.values():
        for contest in share.contests.values():
            for selection in contest.selections.values():
                if selection.object_id == selection_id:
                    cast_shares[share.guardian_id] = (share.public_key, selection)

    return cast_shares


def get_spoiled_shares_for_selection(
    ballot_id: str, selection_id: str, shares: Dict[GUARDIAN_ID, DecryptionShare],
) -> Dict[GUARDIAN_ID, Tuple[ElementModP, CiphertextDecryptionSelection]]:
    """
    Get the spoiled shares for a given selection
    """
    spoiled_shares: Dict[
        GUARDIAN_ID, Tuple[ElementModP, CiphertextDecryptionSelection]
    ] = {}
    for share in shares.values():
        for ballot in share.spoiled_ballots.values():
            if ballot.ballot_id == ballot_id:
                for contest in ballot.contests.values():
                    for selection in contest.selections.values():
                        if selection.object_id == selection_id:
                            spoiled_shares[share.guardian_id] = (
                                share.public_key,
                                selection,
                            )
    return spoiled_shares
