from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
import threading
import os
import time
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

# Auto-install dependencies
def install_dependencies():
    """Install missing dependencies"""
    required_packages = {'yt_dlp': 'yt-dlp', 'requests': 'requests'}
    missing_packages = []
    for module_name, pip_name in required_packages.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"Installing: {', '.join(missing_packages)}")
        import subprocess
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Installed {package}")
            except Exception as e:
                print(f"Failed to install {package}: {e}")

print("Checking dependencies...")
install_dependencies()

# Import after installation
try:
    import yt_dlp
    import requests
except ImportError as e:
    print(f"Warning: {e}")

class DownloadManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        self.is_downloading = False
        self.cancel_flag = False
        
        # Set download folder based on platform
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            self.download_folder = '/sdcard/Download'
        else:
            self.download_folder = str(Path.home() / "Downloads")
        
        os.makedirs(self.download_folder, exist_ok=True)
        self.chunk_size = 1024 * 1024  # 1MB
        self.max_connections = 4
        
        self.create_ui()
    
    def create_ui(self):
        """Create UI elements"""
        # Title
        title = Label(
            text='⚡ ELBASHA Ultra Speed Downloader',
            font_size=sp(20),
            size_hint_y=None,
            height=dp(50),
            color=[0, 1, 0, 1],
            bold=True
        )
        self.add_widget(title)
        
        # URL input section
        url_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        url_label = Label(text='URL:', size_hint_x=0.15, color=[0, 1, 0, 1])
        self.url_input = TextInput(
            multiline=False,
            hint_text='Enter download URL',
            font_size=sp(14),
            size_hint_x=0.7,
            background_color=[0.1, 0.1, 0.15, 1],
            foreground_color=[0, 1, 0, 1]
        )
        paste_btn = Button(
            text='📋 Paste',
            size_hint_x=0.15,
            background_color=[0, 1, 0, 1],
            color=[0, 0, 0, 1]
        )
        paste_btn.bind(on_press=self.paste_url)
        
        url_layout.add_widget(url_label)
        url_layout.add_widget(self.url_input)
        url_layout.add_widget(paste_btn)
        self.add_widget(url_layout)
        
        # Control buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        
        clear_btn = Button(
            text='✖ Clear',
            background_color=[1, 0.3, 0.3, 1]
        )
        clear_btn.bind(on_press=self.clear_url)
        
        folder_btn = Button(
            text='📁 Open Folder',
            background_color=[0, 0.5, 1, 1]
        )
        folder_btn.bind(on_press=self.open_folder)
        
        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(folder_btn)
        self.add_widget(btn_layout)
        
        # Download mode selection
        mode_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        mode_label = Label(text='Mode:', size_hint_x=0.2, color=[0, 1, 0, 1])
        self.mode_spinner = Spinner(
            text='Video',
            values=['Video', 'Audio', 'File'],
            size_hint_x=0.4,
            background_color=[0.2, 0.2, 0.3, 1]
        )
        quality_label = Label(text='Quality:', size_hint_x=0.2, color=[0, 1, 0, 1])
        self.quality_spinner = Spinner(
            text='best',
            values=['best', '1080p', '720p', '480p', '360p'],
            size_hint_x=0.4,
            background_color=[0.2, 0.2, 0.3, 1]
        )
        
        mode_layout.add_widget(mode_label)
        mode_layout.add_widget(self.mode_spinner)
        mode_layout.add_widget(quality_label)
        mode_layout.add_widget(self.quality_spinner)
        self.add_widget(mode_layout)
        
        # Start/Stop buttons
        control_layout = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        
        self.start_btn = Button(
            text='▶ Start Download',
            background_color=[0, 1, 0, 1],
            color=[0, 0, 0, 1],
            font_size=sp(16),
            bold=True
        )
        self.start_btn.bind(on_press=self.start_download)
        
        self.stop_btn = Button(
            text='⏹ Stop',
            background_color=[1, 0.3, 0.3, 1],
            font_size=sp(16),
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_download)
        
        control_layout.add_widget(self.start_btn)
        control_layout.add_widget(self.stop_btn)
        self.add_widget(control_layout)
        
        # Progress bar
        progress_label = Label(
            text='Progress:',
            size_hint_y=None,
            height=dp(30),
            color=[0, 1, 0, 1]
        )
        self.add_widget(progress_label)
        
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(25)
        )
        self.add_widget(self.progress_bar)
        
        self.progress_label = Label(
            text='0%',
            size_hint_y=None,
            height=dp(25),
            color=[0, 1, 0, 1]
        )
        self.add_widget(self.progress_label)
        
        self.speed_label = Label(
            text='Speed: 0 MB/s',
            size_hint_y=None,
            height=dp(25),
            color=[0, 1, 0, 1]
        )
        self.add_widget(self.speed_label)
        
        # Log section
        log_label = Label(
            text='Log:',
            size_hint_y=None,
            height=dp(30),
            color=[0, 1, 0, 1]
        )
        self.add_widget(log_label)
        
        scroll = ScrollView(size_hint=(1, 0.3))
        self.log_label = Label(
            text='Ready to download...\n',
            size_hint_y=None,
            height=dp(400),
            color=[0, 1, 0, 1],
            halign='left',
            valign='top',
            text_size=(Window.width - dp(30), None)
        )
        scroll.add_widget(self.log_label)
        self.add_widget(scroll)
    
    def paste_url(self, instance):
        """Paste from clipboard"""
        try:
            from kivy.core.clipboard import Clipboard
            clipboard_text = Clipboard.paste()
            self.url_input.text = clipboard_text
            self.log('Pasted URL from clipboard')
        except Exception as e:
            self.log(f'Error pasting: {e}')
    
    def clear_url(self, instance):
        """Clear URL input"""
        self.url_input.text = ''
        self.log('URL cleared')
    
    def open_folder(self, instance):
        """Open download folder"""
        if platform == 'android':
            self.log(f'Downloads saved to: {self.download_folder}')
        else:
            try:
                import subprocess
                if sys.platform == 'win32':
                    os.startfile(self.download_folder)
                elif sys.platform == 'darwin':
                    subprocess.call(['open', self.download_folder])
                else:
                    subprocess.call(['xdg-open', self.download_folder])
                self.log('Opened download folder')
            except Exception as e:
                self.log(f'Error opening folder: {e}')
    
    def log(self, message):
        """Add message to log"""
        self.log_label.text += f'{message}\n'
        self.log_label.texture_update()
        self.log_label.height = self.log_label.texture_size[1]
        Clock.schedule_once(lambda dt: None, 0)
    
    def update_progress(self, progress, speed_mbps=0):
        """Update progress bar and labels"""
        self.progress_bar.value = min(progress, 100)
        self.progress_label.text = f'{min(progress, 100):.1f}%'
        self.speed_label.text = f'Speed: {speed_mbps:.2f} MB/s ⚡'
        Clock.schedule_once(lambda dt: None, 0)
    
    def sanitize_filename(self, filename, max_length=200):
        """Sanitize filename for safe saving"""
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
        name, ext = os.path.splitext(filename)
        if len(name) > max_length:
            name = name[:max_length]
        return name + ext
    
    def start_download(self, instance):
        """Start download process"""
        url = self.url_input.text.strip()
        if not url:
            self.log('⚠️ Please enter a URL!')
            return
        
        if self.is_downloading:
            self.log('⚠️ Download already in progress')
            return
        
        self.cancel_flag = False
        self.is_downloading = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.progress_bar.value = 0
        self.log(f'Starting download: {url[:50]}...')
        
        thread = threading.Thread(target=self.download_worker, args=(url,), daemon=True)
        thread.start()
    
    def stop_download(self, instance):
        """Stop download process"""
        if self.is_downloading:
            self.cancel_flag = True
            self.log('⏹ Stopping download...')
            self.stop_btn.disabled = True
    
    def download_worker(self, url):
        """Worker thread for downloading"""
        try:
            mode = self.mode_spinner.text.lower()
            if mode == 'file':
                self.download_direct_file(url)
            else:
                self.download_media(url, mode)
            
            if not self.cancel_flag:
                self.log('✓ Download completed successfully!')
        except Exception as e:
            if not self.cancel_flag:
                self.log(f'✗ Error: {str(e)}')
        finally:
            self.is_downloading = False
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            if not self.cancel_flag:
                self.update_progress(100)
    
    def download_media(self, url, mode):
        """Download media using yt-dlp"""
        import yt_dlp
        self.log(f'🚀 Starting {mode} download...')
        
        quality = self.quality_spinner.text.split()[0]
        ydl_opts = {
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [self.yt_dlp_progress_hook],
            'concurrent_fragment_downloads': self.max_connections,
            'quiet': True,
        }
        
        if mode == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            # Note: Audio extraction requires ffmpeg, which is handled in buildozer.spec
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        else:  # video
            if quality == 'best':
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            else:
                ydl_opts['format'] = f'bestvideo[height<={quality[:-1]}]+bestaudio/best'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if not self.cancel_flag:
                    ydl.download([url])
        except Exception as e:
            if "Canceling" not in str(e):
                raise
    
    def yt_dlp_progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if self.cancel_flag:
            raise Exception("Download cancelled by user")
        
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                speed = d.get('speed', 0)
                speed_mbps = (speed / (1024 * 1024)) if speed else 0
                Clock.schedule_once(lambda dt: self.update_progress(progress, speed_mbps), 0)
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.log('⚙️ Processing file...'), 0)
    
    def download_direct_file(self, url):
        """Download direct file using requests"""
        import requests
        self.log('🚀 Starting fast download...')
        
        try:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"download_{int(time.time())}"
            filename = self.sanitize_filename(filename)
            filepath = os.path.join(self.download_folder, filename)
            
            response = requests.get(url, stream=True, timeout=None)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()
            chunk_size = 2 * 1024 * 1024  # 2MB
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if self.cancel_flag:
                        f.close()
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        Clock.schedule_once(lambda dt: self.log('✗ Download cancelled'), 0)
                        return
                    
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        elapsed = time.time() - start_time
                        speed_mbps = (downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            Clock.schedule_once(lambda dt: self.update_progress(progress, speed_mbps), 0)
            
            Clock.schedule_once(lambda dt: self.log(f'✓ Saved: {filename}'), 0)
        except Exception as e:
            raise Exception(f'Download error: {str(e)}')


class ElbashaDownloaderApp(App):
    def build(self):
        self.title = 'Elbasha Downloader'
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return DownloadManager()


if __name__ == '__main__':
    ElbashaDownloaderApp().run()
