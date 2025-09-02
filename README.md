![MedeX Banner](banner.png)

# 🏥 MedeX - Sistema Avanzado de IA Médica

> **[English Version](README_EN.md) | Versión en Español**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Medical AI](https://img.shields.io/badge/Medical-AI-red.svg)](https://github.com)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com)

> **Sistema Avanzado de IA Médica con detección inteligente de usuarios, protocolos de emergencia y base de conocimiento médico integral**

MedeX representa una evolución sofisticada en la tecnología de IA médica. El proyecto abarca tanto el framework fundamental de MedeX como su implementación insignia **MedeX v25.83**, impulsado por **Kimi K2-0711-Preview** que adapta automáticamente las respuestas para profesionales de la salud y pacientes, proporcionando información médica precisa con protocolos de seguridad integrados.

## 🎯 Resumen del Proyecto

### **Framework MedeX**

La arquitectura central de IA médica diseñada para:

- Procesamiento y recuperación de conocimiento médico
- Implementación RAG (Recuperación Aumentada por Generación)
- Integración de bases de datos médicas
- Sistemas de información farmacéutica

### **MedeX v25.83** - Sistema de Producción Actual

Nuestro asistente de IA médica insignia que incluye:

- **Detección Automática de Usuarios**: Distingue entre profesionales de la salud y pacientes
- **Respuestas Conscientes del Contexto**: Adapta el lenguaje y nivel de detalle según corresponda
- **Detección de Emergencias**: Identifica automáticamente emergencias médicas con protocolos apropiados
- **Streaming en Tiempo Real**: Respuestas progresivas para mejor experiencia de usuario

## ✨ Características Principales

### 🧠 **IA Médica Inteligente**

- **Modo Profesional vs Educativo**: Adaptación automática basada en análisis de consultas
- **Protocolos de Emergencia**: Reconocimiento instantáneo y guía médica de emergencia apropiada
- **Respuestas en Streaming**: Generación de respuestas progresivas en tiempo real
- **Detección de Terminología Médica**: PLN avanzado para comprensión de contexto médico

### 📚 **Conocimiento Médico Integral**

- **Condiciones Codificadas ICD-10**: Base de datos completa de condiciones médicas
- **Información Farmacéutica**: Interacciones medicamentosas, dosificaciones y contraindicaciones
- **Protocolos Clínicos**: Guías de tratamiento basadas en evidencia
- **Búsqueda Mejorada por RAG**: Búsqueda semántica a través de literatura médica
- **Valores de Laboratorio**: Rangos normales y guías de interpretación

### 🔬 **Capacidades Avanzadas**

- **Procesamiento Multi-modal**: Consultas médicas basadas en texto con capacidad de expansión
- **Integración de Búsqueda Web**: Recuperación de información médica en tiempo real
- **Respuestas Estructuradas**: Formato de documentación médica profesional
- **Gestión de Sesiones**: Historial de conversaciones inteligente y estadísticas

### 🛡️ **Seguridad Médica**

- **Disclaimers Integrados**: Disclaimers médicos profesionales en todas las respuestas
- **Protocolos de Emergencia**: Activación automática para condiciones críticas
- **Derivación Profesional**: Guía apropiada para consulta médica
- **Estándares de Calidad**: Adherencia a estándares de información médica

## 📋 Ejemplos de Consultas

Explora nuestros ejemplos de consultas médicas reales procesadas por MedeX v25.83:

### 🎓 **Consultas Educativas**

- **[AINEs y sus Características](docs/consulta_aines_caracteristicas.md)** - Información general sobre antiinflamatorios
- **[Síndrome Pierre Robin](docs/consulta_sindrome_pierre_robin.md)** - Malformación congénita craneofacial
- **[Síndrome de Treacher Collins](docs/consulta_sindrome_treacher_collins.md)** - Disostosis mandibulo-facial

### 👨‍⚕️ **Consultas Profesionales**

- **[Enfermedad Celíaca con Malabsorción](docs/consulta_celiaca_malabsorcion.md)** - Caso clínico gastroenterológico
- **[Dermatomiositis del Adulto](docs/consulta_dermatomiositis_adulto.md)** - Caso reumatológico con manifestaciones cutáneas
- **[Pleuritis Lúpica](docs/consulta_pleuritis_lupica.md)** - Complicación pulmonar en lupus eritematoso sistémico
- **[Síndrome Coronario Agudo](docs/consulta_sindrome_coronario_agudo.md)** - Emergencia cardiológica con protocolos de actuación
- **[Diabetes Insípida Central](docs/consulta_diabetes_insipida.md)** - Caso endocrinológico complejo

_Estos ejemplos demuestran la capacidad dual de MedeX v25.83 para adaptar respuestas según el tipo de usuario detectado._

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8+
- Entorno virtual (recomendado)
- Cuenta en [Moonshot AI](https://platform.moonshot.ai/) con API key

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/medex.git
cd medex

# Crear entorno virtual
python3 -m venv medex_venv
source medex_venv/bin/activate  # Linux/Mac
# o
medex_venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key (OBLIGATORIO)
# Abre api_key.txt y pega tu API key de Moonshot
# (obtén tu API key en: https://platform.moonshot.ai/)

# Iniciar MedeX
python MEDEX_FINAL.py
```

### Uso Básico

**⚠️ Configuración rápida**:

1. Abre `api_key.txt` y pega tu API key de [Moonshot AI](https://platform.moonshot.ai/)
2. Guarda el archivo y ejecuta MedeX

```python
from MEDEX_FINAL import MedeXv2583

# Inicializar sistema (carga automáticamente tu API key)
medex = MedeXv2583()

# Consulta profesional
respuesta = await medex.generate_response(
    "Paciente masculino 45 años con dolor torácico opresivo..."
)

# Consulta educativa
respuesta = await medex.generate_response(
    "¿Qué son los AINEs?"
)
```

## 🏗️ Arquitectura del Proyecto

```
MedeX/
├── 🏥 MEDEX_FINAL.py           # Sistema principal v25.83
├── 💬 medex_chat.py            # Interfaz de chat
├── 🧠 MEDEX_ULTIMATE_RAG.py    # Sistema RAG avanzado
├── 📚 medical_knowledge_base.py # Base de conocimiento médico
├── 🔍 medical_rag_system.py    # Sistema de recuperación RAG
├── 💊 pharmaceutical_database.py # Base de datos farmacéutica
├── 🛠️ core/                    # Módulos centrales
│   ├── ai_engine.py           # Motor de IA
│   ├── pure_kimi_medex.py     # Cliente Kimi
│   └── real_kimi_client.py    # Cliente API real
├── 📖 docs/                   # Documentación y ejemplos
│   ├── guia_de_usuario.md     # Guía completa en español
│   ├── user_guide.md          # Guía completa en inglés
│   └── consulta_*.md          # Ejemplos de consultas
└── 🗄️ rag_cache/              # Cache del sistema RAG
```

## 📖 Documentación

### Documentación Principal

- **[Guía de Usuario](docs/guia_de_usuario.md)** - Documentación completa en español
- **[User Guide](docs/user_guide.md)** - Complete documentation in English
- **[Consultas de Ejemplo](docs/)** - Ejemplos reales de consultas médicas

### Especificaciones Técnicas

| Componente        | Tecnología            | Propósito                                   |
| ----------------- | --------------------- | ------------------------------------------- |
| **Motor IA**      | Kimi K2-0711-Preview  | Procesamiento de lenguaje natural médico    |
| **Sistema RAG**   | Sentence-Transformers | Búsqueda semántica en conocimiento médico   |
| **Base de Datos** | SQLite/Pickle         | Almacenamiento de conocimiento estructurado |
| **API Client**    | OpenAI-Compatible     | Comunicación con Kimi AI                    |
| **Vectorización** | All-MiniLM-L6-v2      | Embeddings semánticos                       |

## ⚠️ Advertencias Médicas Importantes

### 🚨 **DISCLAIMER MÉDICO OBLIGATORIO**

**MedeX es una herramienta de apoyo educativo e informativo. NO sustituye:**

- Consulta médica profesional
- Diagnóstico médico especializado
- Tratamiento médico prescrito
- Decisiones clínicas profesionales

**En emergencias médicas reales:**

- Contacte servicios de emergencia inmediatamente
- Acuda al centro médico más cercano
- No dependa únicamente de información de IA

### 🏥 **Uso Profesional**

Para profesionales de la salud:

- Use como herramienta de apoyo únicamente
- Siempre aplique juicio clínico profesional
- Verifique información con fuentes primarias
- Considere contexto específico del paciente

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork del repositorio
2. Crear branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Áreas de Contribución

- 🧠 Mejoras en detección de usuarios
- 📚 Expansión de base de conocimiento médico
- 🔍 Optimización del sistema RAG
- 🌐 Integración de nuevas fuentes médicas
- 📱 Desarrollo de interfaces de usuario
- 🧪 Testing y validación médica

## 🛣️ Roadmap de Desarrollo

### 📅 **Próximas Versiones**

#### **v26.x - Análisis Multimodal** (Q1 2026)

- 🖼️ **Análisis de Imágenes Médicas**: Radiografías, tomografías, resonancias
- 📊 **Interpretación de Gráficos**: ECG, EEG, espirometrías
- 🧬 **Análisis de Laboratorio**: Interpretación automatizada de resultados
- 🌐 **Interfaz Web**: Dashboard médico profesional

#### **v27.x - Especialización Avanzada** (Q2-Q3 2026)

- 🏥 **Módulos Especializados**: Cardiología, Neurología, Oncología
- 📚 **Dataset Médico Propietario**: Conocimiento médico latinoamericano
- 🤖 **Agentes Médicos**: Especialistas virtuales por área
- 🔗 **Integración FHIR**: Compatibilidad con sistemas hospitalarios

#### **v28.x+ - IA Médica Completa** (2027+)

- 🧠 **Razonamiento Clínico Avanzado**: Diagnóstico diferencial mejorado
- 📱 **Aplicación Móvil**: MedeX para dispositivos móviles
- 🌍 **Soporte Multiidioma**: Expansión internacional
- ⚡ **Procesamiento en Tiempo Real**: Análisis instantáneo

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📬 Contacto

- **Proyecto**: MedeX Medical AI System
- **Versión**: v25.83 Production
- **Soporte**: Crear issue en GitHub
- **Documentación**: [docs/](docs/)

---

⚠️ **Recuerda**: MedeX es una herramienta de apoyo médico. Siempre consulta con profesionales de la salud para decisiones médicas importantes.

🤖 **Desarrollado con IA responsable para el futuro de la medicina digital**
