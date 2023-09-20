import os
import shutil
import gradio as gr
from docs2db import ingest_file

def answer_question(question): 
    # TODO: ensure file is loaded and processed
    from main import qa  # TODO: lazy load this
    print("Asking", question)
    resp = qa({"question": question})
    return resp['answer']

def clean_up():
    print("Cleaning up database store folder")
    folder = 'database_store'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                print("Deleting", file_path)
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def upload_file(file_obj):
    clean_up()
    ingest_file(file_obj.name)
    return file_obj.name

with gr.Blocks(css="style.css") as interface:
    with gr.Column(elem_id="col-container"):
        gr.Markdown(
            """
            # QA your PDF 💬
            """
        )
        with gr.Row(elem_id="row-flex"):
            with gr.Column(scale=1, min_width=50):
                file_output = gr.File()
                upload_button = gr.UploadButton(
                    "Browse File", file_types=[".txt", ".pdf", ".doc", ".docx"]
                )
        user_question = gr.Textbox(value="", label="Ask a question about your file:")
        answer = gr.Textbox(value="", label="Answer:")
        gr.Examples(
            ["What is the main subject of the file?", "Summarise the file in one sentence"],
            user_question,
        )

    upload_button.upload(upload_file, upload_button, [file_output])
    user_question.submit(answer_question, [user_question], [answer])

interface.queue().launch()