# Process_Images_Obsidian
Данный скрипт используется в статье: [Автоматизация публикации записей из Obsidian на WordPress-сайт](https://kostegs.name/auto-publicate-notes-from-obsidian-to-wordpress/)

Скрипт принимает 2 параметра на вход: 
- Путь к исходному файлу Obsidian
- Путь к спец. хранилищу для подготовки заметок к публикации на сайт

Далее, скрипт копирует исходный файл заметки, все изображения сохраняет в спец. хранилище, конвертируя в JPEG и сжимая их. В скопированном исходном файле подменяет ссылки на новые изображения.
