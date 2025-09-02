![MedeX Banner](banner.png)

# 🏥 MedeX - Advanced Medical AI System

> **English Version | [Versión en Español](README.md)**

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

### 🧠 **Intelligent Medical AI**

- **Professional vs Educational Mode**: Automatic adaptation based on query analysis
- **Emergency Protocols**: Instant recognition and appropriate medical emergency guidance
- **Streaming Responses**: Real-time progressive answer generation
- **Medical Terminology Detection**: Advanced NLP for medical context understanding

### 📚 **Comprehensive Medical Knowledge**

- **ICD-10 Coded Conditions**: Complete medical conditions database
- **Pharmaceutical Information**: Drug interactions, dosages, and contraindications
- **Clinical Protocols**: Evidence-based treatment guidelines
- **RAG-Enhanced Search**: Semantic search through medical literature
- **Laboratory Values**: Normal ranges and interpretation guidelines

### 🔬 **Advanced Capabilities**

- **Multi-modal Processing**: Text-based medical consultations with expansion capability
- **Web Search Integration**: Real-time medical information retrieval
- **Structured Responses**: Professional medical documentation format
- **Session Management**: Intelligent conversation history and statistics

### 🛡️ **Medical Safety**

- **Built-in Disclaimers**: Professional medical disclaimers on all responses
- **Emergency Protocols**: Automatic activation for critical conditions
- **Professional Referral**: Appropriate guidance for medical consultation
- **Quality Standards**: Adherence to medical information standards

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

```bash
git clone [repository-url]
cd MedeX
```

2. **Create virtual environment**

```bash
python3 -m venv medex_env
source medex_env/bin/activate  # Linux/Mac
# medex_env\Scripts\activate  # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure your Moonshot API key**

- Open the `api_key.txt` file in the project root
- Paste your API key from [platform.moonshot.ai](https://platform.moonshot.ai/)
- Save the file

5. **Run MedeX**

```bash
python MEDEX_FINAL.py
```

## 📖 Documentation

For detailed usage instructions, examples, and advanced configuration, please refer to our comprehensive **[User Guide](docs/user_guide.md)**.

The user guide covers:

- **System Operation**: Detailed interface explanation
- **Usage Examples**: Professional and educational scenarios
- **Special Commands**: System control and statistics
- **Medical Protocols**: Emergency detection and responses
- **Best Practices**: Optimal usage recommendations

## 💡 Usage Examples

### For Healthcare Professionals

```
🩺 "Paciente masculino 65 años, diabético, dolor precordial 2 horas"

📋 MedeX Response:
🚨 PROTOCOL: ACUTE CORONARY SYNDROME
• 12-lead ECG < 10 minutes
• High-sensitivity troponin I
• Aspirin 300mg PO + Clopidogrel 600mg PO
• Reperfusion < 90 min if STEMI
• GRACE score stratification
```

### For Patients/Students

```
🩺 "¿Qué son los AINEs?"

