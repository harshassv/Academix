from fastapi import FastAPI,Body
import gradio as gr

app = FastAPI()

# Define your machine learning model or function
def predict(text):
    # Your model prediction logic here
    return "Prediction for: " + text

# Create a Gradio interface
io = gr.Interface(predict, "textbox", "textbox")

# Define routes for different Gradio interfaces
@app.get("/")
async def root():
    return {"message": "Welcome to the Gradio application"}

@app.post("/predict")
async def make_prediction(text: str = Body(...)):
    result = predict(text)
    print(result)
    return {"prediction": result}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
