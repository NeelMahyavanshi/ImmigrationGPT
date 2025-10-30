import reflex as rx


def history_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "THIS IS THE HISTORY PAGE",
            class_name="text-4xl font-extrabold text-red-500",
        ),
        class_name="w-full max-w-4xl mx-auto p-4 md:p-8 flex items-center justify-center h-full",
    )


def settings_page() -> rx.Component:
    from hello.states.state import AppState

    def setting_toggle(label: str, key: str, is_checked: rx.Var[bool]) -> rx.Component:
        return rx.el.div(
            rx.el.label(label, class_name="font-medium text-white"),
            rx.el.div(
                rx.el.button(
                    rx.el.span(
                        class_name=rx.cond(is_checked, "translate-x-5", "translate-x-0")
                        + " pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
                    ),
                    on_click=lambda: AppState.update_setting(key, ~is_checked),
                    class_name=rx.cond(is_checked, "bg-purple-600", "bg-gray-600")
                    + " relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900",
                )
            ),
            class_name="flex items-center justify-between w-full p-4 border border-gray-700 rounded-lg",
        )

    def theme_selector() -> rx.Component:
        return rx.el.div(
            rx.el.label("Theme", class_name="font-medium text-white"),
            rx.el.select(
                rx.el.option("System", value="system"),
                rx.el.option("Light", value="light"),
                rx.el.option("Dark", value="dark"),
                value=AppState.settings["theme"],
                on_change=lambda value: AppState.update_setting("theme", value),
                class_name="bg-gray-800 border border-gray-600 rounded-md p-2 text-white focus:ring-purple-500 focus:border-purple-500",
            ),
            class_name="flex items-center justify-between w-full p-4 border border-gray-700 rounded-lg",
        )

    return rx.el.div(
        rx.el.h1("Settings", class_name="text-2xl font-bold mb-4 text-white"),
        rx.el.div(
            setting_toggle(
                "Use Supabase memory",
                "use_supabase_memory",
                AppState.settings["use_supabase_memory"],
            ),
            setting_toggle(
                "Enable streaming",
                "enable_streaming",
                AppState.settings["enable_streaming"],
            ),
            theme_selector(),
            class_name="flex flex-col gap-4",
        ),
        class_name="w-full max-w-2xl mx-auto p-4 md:p-8",
    )