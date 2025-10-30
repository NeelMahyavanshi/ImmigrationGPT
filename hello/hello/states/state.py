import reflex as rx
import asyncio
import uuid
from typing import Any, Optional, TypedDict
import logging
from datetime import datetime


class Download(TypedDict):
    name: str


class Program(TypedDict):
    program_name: str
    program_type: str
    province: str
    official_url: str
    reason: str
    missing_requirements: list[str]


class Document(TypedDict):
    name: str
    description: str
    mandatory: bool
    conditional_on: str
    source_url: str


class Form(TypedDict):
    form_number: str
    title: str
    pdf_url: str
    instructions_url: str


class EligibilityPayload(TypedDict):
    crs_estimate: int
    eligible_programs: list[Program]
    ineligible_programs: list[Program]


class DocumentsPayload(TypedDict):
    required_documents: list[Document]
    conditional_documents: list[Document]
    optional_but_recommended: list[Document]
    forms: list[Form]


class PanelData(TypedDict, total=False):
    crs_estimate: int
    eligible_programs: list[Program]
    ineligible_programs: list[Program]
    required_documents: list[Document]
    conditional_documents: list[Document]
    optional_but_recommended: list[Document]
    forms: list[Form]
    downloads: list[Download]


class Message(TypedDict):
    role: str
    text: str
    panel_type: str
    panel_data: PanelData


class HistoryItem(TypedDict):
    id: str
    question: str
    at: str


class Settings(TypedDict):
    use_supabase_memory: bool
    enable_streaming: bool
    theme: str


class AppState(rx.State):
    sidebar_open: bool = True
    downloads_open: bool = False
    history: list[HistoryItem] = []
    downloads: list[Download] = []
    settings: Settings = {
        "use_supabase_memory": False,
        "enable_streaming": True,
        "theme": "dark",
    }

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def toggle_downloads(self):
        self.downloads_open = not self.downloads_open

    @rx.event
    def add_to_history(self, question: str):
        self.history.append(
            {
                "id": str(uuid.uuid4()),
                "question": question,
                "at": datetime.now().strftime("%B %d, %Y %I:%M %p"),
            }
        )

    @rx.event
    def add_download(self, file: Download):
        self.downloads.append(file)

    @rx.event
    def update_setting(self, key: str, value: Any):
        self.settings[key] = value


