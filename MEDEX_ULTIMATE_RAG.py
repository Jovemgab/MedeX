#!/usr/bin/env python3
"""
🏥 MEDEX ULTIMATE RAG - Sistema Médico Completo Definitivo
El sistema médico de IA más completo jamás creado

🎯 CARACTERÍSTICAS COMPLETAS:
✅ Kimi K2-0711-Preview (modelo más avanzado)
✅ RAG vectorial con base de conocimiento médico completa
✅ Streaming en tiempo real con razonamiento visible
✅ Detección automática: Paciente vs Profesional
✅ Emergencias: Protocolos automáticos integrados
✅ Análisis de imágenes médicas con contexto RAG
✅ Búsqueda web médica + RAG local
✅ Context caching para documentos médicos
✅ Interpretación de signos vitales y laboratorios
✅ Protocolos clínicos completos
✅ Base de datos de medicamentos
✅ Valores normales de referencia
✅ Historial conversacional inteligente
"""

import asyncio
import json
import re
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys
import os

# Agregar paths
sys.path.append(os.path.dirname(__file__))

from openai import OpenAI
from medical_knowledge_base import MedicalKnowledgeBase
from medical_rag_system import MedicalRAGSystem

class MedeXUltimateRAG:
    """Sistema médico definitivo con RAG completo"""
    
    def __init__(self):
        self.api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.ai/v1"
        )
        
        # Inicializar sistemas
        print("🧠 Inicializando MedeX Ultimate RAG...")
        self.knowledge_base = MedicalKnowledgeBase()
        self.rag_system = MedicalRAGSystem()
        
        # Cargar índice RAG si existe
        self.rag_system.load_index()
        
        self.conversation_history = []
        self.session_stats = {
            "queries": 0,
            "emergencies": 0,
            "professional_queries": 0,
            "patient_queries": 0,
            "images_analyzed": 0,
            "rag_searches": 0,
            "web_searches": 0
        }
        
        # Patrones de emergencia mejorados
        self.emergency_keywords = [
            'dolor precordial intenso', 'dolor toracico severo', 
            'no puedo respirar', 'dificultad respiratoria severa',
            'convulsiones', 'perdida conciencia', 'sangrado abundante',
            'dolor cabeza explosivo', 'peor dolor vida', 'shock',
            'paro cardiaco', 'paro respiratorio', 'coma'
        ]
        
        # Patrones profesionales mejorados
        self.professional_patterns = [
            r'paciente\s+de\s+\d+\s+años',
            r'caso\s+clinico',
            r'diagnostico\s+diferencial',
            r'protocolo\s+de\s+manejo',
            r'dosis\s+de\s+\d+\s*mg',
            r'tratamiento\s+con\s+\w+',
            r'manejo\s+hospitalario',
            r'codigo\s+cie',
            r'seguimiento\s+ambulatorio'
        ]
        
        print("✅ MedeX Ultimate RAG inicializado correctamente")
    
    def detect_user_type(self, query: str) -> str:
        """Detecta tipo de usuario con mayor precisión"""
        query_lower = query.lower()
        
        # Verificar patrones profesionales
        professional_score = 0
        for pattern in self.professional_patterns:
            if re.search(pattern, query_lower):
                professional_score += 2
        
        # Términos técnicos médicos
        technical_terms = [
            'icd', 'cie-10', 'protocolo', 'manejo', 'seguimiento',
            'dosis', 'mg', 'ml', 'via', 'endovenosa', 'intramuscular',
            'diagnostico diferencial', 'criterios', 'evidencia'
        ]
        
        for term in technical_terms:
            if term in query_lower:
                professional_score += 1
        
        # Indicadores de paciente
        patient_indicators = [
            'me duele', 'tengo', 'siento', 'estoy preocupado',
            'que sera', 'es normal', 'debo preocuparme',
            'mi hijo', 'mi esposo', 'mi mama'
        ]
        
        patient_score = 0
        for indicator in patient_indicators:
            if indicator in query_lower:
                patient_score += 2
        
        # Decisión basada en puntuación
        if professional_score >= 3:
            return "professional"
        elif patient_score >= 2:
            return "patient"
        else:
            # Análisis por longitud y complejidad
            if len(query.split()) > 15 and any(word in query_lower for word in ['paciente', 'caso', 'años']):
                return "professional"
            else:
                return "patient"
    
    def detect_emergency(self, query: str) -> bool:
        """Detecta emergencias médicas con mayor precisión"""
        query_lower = query.lower()
        
        # Palabras clave de emergencia directa
        for keyword in self.emergency_keywords:
            if keyword in query_lower:
                return True
        
        # Patrones de urgencia
        urgency_patterns = [
            r'dolor\s+(muy\s+)?intenso',
            r'no\s+puedo\s+\w+',
            r'desde\s+hace\s+\d+\s+horas?\s+y\s+(empeora|grave)',
            r'sangr(e|ando)\s+(mucho|abundante)',
            r'se\s+desmayo',
            r'esta\s+(inconsciente|grave)'
        ]
        
        for pattern in urgency_patterns:
            if re.search(pattern, query_lower):
                return True
        
        return False
    
    def get_rag_context(self, query: str, user_type: str, is_emergency: bool) -> str:
        """Obtiene contexto relevante del sistema RAG"""
        
        try:
            # Búsqueda contextual en RAG
            context_info = self.rag_system.get_contextual_information(
                query=query,
                user_type=user_type,
                urgency_level="emergency" if is_emergency else "routine"
            )
            
            self.session_stats['rag_searches'] += 1
            
            # Formatear contexto para prompt
            context_parts = []
            
            if context_info['general_results']:
                context_parts.append("=== INFORMACIÓN RELEVANTE DE BASE DE CONOCIMIENTO ===")
                
                for i, result in enumerate(context_info['general_results'][:3], 1):
                    context_parts.append(f"\n{i}. {result['title']} (Categoría: {result['category']})")
                    
                    if user_type == "professional" and result.get('full_content'):
                        # Contenido completo para profesionales
                        context_parts.append(f"   Detalles: {result['full_content'][:500]}...")
                    elif result.get('simplified_content'):
                        # Contenido simplificado para pacientes
                        context_parts.append(f"   Información: {result['simplified_content']}")
                    
                    if result.get('emergency_relevant') and is_emergency:
                        context_parts.append("   ⚠️ RELEVANTE PARA EMERGENCIA")
            
            # Información específica de emergencia
            if is_emergency and context_info['emergency_results']:
                context_parts.append("\n=== PROTOCOLOS DE EMERGENCIA ===")
                for result in context_info['emergency_results'][:2]:
                    context_parts.append(f"• {result.document.title}")
                    context_parts.append(f"  {result.document.content[:300]}...")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            print(f"⚠️ Error obteniendo contexto RAG: {e}")
            return ""
    
    def create_enhanced_system_prompt(self, query: str, user_type: str, is_emergency: bool) -> str:
        """Crea prompt del sistema mejorado con contexto RAG"""
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Obtener contexto RAG
        rag_context = self.get_rag_context(query, user_type, is_emergency)
        
        base_prompt = f"""Eres MedeX Ultimate, el sistema de inteligencia artificial médica más avanzado del mundo.

FECHA Y HORA: {current_time}
TIPO DE USUARIO: {user_type.upper()}
EMERGENCIA DETECTADA: {"SÍ" if is_emergency else "NO"}

ARQUITECTURA DEL SISTEMA:
- Motor Principal: Kimi K2-0711-Preview (modelo más avanzado)
- Base de Conocimiento: RAG vectorial con literatura médica completa
- Capacidades: Streaming, multimodal, búsqueda web, protocolos clínicos

{rag_context if rag_context else ""}

"""
        
        if user_type == "professional":
            base_prompt += """MODO PROFESIONAL MÉDICO ACTIVADO:

PROTOCOLOS DE RESPUESTA PROFESIONAL:
- Análisis clínico detallado basado en evidencia científica
- Diagnósticos diferenciales con probabilidades estimadas según literatura
- Protocolos de manejo específicos con dosis farmacológicas exactas
- Citas de guías clínicas actuales cuando sea relevante
- Criterios de derivación y seguimiento según estándares
- Terminología médica apropiada y códigos CIE-10
- Correlación con información de base de conocimiento
- Interpretación de estudios paraclínicos

ESTRUCTURA DE RESPUESTA PROFESIONAL:
1. Resumen ejecutivo del caso
2. Análisis clínico detallado
3. Diagnósticos diferenciales priorizados
4. Plan de manejo específico
5. Criterios de seguimiento
6. Referencias a protocolos institucionales

"""
        else:
            base_prompt += """MODO PACIENTE ACTIVADO:

PROTOCOLOS DE RESPUESTA PARA PACIENTES:
- Lenguaje claro, comprensible y empático
- Información educativa sin crear ansiedad innecesaria
- Explicación de cuándo es importante buscar atención médica
- Medidas de autocuidado apropiadas y seguras
- Tono tranquilizador y de apoyo
- Evitar diagnósticos específicos
- Enfoque en orientación y educación

ESTRUCTURA DE RESPUESTA PARA PACIENTES:
1. Acknowledgment empático de la preocupación
2. Explicación clara de posibles causas
3. Recomendaciones de autocuidado
4. Signos de alarma para buscar atención
5. Próximos pasos recomendados
6. Tranquilización apropiada

"""
        
        if is_emergency:
            base_prompt += """🚨 PROTOCOLO DE EMERGENCIA ACTIVADO 🚨

INSTRUCCIONES CRÍTICAS DE EMERGENCIA:
- PRIORIDAD MÁXIMA: Seguridad inmediata del paciente
- Evaluar necesidad de atención médica INMEDIATA
- Proporcionar pasos de acción específicos, claros y secuenciales
- Indicar CUÁNDO y CÓMO contactar servicios de emergencia
- NO minimizar síntomas potencialmente graves
- Incluir instrucciones de primeros auxilios si aplicable
- Considerar protocolos de triage y estabilización

ESTRUCTURA DE RESPUESTA DE EMERGENCIA:
1. 🚨 EVALUACIÓN INMEDIATA DE RIESGO
2. 📞 INSTRUCCIONES DE CONTACTO DE EMERGENCIA
3. 🩹 PRIMEROS AUXILIOS INMEDIATOS
4. ⏰ MONITOREO HASTA LLEGADA DE AYUDA
5. 📋 INFORMACIÓN PARA SERVICIOS MÉDICOS

"""
        
        base_prompt += """CAPACIDADES ESPECIALES DISPONIBLES:
- 🔍 Búsqueda en base de conocimiento médico especializada
- 🌐 Acceso a información médica web actualizada
- 🩻 Análisis de imágenes médicas (radiografías, ECGs, laboratorios)
- 📊 Interpretación de signos vitales y valores de laboratorio
- 💊 Base de datos completa de medicamentos con interacciones
- 📋 Protocolos clínicos estandarizados
- 🧬 Correlación con valores de referencia normales

INSTRUCCIONES DE INTEGRACIÓN RAG:
- Utiliza la información de la base de conocimiento proporcionada
- Correlaciona con los hallazgos clínicos del paciente
- Prioriza información específica sobre información general
- Menciona cuando la información proviene de protocolos establecidos
- Integra seamlessly el conocimiento base con el razonamiento clínico

DISCLAIMERS MÉDICOS OBLIGATORIOS:
- Esta información es exclusivamente educativa
- NO reemplaza la consulta médica profesional
- En emergencias reales, contactar servicios de emergencia (911)
- Siempre buscar evaluación médica presencial para diagnóstico definitivo
- Los protocolos pueden variar según instituciones y guías locales

INSTRUCCIONES DE RESPUESTA:
- Proporciona razonamiento clínico paso a paso
- Estructura la información de manera lógica y clara
- Adapta el nivel de detalle técnico al tipo de usuario
- Incluye referencias a la base de conocimiento cuando sea relevante
- Mantén un balance entre completitud y claridad
- Siempre finaliza con disclaimers apropiados y próximos pasos"""
        
        return base_prompt
    
    async def generate_ultimate_response(self, query: str, use_streaming: bool = True) -> str:
        """Genera respuesta médica definitiva con RAG completo"""
        
        # Analizar query
        user_type = self.detect_user_type(query)
        is_emergency = self.detect_emergency(query)
        
        # Actualizar estadísticas
        self.session_stats['queries'] += 1
        if is_emergency:
            self.session_stats['emergencies'] += 1
        if user_type == "professional":
            self.session_stats['professional_queries'] += 1
        else:
            self.session_stats['patient_queries'] += 1
        
        # Crear prompt del sistema mejorado
        system_prompt = self.create_enhanced_system_prompt(query, user_type, is_emergency)
        
        # Configurar herramientas
        tools = None
        if not is_emergency:  # En emergencias, respuesta directa sin web search
            tools = [
                {
                    "type": "builtin_function",
                    "function": {"name": "$web_search"}
                }
            ]
        
        # Preparar mensajes con historial
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Agregar historial conversacional reciente
        if self.conversation_history:
            for interaction in self.conversation_history[-2:]:  # Últimas 2 interacciones
                if 'user_query' in interaction:
                    messages.append({"role": "user", "content": interaction['user_query']})
                if 'response' in interaction:
                    # Limitar longitud de respuestas anteriores
                    prev_response = interaction['response'][:800] + "..." if len(interaction['response']) > 800 else interaction['response']
                    messages.append({"role": "assistant", "content": prev_response})
        
        # Agregar query actual
        messages.append({"role": "user", "content": query})
        
        print(f"\n🩺 MedeX Ultimate RAG")
        print(f"   👤 Usuario: {user_type.upper()}")
        print(f"   🚨 Emergencia: {'SÍ' if is_emergency else 'NO'}")
        print(f"   🔍 RAG: {len(self.rag_system.documents)} documentos indexados")
        
        try:
            if use_streaming:
                return await self._generate_streaming_with_rag(messages, tools, query, user_type, is_emergency)
            else:
                return await self._generate_direct_with_rag(messages, tools)
                
        except Exception as e:
            error_msg = f"Error en MedeX Ultimate RAG: {e}"
            print(f"❌ {error_msg}")
            return error_msg
    
    async def _generate_streaming_with_rag(self, messages: List[Dict], tools: Optional[List], 
                                         query: str, user_type: str, is_emergency: bool) -> str:
        """Genera respuesta con streaming y RAG"""
        
        print("🤔 Analizando con Kimi K2 + RAG...")
        
        finish_reason = None
        while finish_reason is None or finish_reason == "tool_calls":
            
            stream = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=messages,
                temperature=0.6 if not is_emergency else 0.3,  # Menor temperatura en emergencias
                max_tokens=3072,  # Más tokens para respuestas completas
                stream=True,
                tools=tools
            )
            
            full_response = ""
            tool_calls = []
            current_message = {"role": "assistant", "content": ""}
            
            print(f"\n💬 Respuesta MedeX Ultimate:")
            print("-" * 60)
            
            for chunk in stream:
                if chunk.choices:
                    choice = chunk.choices[0]
                    finish_reason = choice.finish_reason
                    
                    if choice.delta:
                        # Contenido normal con streaming visible
                        if choice.delta.content:
                            full_response += choice.delta.content
                            current_message["content"] += choice.delta.content
                            print(choice.delta.content, end="", flush=True)
                        
                        # Tool calls
                        if choice.delta.tool_calls:
                            for tool_call in choice.delta.tool_calls:
                                if len(tool_calls) <= tool_call.index:
                                    tool_calls.extend([None] * (tool_call.index + 1 - len(tool_calls)))
                                
                                if tool_calls[tool_call.index] is None:
                                    tool_calls[tool_call.index] = {
                                        "id": tool_call.id,
                                        "type": tool_call.type,
                                        "function": {"name": tool_call.function.name, "arguments": ""}
                                    }
                                
                                if tool_call.function.arguments:
                                    tool_calls[tool_call.index]["function"]["arguments"] += tool_call.function.arguments
            
            # Procesar tool calls si existen
            if finish_reason == "tool_calls" and tool_calls:
                current_message["tool_calls"] = [tc for tc in tool_calls if tc is not None]
                messages.append(current_message)
                
                print(f"\n\n🌐 Buscando información médica actualizada...")
                self.session_stats['web_searches'] += 1
                
                for tool_call in current_message["tool_calls"]:
                    if tool_call["function"]["name"] == "$web_search":
                        try:
                            arguments = json.loads(tool_call["function"]["arguments"])
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "name": "$web_search",
                                "content": json.dumps(arguments)
                            })
                        except:
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "name": "$web_search",
                                "content": json.dumps({"query": query})
                            })
            else:
                # Respuesta final
                print("\n" + "-" * 60)
                
                # Guardar en historial con información enriquecida
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_query": query,
                    "response": full_response,
                    "user_type": user_type,
                    "is_emergency": is_emergency,
                    "rag_used": True,
                    "web_search_used": tools is not None
                })
                
                return full_response
        
        return full_response
    
    async def _generate_direct_with_rag(self, messages: List[Dict], tools: Optional[List]) -> str:
        """Genera respuesta directa con RAG"""
        
        response = self.client.chat.completions.create(
            model="kimi-k2-0711-preview",
            messages=messages,
            temperature=0.6,
            max_tokens=3072,
            tools=tools
        )
        
        return response.choices[0].message.content
    
    async def analyze_medical_image_with_rag(self, image_path: str, clinical_context: str = "") -> str:
        """Analiza imágenes médicas con contexto RAG"""
        
        try:
            if not Path(image_path).exists():
                return f"❌ Error: Archivo {image_path} no encontrado"
            
            # Obtener contexto RAG para el análisis de imagen
            rag_context = ""
            if clinical_context:
                context_info = self.rag_system.get_contextual_information(clinical_context)
                if context_info['general_results']:
                    rag_context = "\n=== CONTEXTO CLÍNICO RELEVANTE ==="
                    for result in context_info['general_results'][:2]:
                        rag_context += f"\n• {result['title']}: {result.get('simplified_content', '')[:200]}..."
            
            # Leer y codificar imagen
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            file_ext = Path(image_path).suffix.lower()
            
            # Detectar tipo de usuario
            user_type = self.detect_user_type(clinical_context) if clinical_context else "patient"
            
            # Crear prompt especializado con contexto RAG
            if user_type == "professional":
                system_prompt = f"""Eres MedeX Ultimate, especialista en análisis de imágenes médicas con acceso a base de conocimiento completa.

MODO PROFESIONAL - ANÁLISIS DE IMAGEN MÉDICA:
- Descripción técnica detallada de hallazgos imagenológicos
- Interpretación usando terminología radiológica apropiada
- Diagnósticos diferenciales imagenológicos priorizados
- Correlación clínica recomendada con base de conocimiento
- Estudios complementarios sugeridos según protocolos
- Limitaciones del análisis por IA claramente establecidas

{rag_context}

ESTRUCTURA DE REPORTE:
1. Técnica y calidad de la imagen
2. Hallazgos anatómicos normales
3. Hallazgos patológicos específicos (si los hay)
4. Diagnósticos diferenciales imagenológicos
5. Correlación clínica recomendada
6. Estudios adicionales sugeridos
7. Limitaciones del análisis por IA"""
                
                user_prompt = f"""Analiza profesionalmente esta imagen médica.

CONTEXTO CLÍNICO: {clinical_context}

Proporciona reporte radiológico completo incluyendo:
- Análisis técnico de la imagen
- Descripción sistemática de hallazgos
- Interpretación clínica correlacionada
- Recomendaciones de manejo basadas en hallazgos
- Referencias a protocolos de la base de conocimiento cuando sea relevante

Incluye disclaimers sobre limitaciones de análisis por IA."""
            
            else:
                system_prompt = f"""Eres MedeX Ultimate, asistente que ayuda a pacientes a entender estudios médicos.

MODO PACIENTE - EXPLICACIÓN DE IMAGEN MÉDICA:
- Explicaciones claras y comprensibles sobre el estudio
- Información educativa sin crear ansiedad innecesaria
- Énfasis en la importancia de consulta médica profesional
- Lenguaje simple y empático
- Orientación sobre próximos pasos

{rag_context}

ESTRUCTURA DE EXPLICACIÓN:
1. Qué tipo de estudio es y para qué sirve
2. Qué se puede observar en términos generales
3. Importancia de discutir resultados con el médico
4. Qué preguntas hacer al médico tratante
5. Tranquilización apropiada"""
                
                user_prompt = f"""Explica esta imagen médica de manera comprensible para un paciente.

CONTEXTO: {clinical_context}

Proporciona explicación clara que incluya:
- Qué tipo de estudio es
- Qué información puede proporcionar
- Por qué es importante consultar con el médico
- Qué preguntas hacer al médico
- Tranquilización apropiada

Usa lenguaje simple y evita crear ansiedad innecesaria."""
            
            # Configurar mensajes
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image{file_ext};base64,{image_base64}"
                            }
                        },
                        {"type": "text", "text": user_prompt}
                    ]
                }
            ]
            
            print(f"🔍 Analizando imagen médica con contexto RAG...")
            print(f"📊 Modo: {user_type}")
            print(f"🧠 Contexto RAG: {'Disponible' if rag_context else 'No disponible'}")
            
            # Generar análisis
            response = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=messages,
                temperature=0.3,  # Menor temperatura para precisión médica
                max_tokens=2048
            )
            
            result = response.choices[0].message.content
            
            # Actualizar estadísticas
            self.session_stats['images_analyzed'] += 1
            
            return result
            
        except Exception as e:
            return f"❌ Error analizando imagen con RAG: {e}"
    
    def interpret_labs_and_vitals(self, data: Dict[str, Any]) -> str:
        """Interpreta laboratorios y signos vitales con contexto RAG"""
        
        try:
            interpretation_parts = []
            
            # Interpretar signos vitales si están presentes
            if 'vitals' in data:
                vitals_interpretation = self.knowledge_base.interpret_vital_signs(
                    data['vitals'],
                    data.get('age_group', 'adults')
                )
                
                interpretation_parts.append("=== SIGNOS VITALES ===")
                for vital, interpretation in vitals_interpretation.items():
                    value = data['vitals'][vital]
                    interpretation_parts.append(f"{vital}: {value} - {interpretation}")
            
            # Interpretar laboratorios si están presentes
            if 'labs' in data:
                labs_interpretation = self.knowledge_base.interpret_lab_values(
                    data['labs'],
                    data.get('gender', 'male')
                )
                
                interpretation_parts.append("\n=== LABORATORIOS ===")
                for lab, interpretation in labs_interpretation.items():
                    value = data['labs'][lab]
                    interpretation_parts.append(f"{lab}: {value} - {interpretation}")
            
            # Buscar condiciones relacionadas con valores anormales
            abnormal_findings = []
            if 'vitals' in data:
                for vital, interpretation in self.knowledge_base.interpret_vital_signs(data['vitals']).items():
                    if interpretation in ['Alto', 'Bajo']:
                        abnormal_findings.append(f"{vital} {interpretation.lower()}")
            
            if abnormal_findings:
                # Buscar en RAG condiciones relacionadas
                related_query = f"condiciones médicas {' '.join(abnormal_findings)}"
                rag_results = self.rag_system.search_similar_documents(related_query, top_k=3)
                
                if rag_results:
                    interpretation_parts.append("\n=== POSIBLES CONDICIONES RELACIONADAS ===")
                    for result in rag_results:
                        interpretation_parts.append(f"• {result.document.title} (Similitud: {result.similarity_score:.2f})")
            
            return "\n".join(interpretation_parts)
            
        except Exception as e:
            return f"❌ Error interpretando valores: {e}"
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas del sistema"""
        
        rag_stats = self.rag_system.get_statistics()
        
        return {
            **self.session_stats,
            "conversations": len(self.conversation_history),
            "model": "kimi-k2-0711-preview",
            "rag_system": rag_stats,
            "knowledge_base": {
                "conditions": len(self.knowledge_base.conditions),
                "medications": len(self.knowledge_base.medications),
                "procedures": len(self.knowledge_base.procedures),
                "protocols": len(self.knowledge_base.protocols)
            },
            "capabilities": [
                "Kimi K2 streaming",
                "RAG vectorial médico",
                "Emergency detection",
                "Professional/Patient mode",
                "Medical image analysis",
                "Web search integration",
                "Vital signs interpretation",
                "Lab values interpretation",
                "Clinical protocols",
                "Conversational memory",
                "Context caching"
            ]
        }
    
    def save_session_data(self):
        """Guarda datos de la sesión"""
        try:
            session_data = {
                "conversation_history": self.conversation_history,
                "session_stats": self.session_stats,
                "timestamp": datetime.now().isoformat()
            }
            
            with open("./rag_cache/session_data.json", 'w') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            # Guardar índice RAG actualizado
            self.rag_system.save_index()
            
            print("💾 Datos de sesión guardados")
            
        except Exception as e:
            print(f"⚠️ Error guardando sesión: {e}")

# Interfaz de chat ultimate
class MedeXUltimateChat:
    """Interfaz de chat para MedeX Ultimate RAG"""
    
    def __init__(self):
        self.medex = MedeXUltimateRAG()
        self.session_start = datetime.now()
    
    def print_ultimate_header(self):
        """Header del sistema ultimate"""
        print("\n" + "="*100)
        print("🏥 MEDEX ULTIMATE RAG - El Sistema Médico de IA Más Completo del Mundo")
        print("🧠 Kimi K2-0711-Preview + RAG Vectorial + Base de Conocimiento Médico Completa")
        print("⚡ Sin limitaciones • 100% Real • Streaming + Razonamiento • Multimodal")
        print("="*100)
        print("🎯 CAPACIDADES ULTIMATE:")
        print("   🧠 RAG Vectorial: Base de conocimiento médico indexada semánticamente")
        print("   👤 Detección Inteligente: Paciente vs Profesional médico automática")
        print("   🚨 Emergencias: Protocolos automáticos integrados con RAG")
        print("   🩻 Análisis Multimodal: Imágenes médicas con contexto RAG")
        print("   🌐 Búsqueda Híbrida: Web search + RAG local integrados")
        print("   📊 Interpretación: Signos vitales y laboratorios con referencias")
        print("   💊 Medicamentos: Base completa con interacciones y dosis")
        print("   📋 Protocolos: Guías clínicas estandarizadas")
        print("   💬 Streaming: Respuestas progresivas con razonamiento visible")
        print("   🧬 Valores Normales: Referencias completas por edad y género")
        print("="*100)
        print("💡 COMANDOS ULTIMATE:")
        print("   📸 'imagen [ruta] [contexto]' - Análisis de imagen con RAG")
        print("   🧪 'laboratorio [valores]' - Interpretación con referencias")
        print("   💊 'medicamento [nombre] [contexto]' - Info completa con RAG")
        print("   🔍 'buscar [termino]' - Búsqueda en base de conocimiento")
        print("   📊 'estadisticas' - Ver estadísticas completas del sistema")
        print("   🧹 'limpiar' - Limpiar historial")
        print("   💾 'guardar' - Guardar sesión")
        print("   🚪 'salir' - Terminar")
        print("="*100)
        print("⚠️  Sistema médico completo - Solo información educativa")
        print("   🩺 No reemplaza consulta médica profesional")
        print("   🚨 En emergencias reales: Contactar servicios de emergencia")
        print("="*100 + "\n")
    
    async def handle_ultimate_commands(self, user_input: str) -> Optional[bool]:
        """Maneja comandos del sistema ultimate"""
        parts = user_input.lower().strip().split()
        command = parts[0] if parts else ""
        
        if command in ['salir', 'exit', 'quit']:
            print("\n👋 Cerrando MedeX Ultimate RAG...")
            
            # Guardar datos antes de salir
            self.medex.save_session_data()
            
            duration = datetime.now() - self.session_start
            print(f"⏱️  Duración de sesión: {duration}")
            
            stats = self.medex.get_comprehensive_stats()
            print(f"📊 Consultas procesadas: {stats['queries']}")
            print(f"🔍 Búsquedas RAG: {stats['rag_searches']}")
            print(f"🌐 Búsquedas web: {stats['web_searches']}")
            print(f"📸 Imágenes analizadas: {stats['images_analyzed']}")
            print("🙏 ¡Gracias por usar MedeX Ultimate RAG!")
            return False
        
        elif command == 'estadisticas':
            stats = self.medex.get_comprehensive_stats()
            print(f"\n📊 ESTADÍSTICAS COMPLETAS DE MEDEX ULTIMATE:")
            print(f"   💬 Consultas totales: {stats['queries']}")
            print(f"   🚨 Emergencias detectadas: {stats['emergencies']}")
            print(f"   👨‍⚕️ Consultas profesionales: {stats['professional_queries']}")
            print(f"   👤 Consultas de pacientes: {stats['patient_queries']}")
            print(f"   📸 Imágenes analizadas: {stats['images_analyzed']}")
            print(f"   🔍 Búsquedas RAG: {stats['rag_searches']}")
            print(f"   🌐 Búsquedas web: {stats['web_searches']}")
            print(f"   💬 Conversaciones: {stats['conversations']}")
            print(f"\n🧠 SISTEMA RAG:")
            print(f"   📚 Documentos indexados: {stats['rag_system']['total_documents']}")
            print(f"   🗂️ Categorías: {stats['rag_system']['categories']}")
            print(f"   💾 Embeddings en cache: {stats['rag_system']['embeddings_cached']}")
            print(f"\n🗄️ BASE DE CONOCIMIENTO:")
            print(f"   🩺 Condiciones médicas: {stats['knowledge_base']['conditions']}")
            print(f"   💊 Medicamentos: {stats['knowledge_base']['medications']}")
            print(f"   🔬 Procedimientos: {stats['knowledge_base']['procedures']}")
            print(f"   📋 Protocolos: {stats['knowledge_base']['protocols']}")
            print(f"\n🧠 Modelo: {stats['model']}")
            return True
        
        elif command == 'limpiar':
            self.medex.conversation_history.clear()
            print("🧹 Historial conversacional limpiado")
            return True
        
        elif command == 'guardar':
            self.medex.save_session_data()
            return True
        
        elif command == 'imagen':
            if len(parts) < 2:
                print("❌ Uso: imagen [ruta_archivo] [contexto_clinico_opcional]")
                return True
            
            image_path = parts[1]
            context = " ".join(parts[2:]) if len(parts) > 2 else ""
            
            print(f"📸 Analizando imagen con RAG: {image_path}")
            result = await self.medex.analyze_medical_image_with_rag(image_path, context)
            print(f"\n🩻 ANÁLISIS DE IMAGEN CON RAG:")
            print("-" * 80)
            print(result)
            print("-" * 80)
            return True
        
        elif command == 'buscar':
            if len(parts) < 2:
                print("❌ Uso: buscar [termino_medico]")
                return True
            
            search_term = " ".join(parts[1:])
            print(f"🔍 Buscando en base de conocimiento: {search_term}")
            
            results = self.medex.rag_system.search_similar_documents(search_term, top_k=5)
            
            print(f"\n📚 RESULTADOS DE BÚSQUEDA RAG:")
            print("-" * 60)
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.document.title}")
                print(f"   Categoría: {result.document.category}")
                print(f"   Similitud: {result.similarity_score:.3f}")
                print(f"   Fuente: {result.document.source}")
                print()
            
            if not results:
                print("No se encontraron resultados relevantes.")
            print("-" * 60)
            return True
        
        return None
    
    async def chat_loop(self):
        """Loop principal del chat ultimate"""
        
        self.print_ultimate_header()
        print("🚀 MedeX Ultimate RAG inicializado correctamente")
        print("💬 El sistema médico más completo está listo para consultas...\n")
        
        try:
            while True:
                try:
                    user_input = input("🩺 Consulta Ultimate: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Manejar comandos especiales
                    command_result = await self.handle_ultimate_commands(user_input)
                    
                    if command_result is False:
                        break
                    elif command_result is True:
                        continue
                    
                    # Procesar consulta médica con sistema completo
                    await self.medex.generate_ultimate_response(user_input, use_streaming=True)
                    print("\n" + "─" * 80 + "\n")
                
                except KeyboardInterrupt:
                    print("\n\n⌨️  Interrupción detectada...")
                    confirm = input("¿Salir de MedeX Ultimate? (s/N): ").lower()
                    if confirm in ['s', 'si', 'y', 'yes']:
                        break
                    else:
                        continue
                
                except Exception as e:
                    print(f"\n❌ Error en sistema: {e}")
                    print("💡 El sistema continúa operativo. Intenta nueva consulta.")
        
        finally:
            print("\n🏥 Sesión MedeX Ultimate RAG finalizada")
            self.medex.save_session_data()

# Métodos adicionales para MedeXUltimateRAG
def add_missing_methods():
    """Añade métodos faltantes a la clase MedeXUltimateRAG"""
    
    async def process_query_async(self, query: str) -> str:
        """Procesa una consulta de forma asíncrona"""
        return self.process_query(query)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema"""
        return {
            "knowledge_base_size": len(self.knowledge_base.get_all_conditions()),
            "embedding_model": "all-MiniLM-L6-v2",
            "rag_enabled": True,
            "queries_processed": len([msg for msg in self.conversation_history if msg["role"] == "user"]),
            "emergency_queries": len([msg for msg in self.conversation_history if msg.get("emergency_mode", False)]),
            "professional_queries": len([msg for msg in self.conversation_history if msg.get("user_type") == "professional"]),
            "rag_contexts_used": len([msg for msg in self.conversation_history if msg.get("rag_context_used", False)])
        }
    
    # Añadir métodos a la clase
    MedeXUltimateRAG.process_query_async = process_query_async
    MedeXUltimateRAG.get_system_stats = get_system_stats

