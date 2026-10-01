import streamlit as st
import requests

from backend.utils.documents import (
    format_docx,
    format_pdf,
    format_txt,
    safe_filename,
)

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide",
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 0;
        }

        .subtitle {
            font-size: 18px;
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-top: 10px;
        }

        .stButton > button {
            width: 100%;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.markdown(
    '<div class="main-title">⚖️ LegalEase AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    backend_url = st.text_input(
        "Backend URL",
        value="http://127.0.0.1:8000",
    )

    st.divider()

    st.info(
        "Make sure the FastAPI backend is running before "
        "clicking Generate Document."
    )

# ---------------------------------------------------------
# MAIN FORM
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📝 Create Legal Document</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Rental Agreement",
            "Service Agreement",
            "Consulting Agreement",
            "Partnership Agreement",
            "Freelance Agreement",
            "Sale Agreement",
            "Leave and License Agreement",
            "Custom Legal Document",
        ],
    )

    parties = st.text_area(
        "Parties / Names",
        placeholder=(
            "Example:\n"
            "Jane Doe - Employee\n"
            "ABC Technologies Pvt Ltd - Employer"
        ),
        height=140,
    )

    effective_date = st.text_input(
        "Effective Date",
        placeholder="Example: 1 October 2026",
    )

with col2:
    jurisdiction = st.text_input(
        "Jurisdiction",
        placeholder="Example: Tamil Nadu, India",
    )

    terms = st.text_area(
        "Important Terms / Conditions",
        placeholder=(
            "Enter the important terms of the agreement.\n\n"
            "Example:\n"
            "- Salary: ₹50,000 per month\n"
            "- Working hours: 9 AM to 6 PM\n"
            "- Contract duration: 1 year"
        ),
        height=140,
    )

    additional_instructions = st.text_area(
        "Additional Instructions",
        placeholder=(
            "Example: Generate a formal professional legal document "
            "with clear clauses and signature sections."
        ),
        height=140,
    )

# ---------------------------------------------------------
# GENERATE BUTTON
# ---------------------------------------------------------
st.divider()

generate = st.button(
    "⚡ Generate Document",
    type="primary",
    use_container_width=True,
)

if generate:

    if not parties.strip():
        st.error("❌ Please enter the parties / names.")
        st.stop()

    if not terms.strip():
        st.error("❌ Please enter the important terms.")
        st.stop()

    if not jurisdiction.strip():
        st.error("❌ Please enter the jurisdiction.")
        st.stop()

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": effective_date,
        "jurisdiction": jurisdiction,
        "additional_instructions": additional_instructions,
    }

    with st.spinner("🤖 Generating your legal document..."):

        try:
            response = requests.post(
                f"{backend_url}/generate",
                json=payload,
                timeout=120,
            )

            if response.status_code == 200:

                data = response.json()

                # Support common response field names
                generated_text = (
                    data.get("document")
                    or data.get("content")
                    or data.get("generated_document")
                    or data.get("text")
                    or ""
                )

                if generated_text:

                    st.session_state.generated_document = generated_text
                    st.session_state.document_type = document_type

                    st.success(
                        "✅ Legal document generated successfully!"
                    )

                else:
                    st.error(
                        "❌ Backend response did not contain "
                        "the generated document."
                    )

                    st.json(data)

            else:
                st.error(
                    f"❌ Backend Error: HTTP {response.status_code}"
                )

                try:
                    st.json(response.json())
                except Exception:
                    st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Backend is not running.\n\n"
                "Please start FastAPI using:\n"
                "`python -m uvicorn backend.main:app --reload --port 8000`"
            )

        except requests.exceptions.Timeout:
            st.error(
                "⏳ Request timed out. "
                "The AI model took too long to respond."
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------------------------------------------------------
# GENERATED DOCUMENT
# ---------------------------------------------------------
if st.session_state.generated_document:

    st.divider()

    st.markdown(
        '<div class="section-title">📄 Generated Document</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(
        ["👁️ Preview", "✏️ Edit"]
    )

    # -----------------------------------------------------
    # PREVIEW
    # -----------------------------------------------------
    with tab1:

        st.markdown("### Document Preview")

        preview_text = st.session_state.generated_document

        st.text_area(
            "Generated Legal Document",
            value=preview_text,
            height=650,
            disabled=True,
            label_visibility="collapsed",
        )

    # -----------------------------------------------------
    # EDIT
    # -----------------------------------------------------
    with tab2:

        st.markdown("### Edit Document")

        edited_document = st.text_area(
            "Edit your document",
            value=st.session_state.generated_document,
            height=650,
            key="edited_document",
        )

        if st.button(
            "💾 Save Edits",
            use_container_width=True,
        ):
            st.session_state.generated_document = edited_document
            st.success("✅ Changes saved successfully!")

    # -----------------------------------------------------
    # DOWNLOADS
    # -----------------------------------------------------
    st.divider()

    st.markdown("### 📥 Download Document")

    final_document = st.session_state.generated_document

    filename_base = safe_filename(
        st.session_state.document_type or "LegalEase_Document"
    )

    col1, col2, col3 = st.columns(3)

    # -----------------------------------------------------
    # TXT
    # -----------------------------------------------------
    with col1:

        txt_data = format_txt(final_document)

        st.download_button(
            label="📄 Download TXT",
            data=txt_data,
            file_name=f"{filename_base}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # -----------------------------------------------------
    # DOCX
    # -----------------------------------------------------
    with col2:

        try:
            docx_data = format_docx(final_document)

            st.download_button(
                label="📝 Download DOCX",
                data=docx_data,
                file_name=f"{filename_base}.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"DOCX generation error: {e}")

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------
    with col3:

        try:
            pdf_data = format_pdf(final_document)

            st.download_button(
                label="📕 Download PDF",
                data=pdf_data,
                file_name=f"{filename_base}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"PDF generation error: {e}")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "⚖️ LegalEase AI | AI-powered legal document generation"
)