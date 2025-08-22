#!/usr/bin/env python3
"""
🚀 간단한 PDF 생성 스크립트
- Jekyll 빌드된 HTML 활용 (완벽한 CSS 적용)
- QR코드 자동 삽입
- Playwright로 고품질 PDF 생성

사용법: python3 generate_simple_pdf.py
"""

import os
import sys
from pathlib import Path
import qrcode
import shutil
from datetime import datetime
from urllib.parse import urljoin

def install_requirements():
    """필요한 패키지 자동 설치"""
    try:
        import playwright
        import qrcode
        print("✅ 필요한 패키지가 이미 설치되어 있습니다.")
        return True
    except ImportError:
        print("📦 필요한 패키지를 설치합니다...")
        os.system("pip install playwright qrcode[pil]")
        os.system("playwright install chromium")
        return True

def generate_qr_code(url, size=(200, 200)):
    """QR 코드 생성 및 Base64 인코딩"""
    import base64
    from io import BytesIO
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # 이미지 생성
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize(size)
    
    # Base64로 변환
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"

def fix_css_and_inject_qr(html_content, page_url, project_root):
    """CSS 파일을 HTML에 인라인으로 삽입하고 QR코드 추가"""
    
    # 1. CSS 파일들을 읽어서 인라인으로 삽입
    site_dir = Path(project_root) / "_site"
    css_dir = site_dir / "assets" / "css"
    
    css_files = [
        "just-the-docs-default.css",
        "just-the-docs-head-nav.css"
    ]
    
    all_css = ""
    for css_file in css_files:
        css_path = css_dir / css_file
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                all_css += f.read() + "\n"
            print(f"✅ CSS 로드됨: {css_file}")
    
    # 기존 CSS 링크 제거하고 인라인 CSS 삽입
    import re
    
    # <link rel="stylesheet"> 태그들 제거
    html_content = re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="[^"]*\.css"[^>]*>', '', html_content)
    
    # 커스텀 callout CSS 추가 (SCSS 변수를 실제 값으로 변환)
    custom_callout_css = """
/* Custom Callout Styles */
.note {
  color: #0550AE;
  background-color: #f6f8fa;
  border: 1px solid #d1d9e0;
  border-left: 4px solid #dbeafe;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
}

.note > blockquote {
  color: #0550AE;
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 0;
}

.note > blockquote > p, .note > p {
  margin: 0 0 8px 0;
}

.note > blockquote > p:last-child, .note > p:last-child {
  margin-bottom: 0;
}

.warning {
  color: #BF8700;
  background-color: #f6f8fa;
  border: 1px solid #d1d9e0;
  border-left: 4px solid #fde047;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
}

.warning > blockquote {
  color: #BF8700;
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 0;
}

.warning > blockquote > p, .warning > p {
  margin: 0 0 8px 0;
}

.warning > blockquote > p:last-child, .warning > p:last-child {
  margin-bottom: 0;
}

.important {
  color: #D1242F;
  background-color: #f6f8fa;
  border: 1px solid #d1d9e0;
  border-left: 4px solid #fca5a5;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
}

.important > blockquote {
  color: #D1242F;
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 0;
}

.important > blockquote > p, .important > p {
  margin: 0 0 8px 0;
}

.important > blockquote > p:last-child, .important > p:last-child {
  margin-bottom: 0;
}

.highlight {
  color: #8250df;
  background-color: #f6f8fa;
  border: 1px solid #d1d9e0;
  border-left: 4px solid #e9d5ff;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
}

.highlight > blockquote {
  color: #8250df;
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 0;
}

.highlight > blockquote > p, .highlight > p {
  margin: 0 0 8px 0;
}

.highlight > blockquote > p:last-child, .highlight > p:last-child {
  margin-bottom: 0;
}

.new {
  color: #1F883D;
  background-color: #f6f8fa;
  border: 1px solid #d1d9e0;
  border-left: 4px solid #86efac;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
}

.new > blockquote {
  color: #1F883D;
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 0;
}

.new > blockquote > p, .new > p {
  margin: 0 0 8px 0;
}

.new > blockquote > p:last-child, .new > p:last-child {
  margin-bottom: 0;
}

.success {
  color: #2DA44E;
  background-color: #f6f8fa;
  border: 1px solid #d1d9e0;
  border-left: 4px solid #dcfce7;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
}

.success > blockquote {
  color: #2DA44E;
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 0;
}

.success > blockquote > p, .success > p {
  margin: 0 0 8px 0;
}

.success > blockquote > p:last-child, .success > p:last-child {
  margin-bottom: 0;
}

/* Font Awesome icons in callouts */
.note i.fas, .note i.fa,
.warning i.fas, .warning i.fa,
.important i.fas, .important i.fa,
.highlight i.fas, .highlight i.fa,
.new i.fas, .new i.fa,
.success i.fas, .success i.fa {
  margin-right: 8px;
}

.note > blockquote i.fas, .note > blockquote i.fa,
.warning > blockquote i.fas, .warning > blockquote i.fa,
.important > blockquote i.fas, .important > blockquote i.fa,
.highlight > blockquote i.fas, .highlight > blockquote i.fa,
.new > blockquote i.fas, .new > blockquote i.fa,
.success > blockquote i.fas, .success > blockquote i.fa {
  margin-right: 8px;
}
"""
    
    # 모든 CSS 합치기 (기본 테마 CSS + 커스텀 callout CSS)
    complete_css = all_css + custom_callout_css
    
    # 인라인 CSS 삽입
    inline_css = f"<style>\n{complete_css}\n</style>"
    html_content = html_content.replace('</head>', f'{inline_css}\n</head>')
    
    # 2. QR 코드 HTML 생성
    qr_code_data = generate_qr_code(page_url)
    
    # QR 코드를 문서 제목 근처에 작고 깔끔하게 배치
    qr_html = f"""
    <div style="
        float: right; 
        margin: 10px 0 10px 20px;
        background: white; 
        padding: 8px; 
        border: 1px solid #ddd; 
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 90px;
    ">
        <img src="{qr_code_data}" style="width: 70px; height: 70px; margin-bottom: 4px;" />
        <div style="font-size: 8px; color: #666; font-weight: bold; line-height: 1.2;">
            🌐 Live
        </div>
        <div style="font-size: 6px; color: #888; margin-top: 1px; line-height: 1;">
            Scan me
        </div>
    </div>
    """
    
    # 첫 번째 <h1> 태그 바로 앞에 QR 코드 삽입 (문서 상단에 한 번만)
    if '<h1' in html_content:
        html_content = html_content.replace('<h1', f'{qr_html}<h1', 1)  # 첫 번째만 교체
    else:
        # <h1>이 없다면 main 콘텐츠 시작 부분에 삽입
        if '<main' in html_content:
            html_content = re.sub(r'(<main[^>]*>)', r'\1' + qr_html, html_content)
        else:
            # 그것도 없다면 body 태그 뒤에
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<body>{qr_html}')
            elif '<body' in html_content:
                html_content = re.sub(r'(<body[^>]*>)', r'\1' + qr_html, html_content)
    
    return html_content