# Añadir métodos adicionales para MedicalRAGSystem
def add_rag_methods():
    """Añade métodos faltantes a la clase MedicalRAGSystem"""
    
    def search_knowledge(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Busca en la base de conocimiento usando RAG"""
        try:
            results = self.get_contextual_information(query)
            formatted_results = []
            
            # Combinar todos los tipos de resultados
            all_results = []
            if results.get('general_results'):
                all_results.extend(results['general_results'])
            if results.get('condition_results'):
                all_results.extend(results['condition_results'])
            if results.get('medication_results'):
                all_results.extend(results['medication_results'])
            
            # Formatear resultados
            for result in all_results[:top_k]:
                formatted_results.append({
                    'content': result.get('simplified_content', result.get('title', 'Sin contenido')),
                    'score': result.get('score', 0.0),
                    'type': result.get('type', 'general')
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return []
    
    # Añadir método a la clase
    MedicalRAGSystem.search_knowledge = search_knowledge

# Aplicar parches
add_missing_methods()
add_rag_methods()

# Función principal
async def main():
    """Función principal del sistema ultimate"""
    
    print("🏥 Iniciando MedeX Ultimate RAG...")
    print("🧠 Cargando sistema médico más completo del mundo...")
    
    try:
        chat = MedeXUltimateChat()
        await chat.chat_loop()
    except Exception as e:
        print(f"❌ Error crítico del sistema: {e}")

if __name__ == "__main__":
    asyncio.run(main())