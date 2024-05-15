import io
import json
import os
from random import randint

import PIL
from duckduckgo_search import DDGS
import requests

from litellm import completion

inputs = []

def do_search(search_query):
    with DDGS() as ddg:
        results = ddg.images(search_query)
        if results:
            choice = results[randint(0, min(10, len(results) - 1))]
            url = choice["image"]
            image = requests.get(url).content
            filename = f"inputs/input_{search_query[:15]}.png"
            with open(filename, "wb") as f:
                image = PIL.Image.open(io.BytesIO(image))
                image.save(f, "PNG")
                inputs.append(filename)


def do_workflow(prompt, files: list[str], seed):
    suffix = "no_files" if not files else ""
    with Workflow():
        model, clip, vae = CheckpointLoaderSimple(Checkpoints.dreamshaperXL10_alpha2Xl10)
        model = PerturbedAttentionGuidance(model, 3)
        string = prompt
        latent = EmptyLatentImage(1024, 1024, 4)
        conditioning = CLIPTextEncodeSDXL(4096, 4096, 0, 0, 4096, 4096, string, clip, string)
        model, ipadapter = IPAdapterUnifiedLoader(model, IPAdapterUnifiedLoader.preset.PLUS_high_strength, None)
        clip_vision = CLIPVisionLoader(CLIPVisionLoader.clip_name.CLIP_ViT_bigG_14_laion2B_39B_b160k)
        for file in files:
            image = LoadImage(str(os.path.abspath(file)))[0]
            model = IPAdapter(model, ipadapter, image, 1, 0.4, 1, IPAdapter.weight_type.style_transfer, None)
            clip_vision_output = CLIPVisionEncode(clip_vision, image)
            conditioning = UnCLIPConditioning(conditioning, clip_vision_output, 1, 0)
        conditioning2 = CLIPTextEncode('text, watermark', clip)
        sampler = KSamplerSelect(KSamplerSelect.sampler_name.dpmpp_2m_sde)
        sigmas = AlignYourStepsScheduler(AlignYourStepsScheduler.model_type.SDXL, 20)
        latent, _ = SamplerCustom(model, True, seed, 2.5, conditioning, conditioning2, sampler, sigmas, latent)
        image2 = VAEDecode(latent, vae)
        output = SaveImage(image2, "ComfyUI")

    output.wait()
    results = output.wait()
    for i in range(4):
        with open(f"outputs/output{i}_{suffix}.png", "wb") as f:
            f.write(results[i]._repr_png_())

prompt = 'a photo of jim carrey from liar liar riding on a roller coaster, excitement, motion blur, trending on artstation'

response = completion(
    model="ollama/the-searcher:latest",
    messages=[{"content": f"{prompt}", "role": "user"}],
    temperature=1.0,
    api_base="http://localhost:11434",
    num_retries=3,
    timeout=40
)

json_string = response["choices"][0].message.content

print(json_string)

j = json.loads(json_string)
for search_query in j:
    do_search(search_query)

from comfy_script.runtime import *
load("http://localhost:8123")

from comfy_script.runtime.nodes import *

seed = randint(0, 2 ** 32 - 1)
do_workflow(prompt, inputs[0:], seed)
do_workflow(prompt, [], seed)