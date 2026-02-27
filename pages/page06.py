import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import streamlit as st

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD  = (0.229, 0.224, 0.225)

# 페이지 설정
st.set_page_config(page_title='ResNet50 테스트', layout='centered')
st.title(body='ResNet50 테스트', width='stretch', text_alignment='center')

@st.cache_resource
def load_model(ckpt_path: str, device: str):
    ckpt = torch.load(ckpt_path, map_location=device)
    class_names = ckpt["class_names"]
    img_size = int(ckpt.get("img_size", 224))

    try:
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    except Exception:
        model = models.resnet50(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, len(class_names))
    model.load_state_dict(ckpt["model_state_dict"])
    model.to(device)
    model.eval()

    tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    return model, tf, class_names

def predict(model, tf, class_names, img, device, topk=3):
    x = tf(img).unsqueeze(0).to(device)
    with torch.no_grad():
        probs = torch.softmax(model(x), dim=1).squeeze(0)
    vals, idxs = torch.topk(probs, k=min(topk, probs.numel()))
    results = [(class_names[i], float(v)) for v, i in zip(vals.tolist(), idxs.tolist())]
    return results

st.title("ResNet50 8-class 이미지 분류 테스트")
st.caption("best_model_resnet50_8class.pth 기반")

ckpt_path = st.text_input("Checkpoint path", "best_model_resnet50_8class.pth")
device = "cuda" if torch.cuda.is_available() else "cpu"
st.write("Device:", device)

model, tf, class_names = load_model(ckpt_path, device)

uploaded = st.file_uploader("이미지를 업로드하세요", type=["jpg","jpeg","png","webp","bmp"])
topk = st.slider("Top-K", 1, 7, 3)

if uploaded is not None:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded", width='stretch')

    results = predict(model, tf, class_names, img, device, topk=topk)
    st.subheader("예측 결과")
    for rank, (label, prob) in enumerate(results, start=1):
        st.write(f"Top{rank}: {label} — {prob:.4f}")
