#!/usr/bin/env python3
"""
MedeX AI Engine - Core Medical Intelligence System
Advanced medical AI with multimodal capabilities
"""

import asyncio
import json
import uuid
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import requests
import base64
import numpy as np
from sentence_transformers import SentenceTransformer

@dataclass
class MedicalQuery:
    """Structured medical query with intelligent context"""
    query_id: str
    original_text: str
    user_type: str  # 'patient' or 'professional'
    query_type: str  # 'consultation', 'emergency', 'education', etc.
    urgency_level: str  # 'routine', 'urgent', 'emergency'
    context: Dict[str, Any]
    confidence: float
    timestamp: datetime

@dataclass
class MedicalResponse:
    """Comprehensive medical response with safety protocols"""
    response_id: str
    query_id: str
    user_type: str
    response_text: str
    confidence: float
    medical_sources: List[Dict[str, Any]]
    recommendations: List[str]
    warnings: List[str]
    follow_up: List[str]
    emergency_level: str
    timestamp: datetime

class MedicalContextAnalyzer:
    """Advanced medical context and user detection"""
    
    def __init__(self):
        # Professional medical language indicators
        self.professional_indicators = [
            "paciente", "dx", "diagnóstico diferencial", "protocolo", "manejo",
            "tratamiento de elección", "indicaciones", "contraindicaciones",
            "dosis", "posología", "seguimiento", "derivación", "interconsulta",
            "historia clínica", "examen físico", "estudios complementarios",
            "pronóstico", "epidemiología", "fisiopatología"
        ]
        
        # Patient/personal language indicators
        self.patient_indicators = [
            "me duele", "tengo", "siento", "mi", "estoy", "me preocupa",
            "qué debo hacer", "es normal", "debo ir al doctor", "es grave",
            "me pasa", "me molesta", "mi familia", "mi hijo", "mi esposa"
        ]
        
        # Emergency keywords with high specificity
        self.emergency_keywords = {
            "critical": [
                "dolor torácico", "dolor precordial", "opresión torácica",
                "dificultad respiratoria", "disnea súbita", "pérdida de conciencia",
                "convulsiones", "sangrado abundante", "trauma craneal",
                "quemaduras extensas", "intoxicación", "alergia severa"
            ],
            "urgent": [
                "fiebre alta", "dolor intenso", "vómitos persistentes",
                "deshidratación", "infección", "lesión", "fractura"
            ]
        }
        
        # Medical specialties and contexts
        self.medical_contexts = {
            "cardiology": ["corazón", "cardíaco", "presión", "hipertensión", "arritmia"],
            "neurology": ["cerebro", "neurológico", "convulsión", "parálisis", "cefalea"],
            "endocrinology": ["diabetes", "tiroides", "hormona", "glucosa", "metabolismo"],
            "respiratory": ["pulmón", "respiratorio", "tos", "asma", "neumonía"],
            "gastroenterology": ["estómago", "digestivo", "náusea", "diarrea", "hígado"]
        }
    
    def analyze_medical_query(self, text: str, has_image: bool = False) -> MedicalQuery:
        """Comprehensive medical query analysis"""
        
        query_id = str(uuid.uuid4())
        text_lower = text.lower()
        
        # Detect user type with confidence scoring
        prof_score = sum(2 if indicator in text_lower else 0 for indicator in self.professional_indicators)
        patient_score = sum(1 if indicator in text_lower else 0 for indicator in self.patient_indicators)
        
        # Determine user type
        if prof_score > patient_score:
            user_type = "professional"
            confidence = min(0.95, 0.6 + (prof_score - patient_score) * 0.1)
        else:
            user_type = "patient"
            confidence = min(0.9, 0.5 + patient_score * 0.1)
        
        # Detect query type
        query_type = self._detect_query_type(text, has_image)
        
        # Detect urgency level
        urgency_level = self._detect_urgency(text)
        
        # Extract comprehensive medical context
        context = self._extract_comprehensive_context(text)
        
        return MedicalQuery(
            query_id=query_id,
            original_text=text,
            user_type=user_type,
            query_type=query_type,
            urgency_level=urgency_level,
            context=context,
            confidence=confidence,
            timestamp=datetime.now()
        )
    
    def _detect_query_type(self, text: str, has_image: bool) -> str:
        """Detect the type of medical query"""
        
        text_lower = text.lower()
        
        if has_image:
            return "image_analysis"
        elif any(word in text_lower for word in ["análisis", "laboratorio", "resultado", "valores"]):
            return "lab_interpretation"
        elif any(word in text_lower for word in ["protocolo", "manejo", "tratamiento"]):
            return "clinical_protocol"
        elif any(word in text_lower for word in ["diagnóstico", "síntomas", "dolor", "molestia"]):
            return "diagnostic_consultation"
        elif any(word in text_lower for word in ["medicamento", "dosis", "efectos"]):
            return "medication_inquiry"
        elif any(word in text_lower for word in ["qué es", "información", "explicar"]):
            return "medical_education"
        else:
            return "general_consultation"
    
    def _detect_urgency(self, text: str) -> str:
        """Detect urgency level with medical precision"""
        
        text_lower = text.lower()
        
        # Check critical emergencies
        for keyword in self.emergency_keywords["critical"]:
            if keyword in text_lower:
                return "emergency"
        
        # Check urgent conditions
        for keyword in self.emergency_keywords["urgent"]:
            if keyword in text_lower:
                return "urgent"
        
        # Check for urgency indicators
        urgency_words = ["urgente", "inmediato", "rápido", "ya", "ahora"]
        if any(word in text_lower for word in urgency_words):
            return "urgent"
        
        return "routine"
    
    def _extract_comprehensive_context(self, text: str) -> Dict[str, Any]:
        """Extract detailed medical context from text"""
        
        context = {
            "demographics": {},
            "symptoms": [],
            "medical_history": [],
            "medications": [],
            "allergies": [],
            "time_course": {},
            "severity": {},
            "specialty_context": []
        }
        
        # Extract demographics
        age_match = re.search(r'(\d+)\s*años?', text, re.IGNORECASE)
        if age_match:
            context["demographics"]["age"] = int(age_match.group(1))
        
        gender_patterns = {
            "masculino": r'\b(masculino|hombre|varón|macho)\b',
            "femenino": r'\b(femenino|mujer|hembra)\b'
        }
        
        for gender, pattern in gender_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                context["demographics"]["gender"] = gender
                break
        
        # Extract symptoms with intensity
        symptom_patterns = [
            r'dolor\s+(?:en\s+)?(?:el\s+|la\s+)?(\w+)',
            r'(\w+)\s+dolor',
            r'molestia\s+(?:en\s+)?(\w+)',
            r'síntomas?\s+de\s+(\w+)',
            r'presenta\s+(\w+)',
            r'(\w+)\s+intenso|fuerte|severo'
        ]
        
        for pattern in symptom_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            context["symptoms"].extend(matches)
        
        # Extract time course
        time_patterns = {
            "duration": r'(?:desde\s+hace|hace|durante)\s+(\d+)\s*(horas?|días?|semanas?|meses?)',
            "onset": r'(súbito|gradual|progresivo|agudo|crónico)',
            "frequency": r'(\d+)\s*veces?\s*(?:por|al)\s*(día|semana|mes)'
        }
        
        for key, pattern in time_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                context["time_course"][key] = match.groups()
        
        # Extract medical history
        history_patterns = [
            r'diabético|diabetes',
            r'hipertenso|hipertensión',
            r'cardíaco|cardiaco|corazón',
            r'asmático|asma',
            r'alérgico|alergia',
            r'cirugía|operado',
            r'cáncer|tumor|oncológico'
        ]
        
        for pattern in history_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                context["medical_history"].append(pattern.split('|')[0])
        
        # Determine specialty context
        for specialty, keywords in self.medical_contexts.items():
            if any(keyword in text.lower() for keyword in keywords):
                context["specialty_context"].append(specialty)
        
        return context

