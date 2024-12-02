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
    multidst_hist(number_list, g2_index, title="Histogram of p-values", col1='skyblue', col2='purple', save_plot=True, timestamp=ts, plot_show=False)

    # Significance plot
    methods = ['Bonferroni', 'Holm', 'SGoF', 'BH', 'BY', 'Q value']
    res = multitest(number_list, alpha=request.alpha)
    sig_indices = [res['Bonferroni'], res['Holm'], res['SGoF'], res['BH'], res['BY'], res['Q-value']]
    sigindex_plot(methods, sig_indices, title="Significant Index Plot (SIP)", save_plot=True, timestamp=ts, plot_show=False)

    #top_10
    ascending_order_number_list = sorted(number_list)
    ascending_order_number_list_10=ascending_order_number_list[0:10]
    ascending_order_number_list_10_indices=[number_list.index(num) for num in ascending_order_number_list_10]
    ascending_order_number_list_methods=[]
    for i in ascending_order_number_list_10_indices:
        detected_methods=[]
        if i in res['Bonferroni']:
            detected_methods.append("Bonferroni")
        if i in res['Holm']:
            detected_methods.append("Holm")
        if i in res['SGoF']:
            detected_methods.append("SGoF")
        if i in res['BH']:
            detected_methods.append("BH")
        if i in res['BY']:
            detected_methods.append("BY")
        if i in res['Q-value']:
            detected_methods.append("Q-value")
        ascending_order_number_list_methods.append(detected_methods)


    
    # Carry out MultiDST for a list of p_values
    res = multitest(number_list, alpha=request.alpha, sigplot=False)
    if isinstance(res, dict):
        bonf_p = res['Bonferroni']
        holm_p = res['Holm']
        sgof_p = res['SGoF']
        bh_p = res['BH']
        by_p = res['BY']
        storey_q = res['Q-value']
        return {
            "Bonferroni": [number_list[i] for i in bonf_p],
            "Holm": [number_list[i] for i in holm_p],
            "SGoF": [number_list[i] for i in sgof_p],
            "BH": [number_list[i] for i in bh_p],
            "BY": [number_list[i] for i in by_p],
            "Q-value": [number_list[i] for i in storey_q],
            "sigindexplot": f"sigplot{ts}",
            "hist": f"hist{ts}",
            "top10indices":ascending_order_number_list,
            "top10methods":ascending_order_number_list_methods

        }
    else:
        return {"error": "Unexpected result format from multitest"}
