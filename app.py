import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "documents" / "src"))

import gradio as gr
from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# Georgia Tech OMSA Unofficial Course Guide")
    gr.Markdown(
        "Ask a question about OMSA courses, workload, difficulty, or student experiences."
    )

    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=5)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()
