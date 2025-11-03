"""
Script para verificar as configurações do .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env
project_dir = Path(__file__).parent
load_dotenv(project_dir / ".env")

print("\n" + "="*60)
print("  VERIFICAÇÃO DAS CONFIGURAÇÕES DO .ENV")
print("="*60 + "\n")

# Lista todas as configurações esperadas
configs = {
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    "GEMINI_MODEL": os.getenv("GEMINI_MODEL"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL"),
    "TEMPERATURE": os.getenv("TEMPERATURE"),
    "MAX_OUTPUT_TOKENS": os.getenv("MAX_OUTPUT_TOKENS"),
    "PORT": os.getenv("PORT"),
}

# Exibe as configurações
for key, value in configs.items():
    if value:
        # Oculta parcialmente a API key
        if key == "GEMINI_API_KEY":
            masked_value = value[:10] + "..." + value[-4:] if len(value) > 14 else "***"
            status = "✅"
        else:
            masked_value = value
            status = "✅"
        print(f"{status} {key:20s} = {masked_value}")
    else:
        print(f"❌ {key:20s} = NÃO CONFIGURADO")

print("\n" + "="*60)

# Verifica se a API key está configurada
if not configs["GEMINI_API_KEY"]:
    print("\n⚠️  ATENÇÃO: GEMINI_API_KEY não está configurada!")
    print("   Configure no arquivo .env antes de executar a API.\n")
else:
    print("\n✅ Todas as configurações obrigatórias estão presentes!")
    print(f"   A API usará o modelo: {configs['GEMINI_MODEL'] or 'gemini-1.5-flash (padrão)'}\n")
