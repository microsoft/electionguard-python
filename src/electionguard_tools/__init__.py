# <AUTOGEN_INIT>
from electionguard_tools import factories
from electionguard_tools import helpers
from electionguard_tools import scripts
from electionguard_tools import strategies

from electionguard_tools.factories import (
    AllPrivateElectionData,
    AllPublicElectionData,
    BallotFactory,
    ElectionFactory,
    NUMBER_OF_GUARDIANS,
    QUORUM,
    ballot_factory,
    data,
    election_factory,
    get_contest_description_well_formed,
    get_selection_description_well_formed,
    get_selection_poorly_formed,
    get_selection_well_formed,
)
from electionguard_tools.helpers import (
    BALLOT_PREFIX,
    COEFFICIENTS_FILE_NAME,
    CONSTANTS_FILE_NAME,
    CONTEXT_FILE_NAME,
    DEVICE_PREFIX,
    ENCRYPTED_TALLY_FILE_NAME,
    GUARDIAN_PREFIX,
    KeyCeremonyOrchestrator,
    MANIFEST_FILE_NAME,
    NumberEncodeOption,
    OPTION,
    PLAINTEXT_BALLOT_PREFIX,
    RESULTS_DIR,
    T,
    TALLY_FILE_NAME,
    TallyCeremonyOrchestrator,
    accumulate_plaintext_ballots,
    banlist,
    construct_path,
    custom_decoder,
    custom_encoder,
    export,
    export_private_data,
    from_file_to_dataclass,
    from_list_in_file_to_dataclass,
    from_raw,
    identity_auxiliary_decrypt,
    identity_auxiliary_encrypt,
    identity_encrypt,
    key_ceremony_orchestrator,
    serialize,
    tally_accumulate,
    tally_ceremony_orchestrator,
    to_file,
    to_raw,
)
from electionguard_tools.scripts import (
    DEFAULT_NUMBER_OF_BALLOTS,
    DEFAULT_SPOIL_RATE,
    DEFAULT_USE_ALL_GUARDIANS,
    DEFAULT_USE_PRIVATE_DATA,
    ElectionSampleDataGenerator,
    sample_generator,
)
from electionguard_tools.strategies import (
    CIPHERTEXT_ELECTIONS_TUPLE_TYPE,
    ELECTIONS_AND_BALLOTS_TUPLE_TYPE,
    annotated_strings,
    ballot_styles,
    candidate_contest_descriptions,
    candidates,
    ciphertext_elections,
    contact_infos,
    contest_descriptions,
    contest_descriptions_room_for_overvoting,
    election,
    election_descriptions,
    election_types,
    elections_and_ballots,
    elements_mod_p,
    elements_mod_p_no_zero,
    elements_mod_q,
    elements_mod_q_no_zero,
    elgamal,
    elgamal_keypairs,
    geopolitical_units,
    group,
    human_names,
    internationalized_human_names,
    internationalized_texts,
    language_human_names,
    languages,
    party_lists,
    plaintext_voted_ballot,
    plaintext_voted_ballots,
    referendum_contest_descriptions,
    reporting_unit_types,
    two_letter_codes,
)

__all__ = [
    "AllPrivateElectionData",
    "AllPublicElectionData",
    "BALLOT_PREFIX",
    "BallotFactory",
    "CIPHERTEXT_ELECTIONS_TUPLE_TYPE",
    "COEFFICIENTS_FILE_NAME",
    "CONSTANTS_FILE_NAME",
    "CONTEXT_FILE_NAME",
    "DEFAULT_NUMBER_OF_BALLOTS",
    "DEFAULT_SPOIL_RATE",
    "DEFAULT_USE_ALL_GUARDIANS",
    "DEFAULT_USE_PRIVATE_DATA",
    "DEVICE_PREFIX",
    "ELECTIONS_AND_BALLOTS_TUPLE_TYPE",
    "ENCRYPTED_TALLY_FILE_NAME",
    "ElectionFactory",
    "ElectionSampleDataGenerator",
    "GUARDIAN_PREFIX",
    "KeyCeremonyOrchestrator",
    "MANIFEST_FILE_NAME",
    "NUMBER_OF_GUARDIANS",
    "NumberEncodeOption",
    "OPTION",
    "PLAINTEXT_BALLOT_PREFIX",
    "QUORUM",
    "RESULTS_DIR",
    "T",
    "TALLY_FILE_NAME",
    "TallyCeremonyOrchestrator",
    "accumulate_plaintext_ballots",
    "annotated_strings",
    "ballot_factory",
    "ballot_styles",
    "banlist",
    "candidate_contest_descriptions",
    "candidates",
    "ciphertext_elections",
    "construct_path",
    "contact_infos",
    "contest_descriptions",
    "contest_descriptions_room_for_overvoting",
    "custom_decoder",
    "custom_encoder",
    "data",
    "election",
    "election_descriptions",
    "election_factory",
    "election_types",
    "elections_and_ballots",
    "elements_mod_p",
    "elements_mod_p_no_zero",
    "elements_mod_q",
    "elements_mod_q_no_zero",
    "elgamal",
    "elgamal_keypairs",
    "export",
    "export_private_data",
    "factories",
    "from_file_to_dataclass",
    "from_list_in_file_to_dataclass",
    "from_raw",
    "geopolitical_units",
    "get_contest_description_well_formed",
    "get_selection_description_well_formed",
    "get_selection_poorly_formed",
    "get_selection_well_formed",
    "group",
    "helpers",
    "human_names",
    "identity_auxiliary_decrypt",
    "identity_auxiliary_encrypt",
    "identity_encrypt",
    "internationalized_human_names",
    "internationalized_texts",
    "key_ceremony_orchestrator",
    "language_human_names",
    "languages",
    "party_lists",
    "plaintext_voted_ballot",
    "plaintext_voted_ballots",
    "referendum_contest_descriptions",
    "reporting_unit_types",
    "sample_generator",
    "scripts",
    "serialize",
    "strategies",
    "tally_accumulate",
    "tally_ceremony_orchestrator",
    "to_file",
    "to_raw",
    "two_letter_codes",
]

# </AUTOGEN_INIT>
# single source version from pyproject.toml
try:
    # importlib.metadata is present in Python 3.8 and later
    import importlib.metadata as import_lib_metadata
except ImportError:
    # use the shim package importlib-metadata pre-3.8
    import importlib_metadata as import_lib_metadata

try:
    __version__ = import_lib_metadata.version(__package__.split("_", maxsplit=1)[0])
except import_lib_metadata.PackageNotFoundError:
    __version__ = "0.0.0"