class MedicalKnowledgeEngine:
    """Advanced medical knowledge processing and retrieval"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self._load_medical_knowledge()
    
    def _load_medical_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive medical knowledge base"""
        
        return {
            "conditions": {
                "syndrome_coronario_agudo": {
                    "name": "Síndrome Coronario Agudo",
                    "icd10": "I20-I25",
                    "category": "Cardiovascular",
                    "urgency": "emergency",
                    "description": "Espectro de condiciones causadas por isquemia miocárdica aguda",
                    "symptoms": [
                        "dolor torácico opresivo", "disnea", "náuseas", "diaforesis",
                        "dolor irradiado", "malestar precordial"
                    ],
                    "risk_factors": [
                        "diabetes", "hipertensión", "tabaquismo", "dislipidemia",
                        "edad >45 años (H), >55 años (M)", "antecedentes familiares"
                    ],
                    "professional_management": {
                        "immediate": [
                            "ECG 12 derivaciones <10 minutos",
                            "Troponina I alta sensibilidad",
                            "Aspirina 300mg VO (si no contraindicada)",
                            "Clopidogrel 600mg VO",
                            "Atorvastatina 80mg VO"
                        ],
                        "evaluation": [
                            "Radiografía de tórax",
                            "Gasometría arterial",
                            "Hemograma completo",
                            "Perfil bioquímico"
                        ],
                        "treatment": [
                            "STEMI: Reperfusión <90 min (ICP primaria)",
                            "NSTEMI: Estratificación riesgo (GRACE)",
                            "Anticoagulación según protocolo",
                            "Monitoreo UCI/UCO"
                        ]
                    },
                    "patient_guidance": {
                        "immediate_actions": [
                            "Llamar al 911 inmediatamente",
                            "Tomar aspirina si disponible",
                            "Mantenerse en reposo",
                            "No conducir"
                        ],
                        "warning_signs": [
                            "Dolor que empeora",
                            "Dificultad para respirar",
                            "Sudoración fría",
                            "Náuseas intensas"
                        ]
                    },
                    "sources": ["ESC Guidelines 2020", "AHA/ACC Guidelines 2021"]
                },
                
                "diabetes_tipo_2": {
                    "name": "Diabetes Mellitus Tipo 2",
                    "icd10": "E11",
                    "category": "Endocrinología",
                    "urgency": "routine",
                    "description": "Trastorno metabólico por resistencia insulínica y deficiencia relativa de insulina",
                    "symptoms": [
                        "poliuria", "polidipsia", "polifagia", "pérdida de peso",
                        "fatiga", "visión borrosa", "cicatrización lenta"
                    ],
                    "complications": [
                        "nefropatía diabética", "retinopatía diabética",
                        "neuropatía diabética", "enfermedad cardiovascular"
                    ],
                    "professional_management": {
                        "diagnosis": [
                            "HbA1c ≥6.5%",
                            "Glucosa en ayunas ≥126 mg/dL",
                            "PTOG ≥200 mg/dL a las 2h",
                            "Glucosa random ≥200 mg/dL + síntomas"
                        ],
                        "treatment": [
                            "Metformina 500-2000mg/día (primera línea)",
                            "Objetivos: HbA1c <7%, PA <130/80",
                            "Modificación estilo de vida",
                            "Control lipídico (estatinas)"
                        ],
                        "monitoring": [
                            "HbA1c cada 3-6 meses",
                            "Función renal anual",
                            "Examen oftalmológico anual",
                            "Control podológico"
                        ]
                    },
                    "patient_guidance": {
                        "lifestyle": [
                            "Dieta balanceada baja en carbohidratos refinados",
                            "Ejercicio regular 150 min/semana",
                            "Control de peso",
                            "No fumar"
                        ],
                        "monitoring": [
                            "Automonitoreo glucémico",
                            "Control de pies diario",
                            "Adherencia a medicación",
                            "Consultas regulares"
                        ]
                    },
                    "sources": ["ADA Standards of Care 2023", "EASD/ESC Guidelines 2019"]
                }
            },
            
            "medications": {
                "aspirina": {
                    "name": "Aspirina",
                    "generic": "Ácido acetilsalicílico",
                    "category": "Antiagregante plaquetario",
                    "indications": [
                        "Prevención cardiovascular primaria y secundaria",
                        "Síndrome coronario agudo",
                        "ACV isquémico",
                        "Antiinflamatorio"
                    ],
                    "professional_dosing": {
                        "cardiovascular_prevention": "75-100mg/día",
                        "acute_coronary_syndrome": "300mg dosis carga, luego 75-100mg/día",
                        "stroke_prevention": "75-100mg/día"
                    },
                    "contraindications": [
                        "Alergia al ácido acetilsalicílico",
                        "Úlcera péptica activa",
                        "Hemorragia activa",
                        "Hemofilia",
                        "Asma severa"
                    ],
                    "side_effects": [
                        "Dispepsia", "Úlcera gástrica", "Hemorragia",
                        "Broncoespasmo", "Tinnitus (dosis altas)"
                    ],
                    "patient_guidance": {
                        "instructions": [
                            "Tomar con alimentos para reducir irritación gástrica",
                            "No suspender súbitamente si es para prevención",
                            "Informar si hay sangrado o moretones fáciles"
                        ],
                        "when_to_call_doctor": [
                            "Dolor abdominal severo",
                            "Heces negras o con sangre",
                            "Sangrado que no para",
                            "Dificultad para respirar"
                        ]
                    }
                },
                
                "metformina": {
                    "name": "Metformina",
                    "generic": "Metformina HCl",
                    "category": "Antidiabético oral - Biguanida",
                    "mechanism": "Reduce producción hepática de glucosa, mejora sensibilidad insulínica",
                    "indications": [
                        "Diabetes mellitus tipo 2",
                        "Síndrome metabólico",
                        "Síndrome de ovarios poliquísticos"
                    ],
                    "professional_dosing": {
                        "initial": "500mg 1-2 veces/día con comidas",
                        "maintenance": "500-2000mg/día dividido en 2-3 tomas",
                        "maximum": "2550mg/día"
                    },
                    "contraindications": [
                        "TFG <30 mL/min/1.73m²",
                        "Acidosis metabólica",
                        "Insuficiencia hepática severa",
                        "Insuficiencia cardíaca descompensada"
                    ],
                    "monitoring": [
                        "Función renal cada 6-12 meses",
                        "Vitamina B12 anualmente",
                        "HbA1c cada 3-6 meses"
                    ],
                    "patient_guidance": {
                        "instructions": [
                            "Tomar con alimentos para reducir efectos GI",
                            "Comenzar con dosis baja y aumentar gradualmente",
                            "No suspender sin consultar médico"
                        ],
                        "side_effects_to_report": [
                            "Náuseas o vómitos persistentes",
                            "Dolor abdominal severo",
                            "Dificultad respiratoria",
                            "Fatiga extrema"
                        ]
                    }
                }
            }
        }
    
    def search_medical_knowledge(self, query: str, user_type: str = "patient") -> List[Dict[str, Any]]:
        """Search medical knowledge with user-appropriate filtering"""
        
        results = []
        query_embedding = self.embedding_model.encode(query.lower())
        
        # Search conditions
        for condition_key, condition in self.knowledge_base["conditions"].items():
            # Create searchable text
            searchable_text = f"{condition['name']} {condition['description']} {' '.join(condition['symptoms'])}"
            condition_embedding = self.embedding_model.encode(searchable_text.lower())
            
            # Calculate similarity
            similarity = np.dot(query_embedding, condition_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(condition_embedding)
            )
            
            if similarity > 0.3:
                result = {
                    "type": "condition",
                    "similarity": similarity,
                    "name": condition["name"],
                    "icd10": condition["icd10"],
                    "category": condition["category"],
                    "urgency": condition["urgency"],
                    "description": condition["description"]
                }
                
                # Add user-appropriate information
                if user_type == "professional":
                    result.update({
                        "management": condition.get("professional_management", {}),
                        "sources": condition.get("sources", [])
                    })
                else:
                    result.update({
                        "guidance": condition.get("patient_guidance", {}),
                        "symptoms": condition.get("symptoms", [])
                    })
                
                results.append(result)
        
        # Search medications
        for med_key, medication in self.knowledge_base["medications"].items():
            searchable_text = f"{medication['name']} {medication['generic']} {' '.join(medication['indications'])}"
            med_embedding = self.embedding_model.encode(searchable_text.lower())
            
            similarity = np.dot(query_embedding, med_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(med_embedding)
            )
            
            if similarity > 0.3:
                result = {
                    "type": "medication",
                    "similarity": similarity,
                    "name": medication["name"],
                    "generic": medication["generic"],
                    "category": medication["category"],
                    "indications": medication["indications"]
                }
                
                if user_type == "professional":
                    result.update({
                        "dosing": medication.get("professional_dosing", {}),
                        "contraindications": medication.get("contraindications", []),
                        "monitoring": medication.get("monitoring", [])
                    })
                else:
                    result.update({
                        "guidance": medication.get("patient_guidance", {}),
                        "basic_info": {
                            "what_for": medication["indications"][:2],  # Simplified
                            "category": medication["category"]
                        }
                    })
                
                results.append(result)
        
        # Sort by similarity and return top results
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:5]

