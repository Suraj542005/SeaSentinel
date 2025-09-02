# inference.py
import torch, cv2
import numpy as np
from torchvision import transforms, models
from PIL import Image


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMG_TFMS = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]),
])


class DisasterClassifier:
    def __init__(self, model_path: str):
        ckpt = torch.load(model_path, map_location=DEVICE)
        self.class_names = ckpt["class_names"]

        model = models.resnet18(weights=None)
        model.fc = torch.nn.Linear(model.fc.in_features, len(self.class_names))
        model.load_state_dict(ckpt["model_state"], strict=True)
        model.eval().to(DEVICE)
        self.model = model

    @torch.no_grad()
    def predict_image(self, img_path: str):
        img = Image.open(img_path).convert("RGB")
        x = IMG_TFMS(img).unsqueeze(0).to(DEVICE)
        logits = self.model(x)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
        idx = int(np.argmax(probs))
        return {
            "label": self.class_names[idx],
            "confidence": float(probs[idx]),
            "probs": {self.class_names[i]: float(p) for i, p in enumerate(probs)}
        }

    @torch.no_grad()
    def predict_video(self, video_path: str, num_frames: int = 12):
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        frame_idxs = np.linspace(0, total_frames-1, num_frames).astype(int)

        probs_accum = np.zeros(len(self.class_names), dtype=np.float32)
        for fi in frame_idxs:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(fi))
            ok, frame = cap.read()
            if not ok:
                continue
            # BGR -> RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            x = IMG_TFMS(img).unsqueeze(0).to(DEVICE)
            logits = self.model(x)
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
            probs_accum += probs
        cap.release()

        probs_mean = probs_accum / max(len(frame_idxs), 1)
        idx = int(np.argmax(probs_mean))
        return {
            "label": self.class_names[idx],
            "confidence": float(probs_mean[idx]),
            "probs": {self.class_names[i]: float(p) for i, p in enumerate(probs_mean)}
        }
