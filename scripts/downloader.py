import os
from urllib.parse import urlparse
from scripts.mod.ari import install_aria2, check_aria2_installed
from huggingface_hub import login


api_key = "efc79c7d87f745a9622f6de024035add"


# Ensure aria2 is installed
if not check_aria2_installed():
    install_aria2()

# Function to handle file download
def download_file(download_link, output_folder):
    if not download_link:
        return "Download link cannot be empty!"
    if not output_folder:
        return "Output folder cannot be empty!"
    
    # Handle Civitai link
    if download_link.startswith("https://civitai.com/"):
        parsed_url = urlparse(download_link)
        path_components = parsed_url.path.split("/")
        modelVersionId = path_components[-1]
        dlink = f"https://civitai.com/api/download/models/{modelVersionId}?token={api_key}"

        os.makedirs(output_folder, exist_ok=True)
        os.system(f"aria2c -x 16 -s 16 -k 1M -d {output_folder} {dlink}")
        return f"File downloaded successfully to {output_folder}!"
    
    # Handle Hugging Face link
    elif download_link.startswith("https://huggingface.co/"):
        # Extract the filename from the URL
        filename = download_link.split('/')[-1].split('?')[0]
        
        if download_link.endswith("?download=true"):
            os.makedirs(output_folder, exist_ok=True)
            # Download using aria2c
            os.system(f"aria2c -x 16 -s 16 -k 1M -d {output_folder} {download_link} -o {filename}")
            return f"File downloaded successfully to {output_folder}!"
        else:
            return "Invalid Hugging Face link! The link should follow the format: " \
                   "https://huggingface.co/<user>/<repo>/resolve/main/<filename>?download=true"
  
    # Invalid URL format
    else:
        os.system(f"aria2c -x 16 -s 16 -k 1M -d {output_folder} {download_link}")
        return f"File downloaded successfully to {output_folder}!"

# Function to resolve the output folder
def get_output_folder(link_type, custom_folder):
    folders = {
        "Checkpoints": "models/Stable-diffusion",
        "Lora": "models/Lora",
        "Embedding": "embeddings",
        "vae": "models/VAE",
    }
    return custom_folder if custom_folder.strip() else folders.get(link_type, "models/Stable-diffusion")

# Gradio interface
import gradio as gr

css = """
.gradio-row {
    display: flex;
    align-items: stretch;
    gap: 10px; /* Space between columns */
}
.gradio-column {
    flex: 1;
    padding: 10px;
    box-sizing: border-box;
}
"""

def on_ui_tabs():
    with gr.Blocks(css=css) as file_downloader:
        with gr.Row():
            # Display title
            title = gr.Markdown("### Civitai, Hugging Face, and Direct Link Downloader")
        
        with gr.Row():
            # Example links as instructions
            civit_example = gr.Markdown(
                "#### Civitai Link Example: \n"
                "`https://civitai.com/api/download/models/969441?type=Model&format=SafeTensor&size=full&fp=fp16`"
            )
            huggingface_example = gr.Markdown(
                "#### Hugging Face Link Example: \n"
                "`https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors?download=true`"
            )
        with gr.Row():
            with gr.Column():
                link_type = gr.Radio(
                    ["Checkpoints", "Lora", "Embedding", "vae"],
                    label="Select Folder Type"
                )
                custom_folder = gr.Textbox(
                    label="Custom Output Folder Path",
                    placeholder="Leave empty to use default folders"
                )
            with gr.Column():
                download_link = gr.Textbox(
                    label="Download Link",
                    placeholder="Input download link here"
                )
                output = gr.Textbox(label="Output", interactive=False)
                download_button = gr.Button("Download")
        
        # Define button behavior
        download_button.click(
            lambda dl, lt, cf: download_file(dl, get_output_folder(lt, cf)),
            inputs=[download_link, link_type, custom_folder],
            outputs=[output]
        )

    return [(file_downloader, "Civit & Other Downloader", "file_downloader")]

# Register the extension's UI
from modules import script_callbacks
script_callbacks.on_ui_tabs(on_ui_tabs)
