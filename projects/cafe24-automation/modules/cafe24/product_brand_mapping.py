"""
Cafe24 Product Brand Mapping Script
Reorganizes HTML files from 기타(Others) to correct brand folders
Based on CSV supplier data analysis
"""

import os
import shutil
import json
from pathlib import Path

# Product-Supplier Mapping from CSV analysis
PRODUCT_SUPPLIER_MAPPING = {
    'S000000Y': {
        'name': '씨씨더블유',
        'products': [339, 338, 337, 336, 335, 334, 333, 332, 331, 284, 283, 282, 281, 280, 279, 
                    278, 277, 276, 275, 274, 273, 272, 271, 270, 269, 268, 267, 266, 265, 264, 
                    263, 262, 261, 260, 259, 258, 257, 256]
    },
    'S000000Q': {
        'name': '만원요리',
        'products': [330, 168, 319, 337]  # Added known products from dashboard
    },
    'S000000T': {
        'name': '인생',
        'products': [320, 319, 318, 317, 316, 315, 314, 313, 312, 311, 252, 251, 250, 249, 248, 
                    247, 246, 245, 244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234, 233, 
                    232, 231, 230, 229, 228, 227, 226, 225, 224, 223, 222, 221, 220, 219, 218, 
                    217, 216, 215, 214, 213, 212]
    },
    'S000000U': {
        'name': '인생만두',
        'products': list(range(311, 321))  # 311-320
    },
    'S000000V': {
        'name': '취영루',
        'products': [62, 65] + list(range(131, 146))  # 62, 65, 131-145
    }
}

def reorganize_html_files():
    """Reorganize HTML files from 기타 folder to correct brand folders"""
    
    base_path = Path(r'C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html')
    others_path = base_path / '기타'
    
    if not others_path.exists():
        print(f"기타 folder not found at {others_path}")
        return
    
    # Create brand folders if they don't exist
    brand_folders = {
        '씨씨더블유': base_path / '씨씨더블유',
        '만원요리': base_path / '만원요리',
        '인생': base_path / '인생',
        '인생만두': base_path / '인생만두',
        '취영루': base_path / '취영루'
    }
    
    for brand, folder in brand_folders.items():
        folder.mkdir(exist_ok=True)
        print(f"[OK] Brand folder ready: {brand}")
    
    # Get all HTML files from 기타 folder
    html_files = list(others_path.glob('*.html'))
    print(f"\nFound {len(html_files)} HTML files in 기타 folder")
    
    moved_count = {}
    for supplier_code, info in PRODUCT_SUPPLIER_MAPPING.items():
        brand_name = info['name']
        products = info['products']
        moved_count[brand_name] = 0
        
        for product_num in products:
            # Try different file naming patterns
            patterns = [
                f'product_{product_num}.html',
                f'{product_num}.html',
                f'*_{product_num}.html',
                f'*_{product_num}_*.html'
            ]
            
            for pattern in patterns:
                matching_files = list(others_path.glob(pattern))
                for file in matching_files:
                    dest_folder = brand_folders[brand_name]
                    dest_file = dest_folder / file.name
                    
                    try:
                        shutil.move(str(file), str(dest_file))
                        moved_count[brand_name] += 1
                        print(f"  -> Moved {file.name} to {brand_name}")
                    except Exception as e:
                        print(f"  [ERROR] Error moving {file.name}: {e}")
    
    # Summary
    print("\n=== Reorganization Summary ===")
    for brand, count in moved_count.items():
        print(f"{brand}: {count} files moved")
    
    remaining = len(list(others_path.glob('*.html')))
    print(f"\nRemaining in 기타: {remaining} files")
    
    # Update statistics
    update_statistics()

def update_statistics():
    """Update statistics after reorganization"""
    
    base_path = Path(r'C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html')
    
    stats = {}
    total = 0
    
    for folder in base_path.iterdir():
        if folder.is_dir():
            html_count = len(list(folder.glob('*.html')))
            if html_count > 0:
                stats[folder.name] = html_count
                total += html_count
    
    print("\n=== Updated Statistics ===")
    print(f"Total HTML files: {total}")
    for brand, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {brand}: {count} files")
    
    # Save statistics to JSON
    stats_file = base_path.parent / 'statistics.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': total,
            'brands': stats,
            'last_updated': '2025-09-01'
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Statistics saved to {stats_file}")

if __name__ == "__main__":
    print("Starting HTML file reorganization based on CSV supplier data...")
    print("=" * 50)
    reorganize_html_files()
    print("\n[OK] Reorganization complete!")