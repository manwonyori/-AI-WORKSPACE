"""
Cafe24 FTP    HTML    
AI   FTP  HTML   
"""

import sys
import json
import re
import paramiko
import os
from pathlib import Path
from datetime import datetime
import hashlib
import time

# CUA-MASTER  
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')

from core.claude_code_bridge import ClaudeCodeBridge

class FTPImageUploadSystem:
    """FTP    HTML   """
    
    def __init__(self):
        self.bridge = ClaudeCodeBridge()
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24")
        self.ftp_config_path = self.base_path / "FTP_CONFIG.json"
        self.ftp_mirror_path = self.base_path / "ftp_mirror"
        
        # FTP  
        self.load_ftp_config()
        
        #  
        self.content_path = self.base_path / "complete_content"
        self.html_path = self.content_path / "html" / "temp_txt"
        self.optimized_path = self.content_path / "optimized_with_ai_images"
        self.upload_ready_path = self.content_path / "upload_ready"
        self.upload_ready_path.mkdir(exist_ok=True)
        
        # FTP   -    
        #        
        self.project_folder = f"ai_optimization_{datetime.now().strftime('%Y%m%d')}"
        self.ftp_image_base = f"/web/product/{self.project_folder}"
        self.public_url_base = f"https://manwonyori.cafe24.com/web/product/{self.project_folder}"
        
        print(" FTP    ")
        print(f"  - FTP : {self.ftp_config['sftp_server']['host']}")
        print(f"  -  : {self.ftp_image_base}")
    
    def load_ftp_config(self):
        """FTP  """
        with open(self.ftp_config_path, 'r', encoding='utf-8') as f:
            self.ftp_config = json.load(f)
    
    def get_product_category(self, product_name):
        """  """
        # / 
        categories = {
            '': 'manwon',
            '': 'insaeng',
            '': 'ccw',
            '': 'banchan',
            '': 'chwiyoung',
            '': 'mobidick',
            '': 'pizza',
            'BS': 'bs',
            '': 'choi'
        }
        
        #   
        for brand, folder in categories.items():
            if brand in product_name:
                return folder
        
        #  
        return 'etc'
    
    def connect_sftp(self):
        """SFTP """
        try:
            transport = paramiko.Transport((
                self.ftp_config['sftp_server']['host'],
                self.ftp_config['sftp_server']['port']
            ))
            transport.connect(
                username=self.ftp_config['sftp_server']['username'],
                password=self.ftp_config['sftp_server']['password']
            )
            sftp = paramiko.SFTPClient.from_transport(transport)
            print(" SFTP  ")
            return sftp, transport
        except Exception as e:
            print(f" SFTP  : {e}")
            return None, None
    
    def create_ftp_directory(self, sftp, remote_path):
        """FTP   ()"""
        dirs = []
        dir_path = remote_path
        while len(dir_path) > 1:
            dirs.append(dir_path)
            dir_path = os.path.dirname(dir_path)
        
        #   
        for dir_path in reversed(dirs):
            try:
                sftp.stat(dir_path)
            except:
                try:
                    sftp.mkdir(dir_path)
                    print(f"    : {dir_path}")
                except:
                    pass
    
    def upload_image_to_ftp(self, local_image_path, product_name):
        """ FTP   URL """
        
        sftp, transport = self.connect_sftp()
        if not sftp:
            return None
        
        try:
            #   ( ,  )
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', product_name)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            #   
            local_file = Path(local_image_path)
            if not local_file.exists():
                #    ()
                local_file = self.create_sample_image(product_name)
            
            file_ext = local_file.suffix or '.jpg'
            remote_filename = f"{safe_name}_{timestamp}{file_ext}"
            
            # FTP   -    
            #    
            category = self.get_product_category(product_name)
            remote_dir = f"{self.ftp_image_base}/{category}"
            remote_path = f"{remote_dir}/{remote_filename}"
            
            #  
            self.create_ftp_directory(sftp, remote_dir)
            
            #  
            print(f"    : {remote_filename}")
            sftp.put(str(local_file), remote_path)
            
            #  URL  -    
            public_url = f"{self.public_url_base}/{category}/{remote_filename}"
            
            print(f"    : {public_url}")
            
            #    -    
            local_mirror = self.ftp_mirror_path / "upload" / "web" / "product" / self.project_folder / category
            local_mirror.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(local_file, local_mirror / remote_filename)
            
            return public_url
            
        except Exception as e:
            print(f"    : {e}")
            return None
            
        finally:
            if sftp:
                sftp.close()
            if transport:
                transport.close()
    
    def create_sample_image(self, product_name):
        """   ()"""
        from PIL import Image, ImageDraw, ImageFont
        
        #   
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        #  
        text = f"AI Generated\n{product_name}\n{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        draw.multiline_text(
            (400, 300), 
            text, 
            fill='black',
            anchor='mm',
            align='center'
        )
        
        # 
        sample_path = self.content_path / "temp_images"
        sample_path.mkdir(exist_ok=True)
        
        filename = f"sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = sample_path / filename
        img.save(filepath, 'JPEG', quality=95)
        
        return filepath
    
    def process_html_with_ftp_links(self, html_file):
        """HTML   -  FTP   """
        
        print(f"\n  : {html_file.name}")
        
        # HTML 
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        #  
        title_match = re.search(r'<title>([^<]+)</title>', content)
        product_name = title_match.group(1) if title_match else html_file.stem
        
        #     
        img_pattern = r'<img([^>]+)src=["\']([^"\']+)["\']([^>]*)>'
        
        def replace_image(match):
            """   """
            pre_attr = match.group(1)
            old_src = match.group(2)
            post_attr = match.group(3)
            
            # FTP 
            print(f"    : {old_src[:50]}...")
            new_url = self.upload_image_to_ftp(old_src, product_name)
            
            if new_url:
                # lazy loading 
                return f'<img{pre_attr}src="{new_url}" loading="lazy"{post_attr}>'
            else:
                #    
                return match.group(0)
        
        #    
        content = re.sub(img_pattern, replace_image, content)
        
        #  
        content = self.add_optimization_tags(content, product_name)
        
        return content, product_name
    
    def add_optimization_tags(self, content, product_name):
        """HTML   """
        
        # SEO   
        seo_tags = f"""
    <meta name="description" content="{product_name} -   ">
    <meta property="og:title" content="{product_name}">
    <meta property="og:type" content="product">
    <meta property="og:image" content="{self.public_url_base}/main.jpg">
    
    <!--    -->
    <script>
        // Lazy Loading Polyfill
        if ('loading' in HTMLImageElement.prototype) {{
            const images = document.querySelectorAll('img[loading="lazy"]');
            images.forEach(img => {{
                img.src = img.dataset.src || img.src;
            }});
        }}
    </script>
        """
        
        # </head>   
        if '</head>' in content:
            content = content.replace('</head>', f'{seo_tags}\n</head>')
        else:
            # head     
            content = f'<head>{seo_tags}</head>\n{content}'
        
        return content
    
    def process_all_files(self):
        """ HTML  """
        
        html_files = list(self.html_path.glob("*.txt"))
        total = len(html_files)
        
        print(f"\n{'='*60}")
        print(f" FTP    HTML  ")
        print(f"   {total} ")
        print(f"{'='*60}")
        
        # Claude Bridge   
        request = {
            "task": "FTP    HTML  ",
            "total_files": total,
            "ftp_server": self.ftp_config['sftp_server']['host'],
            "upload_path": self.ftp_image_base
        }
        
        actions = self.bridge.request_action_plan(
            task="Cafe24 FTP  ",
            context=request
        )
        
        success_count = 0
        fail_count = 0
        
        #  ( 3)
        for i, html_file in enumerate(html_files[:3], 1):
            try:
                print(f"\n[{i}/3] {html_file.name}")
                
                # HTML 
                optimized_content, product_name = self.process_html_with_ftp_links(html_file)
                
                # 
                output_file = self.upload_ready_path / f"ftp_ready_{html_file.name.replace('.txt', '.html')}"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(optimized_content)
                
                print(f"   : {output_file.name}")
                success_count += 1
                
                # 
                self.bridge.send_feedback(
                    action_id=f"ftp_upload_{int(time.time())}",
                    result={
                        "file": html_file.name,
                        "success": True,
                        "product": product_name
                    }
                )
                
            except Exception as e:
                print(f"   : {e}")
                fail_count += 1
        
        #  
        print(f"\n{'='*60}")
        print(f"  ")
        print(f"  : {success_count}")
        print(f"  : {fail_count}")
        print(f"   : {self.upload_ready_path}")
        print(f"{'='*60}")
        
        return success_count, fail_count
    
    def verify_ftp_connection(self):
        """FTP  """
        print("\n FTP  ...")
        
        sftp, transport = self.connect_sftp()
        if sftp:
            try:
                #   
                items = sftp.listdir('/')
                print(f"    ")
                print(f"    : {items[:5]}...")
                
                #    /
                self.create_ftp_directory(sftp, self.ftp_image_base)
                print(f"       : {self.ftp_image_base}")
                print(f"      !")
                
                #     
                for category in ['manwon', 'insaeng', 'ccw', 'banchan', 'etc']:
                    category_path = f"{self.ftp_image_base}/{category}"
                    self.create_ftp_directory(sftp, category_path)
                    print(f"    - {category}/  ")
                
                return True
                
            except Exception as e:
                print(f"     : {e}")
                return False
            finally:
                sftp.close()
                transport.close()
        else:
            return False
    
    def interactive_menu(self):
        """ """
        
        while True:
            print("\n" + "="*60)
            print(" FTP   ")
            print("="*60)
            print("\n1. FTP  ")
            print("2.  HTML   (  +  )")
            print("3.   ")
            print("4. FTP   ")
            print("5.    ")
            print("0. ")
            print("-"*60)
            
            choice = input("\n: ").strip()
            
            if choice == "1":
                self.verify_ftp_connection()
                
            elif choice == "2":
                self.process_all_files()
                
            elif choice == "3":
                files = list(self.html_path.glob("*.txt"))
                if files:
                    test_file = files[0]
                    print(f"\n : {test_file.name}")
                    content, product = self.process_html_with_ftp_links(test_file)
                    print("  ")
                    
            elif choice == "4":
                sftp, transport = self.connect_sftp()
                if sftp:
                    try:
                        items = sftp.listdir('/web/product')
                        print(f"\n /web/product :")
                        for item in items[:10]:
                            print(f"  - {item}")
                    except:
                        print("   .")
                    finally:
                        sftp.close()
                        transport.close()
                        
            elif choice == "5":
                ready_files = list(self.upload_ready_path.glob("*.html"))
                print(f"\n    : {len(ready_files)}")
                for f in ready_files[:5]:
                    print(f"  - {f.name}")
                    
            elif choice == "0":
                print(".")
                break
                
            else:
                print(" .")


def main():
    """ """
    system = FTPImageUploadSystem()
    
    #   
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            system.verify_ftp_connection()
        elif command == "process":
            system.process_all_files()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python ftp_image_upload_system.py [test|process]")
    else:
        #  
        system.interactive_menu()


if __name__ == "__main__":
    main()