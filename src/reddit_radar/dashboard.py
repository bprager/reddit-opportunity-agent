from .briefing import DEFAULT_DATABASE_URL, _sqlite_path
from .storage import ALLOWED_DECISIONS, OpportunityStore


def build_dashboard_sections(store: OpportunityStore) -> dict[str, list[dict]]:
    assessments = store.list_assessments(limit=100)
    open_items = [item for item in assessments if item["decision"] is None]

    return {
        "remote_opportunities": [
            item for item in open_items if item["category"] == "remote_opportunity"
        ],
        "local_client_leads": [
            item for item in open_items if item["category"] == "local_client_lead"
        ],
        "rejected_items": [
            item for item in assessments if item["category"] == "reject"
        ],
        "followups": store.list_by_decision("follow_up", limit=50),
    }


def main() -> None:
    import streamlit as st

    store = OpportunityStore(_sqlite_path(DEFAULT_DATABASE_URL))
    store.init_schema()
    sections = build_dashboard_sections(store)

    st.set_page_config(page_title="Reddit Opportunity Radar", layout="wide")
    st.title("Reddit Opportunity Radar")

    _render_section(st, store, "Top Remote Opportunities", sections["remote_opportunities"])
    _render_section(st, store, "Top Local Client Leads", sections["local_client_leads"])
    _render_section(st, store, "Rejected Items", sections["rejected_items"])
    _render_section(st, store, "Follow-ups", sections["followups"])


def _render_section(
    st: object,
    store: OpportunityStore,
    title: str,
    items: list[dict],
) -> None:
    st.header(title)
    if not items:
        st.info("No items.")
        return

    for item in items:
        with st.container(border=True):
            st.subheader(item["title"])
            st.write(f"Score: {item['score']}")
            st.write(f"Source: {item['source']}")
            st.write(f"Category: {item['category']}")
            st.write(f"Risks: {', '.join(item['risk_flags']) or 'none'}")
            st.write(item["recommended_action"])
            st.link_button("Open source", item["url"])
            _render_decision_controls(st, store, item)


def _render_decision_controls(
    st: object,
    store: OpportunityStore,
    item: dict,
) -> None:
    decision_options = sorted(ALLOWED_DECISIONS)
    current_decision = item["decision"] or "saved"
    selected = st.selectbox(
        "Decision",
        decision_options,
        index=decision_options.index(current_decision),
        key=f"decision-{item['assessment_id']}",
    )
    notes = st.text_input("Notes", key=f"notes-{item['assessment_id']}")
    if st.button("Save decision", key=f"save-{item['assessment_id']}"):
        store.record_decision(
            assessment_id=item["assessment_id"],
            decision=selected,
            notes=notes,
        )
        st.rerun()


if __name__ == "__main__":
    main()
