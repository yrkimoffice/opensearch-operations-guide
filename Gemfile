source "https://rubygems.org"

# GitHub Pages 호환성을 위한 Jekyll 버전
gem "github-pages", group: :jekyll_plugins

# 추가 플러그인
gem "jekyll-remote-theme"
gem "jekyll-seo-tag"

# 로컬 개발용
gem "webrick", "~> 1.7"

# Windows 환경 지원
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]