class MedeXAIEngine:
    """Main MedeX AI Engine coordinating all medical intelligence components"""
    
    def __init__(self, kimi_api_key: Optional[str] = None):
        self.context_analyzer = MedicalContextAnalyzer()
        self.knowledge_engine = MedicalKnowledgeEngine()
        self.kimi_api_key = kimi_api_key
        self.session_history = []
    
    async def process_medical_query(self, text: str, image_data: Optional[bytes] = None) -> MedicalResponse:
        """Process comprehensive medical query with full AI capabilities"""
        
        # Analyze query context
        query = self.context_analyzer.analyze_medical_query(text, bool(image_data))
        
        # Search relevant medical knowledge
        knowledge_results = self.knowledge_engine.search_medical_knowledge(text, query.user_type)
        
        # Generate intelligent medical response
        response = await self._generate_medical_response(query, knowledge_results, image_data)
        
        # Store in session history
        self.session_history.append((query, response))
        
        return response
    
    async def _generate_medical_response(self, query: MedicalQuery, 
                                        knowledge_results: List[Dict[str, Any]], 
                                        image_data: Optional[bytes] = None) -> MedicalResponse:
        """Generate comprehensive medical response"""
        
        response_parts = []
        warnings = []
        recommendations = []
        follow_up = []
        
        # Emergency protocol activation
        if query.urgency_level == "emergency":
            if query.user_type == "professional":
                response_parts.extend(self._generate_professional_emergency_response(query, knowledge_results))
            else:
                response_parts.extend(self._generate_patient_emergency_response(query))
            
            warnings.append("EMERGENCIA MÉDICA DETECTADA - Acción inmediata requerida")
        
        # Medical knowledge integration
        if knowledge_results:
            response_parts.append(self._format_knowledge_results(knowledge_results, query.user_type))
        
        # Generate recommendations based on user type
        if query.user_type == "professional":
            recommendations.extend(self._generate_professional_recommendations(query, knowledge_results))
            follow_up.extend(self._generate_professional_followup(query))
        else:
            recommendations.extend(self._generate_patient_recommendations(query, knowledge_results))
            follow_up.extend(self._generate_patient_followup(query))
        
        # Add medical safety warnings
        warnings.extend(self._generate_safety_warnings(query))
        
        # Combine response
        full_response = "\n\n".join(response_parts)
        
        return MedicalResponse(
            response_id=str(uuid.uuid4()),
            query_id=query.query_id,
            user_type=query.user_type,
            response_text=full_response,
            confidence=min(0.95, query.confidence + 0.1),
            medical_sources=knowledge_results,
            recommendations=recommendations,
            warnings=warnings,
            follow_up=follow_up,
            emergency_level=query.urgency_level,
            timestamp=datetime.now()
        )
    
    def _generate_professional_emergency_response(self, query: MedicalQuery, 
                                                 knowledge: List[Dict[str, Any]]) -> List[str]:
        """Generate emergency response for medical professionals"""
        
        response = [
            "🚨 PROTOCOLO DE EMERGENCIA ACTIVADO",
            "",
            "📋 EVALUACIÓN INMEDIATA:",
            "• Evaluación primaria ABCDE",
            "• Signos vitales completos",
            "• Acceso venoso y oxigenoterapia",
            "• Monitoreo cardíaco continuo"
        ]
        
        # Add condition-specific protocols
        for item in knowledge:
            if item["type"] == "condition" and item.get("urgency") == "emergency":
                management = item.get("management", {})
                if "immediate" in management:
                    response.append(f"\n🎯 PROTOCOLO ESPECÍFICO - {item['name']}:")
                    for action in management["immediate"]:
                        response.append(f"• {action}")
        
        return ["\n".join(response)]
    
    def _generate_patient_emergency_response(self, query: MedicalQuery) -> List[str]:
        """Generate emergency response for patients"""
        
        return [
            "🚨 EMERGENCIA MÉDICA DETECTADA",
            "",
            "⚠️ ACCIÓN INMEDIATA REQUERIDA:",
            "• Llame al 911 AHORA",
            "• No conduzca - pida ayuda de transporte",
            "• Si tiene aspirina, tome 300mg",
            "• Manténgase calmado y en reposo",
            "• Informe sus síntomas al personal médico",
            "",
            "🏥 El tiempo es crítico en emergencias médicas",
            "👨‍⚕️ Un profesional debe evaluarlo INMEDIATAMENTE"
        ]
    
    def _format_knowledge_results(self, results: List[Dict[str, Any]], user_type: str) -> str:
        """Format medical knowledge results appropriately for user type"""
        
        if not results:
            return ""
        
        formatted = ["📚 INFORMACIÓN MÉDICA RELEVANTE:", ""]
        
        for i, result in enumerate(results[:3], 1):
            formatted.append(f"{i}. **{result['name']}**")
            
            if result["type"] == "condition":
                formatted.append(f"   🏷️ CIE-10: {result['icd10']}")
                formatted.append(f"   📋 Categoría: {result['category']}")
                
                if user_type == "professional":
                    formatted.append(f"   🩺 Descripción: {result['description']}")
                    management = result.get("management", {})
                    if management:
                        formatted.append("   💊 Manejo profesional disponible")
                else:
                    # Simplified for patients
                    formatted.append(f"   📖 Información: {result['description']}")
                    guidance = result.get("guidance", {})
                    if guidance:
                        formatted.append("   💡 Orientación específica disponible")
            
            elif result["type"] == "medication":
                formatted.append(f"   💊 Principio activo: {result['generic']}")
                formatted.append(f"   📋 Tipo: {result['category']}")
                
                if user_type == "professional":
                    dosing = result.get("dosing", {})
                    if dosing:
                        formatted.append("   ⚖️ Información de dosificación disponible")
                else:
                    formatted.append("   ⚠️ Consulte dosificación con su médico")
            
            formatted.append(f"   📊 Relevancia: {result['similarity']:.0%}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def _generate_professional_recommendations(self, query: MedicalQuery, 
                                             knowledge: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations for medical professionals"""
        
        recommendations = [
            "Evaluación clínica integral con examen físico completo",
            "Correlación con antecedentes médicos y medicación actual",
            "Estudios complementarios según indicación clínica"
        ]
        
        if query.urgency_level == "emergency":
            recommendations.extend([
                "Activación de protocolo de emergencia institucional",
                "Interconsulta con especialista según corresponda",
                "Monitoreo continuo hasta estabilización"
            ])
        
        return recommendations
    
    def _generate_patient_recommendations(self, query: MedicalQuery, 
                                        knowledge: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations for patients"""
        
        recommendations = [
            "Consultar con médico de cabecera para evaluación completa",
            "Mantener registro detallado de síntomas y evolución",
            "No automedicarse sin supervisión médica"
        ]
        
        if query.urgency_level in ["urgent", "emergency"]:
            recommendations.insert(0, "Buscar atención médica inmediata")
        
        return recommendations
    
    def _generate_professional_followup(self, query: MedicalQuery) -> List[str]:
        """Generate follow-up actions for professionals"""
        
        return [
            "Documentación completa en historia clínica",
            "Plan de seguimiento protocolizado",
            "Reevaluación según evolución clínica",
            "Consideración de interconsulta si no hay mejoría"
        ]
    
    def _generate_patient_followup(self, query: MedicalQuery) -> List[str]:
        """Generate follow-up actions for patients"""
        
        return [
            "Seguimiento médico según indicaciones",
            "Control de síntomas y respuesta al tratamiento",
            "Consulta de control en fechas programadas",
            "Buscar atención si empeoran los síntomas"
        ]
    
    def _generate_safety_warnings(self, query: MedicalQuery) -> List[str]:
        """Generate appropriate medical safety warnings"""
        
        warnings = [
            "Esta información es educativa y de apoyo únicamente",
            "NO reemplaza la evaluación médica profesional directa",
            "Cada caso requiere evaluación médica individualizada"
        ]
        
        if query.urgency_level == "emergency":
            warnings.insert(0, "EMERGENCIA MÉDICA - Contacte servicios de urgencia inmediatamente")
        
        return warnings
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        
        if not self.session_history:
            return {"message": "No hay consultas en la sesión actual"}
        
        total_queries = len(self.session_history)
        emergency_queries = sum(1 for q, r in self.session_history if q.urgency_level == "emergency")
        professional_queries = sum(1 for q, r in self.session_history if q.user_type == "professional")
        
        avg_confidence = sum(q.confidence for q, r in self.session_history) / total_queries
        
        return {
            "total_consultations": total_queries,
            "emergency_consultations": emergency_queries,
            "professional_consultations": professional_queries,
            "patient_consultations": total_queries - professional_queries,
            "average_confidence": round(avg_confidence * 100, 1),
            "session_duration": str(datetime.now() - self.session_history[0][0].timestamp),
            "last_consultation": self.session_history[-1][1].timestamp.isoformat()
        }

# Export main classes
__all__ = [
    'MedeXAIEngine',
    'MedicalQuery', 
    'MedicalResponse',
    'MedicalContextAnalyzer',
    'MedicalKnowledgeEngine'
]