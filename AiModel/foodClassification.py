import torch
import os
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load('/Users/parkjihyeon/Desktop/IndonesiaWeb/AiModel/model_augmentation.pt', map_location=device)

path = "/Users/parkjihyeon/Desktop/IndonesiaWeb/AiModel/images/" # food image

import torch
import torchvision.transforms as transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 이미지 크기 조정
    transforms.ToTensor(),           # 이미지를 Tensor로 변환
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),  # 이미지 정규화
    #transforms.RandomHorizontalFlip(),
    #transforms.RandomVerticalFlip(),
])


class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = self.get_image_paths()

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image_path = self.image_paths[index]
        image = Image.open(image_path)
        
        # RGBA 이미지에서 RGB 이미지로 변환
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        if self.transform is not None:
            image = self.transform(image)

        image_name = os.path.basename(image_path)

        return image, image_name

    def get_image_paths(self):
        image_paths = []
        for file in os.listdir(self.root_dir):
            if file.endswith(".jpeg") or file.endswith(".png"):
                image_paths.append(os.path.join(self.root_dir, file))
        return image_paths
    


pred_dataset = CustomDataset(root_dir=path, transform=transform)
pred_loader = torch.utils.data.DataLoader(pred_dataset, batch_size=16, shuffle=False) #test-> no need to shuffle


# 모델을 검증 모드로 변환합니다
model.eval()
predicted = []
with torch.no_grad():
    for images, image_name in pred_loader:
        images = images.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)

         # 예측된 클래스 번호를 클래스 이름으로 변환
        #predicted_labels = [idx_to_label[idx.item()] for idx in predicted]

idx_to_class = {0: '01. Ayam Betutu',
 1: 'Beberuk Terong',
 2: 'Coto Makassar',
 3: 'Gudeg',
 4: 'Kerak Telor',
 5: 'Mie Aceh',
 6: 'Nasi Kuning',
 7: 'Nasi Pecel',
 8: 'Papeda',
 9: 'Pempek',
 10: 'Peuyeum',
 11: 'Rawon',
 12: 'Rendang',
 13: 'Sate Madura',
 14: 'Serabi',
 15: 'Soto Banjar',
 16: 'Soto Lamongan',
 17: 'Tahu Sumedang',
 18: '가지볶음',
 19: '간장게장',
 20: '갈비구이',
 21: '갈비찜',
 22: '갈비탕',
 23: '갈치구이',
 24: '갈치조림',
 25: '감자전',
 26: '감자조림',
 27: '감자채볶음',
 28: '감자탕',
 29: '갓김치',
 30: '건새우볶음',
 31: '경단',
 32: '계란국',
 33: '계란말이',
 34: '계란찜',
 35: '계란후라이',
 36: '고등어구이',
 37: '고등어조림',
 38: '고사리나물',
 39: '곰탕_설렁탕',
 40: '김밥',
 41: '김치볶음밥',
 42: '김치전',
 43: '김치찌개',
 44: '김치찜',
 45: '깍두기',
 46: '깻잎장아찌',
 47: '꽁치조림',
 48: '꽈리고추무침',
 49: '꿀떡',
 50: '나박김치',
 51: '누룽지',
 52: '닭갈비',
 53: '닭계장',
 54: '닭볶음탕',
 55: '더덕구이',
 56: '도라지무침',
 57: '도토리묵',
 58: '된장찌개',
 59: '떡갈비',
 60: '떡국_만두국',
 61: '떡볶이',
 62: '라면',
 63: '막국수',
 64: '매운탕',
 65: '메추리알장조림',
 66: '멸치볶음',
 67: '무국',
 68: '무생채',
 69: '물냉면',
 70: '미역국',
 71: '미역줄기볶음',
 72: '배추김치',
 73: '백김치',
 74: '보쌈',
 75: '부추김치',
 76: '북엇국',
 77: '불고기',
 78: '비빔냉면',
 79: '비빔밥',
 80: '삼겹살',
 81: '삼계탕',
 82: '새우볶음밥',
 83: '생선전',
 84: '소세지볶음',
 85: '수육',
 86: '수정과',
 87: '수제비',
 88: '숙주나물',
 89: '순대',
 90: '순두부찌개',
 91: '시금치나물',
 92: '시래기국',
 93: '식혜',
 94: '애호박볶음',
 95: '약과',
 96: '약식',
 97: '양념치킨',
 98: '어묵볶음',
 99: '열무국수',
 100: '열무김치',
 101: '오이소박이',
 102: '오징어채볶음',
 103: '우엉조림',
 104: '유부초밥',
 105: '육개장',
 106: '잔치국수',
 107: '잡곡밥',
 108: '잡채',
 109: '장어구이',
 110: '장조림',
 111: '제육볶음',
 112: '족발',
 113: '짜장면',
 114: '짬뽕',
 115: '찜닭',
 116: '총각김치',
 117: '추어탕',
 118: '칼국수',
 119: '코다리조림',
 120: '콩국수',
 121: '콩나물국',
 122: '콩나물무침',
 123: '콩자반',
 124: '파김치',
 125: '파전',
 126: '편육',
 127: '피자',
 128: '해물찜',
 129: '호박전',
 130: '황태구이',
 131: '후라이드치킨',
 132: '훈제오리'}


def foodClassification():
    pred_dataset = CustomDataset(root_dir=path, transform=transform)
    pred_loader = torch.utils.data.DataLoader(pred_dataset, batch_size=16, shuffle=False)

    model.eval()
    predictions = []
    with torch.no_grad():
        for images, image_names in pred_loader:
            images = images.to(device)
            outputs = model(images)
            _, predicted_indices = torch.max(outputs, 1)

            for idx in predicted_indices:
                class_name = idx_to_class[int(idx)]
                predictions.append(class_name)

    return predictions    