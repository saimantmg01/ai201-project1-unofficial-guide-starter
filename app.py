import gradio as gr

from query import ask


def handle_query(question: str) -> tuple[str, str]:
    try:
        result = ask(question)
    except Exception as exc:
        return f"Error: {exc}", ""

    if not result["sources"]:
        return result["answer"], "No sufficiently relevant sources were found."

    source_lines = [
        (
            f"- [{source['title']}]({source['url']})  \n"
            f"  {source['source_type']} · distance {source['distance']:.3f}"
        )
        for source in result["sources"]
    ]
    return result["answer"], "\n".join(source_lines)


with gr.Blocks(title="Hunter College Housing and Commuting Guide") as demo:
    gr.Markdown("# Hunter College Housing and Commuting Guide")
    gr.Markdown(
        "Ask about Hunter-affiliated housing, commuting, off-campus options, "
        "tenant rights, or rental warning signs."
    )
    question = gr.Textbox(
        label="Your question",
        placeholder="Is Hunter-affiliated housing guaranteed?",
        lines=2,
    )
    ask_button = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Markdown(label="Retrieved sources")

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources],
    )
    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources],
    )


if __name__ == "__main__":
    demo.launch()
