import reflex as rx
from hello.states.state import ChatState
from hello.components.shell import app_shell
from hello.components.landing import landing
from hello.components.chat import chat_page
from hello.components.main import history_page, settings_page


@rx.page(route="/", on_load=ChatState.on_load)
def index_page() -> rx.Component:
    return app_shell(landing())


@rx.page(route="/chat", on_load=ChatState.on_load)
def chat() -> rx.Component:
    return app_shell(chat_page())


@rx.page(route="/history", on_load=ChatState.on_load)
def history() -> rx.Component:
    return app_shell(history_page())


@rx.page(route="/settings", on_load=ChatState.on_load)
def settings() -> rx.Component:
    return app_shell(settings_page())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ],
)