class ChatState(AppState):
    messages: list[Message] = []
    user_input: str = ""
    loading: bool = False
    session_id: str = ""
    example_prompts: list[dict[str, str]] = [
        {
            "icon": "file-question",
            "title": "Check Eligibility for PR",
            "text": "Am I eligible for Canadian PR with 3 years of experience as a software engineer?",
        },
        {
            "icon": "list-checks",
            "title": "Get Document Checklist",
            "text": "What documents do I need for Express Entry?",
        },
        {
            "icon": "file-text",
            "title": "Draft a Statement of Purpose",
            "text": "Help me draft an SOP for a study permit application.",
        },
        {
            "icon": "calculator",
            "title": "Calculate my CRS Score",
            "text": "Calculate my CRS score with a Master's degree and IELTS 8 band.",
        },
    ]

    @rx.event
    def on_load(self):
        self.session_id = str(uuid.uuid4())

    def _add_message(
        self,
        role: str,
        text: str,
        panel_type: str = "",
        panel_data: PanelData | None = None,
    ):
        message: Message = {
            "role": role,
            "text": text,
            "panel_type": panel_type,
            "panel_data": panel_data or {},
        }
        self.messages.append(message)

    def _handle_response(self, response_json: dict, panel_type: str = ""):
        payload = response_json.get("payload", {})
        reply = response_json.get("reply", "")
        panel_data = payload if panel_type else {}
        files = response_json.get("files", [])
        if files:
            panel_type = "downloads"
            panel_data = {"downloads": files}
            for file in files:
                self.add_download(file)
        if reply or panel_type:
            self._add_message(
                "assistant", reply, panel_type=panel_type, panel_data=panel_data
            )

    async def _mock_chitchat(self):
        await asyncio.sleep(0.5)
        return {
            "reply": "Sure\\[em]what part of the process do you want help with: eligibility, document checklist, or SOP?",
            "files": [],
            "payload": {"escalate_to": "eligibility_agent"},
        }

    async def _mock_eligibility(self):
        await asyncio.sleep(1)
        return {
            "reply": "Here are programs that match your profile and any gaps to address.",
            "files": [],
            "payload": {
                "crs_estimate": 482,
                "eligible_programs": [
                    {
                        "program_name": "Express Entry \\[em] FSW",
                        "program_type": "Federal",
                        "province": "All",
                        "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html",
                        "reason": "Meets minimum eligibility and estimated CRS above historical cutoffs.",
                    },
                    {
                        "program_name": "OINP \\[em] Human Capital Priorities",
                        "program_type": "Provincial Nominee",
                        "province": "Ontario",
                        "official_url": "https://www.ontario.ca/page/ontario-immigrant-nominee-program-oinp",
                        "reason": "NOC in a targeted TEER and competitive CRS for periodic HCP draws.",
                    },
                ],
                "ineligible_programs": [
                    {
                        "program_name": "AIPP (Atlantic Immigration Program)",
                        "missing_requirements": [
                            "No qualifying job offer from an Atlantic employer",
                            "IELTS General not yet taken",
                        ],
                    }
                ],
            },
        }

    async def _mock_documents(self):
        await asyncio.sleep(1)
        return {
            "reply": "Here's the checklist for your study/work pathway with direct source links.",
            "files": [],
            "payload": {
                "required_documents": [
                    {
                        "name": "Valid Passport",
                        "description": "Clear scan of bio page and all visa stamps.",
                        "mandatory": True,
                        "source_url": "https://www.canada.ca/en/immigration-refugees-citizenship.html",
                    },
                    {
                        "name": "Digital Photo",
                        "description": "Meets IRCC photo specifications.",
                        "mandatory": True,
                        "source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/application/photographs.html",
                    },
                ],
                "conditional_documents": [
                    {
                        "name": "Police Certificate",
                        "description": "For countries where you lived 6+ months since age 18.",
                        "mandatory": False,
                        "conditional_on": "Residence history",
                        "source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/application/medical-police/police-certificates.html",
                    }
                ],
                "optional_but_recommended": [
                    {
                        "name": "Letters of Reference",
                        "description": "Confirms job duties and dates to support NOC claims.",
                        "mandatory": False,
                        "source_url": "https://noc.esdc.gc.ca/",
                    }
                ],
                "forms": [
                    {
                        "form_number": "IMM 1294",
                        "title": "Application for Study Permit Made Outside of Canada",
                        "pdf_url": "https://www.canada.ca/content/dam/ircc/migration/ircc/english/pdf/kits/forms/imm1294e.pdf",
                        "instructions_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides/application-study-permit-outside-canada.html",
                    },
                    {
                        "form_number": "IMM 5645",
                        "title": "Family Information Form",
                        "pdf_url": "https://www.canada.ca/content/dam/ircc/migration/ircc/english/pdf/kits/forms/imm5645e.pdf",
                    },
                ],
            },
        }

    async def _mock_sop(self):
        await asyncio.sleep(0.5)
        return {
            "reply": "Your SOP draft is ready\\[em]download the PDF and review the intent and study plan sections.",
            "files": [{"name": "SOP_Rahul_Kumar_UofT.pdf"}],
            "payload": {},
        }

    async def _call_agent(self, agent_name: str):
        self.loading = True
        yield
        try:
            if agent_name == "eligibility":
                response = await self._mock_eligibility()
                self._handle_response(response, panel_type="eligibility")
            elif agent_name == "documents":
                response = await self._mock_documents()
                self._handle_response(response, panel_type="documents")
            elif agent_name == "sop":
                response = await self._mock_sop()
                self._handle_response(response)
            else:
                response = await self._mock_chitchat()
                self._handle_response(response, panel_type="")
            yield response.get("payload")
            return
        except Exception as e:
            logging.exception(f"Error calling mock agent: {e}")
            self._add_message("system", f"An error occurred: {e}")
            return
        finally:
            self.loading = False
            yield

    @rx.event
    async def process_prompt(self, prompt: str):
        self.user_input = prompt
        yield ChatState.send({"user_input": prompt})
        yield rx.redirect("/chat")
        return

    @rx.event
    async def process_history_item(self, question: str):
        self._add_message("user", question)
        return rx.redirect("/chat")

    @rx.event
    async def send(self, form_data: dict):
        user_input = form_data.get("user_input", "").strip()
        if not user_input:
            return
        self._add_message("user", user_input)
        self.add_to_history(user_input)
        text_to_process = user_input.lower()
        self.user_input = ""
        yield
        endpoint = "chat"
        if any((k in text_to_process for k in ["eligible", "crs", "teer", "noc"])):
            endpoint = "eligibility"
        elif any(
            (k in text_to_process for k in ["form", "imm ", "checklist", "documents"])
        ):
            endpoint = "documents"
        elif any(
            (k in text_to_process for k in ["sop", "statement of purpose", "loe"])
        ):
            endpoint = "sop"
        initial_payload = None
        async for payload in self._call_agent(endpoint):
            if payload:
                initial_payload = payload
        if (
            endpoint == "chat"
            and initial_payload
            and initial_payload.get("escalate_to")
        ):
            escalation_map = {
                "eligibility_agent": "eligibility",
                "document_agent": "documents",
                "sop_agent": "sop",
            }
            escalated_endpoint = escalation_map.get(initial_payload["escalate_to"])
            if escalated_endpoint:
                async for _ in self._call_agent(escalated_endpoint):
                    pass
        yield