import reflex as rx
from hello.states.state import ChatState
from hello.components.panels import downloads_panel, eligibility_panel, documents_panel
from hello.components.landing import landing
from hello.states.state import Message


def bubble(message: Message) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.cond(is_user, "/user.png", "/bot.png"),
                class_name="h-8 w-8 rounded-full",
            ),
            rx.el.div(
                rx.cond(
                    message["text"].length() > 0,
                    rx.el.p(message["text"], class_name="text-sm"),
                    None,
                ),
                rx.match(
                    message["panel_type"],
                    ("eligibility", eligibility_panel(payload=message["panel_data"])),
                    ("documents", documents_panel(payload=message["panel_data"])),
                    (
                        "downloads",
                        downloads_panel(
                            downloads=message["panel_data"].get("downloads", [])
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name=rx.cond(
                    message["text"].length() > 0,
                    rx.cond(is_user, "bg-blue-900/50", "bg-gray-700/50")
                    + " p-3 rounded-lg max-w-xl",
                    "max-w-xl",
                ),
            ),
            align="start",
            class_name="flex items-start gap-3",
        ),
        class_name=rx.cond(is_user, "justify-end", "justify-start") + " flex w-full",
    )


def chat_page() -> rx.Component:
    return rx.cond(
        ChatState.messages.length() > 0,
        rx.el.div(
            rx.el.div(
                rx.scroll_area(
                    rx.el.div(
                        rx.foreach(ChatState.messages, bubble),
                        class_name="flex-grow p-4 flex flex-col gap-6",
                    ),
                    type="always",
                    scrollbars="vertical",
                    class_name="h-full",
                ),
                class_name="flex-grow overflow-y-auto",
            ),
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Ask anything...",
                            name="user_input",
                            class_name="w-full p-4 border-none focus:ring-0 bg-transparent text-white placeholder-gray-400",
                            key=ChatState.user_input,
                        ),
                        rx.el.button(
                            rx.icon("arrow-up", class_name="h-5 w-5"),
                            type_="submit",
                            disabled=ChatState.loading,
                            class_name="p-3 bg-purple-600 text-white rounded-full hover:bg-purple-700 disabled:bg-purple-400 transition-colors",
                        ),
                        class_name="flex items-center w-full border border-gray-600 rounded-full bg-gray-800",
                    ),
                    on_submit=ChatState.send,
                    reset_on_submit=True,
                    class_name="w-full max-w-3xl mx-auto",
                ),
                rx.el.a(
                    rx.icon("signal", class_name="h-4 w-4 text-gray-400"),
                    "Built with Reflex",
                    href="https://reflex.dev",
                    target="_blank",
                    class_name="flex items-center gap-2 text-sm text-gray-500 mt-3",
                ),
                class_name="flex flex-col items-center p-4 bg-gray-900/80 backdrop-blur-sm sticky bottom-0",
            ),
            class_name="flex flex-col h-full",
        ),
        landing(),
    )