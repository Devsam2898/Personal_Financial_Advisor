# test_app.py - Minimal version for testing
import gradio as gr

def simple_test(text_input):
    return f"You entered: {text_input}"

demo = gr.Interface(
    fn=simple_test,
    inputs=gr.Textbox(label="Test Input"),
    outputs=gr.Textbox(label="Output"),
    title="Test App"
)

if __name__ == "__main__":
    demo.launch()