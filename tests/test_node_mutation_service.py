import dataclasses
import unittest

from workbench.application.node_mutation import NodeDeleteCommand, NodeMutationError, NodeMutationService, NodeUpdateCommand
from workbench.domain.canvas.models import Position


class Authorizer:
    def __init__(self, allowed=True):
        self.allowed = allowed

    def can_edit(self, *args):
        return self.allowed


class Repository:
    def update_node(self, command):
        return "updated"

    def delete_node(self, command):
        return "deleted"


class Audit:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)


class NodeMutationServiceTests(unittest.TestCase):
    def command(self):
        return dict(actor_id="user", project_id="project", canvas_id="canvas", node_id="node", expected_revision=1)

    def test_updates_and_deletes_through_authorized_audited_boundary(self):
        audit = Audit()
        service = NodeMutationService(authorizer=Authorizer(), repository=Repository(), audit_sink=audit)
        self.assertEqual(service.update(NodeUpdateCommand(**self.command(), position=Position(x=1, y=2))), "updated")
        self.assertEqual(service.delete(NodeDeleteCommand(**self.command())), "deleted")
        self.assertEqual([type(event).__name__ for event in audit.events], ["NodeUpdatedAuditEvent", "NodeDeletedAuditEvent"])

    def test_rejects_unauthorized_or_empty_update(self):
        service = NodeMutationService(authorizer=Authorizer(False), repository=Repository(), audit_sink=Audit())
        with self.assertRaisesRegex(NodeMutationError, "not permitted"):
            service.delete(NodeDeleteCommand(**self.command()))
        with self.assertRaisesRegex(NodeMutationError, "mutable"):
            NodeMutationService(authorizer=Authorizer(), repository=Repository(), audit_sink=Audit()).update(
                NodeUpdateCommand(**self.command())
            )

    def test_update_command_contract_contains_only_title_and_position_mutations(self):
        fields = {field.name for field in dataclasses.fields(NodeUpdateCommand)}
        self.assertEqual(
            fields,
            {"actor_id", "project_id", "canvas_id", "node_id", "expected_revision", "title", "position"},
        )
