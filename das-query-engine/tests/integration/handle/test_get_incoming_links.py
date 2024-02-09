import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction


class TestGetIncomingLinksAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.GET_INCOMING_LINKS

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "atom_handle": "af12f10f9ae2002a1607ba0b47ba8407",
                    "kwargs": {
                        "targets_document": True,
                    },
                },
            }
        }

    @pytest.fixture
    def expected_output(self):
        return [
            [
                {
                    "handle": "16f7e407087bfa0b35b13d13a1aadcae",
                    "composite_type_hash": "ed73ea081d170e1d89fc950820ce1cee",
                    "is_toplevel": True,
                    "composite_type": [
                        "a9dea78180588431ec64d6bc4872fdbc",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                    ],
                    "named_type": "Similarity",
                    "named_type_hash": "a9dea78180588431ec64d6bc4872fdbc",
                    "targets": [
                        "af12f10f9ae2002a1607ba0b47ba8407",
                        "4e8e26e3276af8a5c2ac2cc2dc95c6d2",
                    ],
                    "type": "Similarity",
                },
                [
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "human",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                    {
                        "handle": "4e8e26e3276af8a5c2ac2cc2dc95c6d2",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "ent",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                ],
            ],
            [
                {
                    "handle": "a45af31b43ee5ea271214338a5a5bd61",
                    "composite_type_hash": "ed73ea081d170e1d89fc950820ce1cee",
                    "is_toplevel": True,
                    "composite_type": [
                        "a9dea78180588431ec64d6bc4872fdbc",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                    ],
                    "named_type": "Similarity",
                    "named_type_hash": "a9dea78180588431ec64d6bc4872fdbc",
                    "targets": [
                        "4e8e26e3276af8a5c2ac2cc2dc95c6d2",
                        "af12f10f9ae2002a1607ba0b47ba8407",
                    ],
                    "type": "Similarity",
                },
                [
                    {
                        "handle": "4e8e26e3276af8a5c2ac2cc2dc95c6d2",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "ent",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "human",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                ],
            ],
            [
                {
                    "handle": "2c927fdc6c0f1272ee439ceb76a6d1a4",
                    "composite_type_hash": "ed73ea081d170e1d89fc950820ce1cee",
                    "is_toplevel": True,
                    "composite_type": [
                        "a9dea78180588431ec64d6bc4872fdbc",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                    ],
                    "named_type": "Similarity",
                    "named_type_hash": "a9dea78180588431ec64d6bc4872fdbc",
                    "targets": [
                        "5b34c54bee150c04f9fa584b899dc030",
                        "af12f10f9ae2002a1607ba0b47ba8407",
                    ],
                    "type": "Similarity",
                },
                [
                    {
                        "handle": "5b34c54bee150c04f9fa584b899dc030",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "chimp",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "human",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                ],
            ],
            [
                {
                    "handle": "b5459e299a5c5e8662c427f7e01b3bf1",
                    "composite_type_hash": "ed73ea081d170e1d89fc950820ce1cee",
                    "is_toplevel": True,
                    "composite_type": [
                        "a9dea78180588431ec64d6bc4872fdbc",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                    ],
                    "named_type": "Similarity",
                    "named_type_hash": "a9dea78180588431ec64d6bc4872fdbc",
                    "targets": [
                        "af12f10f9ae2002a1607ba0b47ba8407",
                        "5b34c54bee150c04f9fa584b899dc030",
                    ],
                    "type": "Similarity",
                },
                [
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "human",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                    {
                        "handle": "5b34c54bee150c04f9fa584b899dc030",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "chimp",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                ],
            ],
            [
                {
                    "handle": "c93e1e758c53912638438e2a7d7f7b7f",
                    "composite_type_hash": "41c082428b28d7e9ea96160f7fd614ad",
                    "is_toplevel": True,
                    "composite_type": [
                        "e40489cd1e7102e35469c937e05c8bba",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                    ],
                    "named_type": "Inheritance",
                    "named_type_hash": "e40489cd1e7102e35469c937e05c8bba",
                    "targets": [
                        "af12f10f9ae2002a1607ba0b47ba8407",
                        "bdfe4e7a431f73386f37c6448afe5840",
                    ],
                    "type": "Inheritance",
                },
                [
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "human",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                    {
                        "handle": "bdfe4e7a431f73386f37c6448afe5840",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "mammal",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                ],
            ],
            [
                {
                    "handle": "2a8a69c01305563932b957de4b3a9ba6",
                    "composite_type_hash": "ed73ea081d170e1d89fc950820ce1cee",
                    "is_toplevel": True,
                    "composite_type": [
                        "a9dea78180588431ec64d6bc4872fdbc",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                    ],
                    "named_type": "Similarity",
                    "named_type_hash": "a9dea78180588431ec64d6bc4872fdbc",
                    "targets": [
                        "1cdffc6b0b89ff41d68bec237481d1e1",
                        "af12f10f9ae2002a1607ba0b47ba8407",
                    ],
                    "type": "Similarity",
                },
                [
                    {
                        "handle": "1cdffc6b0b89ff41d68bec237481d1e1",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "monkey",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "human",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                ],
            ],
            [
                {
                    "handle": "bad7472f41a0e7d601ca294eb4607c3a",
                    "composite_type_hash": "ed73ea081d170e1d89fc950820ce1cee",
                    "is_toplevel": True,
                    "composite_type": [
                        "a9dea78180588431ec64d6bc4872fdbc",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "d99a604c79ce3c2e76a2f43488d5d4c3",
                    ],
                    "named_type": "Similarity",
                    "named_type_hash": "a9dea78180588431ec64d6bc4872fdbc",
                    "targets": [
                        "af12f10f9ae2002a1607ba0b47ba8407",
                        "1cdffc6b0b89ff41d68bec237481d1e1",
                    ],
                    "type": "Similarity",
                },
                [
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "human",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                    {
                        "handle": "1cdffc6b0b89ff41d68bec237481d1e1",
                        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
                        "name": "monkey",
                        "named_type": "Concept",
                        "type": "Concept",
                    },
                ],
            ],
        ]

    def test_incoming_links_action(
        self,
        valid_event,
        expected_output,
    ):
        self.assert_successful_execution(valid_event, expected_output)

    def test_malformed_payload(self, malformed_event):
        self.assert_payload_malformed(malformed_event)

    def test_unknown_action(self, unknown_action_event):
        self.assert_unknown_action_dispatcher(unknown_action_event)

    def test_unexpected_exception(
        self,
        mocker,
        valid_event,
    ):
        self.assert_unexpected_exception(mocker, valid_event)
