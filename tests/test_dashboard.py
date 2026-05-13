import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from reddit_radar.dashboard import (
    _render_decision_controls,
    _render_section,
    build_dashboard_sections,
)
from reddit_radar.storage import OpportunityStore

from helpers import save_example
from test_regression_examples import load_examples


class DashboardTests(unittest.TestCase):
    def test_dashboard_sections_use_stored_assessments(self) -> None:
        examples = load_examples()

        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            for example in examples:
                save_example(store, example)

            sections = build_dashboard_sections(store)

        self.assertTrue(sections["remote_opportunities"])
        self.assertTrue(sections["local_client_leads"])
        self.assertTrue(sections["rejected_items"])
        self.assertEqual(
            "[Hiring] Build an internal AI workflow for support triage",
            sections["remote_opportunities"][0]["title"],
        )
        self.assertIn("score", sections["remote_opportunities"][0])

    def test_render_section_handles_empty_and_populated_items(self) -> None:
        class Container:
            def __enter__(self) -> "Container":
                return self

            def __exit__(self, *_args: object) -> None:
                return None

        class FakeStreamlit:
            def __init__(self) -> None:
                self.calls: list[tuple[str, object]] = []

            def header(self, title: str) -> None:
                self.calls.append(("header", title))

            def info(self, message: str) -> None:
                self.calls.append(("info", message))

            def container(self, border: bool = False) -> Container:
                self.calls.append(("container", border))
                return Container()

            def subheader(self, title: str) -> None:
                self.calls.append(("subheader", title))

            def write(self, value: object) -> None:
                self.calls.append(("write", value))

            def link_button(self, label: str, url: str) -> None:
                self.calls.append(("link_button", (label, url)))

            def selectbox(
                self,
                _label: str,
                options: list[str],
                index: int,
                key: str,
            ) -> str:
                self.calls.append(("selectbox", key))
                return options[index]

            def text_input(self, _label: str, key: str) -> str:
                self.calls.append(("text_input", key))
                return "reviewed"

            def button(self, _label: str, key: str) -> bool:
                self.calls.append(("button", key))
                return False

        class Store:
            def record_decision(self, assessment_id: int, decision: str, notes: str) -> None:
                raise AssertionError("button was not pressed")

        item = {
            "assessment_id": 7,
            "title": "Need Python build",
            "score": 88,
            "source": "r/forhire",
            "category": "remote_opportunity",
            "risk_flags": [],
            "recommended_action": "review",
            "url": "https://reddit.com/7",
            "decision": None,
        }
        st = FakeStreamlit()

        _render_section(st, Store(), "Empty", [])
        _render_section(st, Store(), "Items", [item])

        self.assertIn(("info", "No items."), st.calls)
        self.assertIn(("subheader", "Need Python build"), st.calls)

    def test_decision_controls_record_and_rerun_when_button_is_pressed(self) -> None:
        class FakeStreamlit:
            def __init__(self) -> None:
                self.reran = False

            def selectbox(self, _label: str, options: list[str], index: int, key: str) -> str:
                self.selected_key = key
                return "follow_up" if options[index] == "saved" else options[index]

            def text_input(self, _label: str, key: str) -> str:
                self.notes_key = key
                return "Worth a reply"

            def button(self, _label: str, key: str) -> bool:
                self.button_key = key
                return True

            def rerun(self) -> None:
                self.reran = True

        class Store:
            def __init__(self) -> None:
                self.recorded: tuple[int, str, str] | None = None

            def record_decision(self, assessment_id: int, decision: str, notes: str) -> None:
                self.recorded = (assessment_id, decision, notes)

        st = FakeStreamlit()
        store = Store()

        _render_decision_controls(
            st,
            store,
            {"assessment_id": 9, "decision": None},
        )

        self.assertEqual((9, "follow_up", "Worth a reply"), store.recorded)
        self.assertTrue(st.reran)

    def test_main_renders_all_sections(self) -> None:
        from reddit_radar import dashboard

        class FakeStore:
            def __init__(self, database_path: str) -> None:
                self.database_path = database_path

            def init_schema(self) -> None:
                return None

            def list_assessments(self, limit: int = 100) -> list[dict]:
                return []

            def list_by_decision(self, decision: str, limit: int = 50) -> list[dict]:
                return []

        calls: list[tuple[str, object]] = []
        fake_streamlit = SimpleNamespace(
            set_page_config=lambda **kwargs: calls.append(("page", kwargs)),
            title=lambda value: calls.append(("title", value)),
            header=lambda value: calls.append(("header", value)),
            info=lambda value: calls.append(("info", value)),
        )

        with (
            patch.dict("sys.modules", {"streamlit": fake_streamlit}),
            patch.object(dashboard, "OpportunityStore", FakeStore),
        ):
            dashboard.main()

        self.assertEqual(
            [
                "Top Remote Opportunities",
                "Top Local Client Leads",
                "Rejected Items",
                "Follow-ups",
            ],
            [value for name, value in calls if name == "header"],
        )


if __name__ == "__main__":
    unittest.main()
