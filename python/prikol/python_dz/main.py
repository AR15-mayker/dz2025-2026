
import os
import tempfile
import shutil
import subprocess
from collections import Counter, defaultdict

# Карта расширений к языкам программирования
EXT_TO_LANG = {
	'.py': 'Python',
	'.js': 'JavaScript',
	'.ts': 'TypeScript',
	'.java': 'Java',
	'.c': 'C',
	'.cpp': 'C++',
	'.cs': 'C#',
	'.rb': 'Ruby',
	'.go': 'Go',
	'.php': 'PHP',
	'.rs': 'Rust',
	'.swift': 'Swift',
	'.kt': 'Kotlin',
	'.m': 'Objective-C',
	'.sh': 'Shell',
	'.html': 'HTML',
	'.css': 'CSS',
	'.json': 'JSON',
	'.xml': 'XML',
	'.md': 'Markdown',
	'.yml': 'YAML',
	'.yaml': 'YAML',
	'.pl': 'Perl',
	'.r': 'R',
	'.dart': 'Dart',
	'.scala': 'Scala',
	'.lua': 'Lua',
	'.bat': 'Batch',
	'.ps1': 'PowerShell',
	'.sql': 'SQL',
	'.h': 'C/C++ header',
	'.hpp': 'C++ header',
	'.vue': 'Vue',
	'.tsx': 'TypeScript JSX',
	'.jsx': 'JavaScript JSX',
	'.ini': 'INI',
	'.conf': 'Config',
	'.toml': 'TOML',
	'.make': 'Makefile',
	'.dockerfile': 'Dockerfile',
	'.gradle': 'Gradle',
	'.lock': 'Lockfile',
	'.gitignore': 'Gitignore',
	'.env': 'Env',
}

def clone_repo(repo_url, dest_dir):
	result = subprocess.run(["git", "clone", repo_url, dest_dir], capture_output=True, text=True)
	if result.returncode != 0:
		print("Ошибка клонирования:", result.stderr)
		return False
	return True

def analyze_repo(path):
	file_count = 0
	total_lines = 0
	extensions = []
	lang_files = defaultdict(int)
	lang_lines = defaultdict(int)
	for root, dirs, files in os.walk(path):
		for file in files:
			file_count += 1
			ext = os.path.splitext(file)[1].lower()
			extensions.append(ext)
			lang = EXT_TO_LANG.get(ext, 'Other/Unknown')
			lang_files[lang] += 1
			try:
				with open(os.path.join(root, file), encoding="utf-8", errors="ignore") as f:
					lines = sum(1 for _ in f)
					total_lines += lines
					lang_lines[lang] += lines
			except Exception:
				pass
	lang_counter = Counter(extensions)
	print(f"Всего файлов: {file_count}")
	print(f"Всего строк кода: {total_lines}")
	if file_count:
		print(f"Среднее строк на файл: {total_lines // file_count}")
	print("\nТоп-5 расширений:")
	for ext, count in lang_counter.most_common(5):
		print(f"  {ext or '[без расширения]'}: {count}")
	print("\nЯзыки программирования:")
	for lang, count in sorted(lang_files.items(), key=lambda x: -x[1]):
		percent = 100 * count / file_count if file_count else 0
		lines = lang_lines[lang]
		print(f"  {lang}: файлов {count} ({percent:.1f}%), строк {lines}")

if __name__ == "__main__":
	repo_url = input("Введите ссылку на публичный GitHub-репозиторий: ")
	with tempfile.TemporaryDirectory() as tmpdir:
		print("Клонирование репозитория...")
		if clone_repo(repo_url, tmpdir):
			print("Анализ...")
			analyze_repo(tmpdir)
		else:
			print("Не удалось клонировать репозиторий.")
