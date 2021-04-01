# pylint: disable=too-many-instance-attributes

from unittest import TestCase
from datetime import timedelta
from typing import Dict, List
from random import randrange

from hypothesis import given, HealthCheck, settings, Phase
from hypothesis.strategies import integers, data

from electionguard.ballot import PlaintextBallot, from_ciphertext_ballot
from electionguard.ballot_box import get_ballots
from electionguard.data_store import DataStore

from electionguard.ballot_box import BallotBox, BallotBoxState
from electionguard.decryption_mediator import DecryptionMediator
from electionguard.election import CiphertextElectionContext
from electionguard.election_builder import ElectionBuilder
from electionguard.encrypt import (
    EncryptionMediator,
    encrypt_ballot,
)
from electionguard.group import (
    int_to_q_unchecked,
)
from electionguard.guardian import Guardian
from electionguard.key_ceremony import CeremonyDetails
from electionguard.key_ceremony_mediator import KeyCeremonyMediator
from electionguard.manifest import InternalManifest
from electionguard.tally import (
    CiphertextTally,
    PlaintextTally,
    tally_ballots,
)
from electionguard.utils import get_optional

import electionguardtest.ballot_factory as BallotFactory
import electionguardtest.election_factory as ElectionFactory
from electionguardtest.election import election_descriptions, plaintext_voted_ballots
from electionguardtest.identity_encrypt import identity_auxiliary_decrypt
from electionguardtest.key_ceremony_helper import KeyCeremonyHelper
from electionguardtest.tally import accumulate_plaintext_ballots

election_factory = ElectionFactory.ElectionFactory()
ballot_factory = BallotFactory.BallotFactory()


