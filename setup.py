#!/usr/bin/env python3
"""
MedeX Setup Script
Professional setup for MedeX Medical AI System
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: MedeX requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        print("   Por favor actualice Python antes de continuar")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Instalando dependencias de MedeX...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        print("   Intente ejecutar manualmente: pip install -r requirements.txt")
        return False

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Configurando estructura de directorios...")
    
    directories = [
        "data/medical_conditions",
        "data/medications", 
        "data/protocols",
        "logs",
        "cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("✅ Estructura de directorios configurada")

def test_system():
    """Test basic system functionality"""
    print("\n🧪 Probando funcionalidad básica...")
    
    try:
        # Test imports
        from core.ai_engine import MedeXAIEngine
        print("   ✅ Motor de IA médica")
        
        # Test AI engine initialization
        engine = MedeXAIEngine()
        print("   ✅ Inicialización del motor")
        
        # Test knowledge base
        results = engine.knowledge_engine.search_medical_knowledge("diabetes")
        if results:
            print("   ✅ Base de conocimientos médicos")
        
        print("✅ Sistema funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba del sistema: {e}")
        return False

def display_completion_message():
    """Display setup completion message"""
    print("\n" + "="*60)
    print("🏥 MedeX - CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print("\n🎉 MedeX Medical AI System está listo para usar!")
    
    print("\n🚀 PARA COMENZAR:")
    print("   python3 medex_chat.py")
    
    print("\n📖 DOCUMENTACIÓN:")
    print("   docs/user_guide.md - Guía completa de usuario")
    
    print("\n🔧 CONFIGURACIÓN OPCIONAL:")
    print("   export KIMI_API_KEY='your-key' - Para integración Kimi")
    
    print("\n💡 EJEMPLOS DE USO:")
    print("   👨‍⚕️'Paciente 65 años, dolor torácico'")
    print("   👤 'Me duele el pecho'")
    print("   💊 'Dosis de aspirina'")
    
    print("\n⚠️ IMPORTANTE:")
    print("   🔬 Solo para uso educativo y de apoyo")
    print("   👨‍⚕️ No reemplaza evaluación médica profesional")
    print("   🚨 En emergencias: llame al 911")
    
    print("\n🏥 ¡Bienvenido a MedeX!")
    print("="*60)

def main():
    """Main setup function"""
    print("🏥 MedeX Medical AI System - Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️ Continuando sin algunas dependencias...")
        print("   Puede instalarlas manualmente después")
    
    # Setup directories
    setup_directories()
    
    # Test system
    if test_system():
        display_completion_message()
    else:
        print("\n⚠️ Setup completado con advertencias")
        print("   El sistema puede funcionar parcialmente")
        print("   Revise los errores arriba para resolverlos")

if __name__ == "__main__":
    main()