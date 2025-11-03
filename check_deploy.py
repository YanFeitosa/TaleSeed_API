"""
Script para verificar se o projeto está pronto para deploy
"""

import os
import sys
from pathlib import Path

print("\n" + "="*60)
print("  🚀 VERIFICAÇÃO PRÉ-DEPLOY")
print("="*60 + "\n")

errors = []
warnings = []
success = []

# 1. Verifica arquivos necessários
required_files = [
    "main.py",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "render.yaml",
    "Procfile"
]

print("📁 Verificando arquivos necessários...")
for file in required_files:
    if Path(file).exists():
        success.append(f"✅ {file} encontrado")
    else:
        errors.append(f"❌ {file} NÃO encontrado")

# 2. Verifica se .env está no .gitignore
print("\n🔒 Verificando .gitignore...")
if Path(".gitignore").exists():
    with open(".gitignore", "r") as f:
        content = f.read()
        if ".env" in content:
            success.append("✅ .env está no .gitignore")
        else:
            errors.append("❌ .env NÃO está no .gitignore")
else:
    errors.append("❌ .gitignore não encontrado")

# 3. Verifica se .env existe localmente (não deve ser commitado)
print("\n🔑 Verificando configurações...")
if Path(".env").exists():
    warnings.append("⚠️  .env existe localmente (OK, mas NÃO deve ser commitado)")
    success.append("✅ .env existe para testes locais")
else:
    warnings.append("⚠️  .env não existe (use .env.example como base)")

# 4. Verifica requirements.txt
print("\n📦 Verificando dependências...")
if Path("requirements.txt").exists():
    with open("requirements.txt", "r") as f:
        deps = f.read()
        required_deps = ["fastapi", "uvicorn", "google-generativeai", "python-dotenv", "pydantic"]
        missing = []
        for dep in required_deps:
            if dep not in deps.lower():
                missing.append(dep)
        
        if missing:
            errors.append(f"❌ Dependências faltando: {', '.join(missing)}")
        else:
            success.append("✅ Todas as dependências necessárias estão presentes")

# 5. Verifica estrutura de diretórios
print("\n📂 Verificando estrutura...")
if Path("src").exists():
    if Path("src/models.py").exists() and Path("src/services/ai_service.py").exists():
        success.append("✅ Estrutura src/ correta")
    else:
        errors.append("❌ Arquivos faltando em src/")
else:
    errors.append("❌ Diretório src/ não encontrado")

# 6. Testa importação do módulo principal
print("\n🐍 Testando importações...")
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from main import app
    success.append("✅ main.py importa corretamente")
except Exception as e:
    errors.append(f"❌ Erro ao importar main.py: {e}")

# Resumo
print("\n" + "="*60)
print("  📊 RESUMO")
print("="*60 + "\n")

print("✅ SUCESSO:")
for s in success:
    print(f"  {s}")

if warnings:
    print("\n⚠️  AVISOS:")
    for w in warnings:
        print(f"  {w}")

if errors:
    print("\n❌ ERROS:")
    for e in errors:
        print(f"  {e}")
    print("\n⚠️  Corrija os erros antes de fazer deploy!\n")
    sys.exit(1)
else:
    print("\n🎉 PROJETO PRONTO PARA DEPLOY!")
    print("\nPróximos passos:")
    print("  1. git add .")
    print("  2. git commit -m 'Ready for deploy'")
    print("  3. git push")
    print("  4. Deploy no Render ou Railway")
    print("\n📚 Veja DEPLOY_QUICK.md para instruções detalhadas\n")
    sys.exit(0)
