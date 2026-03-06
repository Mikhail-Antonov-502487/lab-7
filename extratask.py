import tkinter as tk
import requests
from PIL import Image, ImageTk
import io


class CatAPI:
    
    def __init__(self):
        self.url = "https://cataas.com/cat"
    
    def get_cat(self):
        """Получить картинку котика"""
        try:
            response = requests.get(self.url, timeout=25)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None


class ImageProcessor:
    
    def prepare_image(self, image_data, size=(400, 400)):
        try:
            img = Image.open(io.BytesIO(image_data))
            img = img.resize(size)
            return ImageTk.PhotoImage(img)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None


class CatClient:
    
    def __init__(self, root):
        self.root = root
        self.api = CatAPI()
        self.processor = ImageProcessor()
        
        self.root.title("Генератор котиков")
        self.root.geometry("500x550")
        
        self.setup_ui()
        
        self.show_new_cat()
    
    def setup_ui(self):
        self.button = tk.Button(
            self.root,
            text="Новый котик",
            command=self.show_new_cat,
            font=("Arial", 14),
            bg='#ff9999',
            fg='white',
            padx=20,
            pady=10
        )
        self.button.pack(pady=20)
        
        self.image_label = tk.Label(
            self.root,
            bg='#f0f0f0',
            relief=tk.SUNKEN,
            bd=2
        )
        self.image_label.pack(pady=10)
        
        self.status_label = tk.Label(
            self.root,
            text="Готов",
            font=("Arial", 10),
            fg='gray'
        )
        self.status_label.pack()
    
    def show_new_cat(self):
        self.button.config(text="Загрузка...", state=tk.DISABLED)
        self.status_label.config(text="Загружаю котика...")
        
        self.root.after(100, self.load_cat)
    
    def load_cat(self):
        image_data = self.api.get_cat()
        
        if image_data:
            photo = self.processor.prepare_image(image_data)
            
            if photo:
                self.image_label.config(image=photo)
                self.image_label.image = photo  # сохраняем ссылку
                self.status_label.config(text="Котик загружен!")
            else:
                self.status_label.config(text="Ошибка обработки")
        else:
            self.status_label.config(text="Ошибка загрузки")
        
        self.button.config(text="Новый котик", state=tk.NORMAL)



if __name__ == "__main__":
    root = tk.Tk()
    client = CatClient(root)
    root.mainloop()