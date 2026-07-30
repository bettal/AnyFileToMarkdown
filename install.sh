#!/bin/bash
# install-anyfile-to-markdown.sh
# Скрипт установки AnyFileToMarkdown v2.0.0 на Debian/Ubuntu

set -e

DEB_FILE="dist/anyfile-to-markdown_2.0.0-1_all.deb"

if [ ! -f "$DEB_FILE" ]; then
    echo "Файл $DEB_FILE не найден. Сначала соберите пакет: make build-deb"
    exit 1
fi

echo "Установка $DEB_FILE..."
sudo dpkg -i "$DEB_FILE"

echo "Установка зависимостей..."
sudo apt-get install -f -y

echo "Готово! Запуск: anyfile-to-markdown"