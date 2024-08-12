import gradio as gr

# Define the function that will process the input
def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

# Create the Gradio interface
demo = gr.Interface(
    fn=greet,  # the function to call
    inputs=["text", "slider"],  # the inputs to the function
    outputs="text"  # the type of output to return
)

# Launch the app
demo.launch()