def generate_pdf_from_jekyll():
    """Jekyll 빌드 결과를 사용해 PDF 생성"""
    
    # 경로 설정
    project_root = Path(__file__).parent
    site_dir = project_root / "_site"
    docs_dir = site_dir / "docs"
    output_dir = project_root / "portfolio" / "pdf"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Jekyll 사이트가 빌드되었는지 확인
    if not site_dir.exists() or not docs_dir.exists():
        print("❌ Jekyll 사이트가 빌드되지 않았습니다.")
        print("💡 다음 명령어로 Jekyll을 먼저 빌드하세요:")
        print("   bundle exec jekyll build")
        return False
    
    # GitHub Pages URL (실제 배포 URL로 변경)
    BASE_URL = "https://yrkimoffice.github.io/opensearch-operations-guide"
    
    # 생성할 문서들
    documents = [
        {
            "html_file": "guide.html",
            "output_name": "OpenSearch_운영가이드.pdf",
            "page_url": f"{BASE_URL}/docs/guide"
        },
        {
            "html_file": "quick-reference.html", 
            "output_name": "빠른참조가이드.pdf",
            "page_url": f"{BASE_URL}/docs/quick-reference"
        }
    ]
    
    # Playwright 설치 확인
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright가 설치되지 않았습니다.")
        if input("📦 지금 설치하시겠습니까? (y/n): ").lower() == 'y':
            install_requirements()
            from playwright.sync_api import sync_playwright
        else:
            return False
    
    print("🚀 PDF 생성 시작...")
    
    # 각 문서에 대해 PDF 생성
    for doc in documents:
        html_path = docs_dir / doc["html_file"]
        output_path = output_dir / doc["output_name"]
        
        if not html_path.exists():
            print(f"❌ HTML 파일이 없습니다: {html_path}")
            continue
        
        print(f"📄 처리 중: {doc['output_name']}")
        
        # HTML 파일 읽기
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # CSS 수정 및 QR 코드 삽입
        html_with_qr = fix_css_and_inject_qr(html_content, doc["page_url"], project_root)
        
        # 임시 HTML 파일 생성
        temp_html = output_dir / f"temp_{doc['html_file']}"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_with_qr)
        
        # Playwright로 PDF 생성
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # HTML 로드
                page.goto(f"file://{temp_html.absolute()}")
                
                # PDF 생성 (75% 크기로 축소)
                page.pdf(
                    path=str(output_path),
                    format='A4',
                    scale=0.75,  # 75% 크기로 축소
                    margin={
                        'top': '15mm',
                        'bottom': '15mm', 
                        'left': '12mm',
                        'right': '12mm'
                    },
                    print_background=True  # CSS 배경색 포함
                )
                
                browser.close()
            
            print(f"✅ PDF 생성 성공: {output_path}")
            
            # 임시 파일 삭제
            temp_html.unlink()
            
        except Exception as e:
            print(f"❌ PDF 생성 실패 ({doc['output_name']}): {e}")
            # 임시 파일 정리
            if temp_html.exists():
                temp_html.unlink()
    
    print(f"\n🎉 PDF 생성 완료!")
    print(f"📂 출력 위치: {output_dir}")
    print(f"✨ 특징:")
    print(f"   - Jekyll과 동일한 CSS 스타일 ✅")
    print(f"   - QR코드 자동 삽입 ✅")
    print(f"   - 고품질 PDF 출력 ✅")
    
    return True

if __name__ == "__main__":
    # 요구사항 확인
    if not install_requirements():
        print("❌ 패키지 설치에 실패했습니다.")
        sys.exit(1)
    
    # PDF 생성
    success = generate_pdf_from_jekyll()
    
    if success:
        print("\n💡 사용 팁:")
        print("   1. Jekyll 서버 실행: bundle exec jekyll serve")
        print("   2. 브라우저에서 확인: http://localhost:4000")
        print("   3. PDF 생성: python3 generate_simple_pdf.py")
    else:
        print("\n❌ PDF 생성에 실패했습니다.")
        sys.exit(1)