📋 MedeX Response:
💊 ANTI-INFLAMMATORY DRUGS (NSAIDs)
📚 Non-steroidal anti-inflammatory drugs that work by...
💡 Common examples: Ibuprofen, Naproxen, Aspirin
⚠️ Important considerations: Stomach protection, kidney function...
```

## 🏗️ Project Architecture

```
MedeX/
├── MEDEX_FINAL.py          # 🎯 Main application (v25.83)
├── medex_chat.py           # 💬 Alternative chat interface
├── MEDEX_ULTIMATE_RAG.py   # 🧠 Advanced RAG system
├── medical_knowledge_base.py # 📚 Medical knowledge core
├── medical_rag_system.py   # 🔍 RAG implementation
├── pharmaceutical_database.py # 💊 Drug database
├── core/                   # ⚙️ AI engine modules
├── docs/                   # 📖 Documentation & examples
├── rag_cache/             # 💾 RAG index cache
└── requirements.txt       # 📦 Dependencies
```

## 🛠️ Technical Specifications

- **AI Engine**: Kimi K2-0711-Preview (Advanced Language Model)
- **Architecture**: Modular design with RAG integration
- **Knowledge Base**: Curated medical database with continuous updates
- **Response Modes**: Professional (5120 tokens) / Educational (4096 tokens)
- **Emergency Detection**: Real-time critical condition identification
- **Streaming**: Asynchronous real-time response generation

## 🗺️ Development Roadmap

### 🚀 **Immediate Next Release (v26.x)**

- **Medical Image Analysis**: Advanced radiological image interpretation (RX, CT, MRI, Ultrasound)
- **Web UI Platform**: Comprehensive web-based interface for MedeX v25.83
- **Mobile Compatibility**: Responsive design for healthcare mobility
- **Integration APIs**: RESTful endpoints for healthcare systems

### 🎯 **Future Development**

- **Specialized Medical Dataset**: Custom-trained medical knowledge corpus
- **Multi-language Support**: Spanish, English, Portuguese medical consultation
- **Clinical Decision Support**: Advanced diagnostic assistance algorithms
- **Telemedicine Integration**: Real-time consultation platform

## 📊 Current Status

- ✅ **Core System**: Production ready (v25.83)
- ✅ **Medical Knowledge**: Comprehensive database integrated
- ✅ **Safety Protocols**: Medical disclaimers and emergency detection
- 🚧 **Image Analysis**: In active development
- 🚧 **Web Platform**: Design and development phase
- 📋 **Medical Dataset**: Research and curation phase

## ⚠️ Medical Disclaimer

**IMPORTANT**: MedeX is designed for educational and clinical decision support purposes only. It does not replace professional medical evaluation, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.

### For Emergencies

🚨 **In case of medical emergency**: Call emergency services immediately (911, local emergency number)

### Professional Use

👨‍⚕️ **Healthcare professionals**: Use as supplementary tool only. Validate all information with current clinical guidelines and institutional protocols.

### Educational Use

🎓 **Students and patients**: Information provided is for educational purposes. Always seek professional medical advice for health concerns.

## 🤝 Contributing

We welcome contributions from the medical and AI communities. Please read our contributing guidelines and ensure all medical information follows evidence-based standards.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏥 About

Developed with the mission of advancing medical AI technology while maintaining the highest standards of medical safety and professional ethics. MedeX represents the future of intelligent medical assistance.

---

**MedeX Team** - Advancing Medical AI Technology

- pip package manager

### Installation

1. **Clone and navigate to the project:**

```bash
git clone <repository-url>
cd MedeX
```

2. **Create and activate virtual environment:**

```bash
python3 -m venv medex_venv
source medex_venv/bin/activate  # On Windows: medex_venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Usage

#### **Primary Application (Recommended):**

```bash
python3 MEDEX_FINAL.py
```

#### **Alternative Chat Interface:**

```bash
python3 medex_chat.py
```

#### **Advanced RAG System:**

```bash
python3 MEDEX_ULTIMATE_RAG.py
```

## 💡 Usage Examples

### For Healthcare Professionals

```
🩺 "65-year-old diabetic patient presenting with 2-hour onset chest pain"

📋 MedeX Response:
🚨 ACUTE CORONARY SYNDROME PROTOCOL
• 12-lead ECG < 10 minutes
• High-sensitivity troponin I
• Aspirin 300mg PO + Clopidogrel 600mg PO
• Reperfusion < 90 min if STEMI
• GRACE score stratification
```

### For Patients

```
🩺 "I have chest pain for 2 hours"

📋 MedeX Response:
🚨 MEDICAL EMERGENCY DETECTED
⚠️ IMMEDIATE ACTION REQUIRED:
• Call 911 NOW
• Do not drive - get help
• Take aspirin if available
• Stay calm and rest
```

### Educational Queries

