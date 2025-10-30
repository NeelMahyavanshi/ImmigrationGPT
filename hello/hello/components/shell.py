import reflex as rx
from hello.states.state import AppState, ChatState, Download


def nav_item(text: str, href: str, icon: str, is_active: rx.Var[bool]) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon,
            class_name=rx.cond(
                is_active, "text-purple-400", "text-gray-400 group-hover:text-white"
            )
            + " h-5 w-5 transition-colors",
        ),
        rx.el.span(
            text,
            class_name=rx.cond(AppState.sidebar_open, "opacity-100", "opacity-0 w-0")
            + " transition-opacity duration-200",
        ),
        href=href,
        class_name="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-800 group transition-colors",
    )


def downloads_drawer() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Downloads", class_name="text-lg font-bold text-white"),
                rx.el.button(
                    rx.icon("x", class_name="h-5 w-5 text-gray-400"),
                    on_click=AppState.toggle_downloads,
                    class_name="p-1 rounded-full hover:bg-gray-700",
                ),
                class_name="flex items-center justify-between p-4 border-b border-gray-700",
            ),
            rx.cond(
                AppState.downloads.length() > 0,
                rx.el.div(
                    rx.foreach(
                        AppState.downloads,
                        lambda file: rx.el.a(
                            rx.icon("cloud_download", class_name="h-5 w-5 mr-3"),
                            file["name"],
                            href=rx.get_upload_url(file["name"]),
                            target="_blank",
                            class_name="flex items-center p-3 rounded-lg hover:bg-gray-800 text-white transition-colors",
                        ),
                    ),
                    class_name="p-4 flex flex-col gap-2",
                ),
                rx.el.div(
                    rx.el.p("No downloads yet.", class_name="text-gray-400"),
                    class_name="flex items-center justify-center h-full p-4",
                ),
            ),
        ),
        class_name=rx.cond(AppState.downloads_open, "translate-x-0", "translate-x-full")
        + " fixed top-0 right-0 h-full w-80 bg-gray-900 shadow-lg z-30 transition-transform duration-300 ease-in-out border-l border-gray-700",
    )


def app_shell(page_content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("signal", class_name="h-8 w-8 text-purple-400"),
                        rx.el.span(
                            "ImmigrationGPT",
                            class_name=rx.cond(
                                AppState.sidebar_open, "opacity-100", "opacity-0 w-0"
                            )
                            + " text-lg font-bold text-white transition-opacity duration-200",
                        ),
                        class_name="flex items-center gap-3 h-16 px-4",
                    )
                ),
                rx.el.nav(
                    nav_item("Home", "/", "home", AppState.router.page.path == "/"),
                    nav_item(
                        "Chat",
                        "/chat",
                        "message-circle",
                        AppState.router.page.path.contains("/chat"),
                    ),
                    nav_item(
                        "History",
                        "/history",
                        "history",
                        AppState.router.page.path.contains("/history"),
                    ),
                    rx.el.div(
                        rx.icon(
                            "download",
                            class_name="text-gray-400 group-hover:text-white h-5 w-5 transition-colors",
                        ),
                        rx.el.span(
                            "Downloads",
                            class_name=rx.cond(
                                AppState.sidebar_open, "opacity-100", "opacity-0 w-0"
                            )
                            + " transition-opacity duration-200",
                        ),
                        on_click=AppState.toggle_downloads,
                        class_name="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-800 group cursor-pointer transition-colors",
                    ),
                    nav_item(
                        "Settings",
                        "/settings",
                        "settings",
                        AppState.router.page.path.contains("/settings"),
                    ),
                    class_name="flex flex-col gap-2 p-2",
                ),
            ),
            class_name=rx.cond(AppState.sidebar_open, "w-64", "w-20")
            + " fixed top-0 left-0 h-full bg-gray-900 border-r border-gray-800 z-20 transition-all duration-300 ease-in-out",
        ),
        rx.el.div(
            rx.el.header(
                rx.el.button(
                    rx.icon(
                        rx.cond(
                            AppState.sidebar_open, "panel-left-close", "panel-left-open"
                        ),
                        class_name="h-6 w-6 text-white",
                    ),
                    on_click=AppState.toggle_sidebar,
                    class_name="p-2 rounded-md hover:bg-gray-800",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("copy", class_name="h-5 w-5 mr-2"),
                        "Copy Session ID",
                        on_click=rx.set_clipboard(ChatState.session_id),
                        class_name="flex items-center px-3 py-1.5 text-sm bg-gray-800 border border-gray-700 rounded-md hover:bg-gray-700 text-white",
                    ),
                    rx.el.div(
                        rx.el.div(
                            class_name="h-2 w-2 rounded-full bg-green-500 animate-pulse"
                        ),
                        "Online",
                        class_name="flex items-center gap-2 text-sm text-gray-300",
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="flex items-center justify-between h-16 px-6 border-b border-gray-800",
            ),
            rx.el.main(page_content, class_name="flex-1 overflow-y-auto"),
            class_name="flex flex-col flex-1 h-screen",
        ),
        downloads_drawer(),
        class_name=rx.cond(AppState.sidebar_open, "pl-64", "pl-20")
        + " bg-gray-900 text-white font-['Lato'] transition-all duration-300 ease-in-out",
    )