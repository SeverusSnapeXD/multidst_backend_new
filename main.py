from fastapi import FastAPI
from pydantic import BaseModel
from multidst.functions import multitest
from multidst.utils.visualization import multidst_hist , sigindex_plot
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import time 
class P_Values(BaseModel):
    p_values: str
    alpha: float

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the images directory exists
images_dir = "images"
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Serve the images directory
app.mount("/images",StaticFiles(directory=images_dir), name="images")

# to run the uvicorn dev server uvicorn api:app
@app.get("/")
async def root():
    return {"message": "Hello World"}


#send p values and methods

@app.post("/analyze")
async def analyze(request: P_Values):
    print("called")
    number_strings = request.p_values.split(',')
    number_list = [float(num) for num in number_strings]
    number_tuple = tuple(number_list)
    
    # Unique plot name
    ts = str(time.time()).replace('.', '')

    # Histogram
    g2_index = []
    multidst_hist(number_tuple, g2_index, title="Histogram of p-values", col1='skyblue', col2='purple', save_plot=True, timestamp=ts, plot_show=False)

    # Significance plot
    methods = ['Bonferroni', 'Holm', 'SGoF', 'BH', 'BY', 'Q value']
    res = multitest(number_tuple, alpha=request.alpha)
    sig_indices = [res['Bonferroni'], res['Holm'], res['SGoF'], res['BH'], res['BY'], res['Q-value']]
    sigindex_plot(methods, sig_indices, title=None, save_plot=True, timestamp=ts, plot_show=False)
    
    # Carry out MultiDST for a list of p_values
    res = multitest(number_tuple, alpha=request.alpha, sigplot=False)
    if isinstance(res, dict):
        return {
            "Bonferroni": res["Bonferroni"],
            "Holm": res["Holm"],
            "SGoF": res["SGoF"],
            "BH": res["BH"],
            "BY": res["BY"],
            "Q-value": res["Q-value"],
            "sigindexplot": f"sigplot{ts}",
            "hist": f"hist{ts}"
        }
    else:
        return {"error": "Unexpected result format from multitest"}