```
🩺 "What is Type 2 diabetes?"

📋 MedeX Response:
📚 TYPE 2 DIABETES MELLITUS
📖 A condition where the body cannot use insulin properly...
💡 Symptoms: excessive thirst, frequent urination, fatigue...
🏥 When to consult: If you experience these symptoms...
```

## 🏗️ Architecture

```
MedeX/
├── MEDEX_FINAL.py                 # 🥇 Primary application
├── medex_chat.py                  # 💬 Alternative chat interface
├── MEDEX_ULTIMATE_RAG.py          # 🧠 Advanced RAG system
├── medical_knowledge_base.py      # 📚 Medical knowledge database
├── medical_rag_system.py          # 🔍 RAG search system
├── pharmaceutical_database.py     # 💊 Drug database
├── core/                          # ⚙️ Core AI engine
│   ├── ai_engine.py              # Main AI engine
│   ├── enhanced_ai_engine.py     # Enhanced capabilities
│   ├── pure_kimi_medex.py        # Kimi integration
│   └── real_kimi_client.py       # Kimi client
├── docs/                          # 📖 Documentation
│   └── user_guide.md             # Complete user guide
├── rag_cache/                     # 💾 RAG system cache
└── requirements.txt               # 📦 Dependencies
```

## 🛠️ Technical Specifications

- **AI Model**: Kimi K2-0711-Preview
- **Backend**: Python 3.8+
- **ML Libraries**: PyTorch, Transformers, Sentence-Transformers
- **Medical Data**: ICD-10, Clinical protocols, Drug databases
- **Response Mode**: Real-time streaming
- **Image Analysis**: OpenCV, Pillow
- **Search**: Semantic similarity with RAG

## 📋 Available Commands

| Command         | Function                       |
| --------------- | ------------------------------ |
| `imagen [path]` | Analyze medical image          |
| `estado`        | View system status             |
| `limpiar`       | Clear conversation history     |
| `demo paciente` | Patient consultation demo      |
| `demo pro`      | Professional consultation demo |
| `salir`         | Exit application               |

## 🔬 Medical Knowledge Base

### Included Medical Conditions

- **Cardiovascular**: Acute coronary syndrome, hypertension, heart failure
- **Endocrine**: Type 2 diabetes, thyroid disorders
- **Respiratory**: Pneumonia, COPD, asthma
- **Emergency**: Stroke, MI, sepsis protocols

### Pharmaceutical Database

- **Essential Medications**: Aspirin, metformin, lisinopril, atorvastatin
- **Drug Interactions**: Comprehensive interaction database
- **Dosage Guidelines**: Age and condition-specific dosing
- **Safety Information**: Contraindications and monitoring requirements

## ⚠️ Medical Disclaimer

**IMPORTANT: MedeX is for educational and informational purposes only.**

- ❌ **NOT a substitute** for professional medical advice, diagnosis, or treatment
- ❌ **NOT for emergency** medical situations - call emergency services
- ❌ **NOT for definitive** medical decision-making
- ✅ **Educational information** based on current medical literature
- ✅ **Safety protocols** to guide appropriate care-seeking
- 🚨 **In emergencies**: Always contact emergency services (911) immediately

## 🤝 Contributing

Contributions are welcome! Please ensure all medical content adheres to evidence-based standards and includes appropriate safety disclaimers.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Acknowledgments

- Medical protocols based on current clinical guidelines
- Powered by Kimi K2-0711-Preview AI model
- Designed with healthcare professional input
- Built with patient safety as the primary concern

---

<div align="center">
  
**🏥 MedeX - Advancing Healthcare Through AI**

_Educational medical AI system designed for healthcare professionals and patients_

[📚 Documentation](docs/user_guide.md) • [🚀 Quick Start](#quick-start) • [💡 Examples](#usage-examples) • [⚠️ Medical Disclaimer](#medical-disclaimer)

</div>
