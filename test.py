import whisper

model = whisper.load_model("base")  # You can use "small", "medium", or "large"
result = model.transcribe("C://Users//prath//OneDrive//Desktop//miniproj//meeting-minutes//audio//EarningsCall.wav")
print(result["text"])
