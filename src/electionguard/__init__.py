import importlib.metadata

# <AUTOGEN_INIT>
from electionguard import auxiliary
from electionguard import ballot
from electionguard import ballot_box
from electionguard import ballot_code
from electionguard import ballot_compact
from electionguard import ballot_validator
from electionguard import chaum_pedersen
from electionguard import constants
from electionguard import data_store
from electionguard import decrypt_with_secrets
from electionguard import decrypt_with_shares
from electionguard import decryption
from electionguard import decryption_mediator
from electionguard import decryption_share
from electionguard import discrete_log
from electionguard import election
from electionguard import election_builder
from electionguard import election_object_base
from electionguard import election_polynomial
from electionguard import elgamal
from electionguard import encrypt
from electionguard import group
from electionguard import guardian
from electionguard import hash
from electionguard import key_ceremony
from electionguard import key_ceremony_mediator
from electionguard import logs
from electionguard import manifest
from electionguard import nonces
from electionguard import proof
from electionguard import rsa
from electionguard import scheduler
from electionguard import schnorr
from electionguard import singleton
from electionguard import tally
from electionguard import type
from electionguard import utils

from electionguard.auxiliary import (
    AUXILIARY_PUBLIC_KEY,
    AUXILIARY_SECRET_KEY,
    AuxiliaryDecrypt,
    AuxiliaryEncrypt,
    AuxiliaryKeyPair,
    AuxiliaryPublicKey,
    ENCRYPTED_MESSAGE,
    MESSAGE,
)
from electionguard.ballot import (
    BallotBoxState,
    CiphertextBallot,
    CiphertextBallotContest,
    CiphertextBallotSelection,
    CiphertextContest,
    CiphertextSelection,
    ExtendedData,
    PlaintextBallot,
    PlaintextBallotContest,
    PlaintextBallotSelection,
    SubmittedBallot,
    create_ballot_hash,
    from_ciphertext_ballot,
    make_ciphertext_ballot,
    make_ciphertext_ballot_contest,
    make_ciphertext_ballot_selection,
    make_ciphertext_submitted_ballot,
)
from electionguard.ballot_box import (
    BallotBox,
    accept_ballot,
    get_ballots,
)
from electionguard.ballot_code import (
    get_ballot_code,
    get_hash_for_device,
)
from electionguard.ballot_compact import (
    CompactPlaintextBallot,
    CompactSubmittedBallot,
    NO_VOTE,
    YES_VOTE,
    compress_plaintext_ballot,
    compress_submitted_ballot,
    expand_compact_plaintext_ballot,
    expand_compact_submitted_ballot,
)
from electionguard.ballot_validator import (
    ballot_is_valid_for_election,
    ballot_is_valid_for_style,
    contest_is_valid_for_style,
    selection_is_valid_for_style,
)
from electionguard.chaum_pedersen import (
    ChaumPedersenProof,
    ConstantChaumPedersenProof,
    DisjunctiveChaumPedersenProof,
    make_chaum_pedersen,
    make_constant_chaum_pedersen,
    make_disjunctive_chaum_pedersen,
    make_disjunctive_chaum_pedersen_one,
    make_disjunctive_chaum_pedersen_zero,
)
from electionguard.constants import (
    DEFAULT_POW_RADIX_STYLE,
    EXTRA_SMALL_TEST_CONSTANTS,
    ElectionConstants,
    LARGE_TEST_CONSTANTS,
    MEDIUM_TEST_CONSTANTS,
    PowRadixStyle,
    PrimeOption,
    SMALL_TEST_CONSTANTS,
    STANDARD_CONSTANTS,
    create_constants,
    flush_saved_constants,
    get_cofactor,
    get_constants,
    get_generator,
    get_large_prime,
    get_small_prime,
    using_test_constants,
)
from electionguard.data_store import (
    DataStore,
    ReadOnlyDataStore,
)
from electionguard.decrypt_with_secrets import (
    decrypt_ballot_with_nonce,
    decrypt_ballot_with_secret,
    decrypt_contest_with_nonce,
    decrypt_contest_with_secret,
    decrypt_selection_with_nonce,
    decrypt_selection_with_secret,
)
from electionguard.decrypt_with_shares import (
    decrypt_ballot,
    decrypt_contest_with_decryption_shares,
    decrypt_selection_with_decryption_shares,
    decrypt_tally,
)
from electionguard.decryption import (
    RECOVERY_PUBLIC_KEY,
    compensate_decrypt,
    compute_compensated_decryption_share,
    compute_compensated_decryption_share_for_ballot,
    compute_compensated_decryption_share_for_contest,
    compute_compensated_decryption_share_for_selection,
    compute_decryption_share,
    compute_decryption_share_for_ballot,
    compute_decryption_share_for_contest,
    compute_decryption_share_for_selection,
    compute_lagrange_coefficients_for_guardian,
    compute_lagrange_coefficients_for_guardians,
    compute_recovery_public_key,
    partially_decrypt,
    reconstruct_decryption_contest,
    reconstruct_decryption_share,
    reconstruct_decryption_share_for_ballot,
)
from electionguard.decryption_mediator import (
    DecryptionMediator,
)
from electionguard.decryption_share import (
    CiphertextCompensatedDecryptionContest,
    CiphertextCompensatedDecryptionSelection,
    CiphertextDecryptionContest,
    CiphertextDecryptionSelection,
    CompensatedDecryptionShare,
    DecryptionShare,
    ProofOrRecovery,
    create_ciphertext_decryption_selection,
    get_shares_for_selection,
)
from electionguard.discrete_log import (
    DLOG_CACHE,
    DLOG_MAX,
    DiscreteLog,
    compute_discrete_log,
    compute_discrete_log_cache,
)
from electionguard.election import (
    CiphertextElectionContext,
    make_ciphertext_election_context,
)
from electionguard.election_builder import (
    ElectionBuilder,
)
from electionguard.election_object_base import (
    ElectionObjectBase,
    OrderedObjectBase,
    sequence_order_sort,
)
from electionguard.election_polynomial import (
    ElectionPolynomial,
    LagrangeCoefficientsRecord,
    PUBLIC_COMMITMENT,
    SECRET_COEFFICIENT,
    compute_lagrange_coefficient,
    compute_polynomial_coordinate,
    generate_polynomial,
    verify_polynomial_coordinate,
)
from electionguard.elgamal import (
    ELGAMAL_PUBLIC_KEY,
    ELGAMAL_SECRET_KEY,
    ElGamalCiphertext,
    ElGamalKeyPair,
    elgamal_add,
    elgamal_combine_public_keys,
    elgamal_encrypt,
    elgamal_keypair_from_secret,
    elgamal_keypair_random,
)
from electionguard.encrypt import (
    EncryptionDevice,
    EncryptionMediator,
    contest_from,
    encrypt_ballot,
    encrypt_ballot_contests,
    encrypt_contest,
    encrypt_selection,
    generate_device_uuid,
    selection_from,
)
from electionguard.group import (
    BaseElement,
    ElementModP,
    ElementModPAcceleratedPow,
    ElementModPOrQ,
    ElementModPOrQorInt,
    ElementModPorInt,
    ElementModQ,
    ElementModQorInt,
    PowRadix,
    a_minus_b_q,
    a_plus_bc_q,
    add_q,
    div_p,
    div_q,
    g_pow_p,
    get_generator_element,
    hex_to_int,
    hex_to_p,
    hex_to_q,
    int_to_hex,
    int_to_p,
    int_to_q,
    mult_inv_p,
    mult_p,
    mult_q,
    negate_q,
    pow_p,
    pow_q,
    rand_q,
    rand_range_q,
)
from electionguard.guardian import (
    Guardian,
    GuardianRecord,
    PrivateGuardianRecord,
    get_valid_ballot_shares,
    publish_guardian_record,
)
from electionguard.hash import (
    CRYPTO_HASHABLE_ALL,
    CRYPTO_HASHABLE_T,
    CryptoHashCheckable,
    CryptoHashable,
    hash_elems,
)
from electionguard.key_ceremony import (
    CeremonyDetails,
    ElectionJointKey,
    ElectionKeyPair,
    ElectionPartialKeyBackup,
    ElectionPartialKeyChallenge,
    ElectionPartialKeyVerification,
    ElectionPublicKey,
    PublicKeySet,
    combine_election_public_keys,
    generate_election_key_pair,
    generate_election_partial_key_backup,
    generate_election_partial_key_challenge,
    generate_elgamal_auxiliary_key_pair,
    generate_rsa_auxiliary_key_pair,
    verify_election_partial_key_backup,
    verify_election_partial_key_challenge,
)
from electionguard.key_ceremony_mediator import (
    BackupVerificationState,
    GuardianPair,
    KeyCeremonyMediator,
)
from electionguard.logs import (
    ElectionGuardLog,
    FORMAT,
    LOG,
    get_file_handler,
    get_stream_handler,
    log_add_handler,
    log_critical,
    log_debug,
    log_error,
    log_handlers,
    log_info,
    log_remove_handler,
    log_warning,
)
from electionguard.manifest import (
    AnnotatedString,
    BallotStyle,
    Candidate,
    CandidateContestDescription,
    ContactInformation,
    ContestDescription,
    ContestDescriptionWithPlaceholders,
    ElectionType,
    GeopoliticalUnit,
    InternalManifest,
    InternationalizedText,
    Language,
    Manifest,
    Party,
    ReferendumContestDescription,
    ReportingUnitType,
    SelectionDescription,
    VoteVariationType,
    contest_description_with_placeholders_from,
    generate_placeholder_selection_from,
    generate_placeholder_selections_from,
)
from electionguard.nonces import (
    Nonces,
)
from electionguard.proof import (
    Proof,
    ProofUsage,
)
from electionguard.rsa import (
    BYTE_ORDER,
    ISO_ENCODING,
    KEY_SIZE,
    MAX_BITS,
    PADDING,
    PUBLIC_EXPONENT,
    RSAKeyPair,
    rsa_decrypt,
    rsa_encrypt,
    rsa_keypair,
)
from electionguard.scheduler import (
    Scheduler,
)
from electionguard.schnorr import (
    SchnorrProof,
    make_schnorr_proof,
)
from electionguard.singleton import (
    Singleton,
)
from electionguard.tally import (
    CiphertextTally,
    CiphertextTallyContest,
    CiphertextTallySelection,
    PlaintextTally,
    PlaintextTallyContest,
    PlaintextTallySelection,
    PublishedCiphertextTally,
    tally_ballot,
    tally_ballots,
)
from electionguard.type import (
    BALLOT_ID,
    CONTEST_ID,
    GUARDIAN_ID,
    MEDIATOR_ID,
    SELECTION_ID,
    VERIFIER_ID,
)
from electionguard.utils import (
    flatmap_optional,
    get_optional,
    get_or_else_optional,
    get_or_else_optional_func,
    match_optional,
    space_between_capitals,
    to_iso_date_string,
    to_ticks,
)

