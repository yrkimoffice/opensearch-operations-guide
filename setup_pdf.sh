#!/bin/bash
# 🚀 PDF 생성 환경 설정 스크립트

echo "📋 OpenSearch 가이드 PDF 생성 설정"
echo "=================================="

# 1. Jekyll 빌드
echo "🏗️  Jekyll 사이트 빌드 중..."
if bundle exec jekyll build; then
    echo "✅ Jekyll 빌드 성공"
else
    echo "❌ Jekyll 빌드 실패"
    echo "💡 다음을 확인하세요:"
    echo "   - bundle install 실행했는지"
    echo "   - Gemfile이 있는 디렉토리에서 실행했는지"
    exit 1
fi

# 2. Python 패키지 설치
echo ""
echo "📦 Python 패키지 설치 중..."
pip install playwright qrcode[pil] || {
    echo "❌ 패키지 설치 실패"
    echo "💡 pip를 업데이트하고 다시 시도하세요: pip install --upgrade pip"
    exit 1
}

# 3. Playwright 브라우저 설치
echo ""
echo "🌐 Playwright 브라우저 설치 중..."
playwright install chromium || {
    echo "❌ 브라우저 설치 실패"
    exit 1
}

# 4. PDF 생성 실행
echo ""
echo "📄 PDF 생성 중..."
python3 generate_simple_pdf.py

echo ""
echo "🎉 설정 및 PDF 생성 완료!"
echo "📂 생성된 파일 확인: portfolio/pdf/"
echo ""
echo "📋 다음에는 이 명령어만 실행하세요:"
echo "   python3 generate_simple_pdf.py"