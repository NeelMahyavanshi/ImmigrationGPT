import reflex as rx


def badge(text: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        text,
        class_name="text-xs font-medium me-2 px-2.5 py-0.5 rounded-full bg-blue-900 text-blue-300 border border-blue-400",
    )


from hello.states.state import Download


def downloads_panel(downloads: rx.Var[list[Download]]) -> rx.Component:
    return rx.cond(
        downloads & (downloads.length() > 0),
        rx.el.div(
            rx.el.h3("Downloads", class_name="text-lg font-semibold mb-2 text-white"),
            rx.el.div(
                rx.foreach(
                    downloads,
                    lambda file: rx.el.a(
                        rx.icon("download", class_name="mr-2"),
                        file["name"],
                        href=rx.get_upload_url(file["name"]),
                        target="_blank",
                        class_name="flex items-center p-2 rounded-md bg-gray-800 hover:bg-gray-700 text-white",
                    ),
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="w-full p-4 rounded-lg bg-gray-800/50 border border-gray-700",
        ),
        None,
    )


from hello.states.state import EligibilityPayload, Program


def eligibility_panel(payload: rx.Var[EligibilityPayload]) -> rx.Component:
    safe_payload = rx.cond(payload, payload, {})
    return rx.cond(
        payload,
        rx.el.div(
            rx.el.h3(
                "Eligibility Results",
                class_name="text-lg font-semibold mb-2 text-white",
            ),
            rx.cond(
                safe_payload.contains("crs_estimate"),
                badge(f"CRS: {safe_payload['crs_estimate']}"),
                None,
            ),
            rx.el.h4(
                "Eligible Programs",
                class_name="text-md font-semibold mt-4 mb-2 text-gray-300",
            ),
            rx.el.div(
                rx.foreach(
                    safe_payload.get("eligible_programs", []).to(list[Program]),
                    lambda program: rx.el.div(
                        rx.el.h5(
                            program["program_name"], class_name="font-bold text-white"
                        ),
                        rx.el.div(
                            rx.cond(
                                program.contains("program_type"),
                                badge(program["program_type"]),
                                None,
                            ),
                            rx.cond(
                                program.contains("province"),
                                badge(program["province"]),
                                None,
                            ),
                            class_name="flex gap-2 my-1",
                        ),
                        rx.el.p(program["reason"], class_name="text-sm text-gray-400"),
                        rx.cond(
                            program.contains("official_url"),
                            rx.el.a(
                                "Official Link",
                                href=program["official_url"],
                                target="_blank",
                                class_name="text-sm text-blue-400 hover:underline",
                            ),
                            None,
                        ),
                        class_name="p-4 rounded-lg border border-gray-700 bg-green-900/20",
                    ),
                ),
                class_name="flex flex-col gap-2",
            ),
            rx.el.h4(
                "Ineligible Programs",
                class_name="text-md font-semibold mt-4 mb-2 text-gray-300",
            ),
            rx.el.div(
                rx.foreach(
                    safe_payload.get("ineligible_programs", []).to(list[Program]),
                    lambda program: rx.el.details(
                        rx.el.summary(
                            program["program_name"],
                            class_name="font-semibold cursor-pointer text-white",
                        ),
                        rx.el.ul(
                            rx.foreach(
                                program["missing_requirements"].to(list[str]),
                                lambda req: rx.el.li(
                                    req, class_name="ml-4 list-disc text-gray-400"
                                ),
                            ),
                            class_name="mt-2",
                        ),
                        class_name="p-4 rounded-lg border border-gray-700 bg-red-900/20",
                    ),
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="w-full p-4 rounded-lg bg-gray-800/50 border border-gray-700",
        ),
        None,
    )


from app.states.state import DocumentsPayload, Document, Form


def documents_panel(payload: rx.Var[DocumentsPayload]) -> rx.Component:
    safe_payload = rx.cond(payload, payload, {})

    def doc_card(doc: rx.Var[Document]):
        return rx.el.div(
            rx.el.h5(doc["name"], class_name="font-bold text-white"),
            rx.el.p(doc["description"], class_name="text-sm text-gray-400 my-1"),
            rx.cond(doc["mandatory"], badge("Mandatory"), None),
            rx.cond(
                doc.contains("conditional_on"),
                rx.el.p(
                    f"Conditional on: {doc['conditional_on']}",
                    class_name="text-sm italic text-gray-500",
                ),
                None,
            ),
            rx.cond(
                doc.contains("source_url"),
                rx.el.a(
                    "Source",
                    href=doc["source_url"],
                    target="_blank",
                    class_name="text-sm text-blue-400 hover:underline",
                ),
                None,
            ),
            class_name="p-4 rounded-lg border border-gray-700 bg-gray-800/50",
        )

    def forms_tab(forms: rx.Var[list[Form]]):
        return rx.el.div(
            rx.foreach(
                forms,
                lambda form: rx.el.div(
                    rx.el.p(
                        f"{form['form_number']} - {form['title']}",
                        class_name="text-white",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "PDF",
                            href=form["pdf_url"],
                            target="_blank",
                            class_name="text-sm text-blue-400 hover:underline",
                        ),
                        rx.cond(
                            form.contains("instructions_url"),
                            rx.el.a(
                                "Instructions",
                                href=form["instructions_url"],
                                target="_blank",
                                class_name="text-sm text-blue-400 hover:underline ml-4",
                            ),
                            None,
                        ),
                        class_name="flex gap-4",
                    ),
                    class_name="flex justify-between items-center p-2 border-b border-gray-700",
                ),
            ),
            class_name="flex flex-col",
        )

    return rx.cond(
        payload,
        rx.el.div(
            rx.el.h3(
                "Document Checklist", class_name="text-lg font-semibold mb-2 text-white"
            ),
            rx.el.div(
                rx.el.h4(
                    "Required",
                    class_name="font-semibold border-b border-gray-700 pb-1 mb-2 text-gray-300",
                ),
                rx.foreach(
                    safe_payload.get("required_documents", []).to(list[Document]),
                    doc_card,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.h4(
                    "Conditional",
                    class_name="font-semibold border-b border-gray-700 pb-1 mb-2 text-gray-300",
                ),
                rx.foreach(
                    safe_payload.get("conditional_documents", []).to(list[Document]),
                    doc_card,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.h4(
                    "Optional",
                    class_name="font-semibold border-b border-gray-700 pb-1 mb-2 text-gray-300",
                ),
                rx.foreach(
                    safe_payload.get("optional_but_recommended", []).to(list[Document]),
                    doc_card,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.h4(
                    "Forms",
                    class_name="font-semibold border-b border-gray-700 pb-1 mb-2 text-gray-300",
                ),
                forms_tab(safe_payload.get("forms", []).to(list[Form])),
                class_name="mb-4",
            ),
            class_name="w-full p-4 rounded-lg bg-gray-800/50 border border-gray-700",
        ),
        None,
    )