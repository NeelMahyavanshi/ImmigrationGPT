import reflex as rx
from hello.states.state import ChatState


def landing() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("signal", class_name="h-10 w-10 p-2 bg-purple-600 rounded-lg"),
            rx.image(
                src="placeholder.svg", class_name="h-10 w-10 p-2 bg-gray-700 rounded-lg"
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.foreach(ChatState.example_prompts, prompt_card),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-3xl",
        ),
        class_name="flex flex-col items-center justify-center gap-8 h-full p-4",
    )


def prompt_card(prompt: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(prompt["icon"], class_name="h-5 w-5 text-green-400"),
            rx.el.p(prompt["title"], class_name="font-semibold text-white"),
            class_name="flex items-center gap-3",
        ),
        rx.el.p(prompt["text"], class_name="text-sm text-gray-400"),
        on_click=lambda: ChatState.process_prompt(
            f"{prompt['title']}: {prompt['text']}"
        ),
        class_name="p-4 border border-gray-700 rounded-lg hover:bg-gray-800 cursor-pointer transition-colors flex flex-col gap-2",
    )