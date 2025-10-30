import reflex as rx
import asyncio
import uuid
from typing import Any, Optional, TypedDict
import logging
from datetime import datetime
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
if str(BASE / "bridge") not in sys.path:
    sys.path.insert(0, str(BASE / "bridge"))

from router_bridge import run_chitchat, run_eligibility, run_documents, run_sop


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

    def _handle_response(self, reply: str, files: list, payload: dict, panel_type: str = ""):
        panel_data = payload if panel_type else {}
        if files:
            panel_type = "downloads"
            panel_data = {"downloads": files}
            for file in files:
                self.add_download(file)
        if reply or panel_type:
            self._add_message(
                "assistant", reply, panel_type=panel_type, panel_data=panel_data
            )

    async def _call_real_agent(self, agent_name: str, user_text: str):
        try:
            if agent_name == "eligibility":
                reply, files, payload = await asyncio.to_thread(
                    run_eligibility, user_text, self.session_id
                )
                return reply, files, payload
            elif agent_name == "documents":
                reply, files, payload = await asyncio.to_thread(
                    run_documents, user_text, self.session_id
                )
                return reply, files, payload
            elif agent_name == "sop":
                reply, files, payload = await asyncio.to_thread(
                    run_sop, user_text, self.session_id
                )
                return reply, files, payload
            else:
                reply, files, payload = await asyncio.to_thread(
                    run_chitchat, user_text, self.session_id
                )
                return reply, files, payload
        except Exception as e:
            logging.exception(f"Error calling real agent: {e}")
            return f"An error occurred: {str(e)}", [], {}

    async def _call_agent(self, agent_name: str, user_text: str):
        self.loading = True
        yield
        try:
            reply, files, payload = await self._call_real_agent(agent_name, user_text)

            panel_type = ""
            if agent_name == "eligibility":
                panel_type = "eligibility"
            elif agent_name == "documents":
                panel_type = "documents"

            self._handle_response(reply, files, payload, panel_type=panel_type)
            yield payload
            return
        except Exception as e:
            logging.exception(f"Error calling agent: {e}")
            self._add_message("system", f"An error occurred: {str(e)}")
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
        async for payload in self._call_agent(endpoint, user_input):
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
                "SOP_Agent": "sop",
            }
            escalated_endpoint = escalation_map.get(initial_payload["escalate_to"])
            if escalated_endpoint:
                async for _ in self._call_agent(escalated_endpoint, user_input):
                    pass
        yield