class TestDecryptionMediator(TestCase):
    """Test suite for DecryptionMediator"""

    NUMBER_OF_GUARDIANS = 3
    QUORUM = 2
    CEREMONY_DETAILS = CeremonyDetails(NUMBER_OF_GUARDIANS, QUORUM)
    internal_manifest: InternalManifest

    def setUp(self):

        # Key Ceremony
        key_ceremony_mediator = KeyCeremonyMediator(
            "key_ceremony_mediator_mediator", self.CEREMONY_DETAILS
        )
        self.guardians: List[Guardian] = KeyCeremonyHelper.create_guardians(
            self.CEREMONY_DETAILS
        )
        KeyCeremonyHelper.perform_full_ceremony(self.guardians, key_ceremony_mediator)
        self.joint_public_key = key_ceremony_mediator.publish_joint_key()
        self.assertIsNotNone(self.joint_public_key)

        # Setup the election
        manifest = election_factory.get_fake_manifest()
        builder = ElectionBuilder(self.NUMBER_OF_GUARDIANS, self.QUORUM, manifest)

        self.assertIsNone(builder.build())  # Can't build without the public key

        builder.set_public_key(self.joint_public_key.joint_public_key)
        builder.set_commitment_hash(self.joint_public_key.commitment_hash)
        self.internal_manifest, self.context = get_optional(builder.build())

        self.encryption_device = election_factory.get_encryption_device()
        self.ballot_marking_device = EncryptionMediator(
            self.internal_manifest, self.context, self.encryption_device
        )

        # get some fake ballots
        self.fake_cast_ballot = ballot_factory.get_fake_ballot(
            self.internal_manifest, "some-unique-ballot-id-cast"
        )
        more_fake_ballots = []
        for i in range(10):
            more_fake_ballots.append(
                ballot_factory.get_fake_ballot(
                    self.internal_manifest, f"some-unique-ballot-id-cast{i}"
                )
            )
        self.fake_spoiled_ballot = ballot_factory.get_fake_ballot(
            self.internal_manifest, "some-unique-ballot-id-spoiled"
        )
        more_fake_spoiled_ballots = []
        for i in range(2):
            more_fake_spoiled_ballots.append(
                ballot_factory.get_fake_ballot(
                    self.internal_manifest, f"some-unique-ballot-id-spoiled{i}"
                )
            )
        self.assertTrue(
            self.fake_cast_ballot.is_valid(
                self.internal_manifest.ballot_styles[0].object_id
            )
        )
        self.assertTrue(
            self.fake_spoiled_ballot.is_valid(
                self.internal_manifest.ballot_styles[0].object_id
            )
        )
        self.expected_plaintext_tally = accumulate_plaintext_ballots(
            [self.fake_cast_ballot] + more_fake_ballots
        )

        # Fill in the expected values with any missing selections
        # that were not made on any ballots
        selection_ids = {
            selection.object_id
            for contest in self.internal_manifest.contests
            for selection in contest.ballot_selections
        }

        missing_selection_ids = selection_ids.difference(
            set(self.expected_plaintext_tally)
        )

        for id in missing_selection_ids:
            self.expected_plaintext_tally[id] = 0

        # Encrypt
        self.encrypted_fake_cast_ballot = self.ballot_marking_device.encrypt(
            self.fake_cast_ballot
        )
        self.encrypted_fake_spoiled_ballot = self.ballot_marking_device.encrypt(
            self.fake_spoiled_ballot
        )
        self.assertIsNotNone(self.encrypted_fake_cast_ballot)
        self.assertIsNotNone(self.encrypted_fake_spoiled_ballot)
        self.assertTrue(
            self.encrypted_fake_cast_ballot.is_valid_encryption(
                self.internal_manifest.manifest_hash,
                self.joint_public_key.joint_public_key,
                self.context.crypto_extended_base_hash,
            )
        )

        # encrypt some more fake ballots
        more_fake_encrypted_ballots = []
        for fake_ballot in more_fake_ballots:
            more_fake_encrypted_ballots.append(
                self.ballot_marking_device.encrypt(fake_ballot)
            )
        # encrypt some more fake ballots
        self.more_fake_encrypted_spoiled_ballots = []
        for fake_ballot in more_fake_spoiled_ballots:
            self.more_fake_encrypted_spoiled_ballots.append(
                self.ballot_marking_device.encrypt(fake_ballot)
            )

        # configure the ballot box
        ballot_store = DataStore()
        ballot_box = BallotBox(self.internal_manifest, self.context, ballot_store)
        ballot_box.cast(self.encrypted_fake_cast_ballot)
        ballot_box.spoil(self.encrypted_fake_spoiled_ballot)

        # Cast some more fake ballots
        for fake_ballot in more_fake_encrypted_ballots:
            ballot_box.cast(fake_ballot)
        # Spoil some more fake ballots
        for fake_ballot in self.more_fake_encrypted_spoiled_ballots:
            ballot_box.spoil(fake_ballot)

        # generate encrypted tally
        self.ciphertext_tally = tally_ballots(
            ballot_store, self.internal_manifest, self.context
        )
        self.ciphertext_ballots = get_ballots(ballot_store, BallotBoxState.SPOILED)

    def test_announce(self):
        # Arrange
        subject = DecryptionMediator(
            self.context,
            self.ciphertext_tally,
            self.ciphertext_ballots,
        )

        # act
        result = subject.announce(self.guardians[0])

        # assert
        self.assertIsNotNone(result)

        # Can only announce once
        self.assertIsNotNone(subject.announce(self.guardians[0]))

        # Cannot get plaintext tally or spoiled ballots without a quorum
        self.assertIsNone(subject.get_plaintext_tally())
        self.assertIsNone(subject.get_plaintext_ballots())

        # Assert a second
        self.assertIsNotNone(subject.announce(self.guardians[1]))

    def test_get_plaintext_tally_all_guardians_present_simple(self):
        # Arrange
        decrypter = DecryptionMediator(self.context, self.ciphertext_tally, {})

        # act
        for guardian in self.guardians:
            self.assertIsNotNone(decrypter.announce(guardian))

        decrypted_tallies = decrypter.get_plaintext_tally()
        spoiled_ballots = decrypter.get_plaintext_ballots()
        result = _convert_to_selections(decrypted_tallies)

        # assert
        self.assertIsNotNone(result)
        self.assertIsNotNone(spoiled_ballots)
        self.assertEqual(self.expected_plaintext_tally, result)

        # Verify we get the same tally back if we call again
        another_decrypted_tally = decrypter.get_plaintext_tally()

        self.assertEqual(decrypted_tallies, another_decrypted_tally)

    def test_get_plaintext_tally_compensate_missing_guardian_simple(self):

        # Arrange
        decrypter = DecryptionMediator(
            self.context,
            self.ciphertext_tally,
            self.ciphertext_ballots,
        )

        # Act

        self.assertIsNotNone(decrypter.announce(self.guardians[0]))
        self.assertIsNotNone(decrypter.announce(self.guardians[1]))

        decrypted_tallies = decrypter.get_plaintext_tally(identity_auxiliary_decrypt)
        self.assertIsNotNone(decrypted_tallies)
        result = _convert_to_selections(decrypted_tallies)

        # assert
        self.assertIsNotNone(result)
        print(result)
        self.assertEqual(self.expected_plaintext_tally, result)

    @settings(
        deadline=timedelta(milliseconds=15000),
        suppress_health_check=[HealthCheck.too_slow],
        max_examples=8,
        # disabling the "shrink" phase, because it runs very slowly
        phases=[Phase.explicit, Phase.reuse, Phase.generate, Phase.target],
    )
    @given(data(), integers(1, 3), integers(2, 5))
    def test_get_plaintext_tally_all_guardians_present(
        self, values, parties: int, contests: int
    ):
        # Arrange
        description = values.draw(election_descriptions(parties, contests))
        builder = ElectionBuilder(self.NUMBER_OF_GUARDIANS, self.QUORUM, description)
        internal_manifest, context = (
            builder.set_public_key(self.joint_public_key.joint_public_key)
            .set_commitment_hash(self.joint_public_key.commitment_hash)
            .build()
        )

        plaintext_ballots: List[PlaintextBallot] = values.draw(
            plaintext_voted_ballots(internal_manifest, randrange(3, 6))
        )
        plaintext_tallies = accumulate_plaintext_ballots(plaintext_ballots)

        encrypted_tally = self._generate_encrypted_tally(
            internal_manifest, context, plaintext_ballots
        )

        decrypter = DecryptionMediator(context, encrypted_tally, {})

        # act
        for guardian in self.guardians:
            self.assertIsNotNone(decrypter.announce(guardian))

        decrypted_tallies = decrypter.get_plaintext_tally()
        spoiled_ballots = decrypter.get_plaintext_ballots()
        result = _convert_to_selections(decrypted_tallies)

        # assert
        self.assertIsNotNone(result)
        self.assertIsNotNone(spoiled_ballots)
        self.assertEqual(plaintext_tallies, result)

    def _generate_encrypted_tally(
        self,
        internal_manifest: InternalManifest,
        context: CiphertextElectionContext,
        ballots: List[PlaintextBallot],
    ) -> CiphertextTally:

        # encrypt each ballot
        store = DataStore()
        for ballot in ballots:
            encrypted_ballot = encrypt_ballot(
                ballot, internal_manifest, context, int_to_q_unchecked(1)
            )
            self.assertIsNotNone(encrypted_ballot)
            # add to the ballot store
            store.set(
                encrypted_ballot.object_id,
                from_ciphertext_ballot(encrypted_ballot, BallotBoxState.CAST),
            )

        tally = tally_ballots(store, internal_manifest, context)
        self.assertIsNotNone(tally)
        return get_optional(tally)


def _convert_to_selections(tally: PlaintextTally) -> Dict[str, int]:
    plaintext_selections: Dict[str, int] = {}
    for _, contest in tally.contests.items():
        for selection_id, selection in contest.selections.items():
            plaintext_selections[selection_id] = selection.tally

    return plaintext_selections