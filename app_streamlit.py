import streamlit as st
import uuid
import os
from typing import Optional
from supabase import create_client
import logging

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logger.info(f"🚀 New session started: {st.session_state.session_id}")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_checklist" not in st.session_state:
    st.session_state.document_checklist = {}

# --- Import your bridge functions AFTER initialization ---
from bridge.router_bridge import run_chitchat, run_eligibility, run_documents, run_sop

# --- Supabase Client for Document Library ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("Supabase client initialized successfully.")
except Exception as e:
    supabase = None
    logger.error(f"Failed to initialize Supabase client: {e}")
    st.error("Could not connect to Supabase. Document library will be unavailable.")

# --- Page Config ---
st.set_page_config(page_title="ImmigrationGPT", page_icon="🇨🇦", layout="wide")
st.markdown("""
    <style>
        /* Your CSS styles here - unchanged */
    </style>
""", unsafe_allow_html=True)

# --- Custom CSS for better styling ---
st.markdown("""
    <style>
    .stMetric {
        background-color: #23272f;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .card {
        background-color: #23272f;
        padding: 1.2em 1.5em;
        margin-bottom: 1em;
        border-radius: 10px;
        border-left: 4px solid #FFD700;
    }
    .card h4 {
        color: #FFD700;
        margin-top: 0;
    }
    .program-detail {
        color: #bbb;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# --- LEFT Sidebar with session management ---
with st.sidebar:
    st.header("⚙️ Session Management")
    st.info(f"Session ID: `{st.session_state.session_id[:8]}...`")
    
    # This is the corrected logic
    if st.button("🔄 Start New Session", use_container_width=True):
        # Clear the entire session state
        st.session_state.clear()
        
        # Generate a BRAND NEW session ID to truly reset the memory
        st.session_state.session_id = str(uuid.uuid4())
        
        logger.info(f"🚀 New session explicitly started: {st.session_state.session_id}")
        
        # Rerun the app to reflect the new, empty session
        st.rerun()
    

# --- UI: Main Panel ---
st.title("🇨🇦 ImmigrationGPT")
st.caption("Your AI-powered Canadian immigration assistant")


# --- Add a one-time welcome message if the chat is empty ---
if not st.session_state.messages:
    welcome_message = {
        "role": "assistant",
        "content": "👋 Welcome to ImmigrationGPT! I can help you with Canadian immigration eligibility, document checklists, and drafting professional documents. What would you like to know?"
    }
    st.session_state.messages.append(welcome_message)

# --- 2. Helper Functions to Display Rich Data ---

def display_eligibility_results(user_profile, eligible, ineligible, crs, improvement, steps, followup):
    """Renders a beautiful UI for the eligibility agent's response."""
    crs_value_to_check = str(crs) if crs is not None else ""

    if crs_value_to_check and crs_value_to_check.lower() != "none" and crs_value_to_check.isdigit():
        st.metric(label="📊 Estimated CRS Score", value=int(crs_value_to_check))
    elif crs_value_to_check:
        st.info(f"**CRS Score:** {crs_value_to_check}")

    if eligible:
        st.success("🎉 You may be eligible for the following programs:")
        for program in eligible:
            if isinstance(program, dict):
                st.markdown(f"""
                    <div class="card">
                        <h4>{program.get('program_name', 'Unknown Program')}</h4>
                        <div class="program-detail"><b>Type:</b> {program.get('program_type', 'N/A')}</div>
                        <div class="program-detail"><b>Province:</b> {program.get('province', 'N/A')}</div>
                        <div class="program-detail" style="color:#7fdbca;margin-top:8px;">{program.get('reason', '')}</div>
                        {f'<a href="{program.get("official_url", "#")}" target="_blank" style="color:#FFD700;">Official Link →</a>' if program.get('official_url') and program.get('official_url') != "None" else ''}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"* **{program}**")

    if ineligible:
        with st.expander("❌ Programs you may not be eligible for"):
            for program in ineligible:
                if isinstance(program, dict):
                    st.markdown(f"**{program.get('program_name', program)}**: {program.get('reason', '')}")
                else:
                    st.markdown(f"* {program}")

    if improvement:
        with st.expander("💡 How to improve your profile", expanded=True):
            for item in improvement:
                action = item.get("action", "Unknown Action")
                steps_list = item.get("steps", [])
                st.markdown(f"**{action}**")
                if isinstance(steps_list, list):
                    for step in steps_list:
                        st.markdown(f"  - {step}")
                else:
                    st.markdown(f"  - {steps_list}")
                st.divider()

    if steps:
        st.info("**📋 Next Steps:**")
        for i, step in enumerate(steps, 1):
            st.markdown(f"{i}. {step}")

    if followup:
        st.warning("⚠️ Your profile requires a follow-up. Please provide more details.")

    with st.expander("👤 See your profile details"):
        st.json(user_profile)

# ___________ DOCUMENT RESULTS RENDERING ___________

def get_checked_items(checklist_state):
    """Filters the checklist from session_state to return only checked items."""
    return [item for item, checked in checklist_state.items() if checked]

# Add this new CSS to your main st.markdown block in app_streamlit.py
st.markdown("""
    <style>
        /* ... keep your other styles ... */
        .doc-card {
            border-left: 3px solid #007bff;
            padding: 1rem 1rem 0.5rem 1.5rem;
            margin-bottom: 1rem;
            background-color: #2a2f35;
            border-radius: 8px;
        }
        .doc-card .stCheckbox {
            border-bottom: 1px solid #3a3f45;
            padding-bottom: 0.8rem;
            margin-bottom: 0.8rem;
        }
        .doc-card-section {
            font-size: 0.95em;
            margin-bottom: 0.75rem;
        }
        .doc-card-section strong {
            color: #00aaff;
        }
        .doc-card-section p {
            margin: 0;
            padding: 0;
            color: #ccc;
        }
        .doc-card-links a {
            margin-right: 1rem;
            color: #17a2b8;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)


def display_document_results(
    program: str,
    overview: str,
    required_documents: list,
    conditional_documents: list,
    optional_but_recommended: list,
    forms: list,
    official_guide_url: str
):
    """
    Renders a rich, interactive, and detailed document checklist UI.
    """
    st.header(f"📄 Document Checklist: {program}")
    if overview:
        st.info(overview)
    if official_guide_url and official_guide_url != "N/A":
        st.link_button("📖 Official Program Guide", official_guide_url)

    if 'document_checklist' not in st.session_state:
        st.session_state.document_checklist = {}

    tab_list = []
    if required_documents: tab_list.append(f"Required ({len(required_documents)})")
    if conditional_documents: tab_list.append(f"Conditional ({len(conditional_documents)})")
    if optional_but_recommended: tab_list.append(f"Recommended ({len(optional_but_recommended)})")
    if forms: tab_list.append(f"Forms ({len(forms)})")

    if not tab_list:
        st.warning("The agent did not return any documents for this program.")
        return

    tabs = st.tabs(tab_list)
    tab_map = {tab_list[i]: tab for i, tab in enumerate(tabs)}

    def render_doc_list(tab_container, doc_list, list_type_prefix):
        with tab_container:
            if not doc_list:
                st.write("No documents in this category.")
                return

            for idx, doc_data in enumerate(doc_list):
                # Ensure doc_data is a dict from your Pydantic model
                if not isinstance(doc_data, dict):
                    st.warning(f"Skipping malformed document data: {doc_data}")
                    continue

                doc_name = doc_data.get("name", f"Unnamed Document #{idx}")
                unique_key = f"{list_type_prefix}_{program}_{doc_name}_{idx}"

                st.markdown('<div class="doc-card">', unsafe_allow_html=True)
                
                # Checkbox at the top
                is_checked = st.checkbox(
                    label=f"**{doc_name}**",
                    key=unique_key,
                    value=st.session_state.document_checklist.get(unique_key, False)
                )
                st.session_state.document_checklist[unique_key] = is_checked

                # Collapsible details
                with st.expander("Show Details & Tips"):
                    # Description
                    if doc_data.get("description"):
                        st.markdown(f"""<div class="doc-card-section">
                            <strong>What it is:</strong><p>{doc_data['description']}</p>
                        </div>""", unsafe_allow_html=True)

                    # Conditional logic
                    if doc_data.get("conditional_on"):
                        st.markdown(f"""<div class="doc-card-section">
                            <strong>When it’s needed:</strong><p>{doc_data['conditional_on']}</p>
                        </div>""", unsafe_allow_html=True)

                    # Tips
                    if doc_data.get("tips"):
                        st.markdown(f"""<div class="doc-card-section">
                            <strong>💡 Pro Tip:</strong><p>{doc_data['tips']}</p>
                        </div>""", unsafe_allow_html=True)

                    # Common Mistakes
                    if doc_data.get("common_mistakes"):
                        st.markdown(f"""<div class="doc-card-section">
                            <strong>❌ Common Mistakes:</strong><p>{doc_data['common_mistakes']}</p>
                        </div>""", unsafe_allow_html=True)
                    
                    # Links
                    if doc_data.get("source_url"):
                        st.markdown(f'<div class="doc-card-links"><a href="{doc_data["source_url"]}" target="_blank">Official Source →</a></div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

    def render_form_list(tab_container, form_list):
        with tab_container:
            if not form_list:
                st.write("No forms in this category.")
                return

            for idx, form_data in enumerate(form_list):
                if not isinstance(form_data, dict):
                    st.warning(f"Skipping malformed form data: {form_data}")
                    continue

                form_title = form_data.get("title", f"Unnamed Form #{idx}")
                form_num = form_data.get("form_number", "")
                unique_key = f"form_{program}_{form_num}_{idx}"
                
                label = f"**{form_num}: {form_title}**" if form_num else f"**{form_title}**"

                st.markdown('<div class="doc-card">', unsafe_allow_html=True)
                
                is_checked = st.checkbox(
                    label=label,
                    key=unique_key,
                    value=st.session_state.document_checklist.get(unique_key, False)
                )
                st.session_state.document_checklist[unique_key] = is_checked

                with st.expander("Download Links"):
                    links_html = ""
                    if form_data.get("pdf_url"):
                        links_html += f'<a href="{form_data["pdf_url"]}" target="_blank">Download PDF Form →</a>'
                    if form_data.get("instructions_url"):
                        if links_html: links_html += " &nbsp; | &nbsp; "
                        links_html += f'<a href="{form_data["instructions_url"]}" target="_blank">View Instructions →</a>'
                    
                    if links_html:
                        st.markdown(f'<div class="doc-card-links">{links_html}</div>', unsafe_allow_html=True)
                    else:
                        st.write("No links available.")
                
                st.markdown('</div>', unsafe_allow_html=True)

    # Populate tabs with the rich renderers
    if required_documents and f"Required ({len(required_documents)})" in tab_map:
        render_doc_list(tab_map[f"Required ({len(required_documents)})"], required_documents, "req")
    if conditional_documents and f"Conditional ({len(conditional_documents)})" in tab_map:
        render_doc_list(tab_map[f"Conditional ({len(conditional_documents)})"], conditional_documents, "cond")
    if optional_but_recommended and f"Recommended ({len(optional_but_recommended)})" in tab_map:
        render_doc_list(tab_map[f"Recommended ({len(optional_but_recommended)})"], optional_but_recommended, "opt")
    if forms and f"Forms ({len(forms)})" in tab_map:
        render_form_list(tab_map[f"Forms ({len(forms)})"], forms)

# ___________ SOP RESULTS RENDERING ___________

def display_sop_results(reply_text: str, pdf_file_url: Optional[str]):
    """Renders the UI for the SOP agent's response with Supabase URL."""
    logger.info(f"🎨 Rendering SOP: reply={reply_text[:50] if reply_text else 'None'}, url_exists={bool(pdf_file_url)}")
    
    if reply_text:
        st.info(reply_text)
    
    # Check if URL is valid
    if pdf_file_url and isinstance(pdf_file_url, str) and pdf_file_url.startswith("http"):
        st.success("✅ Your document has been generated and saved!")
        
        # Extract filename from URL for better display
        filename = pdf_file_url.split("/")[-1] if "/" in pdf_file_url else "Document.pdf"
        
        st.link_button(
            label=f"📥 Download {filename}",
            url=pdf_file_url,
            use_container_width=True
        )
        st.balloons()
        logger.info(f"✅ PDF download button displayed: {pdf_file_url[:80]}...")
    
    elif pdf_file_url:
        # URL exists but is invalid format
        st.error(f"❌ Invalid PDF URL format: {pdf_file_url[:100]}")
        logger.error(f"Invalid URL format: {pdf_file_url}")
    
    else:
        # No URL provided
        if reply_text:
            st.info("⏳ Document is being processed. Please check back in a moment.")
        else:
            st.info("💬 Please provide additional information if needed.")


# --- 3. Chat Interface ---

# Display all past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "results" in message:
            if message["type"] == "eligibility":
                display_eligibility_results(**message["results"])
            elif message["type"] == "documents":
                display_document_results(**message["results"])
            elif message["type"] == "sop":
                display_sop_results(**message["results"])

# Get new user input
if query := st.chat_input("Ask your immigration question..."):
    user_id = st.session_state.session_id
    logger.info(f"Processing query for user_id: {user_id}")

    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.markdown(query)  

    # --- 4. Agent Routing and Response ---
    status_placeholder = st.empty()
    
    try:
        with status_placeholder.container():
            with st.status("Thinking...", expanded=False) as status:
                status.update(label="Thinking...")
                reply, escalate_to = run_chitchat(query, user_id)

                if escalate_to:
                    escalate_to = escalate_to.lower()

                assistant_reply_content = ""
                results_to_store = None
                result_type = None

                if escalate_to == "eligibility_agent":
                    status.update(label="Running Eligibility Agent...")
                    user_profile, eligible, ineligible, crs, improvement, steps, followup = run_eligibility(query, user_id)
                    assistant_reply_content = f"I've analyzed your eligibility. Here's what I found:"
                    if crs and crs.lower() != "none":
                        assistant_reply_content = f"I've analyzed your eligibility. Your estimated CRS score is **{crs}**."
                    results_to_store = {
                        "user_profile": user_profile, "eligible": eligible, "ineligible": ineligible,
                        "crs": crs, "improvement": improvement, "steps": steps, "followup": followup
                    }
                    result_type = "eligibility"
                
                elif escalate_to == "document_agent":
                    status.update(label="Running Document Agent...")
                    (
                        program,
                        overview,
                        required_docs,
                        conditional_docs,
                        optional_docs,
                        forms,
                        guide_url,
                    ) = run_documents(query, user_id)                    
                    assistant_reply_content = f"I've generated a document checklist for the **{program}** program."
                    results_to_store = {
                        "program": program,
                        "overview": overview,
                        "required_documents": required_docs,  # MUST be 'required_documents', not 'required'
                        "conditional_documents": conditional_docs, # MUST be 'conditional_documents'
                        "optional_but_recommended": optional_docs, # MUST be 'optional_but_recommended'
                        "forms": forms,
                        "official_guide_url": guide_url,
                    }
                    result_type = "documents"


                elif escalate_to == "sop_agent":
                    status.update(label="Running SOP Agent...")
                    reply_text, pdf_file_url = run_sop(query, user_id)
                    assistant_reply_content = reply_text or "Your document request has been processed."
                    
                    logger.info(f"📄 SOP Result: reply_text={reply_text[:50]}, pdf_url={pdf_file_url[:50] if pdf_file_url else 'None'}")
                    
                    results_to_store = {
                        "reply_text": reply_text,
                        "pdf_file_url": pdf_file_url
                    }
                    result_type = "sop"

                elif reply:
                    assistant_reply_content = reply
                    result_type = None

                if not assistant_reply_content:
                    assistant_reply_content = "Sorry, I'm not sure how to help with that. Can you rephrase?"

                status.update(label="Done!", state="complete")
        
        # FIXED: Clear the status placeholder after response
        status_placeholder.empty()
        
    except Exception as e:
        status_placeholder.empty()
        st.error(f"An error occurred: {e}")
        logger.error(f"Error during agent run for user {user_id}: {e}", exc_info=True)
        assistant_reply_content = f"An error occurred: {e}"
        results_to_store = None
        result_type = None

    # --- 5. Display Assistant's Response ---
    with st.chat_message("assistant"):
        if assistant_reply_content:
            st.markdown(assistant_reply_content)
        if result_type == "eligibility" and results_to_store:
            display_eligibility_results(**results_to_store)
        elif result_type == "documents" and results_to_store:
            display_document_results(**results_to_store)
        elif result_type == "sop" and results_to_store:
            display_sop_results(**results_to_store)


    # --- 6. Save the full context to session state ---
    assistant_message = {"role": "assistant", "content": assistant_reply_content}
    if results_to_store:
        assistant_message["results"] = results_to_store
        assistant_message["type"] = result_type
    st.session_state.messages.append(assistant_message)
    
    # --- CRITICAL: Force sidebar refresh if PDF was generated ---
    if result_type == "sop" and results_to_store and results_to_store.get("pdf_file_url"):
        logger.info(f"🔄 PDF generated, forcing page refresh to update sidebar")
        st.rerun()

    st.rerun()
# ============================================
# RIGHT SIDEBAR - DOCUMENT LIBRARY (FIXED!)
# ============================================

with st.sidebar:
    st.divider()
    st.header("🗂️ My Documents")
    
    # Track found URLs to avoid duplicates
    found_urls = {}
    
    # First: Check recent SOP messages for URLs
    logger.info(f"📂 Checking recent messages for URLs...")
    for message in reversed(st.session_state.messages):
        if (message.get("type") == "sop" and 
            "results" in message and 
            message["results"].get("pdf_file_url")):
            
            pdf_url = message["results"]["pdf_file_url"]
            filename = pdf_url.split("/")[-1] if "/" in pdf_url else "Document.pdf"
            
            if filename not in found_urls:
                found_urls[filename] = pdf_url
                logger.info(f"📄 Found PDF in message: {filename}")
    
    # Second: Check Supabase for all files
    try:
        user_folder = st.session_state.session_id
        logger.info(f"📂 Fetching documents from Supabase for user: {user_folder}")
        
        files = supabase.storage.from_("user_documents").list(user_folder)
        logger.info(f"📂 Files in Supabase: {len(files) if files else 0}")
        
        if files and len(files) > 0:
            for file in files:
                file_name = file.get('name', file) if isinstance(file, dict) else file
                
                # Skip if we already found this from messages
                if file_name in found_urls:
                    continue
                
                file_url = supabase.storage.from_("user_documents").get_public_url(f"{user_folder}/{file_name}")
                found_urls[file_name] = file_url
                logger.info(f"📄 Added from Supabase: {file_name}")
        
    except Exception as e:
        logger.error(f"❌ Error loading from Supabase: {e}", exc_info=True)
    
    # Display all found documents
    if found_urls:
        st.success(f"**{len(found_urls)} document(s)** found")
        
        for filename, file_url in found_urls.items():
            logger.info(f"📍 Displaying: {filename} → {file_url[:60]}...")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"📄 **{filename}**")
            with col2:
                st.link_button("⬇️", file_url, use_container_width=True)
    else:
        st.info("✨ No documents yet.\n\nGenerate one by asking:\n- 'Write an SOP'\n- 'Create a letter'\n- 'Draft an EOI'")
    
    st.divider()
    st.subheader("💾 Save Session")
    email = st.text_input("Email (optional)", placeholder="your@email.com")
    if st.button("📧 Save & Email", use_container_width=True):
        if email:
            st.success(f"✅ Saved for {email}!")
        else:
            st.info("💡 Add an email to save your session.")
