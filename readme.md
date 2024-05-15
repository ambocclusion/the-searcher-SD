# THE SEARCHER

ok this is not anything super special but I had an idea I wanted to get out of my head

this script will use an llm to break the prompt down into a list consisting of the main subject and any other concepts. it'll then do a search on duckduckgo for an image of the subject and feed that into stable diffusion using a mixture of ipadapter and unclip. this will enhance the likeness slightly. I can see ways this could be improved in the future but I wanted to see what kind of gains could be had with this method.

I could see future improvements that will be able to take obscure concepts and enhance their output from SDXL.

here are some examples:

`a photo of jim carrey from liar liar riding on a roller coaster, excitement, motion blur, trending on artstation`

without:
<p float="left">
    <img alt="output0_no_files.png" src="assets%2Foutput0_no_files.png" width="200"/>
    <img alt="output1_no_files.png" src="assets%2Foutput1_no_files.png" width="200"/>
    <img alt="output2_no_files.png" src="assets%2Foutput2_no_files.png" width="200"/>
    <img alt="output3_no_files.png" src="assets%2Foutput3_no_files.png" width="200"/>
</p>

with

<p float="left">
    <img alt="output0_.png" src="assets%2Foutput0_.png" width="200"/>
    <img alt="output1_.png" src="assets%2Foutput1_.png" width="200"/>
    <img alt="output2_.png" src="assets%2Foutput2_.png" width="200"/>
    <img alt="output3_.png" src="assets%2Foutput3_.png" width="200"/>
</p>