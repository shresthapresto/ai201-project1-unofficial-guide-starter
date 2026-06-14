import gradio as gr
from generate import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("""
    # 🎓 The Unofficial Guide
    ### CS Master's Admissions — Real Student Data
    Ask questions about GPA, GRE scores, and admission outcomes
    from real student posts on Reddit and Gradcafe.
    """)
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What GPA do most admitted CMU MSCS students have?"
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=3)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()