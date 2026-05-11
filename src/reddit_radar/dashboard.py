import streamlit as st


def main() -> None:
    st.set_page_config(page_title="Reddit Opportunity Radar", layout="wide")
    st.title("Reddit Opportunity Radar")
    st.write("MVP dashboard placeholder.")
    st.info("Next step: connect this to SQLite and show top scored items.")


if __name__ == "__main__":
    main()