__all__ = [
    "AUXILIARY_PUBLIC_KEY",
    "AUXILIARY_SECRET_KEY",
    "AnnotatedString",
    "AuxiliaryDecrypt",
    "AuxiliaryEncrypt",
    "AuxiliaryKeyPair",
    "AuxiliaryPublicKey",
    "BALLOT_ID",
    "BYTE_ORDER",
    "BackupVerificationState",
    "BallotBox",
    "BallotBoxState",
    "BallotStyle",
    "BaseElement",
    "CONTEST_ID",
    "CRYPTO_HASHABLE_ALL",
    "CRYPTO_HASHABLE_T",
    "Candidate",
    "CandidateContestDescription",
    "CeremonyDetails",
    "ChaumPedersenProof",
    "CiphertextBallot",
    "CiphertextBallotContest",
    "CiphertextBallotSelection",
    "CiphertextCompensatedDecryptionContest",
    "CiphertextCompensatedDecryptionSelection",
    "CiphertextContest",
    "CiphertextDecryptionContest",
    "CiphertextDecryptionSelection",
    "CiphertextElectionContext",
    "CiphertextSelection",
    "CiphertextTally",
    "CiphertextTallyContest",
    "CiphertextTallySelection",
    "CompactPlaintextBallot",
    "CompactSubmittedBallot",
    "CompensatedDecryptionShare",
    "ConstantChaumPedersenProof",
    "ContactInformation",
    "ContestDescription",
    "ContestDescriptionWithPlaceholders",
    "CryptoHashCheckable",
    "CryptoHashable",
    "DEFAULT_POW_RADIX_STYLE",
    "DLOG_CACHE",
    "DLOG_MAX",
    "DataStore",
    "DecryptionMediator",
    "DecryptionShare",
    "DiscreteLog",
    "DisjunctiveChaumPedersenProof",
    "ELGAMAL_PUBLIC_KEY",
    "ELGAMAL_SECRET_KEY",
    "ENCRYPTED_MESSAGE",
    "EXTRA_SMALL_TEST_CONSTANTS",
    "ElGamalCiphertext",
    "ElGamalKeyPair",
    "ElectionBuilder",
    "ElectionConstants",
    "ElectionGuardLog",
    "ElectionJointKey",
    "ElectionKeyPair",
    "ElectionObjectBase",
    "ElectionPartialKeyBackup",
    "ElectionPartialKeyChallenge",
    "ElectionPartialKeyVerification",
    "ElectionPolynomial",
    "ElectionPublicKey",
    "ElectionType",
    "ElementModP",
    "ElementModPAcceleratedPow",
    "ElementModPOrQ",
    "ElementModPOrQorInt",
    "ElementModPorInt",
    "ElementModQ",
    "ElementModQorInt",
    "EncryptionDevice",
    "EncryptionMediator",
    "ExtendedData",
    "FORMAT",
    "GUARDIAN_ID",
    "GeopoliticalUnit",
    "Guardian",
    "GuardianPair",
    "GuardianRecord",
    "ISO_ENCODING",
    "InternalManifest",
    "InternationalizedText",
    "KEY_SIZE",
    "KeyCeremonyMediator",
    "LARGE_TEST_CONSTANTS",
    "LOG",
    "LagrangeCoefficientsRecord",
    "Language",
    "MAX_BITS",
    "MEDIATOR_ID",
    "MEDIUM_TEST_CONSTANTS",
    "MESSAGE",
    "Manifest",
    "NO_VOTE",
    "Nonces",
    "OrderedObjectBase",
    "PADDING",
    "PUBLIC_COMMITMENT",
    "PUBLIC_EXPONENT",
    "Party",
    "PlaintextBallot",
    "PlaintextBallotContest",
    "PlaintextBallotSelection",
    "PlaintextTally",
    "PlaintextTallyContest",
    "PlaintextTallySelection",
    "PowRadix",
    "PowRadixStyle",
    "PrimeOption",
    "PrivateGuardianRecord",
    "Proof",
    "ProofOrRecovery",
    "ProofUsage",
    "PublicKeySet",
    "PublishedCiphertextTally",
    "RECOVERY_PUBLIC_KEY",
    "RSAKeyPair",
    "ReadOnlyDataStore",
    "ReferendumContestDescription",
    "ReportingUnitType",
    "SECRET_COEFFICIENT",
    "SELECTION_ID",
    "SMALL_TEST_CONSTANTS",
    "STANDARD_CONSTANTS",
    "Scheduler",
    "SchnorrProof",
    "SelectionDescription",
    "Singleton",
    "SubmittedBallot",
    "VERIFIER_ID",
    "VoteVariationType",
    "YES_VOTE",
    "a_minus_b_q",
    "a_plus_bc_q",
    "accept_ballot",
    "add_q",
    "auxiliary",
    "ballot",
    "ballot_box",
    "ballot_code",
    "ballot_compact",
    "ballot_is_valid_for_election",
    "ballot_is_valid_for_style",
    "ballot_validator",
    "chaum_pedersen",
    "combine_election_public_keys",
    "compensate_decrypt",
    "compress_plaintext_ballot",
    "compress_submitted_ballot",
    "compute_compensated_decryption_share",
    "compute_compensated_decryption_share_for_ballot",
    "compute_compensated_decryption_share_for_contest",
    "compute_compensated_decryption_share_for_selection",
    "compute_decryption_share",
    "compute_decryption_share_for_ballot",
    "compute_decryption_share_for_contest",
    "compute_decryption_share_for_selection",
    "compute_discrete_log",
    "compute_discrete_log_cache",
    "compute_lagrange_coefficient",
    "compute_lagrange_coefficients_for_guardian",
    "compute_lagrange_coefficients_for_guardians",
    "compute_polynomial_coordinate",
    "compute_recovery_public_key",
    "constants",
    "contest_description_with_placeholders_from",
    "contest_from",
    "contest_is_valid_for_style",
    "create_ballot_hash",
    "create_ciphertext_decryption_selection",
    "create_constants",
    "data_store",
    "decrypt_ballot",
    "decrypt_ballot_with_nonce",
    "decrypt_ballot_with_secret",
    "decrypt_contest_with_decryption_shares",
    "decrypt_contest_with_nonce",
    "decrypt_contest_with_secret",
    "decrypt_selection_with_decryption_shares",
    "decrypt_selection_with_nonce",
    "decrypt_selection_with_secret",
    "decrypt_tally",
    "decrypt_with_secrets",
    "decrypt_with_shares",
    "decryption",
    "decryption_mediator",
    "decryption_share",
    "discrete_log",
    "div_p",
    "div_q",
    "election",
    "election_builder",
    "election_object_base",
    "election_polynomial",
    "elgamal",
    "elgamal_add",
    "elgamal_combine_public_keys",
    "elgamal_encrypt",
    "elgamal_keypair_from_secret",
    "elgamal_keypair_random",
    "encrypt",
    "encrypt_ballot",
    "encrypt_ballot_contests",
    "encrypt_contest",
    "encrypt_selection",
    "expand_compact_plaintext_ballot",
    "expand_compact_submitted_ballot",
    "flatmap_optional",
    "flush_saved_constants",
    "from_ciphertext_ballot",
    "g_pow_p",
    "generate_device_uuid",
    "generate_election_key_pair",
    "generate_election_partial_key_backup",
    "generate_election_partial_key_challenge",
    "generate_elgamal_auxiliary_key_pair",
    "generate_placeholder_selection_from",
    "generate_placeholder_selections_from",
    "generate_polynomial",
    "generate_rsa_auxiliary_key_pair",
    "get_ballot_code",
    "get_ballots",
    "get_cofactor",
    "get_constants",
    "get_file_handler",
    "get_generator",
    "get_generator_element",
    "get_hash_for_device",
    "get_large_prime",
    "get_optional",
    "get_or_else_optional",
    "get_or_else_optional_func",
    "get_shares_for_selection",
    "get_small_prime",
    "get_stream_handler",
    "get_valid_ballot_shares",
    "group",
    "guardian",
    "hash",
    "hash_elems",
    "hex_to_int",
    "hex_to_p",
    "hex_to_q",
    "int_to_hex",
    "int_to_p",
    "int_to_q",
    "key_ceremony",
    "key_ceremony_mediator",
    "log_add_handler",
    "log_critical",
    "log_debug",
    "log_error",
    "log_handlers",
    "log_info",
    "log_remove_handler",
    "log_warning",
    "logs",
    "make_chaum_pedersen",
    "make_ciphertext_ballot",
    "make_ciphertext_ballot_contest",
    "make_ciphertext_ballot_selection",
    "make_ciphertext_election_context",
    "make_ciphertext_submitted_ballot",
    "make_constant_chaum_pedersen",
    "make_disjunctive_chaum_pedersen",
    "make_disjunctive_chaum_pedersen_one",
    "make_disjunctive_chaum_pedersen_zero",
    "make_schnorr_proof",
    "manifest",
    "match_optional",
    "mult_inv_p",
    "mult_p",
    "mult_q",
    "negate_q",
    "nonces",
    "partially_decrypt",
    "pow_p",
    "pow_q",
    "proof",
    "publish_guardian_record",
    "rand_q",
    "rand_range_q",
    "reconstruct_decryption_contest",
    "reconstruct_decryption_share",
    "reconstruct_decryption_share_for_ballot",
    "rsa",
    "rsa_decrypt",
    "rsa_encrypt",
    "rsa_keypair",
    "scheduler",
    "schnorr",
    "selection_from",
    "selection_is_valid_for_style",
    "sequence_order_sort",
    "singleton",
    "space_between_capitals",
    "tally",
    "tally_ballot",
    "tally_ballots",
    "to_iso_date_string",
    "to_ticks",
    "type",
    "using_test_constants",
    "utils",
    "verify_election_partial_key_backup",
    "verify_election_partial_key_challenge",
    "verify_polynomial_coordinate",
]

# </AUTOGEN_INIT>

# single source version from pyproject.toml
try:
    __version__ = importlib.metadata.version(__package__.split("_", maxsplit=1)[0])
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"
