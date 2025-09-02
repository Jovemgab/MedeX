#!/usr/bin/env python3
"""
Enhanced MedeX AI Engine - Hybrid System
Real medical AI with fallback to advanced local capabilities
"""

import asyncio
import json
import uuid
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

# Import our real Kimi client
from .real_kimi_client import RealKimiClient, KimiRequest

@dataclass
class EnhancedMedicalQuery:
    """Enhanced medical query with full context analysis"""
    query_id: str
    original_text: str
    user_type: str  # 'patient' or 'professional'
    query_type: str  # 'consultation', 'emergency', 'education', etc.
    urgency_level: str  # 'routine', 'urgent', 'emergency'
    context: Dict[str, Any]
    confidence: float
    medical_specialty: Optional[str]
    timestamp: datetime

@dataclass
class EnhancedMedicalResponse:
    """Enhanced medical response with rich metadata"""
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
    ai_source: str  # 'kimi_real', 'local_advanced', 'hybrid'
    processing_time: float
    timestamp: datetime

class AdvancedMedicalReasoningEngine:
    """Advanced medical reasoning with sophisticated logic"""
    
    def __init__(self):
        self.medical_patterns = self._load_medical_patterns()
        self.diagnostic_algorithms = self._load_diagnostic_algorithms()
        self.emergency_protocols = self._load_emergency_protocols()
    
    def _load_medical_patterns(self) -> Dict[str, Any]:
        """Load sophisticated medical pattern recognition"""
        
        return {
            "cardiovascular_patterns": {
                "acute_coronary_syndrome": {
                    "primary_indicators": [
                        "dolor torácico", "dolor precordial", "opresión torácica",
                        "dolor subesternal", "malestar torácico"
                    ],
                    "secondary_indicators": [
                        "disnea", "diaforesis", "náuseas", "dolor irradiado",
                        "brazo izquierdo", "mandíbula", "espalda"
                    ],
                    "risk_factors": [
                        "diabetes", "hipertensión", "tabaquismo", "edad",
                        "antecedentes familiares", "dislipidemia"
                    ],
                    "urgency_weight": 0.95,
                    "confidence_threshold": 0.7
                },
                "hypertensive_emergency": {
                    "primary_indicators": [
                        "presión arterial alta", "hipertensión severa",
                        "cefalea intensa", "visión borrosa"
                    ],
                    "secondary_indicators": [
                        "confusión", "convulsiones", "dolor torácico",
                        "dificultad respiratoria"
                    ],
                    "urgency_weight": 0.85,
                    "confidence_threshold": 0.6
                }
            },
            
            "neurological_patterns": {
                "stroke": {
                    "primary_indicators": [
                        "debilidad súbita", "parálisis", "dificultad hablar",
                        "confusión súbita", "pérdida visión"
                    ],
                    "secondary_indicators": [
                        "cefalea súbita", "mareos", "pérdida equilibrio",
                        "entumecimiento facial"
                    ],
                    "urgency_weight": 0.98,
                    "confidence_threshold": 0.8
                }
            },
            
            "respiratory_patterns": {
                "acute_respiratory_distress": {
                    "primary_indicators": [
                        "dificultad respiratoria", "disnea severa",
                        "falta aire", "respiración laboriosa"
                    ],
                    "secondary_indicators": [
                        "cianosis", "uso músculos accesorios",
                        "taquipnea", "ortopnea"
                    ],
                    "urgency_weight": 0.90,
                    "confidence_threshold": 0.7
                }
            }
        }
    
    def _load_diagnostic_algorithms(self) -> Dict[str, Any]:
        """Load diagnostic reasoning algorithms"""
        
        return {
            "bayesian_inference": {
                "prior_probabilities": {
                    "chest_pain_cardiac": 0.15,  # 15% of chest pain is cardiac
                    "chest_pain_musculoskeletal": 0.35,
                    "chest_pain_gastrointestinal": 0.25,
                    "chest_pain_pulmonary": 0.15,
                    "chest_pain_other": 0.10
                },
                "likelihood_ratios": {
                    "diabetes_present": 2.5,  # Increases cardiac probability
                    "age_over_50": 2.0,
                    "male_gender": 1.5,
                    "smoking": 2.0,
                    "family_history": 1.8
                }
            },
            
            "clinical_decision_rules": {
                "chest_pain_risk_stratification": {
                    "very_high_risk": {
                        "criteria": ["ST_elevation", "hemodynamic_instability", "ongoing_chest_pain"],
                        "action": "immediate_catheterization"
                    },
                    "high_risk": {
                        "criteria": ["troponin_elevation", "ECG_changes", "diabetes_with_symptoms"],
                        "action": "urgent_cardiology_consultation"
                    },
                    "intermediate_risk": {
                        "criteria": ["risk_factors_present", "atypical_symptoms"],
                        "action": "stress_testing_or_imaging"
                    }
                }
            }
        }
    
    def _load_emergency_protocols(self) -> Dict[str, Any]:
        """Load emergency medical protocols"""
        
        return {
            "stemi_protocol": {
                "recognition_criteria": [
                    "ST elevation > 1mm in ≥2 contiguous leads",
                    "new LBBB",
                    "posterior MI equivalent"
                ],
                "time_targets": {
                    "door_to_ECG": "< 10 minutes",
                    "door_to_balloon": "< 90 minutes",
                    "door_to_needle": "< 30 minutes"
                },
                "medications": {
                    "aspirin": "300mg chewed",
                    "clopidogrel": "600mg loading dose",
                    "atorvastatin": "80mg",
                    "metoprolol": "25mg BID if no contraindications"
                }
            },
            
            "stroke_protocol": {
                "recognition_criteria": [
                    "FAST positive",
                    "NIHSS > 0",
                    "symptom onset < 4.5 hours"
                ],
                "time_targets": {
                    "door_to_CT": "< 25 minutes",
                    "door_to_needle": "< 60 minutes"
                },
                "exclusion_criteria": [
                    "hemorrhage on CT",
                    "recent surgery",
                    "anticoagulation"
                ]
            }
        }
    
    def analyze_medical_condition(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced medical condition analysis"""
        
        analysis_results = {
            "conditions_detected": [],
            "urgency_score": 0.0,
            "confidence": 0.0,
            "recommended_actions": [],
            "risk_factors": [],
            "differential_diagnosis": []
        }
        
        text_lower = text.lower()
        
        # Analyze all medical patterns
        for category, patterns in self.medical_patterns.items():
            for condition, pattern_data in patterns.items():
                
                condition_score = 0.0
                indicators_found = []
                
                # Check primary indicators
                primary_matches = sum(1 for indicator in pattern_data["primary_indicators"] 
                                    if indicator in text_lower)
                primary_score = primary_matches / len(pattern_data["primary_indicators"])
                
                # Check secondary indicators
                secondary_matches = sum(1 for indicator in pattern_data["secondary_indicators"] 
                                      if indicator in text_lower)
                secondary_score = secondary_matches / len(pattern_data["secondary_indicators"]) * 0.6
                
                # Check risk factors from context
                risk_factor_score = 0.0
                if "medical_history" in context:
                    risk_matches = sum(1 for rf in pattern_data.get("risk_factors", [])
                                     if any(rf in hist for hist in context["medical_history"]))
                    risk_factor_score = risk_matches / max(1, len(pattern_data.get("risk_factors", []))) * 0.4
                
                # Calculate total condition score
                condition_score = primary_score + secondary_score + risk_factor_score
                
                # If above threshold, add to detected conditions
                if condition_score >= pattern_data["confidence_threshold"]:
                    analysis_results["conditions_detected"].append({
                        "condition": condition,
                        "category": category,
                        "confidence": min(0.95, condition_score),
                        "urgency_weight": pattern_data["urgency_weight"],
                        "indicators_found": indicators_found
                    })
                    
                    # Update overall urgency score
                    weighted_urgency = condition_score * pattern_data["urgency_weight"]
                    analysis_results["urgency_score"] = max(analysis_results["urgency_score"], weighted_urgency)
        
        # Apply Bayesian inference for differential diagnosis
        if analysis_results["conditions_detected"]:
            analysis_results["differential_diagnosis"] = self._generate_differential_diagnosis(
                analysis_results["conditions_detected"], context
            )
        
        # Generate recommendations based on findings
        analysis_results["recommended_actions"] = self._generate_clinical_recommendations(
            analysis_results["conditions_detected"], analysis_results["urgency_score"]
        )
        
        # Calculate overall confidence
        if analysis_results["conditions_detected"]:
            analysis_results["confidence"] = np.mean([
                cond["confidence"] for cond in analysis_results["conditions_detected"]
            ])
        
        return analysis_results
    
    def _generate_differential_diagnosis(self, conditions: List[Dict], context: Dict) -> List[Dict]:
        """Generate differential diagnosis using Bayesian reasoning"""
        
        differential = []
        
        for condition in conditions:
            # Apply Bayesian inference
            prior_prob = 0.1  # Base probability
            likelihood_ratio = 1.0
            
            # Adjust based on risk factors
            if context.get("demographics", {}).get("age", 0) > 50:
                likelihood_ratio *= 1.5
            
            if "diabetes" in context.get("medical_history", []):
                likelihood_ratio *= 2.0
            
            # Calculate posterior probability
            posterior_odds = (prior_prob / (1 - prior_prob)) * likelihood_ratio
            posterior_prob = posterior_odds / (1 + posterior_odds)
            
            differential.append({
                "condition": condition["condition"],
                "probability": min(0.95, posterior_prob * condition["confidence"]),
                "evidence_strength": "strong" if condition["confidence"] > 0.8 else "moderate"
            })
        
        # Sort by probability
        differential.sort(key=lambda x: x["probability"], reverse=True)
        
        return differential[:5]  # Top 5 differential diagnoses
    
    def _generate_clinical_recommendations(self, conditions: List[Dict], urgency_score: float) -> List[str]:
        """Generate evidence-based clinical recommendations"""
        
        recommendations = []
        
        if urgency_score > 0.8:  # High urgency
            recommendations.extend([
                "Evaluación médica inmediata requerida",
                "Considerar activación de protocolo de emergencia",
                "Monitoreo continuo de signos vitales",
                "Acceso venoso y preparación para intervención"
            ])
        elif urgency_score > 0.5:  # Moderate urgency
            recommendations.extend([
                "Evaluación médica urgente dentro de 2-4 horas",
                "Estudios diagnósticos inmediatos",
                "Observación clínica estrecha"
            ])
        else:  # Routine
            recommendations.extend([
                "Evaluación médica programada",
                "Seguimiento clínico apropiado",
                "Educación al paciente sobre signos de alarma"
            ])
        
        # Add condition-specific recommendations
        for condition in conditions:
            if condition["condition"] == "acute_coronary_syndrome":
                recommendations.extend([
                    "ECG de 12 derivaciones inmediato",
                    "Troponinas seriadas",
                    "Aspirina 300mg si no contraindicada",
                    "Evaluación cardiológica urgente"
                ])
            elif condition["condition"] == "stroke":
                recommendations.extend([
                    "TC craneal urgente",
                    "Evaluación neurológica (NIHSS)",
                    "Considerar trombolisis si indicada",
                    "Neuroprotección"
                ])
        
        return list(set(recommendations))  # Remove duplicates

class EnhancedMedeXAIEngine:
    """Enhanced MedeX AI Engine with hybrid capabilities"""
    
    def __init__(self, kimi_api_key: Optional[str] = None):
        self.kimi_client = None
        self.kimi_available = False
        
        # Initialize Kimi if API key provided
        if kimi_api_key:
            self.kimi_client = RealKimiClient(kimi_api_key)
            # Test availability will be done on first use
        
        # Initialize advanced local components
        self.reasoning_engine = AdvancedMedicalReasoningEngine()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load enhanced medical knowledge
        self.medical_knowledge = self._load_enhanced_medical_knowledge()
        
        # Session tracking
        self.session_history = []
        self.performance_metrics = {
            "kimi_requests": 0,
            "local_requests": 0,
            "hybrid_requests": 0,
            "average_confidence": 0.0,
            "average_response_time": 0.0
        }
    
    def _load_enhanced_medical_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive medical knowledge base"""
        
        return {
            "conditions": {
                "acute_coronary_syndrome": {
                    "name": "Síndrome Coronario Agudo",
                    "icd10": "I20-I25",
                    "category": "Cardiovascular",
                    "urgency": "critical",
                    "description": "Espectro de condiciones causadas por isquemia miocárdica aguda, incluyendo angina inestable, NSTEMI y STEMI",
                    "pathophysiology": "Ruptura o erosión de placa aterosclerótica con trombosis coronaria resultante",
                    "clinical_presentation": {
                        "typical": [
                            "Dolor torácico subesternal opresivo",
                            "Duración > 20 minutos",
                            "Irradiación a brazo izquierdo, cuello, mandíbula",
                            "Asociado a diaforesis, náuseas, disnea"
                        ],
                        "atypical": [
                            "Dolor epigástrico",
                            "Disnea aislada",
                            "Síncope",
                            "Presentación silente (especialmente diabéticos)"
                        ]
                    },
                    "risk_factors": {
                        "non_modifiable": ["edad", "género masculino", "antecedentes familiares"],
                        "modifiable": ["diabetes", "hipertensión", "dislipidemia", "tabaquismo", "obesidad"]
                    },
                    "diagnostic_criteria": {
                        "stemi": [
                            "Elevación ST ≥ 1mm en ≥2 derivaciones contiguas",
                            "Nuevo bloqueo rama izquierda",
                            "Ondas Q patológicas de nueva aparición"
                        ],
                        "nstemi": [
                            "Elevación troponinas sin elevación ST",
                            "Depresión ST o inversión T",
                            "Síntomas compatibles"
                        ]
                    },
                    "professional_management": {
                        "immediate_actions": [
                            "Evaluación primaria ABCDE",
                            "ECG < 10 minutos",
                            "Acceso venoso bilateral",
                            "Oxígeno si SatO2 < 90%",
                            "Monitoreo cardíaco continuo"
                        ],
                        "pharmacotherapy": {
                            "antiplatelet": {
                                "aspirin": "300mg VO dosis carga, luego 75-100mg/día",
                                "clopidogrel": "600mg VO dosis carga, luego 75mg/día",
                                "ticagrelor": "180mg VO dosis carga, luego 90mg BID"
                            },
                            "anticoagulation": {
                                "heparina": "60 UI/kg IV bolo, luego 12 UI/kg/h",
                                "enoxaparina": "1mg/kg SC BID"
                            },
                            "additional": {
                                "atorvastatina": "80mg VO",
                                "metoprolol": "25mg BID si no contraindicado"
                            }
                        },
                        "reperfusion": {
                            "primary_pci": "< 90 minutos door-to-balloon",
                            "thrombolysis": "< 30 minutos door-to-needle si PCI no disponible"
                        }
                    },
                    "patient_guidance": {
                        "emergency_signs": [
                            "Dolor de pecho intenso > 5 minutos",
                            "Dolor que se extiende al brazo, cuello o mandíbula",
                            "Sudoración fría profusa",
                            "Náuseas y vómitos con dolor pecho",
                            "Sensación de muerte inminente"
                        ],
                        "immediate_actions": [
                            "Llamar al 911 inmediatamente",
                            "Tomar aspirina 300mg si disponible",
                            "Sentarse o recostarse",
                            "No conducir al hospital",
                            "Aflojar ropa ajustada"
                        ]
                    },
                    "prognosis": {
                        "stemi": "Mortalidad hospitalaria 4-6%, mejor pronóstico con reperfusión oportuna",
                        "nstemi": "Mortalidad hospitalaria 2-4%, pronóstico depende de estratificación de riesgo"
                    },
                    "evidence_level": "A",
                    "guidelines": ["ESC 2020", "AHA/ACC 2021", "STEMI Task Force 2017"]
                },
                
                "diabetes_mellitus_type_2": {
                    "name": "Diabetes Mellitus Tipo 2",
                    "icd10": "E11",
                    "category": "Endocrinología",
                    "urgency": "routine",
                    "description": "Trastorno metabólico crónico caracterizado por hiperglucemia debido a resistencia insulínica y deficiencia relativa de insulina",
                    "pathophysiology": "Combinación de resistencia periférica a la insulina y disfunción de células beta pancreáticas",
                    "clinical_presentation": {
                        "classic_triad": ["poliuria", "polidipsia", "polifagia"],
                        "additional_symptoms": [
                            "pérdida de peso inexplicada",
                            "fatiga crónica",
                            "visión borrosa",
                            "cicatrización lenta",
                            "infecciones recurrentes"
                        ],
                        "asymptomatic": "Hasta 50% de casos pueden ser asintomáticos al diagnóstico"
                    },
                    "diagnostic_criteria": {
                        "hba1c": "≥ 6.5% (48 mmol/mol)",
                        "fasting_glucose": "≥ 126 mg/dL (7.0 mmol/L)",
                        "ogtt_2h": "≥ 200 mg/dL (11.1 mmol/L)",
                        "random_glucose": "≥ 200 mg/dL con síntomas clásicos"
                    },
                    "complications": {
                        "microvascular": [
                            "Retinopatía diabética",
                            "Nefropatía diabética",
                            "Neuropatía diabética"
                        ],
                        "macrovascular": [
                            "Enfermedad coronaria",
                            "Enfermedad cerebrovascular",
                            "Enfermedad arterial periférica"
                        ],
                        "acute": [
                            "Cetoacidosis diabética (rara en T2DM)",
                            "Estado hiperosmolar hiperglucémico",
                            "Hipoglucemia (iatrogénica)"
                        ]
                    },
                    "professional_management": {
                        "lifestyle_intervention": [
                            "Reducción peso 5-10% si sobrepeso",
                            "Actividad física 150 min/semana moderada",
                            "Dieta mediterránea o baja en carbohidratos",
                            "Cesación tabáquica"
                        ],
                        "pharmacotherapy": {
                            "first_line": {
                                "metformin": "500-2000mg/día dividido en 2-3 tomas"
                            },
                            "second_line": {
                                "sulfonylureas": "glimepiride 1-4mg/día",
                                "dpp4_inhibitors": "sitagliptin 100mg/día",
                                "sglt2_inhibitors": "empagliflozin 10-25mg/día",
                                "glp1_agonists": "liraglutide 0.6-1.8mg SC/día"
                            },
                            "insulin": "Si HbA1c > 9% o síntomas severos"
                        },
                        "targets": {
                            "hba1c": "< 7% (< 53 mmol/mol) en mayoría",
                            "blood_pressure": "< 130/80 mmHg",
                            "ldl_cholesterol": "< 100 mg/dL (< 70 si alto riesgo)"
                        },
                        "monitoring": {
                            "hba1c": "Cada 3-6 meses",
                            "lipid_profile": "Anualmente",
                            "renal_function": "Anualmente",
                            "eye_exam": "Anualmente",
                            "foot_exam": "Cada visita"
                        }
                    },
                    "patient_guidance": {
                        "daily_management": [
                            "Monitoreo glucémico según indicación médica",
                            "Tomar medicación según prescrito",
                            "Mantener horarios regulares de comida",
                            "Inspección diaria de pies",
                            "Hidratación adecuada"
                        ],
                        "warning_signs": [
                            "Glucosa > 300 mg/dL persistente",
                            "Síntomas de cetoacidosis",
                            "Hipoglucemia severa",
                            "Úlceras en pies que no cicatrizan",
                            "Cambios visuales súbitos"
                        ]
                    },
                    "prognosis": "Con manejo adecuado, expectativa de vida normal. Complicaciones evitables con control glucémico estricto",
                    "evidence_level": "A",
                    "guidelines": ["ADA Standards 2023", "EASD/ESC 2019", "AACE 2022"]
                }
            },
            
            "medications": {
                "aspirin": {
                    "name": "Aspirina",
                    "generic": "Ácido acetilsalicílico",
                    "drug_class": "Antiagregante plaquetario, AINE",
                    "mechanism": "Inhibición irreversible de COX-1 plaquetaria, reduciendo síntesis de tromboxano A2",
                    "pharmacokinetics": {
                        "absorption": "Rápida, pico plasmático 1-2 horas",
                        "metabolism": "Hepático a ácido salicílico",
                        "elimination": "Renal, vida media 15-20 minutos",
                        "effect_duration": "Duración antiagregante 7-10 días"
                    },
                    "indications": {
                        "cardiovascular": [
                            "Prevención primaria en riesgo alto (>10% a 10 años)",
                            "Prevención secundaria post-infarto",
                            "Síndrome coronario agudo",
                            "Post-revascularización coronaria"
                        ],
                        "cerebrovascular": [
                            "Prevención secundaria post-ACV isquémico",
                            "Ataque isquémico transitorio"
                        ],
                        "other": [
                            "Antiinflamatorio (dosis altas)",
                            "Antipirético"
                        ]
                    },
                    "dosing": {
                        "cardiovascular_prevention": "75-100mg/día",
                        "acute_coronary_syndrome": "300mg dosis carga, luego 75-100mg/día",
                        "stroke_prevention": "75-100mg/día",
                        "anti_inflammatory": "500-1000mg cada 6 horas PRN"
                    },
                    "contraindications": {
                        "absolute": [
                            "Alergia a salicilatos",
                            "Hemorragia activa",
                            "Hemofilia u otros trastornos hemorrágicos",
                            "Úlcera péptica activa"
                        ],
                        "relative": [
                            "Historia de sangrado GI",
                            "Asma inducida por aspirina",
                            "Insuficiencia renal severa",
                            "Cirugía programada"
                        ]
                    },
                    "side_effects": {
                        "common": [
                            "Dispepsia (10-40%)",
                            "Náuseas",
                            "Dolor abdominal"
                        ],
                        "serious": [
                            "Hemorragia gastrointestinal (0.3-0.5%/año)",
                            "Hemorragia intracraneal (0.1-0.2%/año)",
                            "Broncoespasmo (pacientes susceptibles)",
                            "Síndrome de Reye (niños con infecciones virales)"
                        ]
                    },
                    "drug_interactions": {
                        "major": [
                            "Warfarina: ↑↑ riesgo hemorrágico",
                            "Metotrexato: ↑ toxicidad por ↓ eliminación",
                            "IECA: ↓ efecto antihipertensivo"
                        ],
                        "moderate": [
                            "Diuréticos: ↓ efecto diurético",
                            "Corticosteroides: ↑ riesgo úlcera GI",
                            "Alcohol: ↑ riesgo sangrado GI"
                        ]
                    },
                    "monitoring": [
                        "Síntomas de sangrado GI",
                        "Función renal (uso crónico)",
                        "Signos de toxicidad salicílica (dosis altas)"
                    ],
                    "patient_counseling": {
                        "administration": [
                            "Tomar con alimentos para ↓ irritación GI",
                            "No masticar tabletas entéricas",
                            "Mantener hidratación adecuada"
                        ],
                        "monitoring": [
                            "Reportar sangrado inusual",
                            "Dolor abdominal persistente",
                            "Heces negras o con sangre",
                            "Mareos o confusión"
                        ]
                    },
                    "evidence_level": "A",
                    "guidelines": ["ESC 2019", "AHA/ACC 2019", "USPSTF 2022"]
                }
            }
        }
    
    async def process_enhanced_medical_query(self, 
                                           text: str, 
                                           image_data: Optional[bytes] = None) -> EnhancedMedicalResponse:
        """Process medical query with enhanced AI capabilities"""
        
        start_time = datetime.now()
        
        # Enhanced context analysis
        enhanced_query = await self._analyze_enhanced_context(text, bool(image_data))
        
        # Try Kimi first if available
        ai_source = "local_advanced"
        response_text = ""
        
        if self.kimi_client and await self._test_kimi_availability():
            try:
                response_text = await self._process_with_kimi(enhanced_query, image_data)
                ai_source = "kimi_real"
                self.performance_metrics["kimi_requests"] += 1
            except Exception as e:
                print(f"⚠️ Kimi unavailable, using advanced local: {e}")
                response_text = await self._process_with_advanced_local(enhanced_query)
                ai_source = "local_advanced"
                self.performance_metrics["local_requests"] += 1
        else:
            # Use advanced local processing
            response_text = await self._process_with_advanced_local(enhanced_query)
            self.performance_metrics["local_requests"] += 1
        
        # Get medical knowledge sources
        medical_sources = self._search_enhanced_knowledge(text)
        
        # Generate comprehensive recommendations
        recommendations = self._generate_enhanced_recommendations(enhanced_query, medical_sources)
        
        # Generate warnings and follow-up
        warnings = self._generate_enhanced_warnings(enhanced_query)
        follow_up = self._generate_enhanced_followup(enhanced_query)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create enhanced response
        response = EnhancedMedicalResponse(
            response_id=str(uuid.uuid4()),
            query_id=enhanced_query.query_id,
            user_type=enhanced_query.user_type,
            response_text=response_text,
            confidence=enhanced_query.confidence,
            medical_sources=medical_sources,
            recommendations=recommendations,
            warnings=warnings,
            follow_up=follow_up,
            emergency_level=enhanced_query.urgency_level,
            ai_source=ai_source,
            processing_time=processing_time,
            timestamp=datetime.now()
        )
        
        # Update performance metrics
        self._update_performance_metrics(response)
        
        # Store in history
        self.session_history.append((enhanced_query, response))
        
        return response
    
    async def _analyze_enhanced_context(self, text: str, has_image: bool) -> EnhancedMedicalQuery:
        """Enhanced context analysis with medical reasoning"""
        
        query_id = str(uuid.uuid4())
        text_lower = text.lower()
        
        # Advanced user type detection
        professional_score = self._calculate_professional_score(text)
        patient_score = self._calculate_patient_score(text)
        
        user_type = "professional" if professional_score > patient_score else "patient"
        confidence = max(professional_score, patient_score)
        
        # Enhanced query type detection
        query_type = self._detect_enhanced_query_type(text, has_image)
        
        # Advanced urgency detection
        urgency_level = self._detect_enhanced_urgency(text)
        
        # Medical specialty detection
        medical_specialty = self._detect_medical_specialty(text)
        
        # Comprehensive context extraction
        context = self._extract_comprehensive_context(text)
        
        # Apply medical reasoning
        medical_analysis = self.reasoning_engine.analyze_medical_condition(text, context)
        context["medical_analysis"] = medical_analysis
        
        # Adjust urgency based on medical analysis
        if medical_analysis["urgency_score"] > 0.8:
            urgency_level = "emergency"
        elif medical_analysis["urgency_score"] > 0.5:
            urgency_level = "urgent"
        
        return EnhancedMedicalQuery(
            query_id=query_id,
            original_text=text,
            user_type=user_type,
            query_type=query_type,
            urgency_level=urgency_level,
            context=context,
            confidence=confidence,
            medical_specialty=medical_specialty,
            timestamp=datetime.now()
        )
    
    def _calculate_professional_score(self, text: str) -> float:
        """Calculate professional medical language score"""
        
        professional_indicators = [
            "paciente", "dx", "diagnóstico diferencial", "protocolo", "manejo",
            "tratamiento de elección", "indicaciones", "contraindicaciones",
            "dosis", "posología", "seguimiento", "derivación", "interconsulta",
            "historia clínica", "examen físico", "estudios complementarios",
            "pronóstico", "epidemiología", "fisiopatología", "farmacoterapia",
            "biomarkers", "troponinas", "electrocardiograma", "ecocardiograma"
        ]
        
        text_lower = text.lower()
        matches = sum(2 if indicator in text_lower else 0 for indicator in professional_indicators)
        
        # Weight by text length and complexity
        length_factor = min(1.5, len(text.split()) / 10)
        complexity_factor = 1.2 if any(term in text_lower for term in ["fisiopatología", "farmacoterapia"]) else 1.0
        
        score = (matches / len(professional_indicators)) * length_factor * complexity_factor
        
        return min(0.95, score)
    
    def _calculate_patient_score(self, text: str) -> float:
        """Calculate patient language score"""
        
        patient_indicators = [
            "me duele", "tengo", "siento", "estoy", "mi", "me preocupa",
            "qué debo hacer", "es normal", "debo ir al doctor", "es grave",
            "me pasa", "me molesta", "mi familia", "mi hijo", "mi esposa",
            "desde hace", "me siento", "estoy asustado", "no sé qué hacer"
        ]
        
        text_lower = text.lower()
        matches = sum(1 if indicator in text_lower else 0 for indicator in patient_indicators)
        
        # Personal pronouns increase patient score
        personal_pronouns = ["me", "mi", "yo", "estoy", "tengo", "siento"]
        pronoun_count = sum(text_lower.count(pronoun) for pronoun in personal_pronouns)
        
        base_score = matches / len(patient_indicators)
        pronoun_bonus = min(0.3, pronoun_count * 0.05)
        
        return min(0.9, base_score + pronoun_bonus)
    
    def _detect_enhanced_query_type(self, text: str, has_image: bool) -> str:
        """Enhanced query type detection"""
        
        text_lower = text.lower()
        
        if has_image:
            return "image_analysis"
        
        # Medical education queries
        education_patterns = ["qué es", "explicar", "información sobre", "cómo funciona"]
        if any(pattern in text_lower for pattern in education_patterns):
            return "medical_education"
        
        # Medication queries
        medication_patterns = ["dosis", "medicamento", "fármaco", "efectos secundarios", "interacciones"]
        if any(pattern in text_lower for pattern in medication_patterns):
            return "medication_inquiry"
        
        # Diagnostic queries
        diagnostic_patterns = ["diagnóstico", "síntomas", "dolor", "molestia", "presenta"]
        if any(pattern in text_lower for pattern in diagnostic_patterns):
            return "diagnostic_consultation"
        
        # Protocol queries
        protocol_patterns = ["protocolo", "manejo", "tratamiento", "guía", "algoritmo"]
        if any(pattern in text_lower for pattern in protocol_patterns):
            return "clinical_protocol"
        
        # Lab interpretation
        lab_patterns = ["análisis", "laboratorio", "resultado", "valores", "examen"]
        if any(pattern in text_lower for pattern in lab_patterns):
            return "lab_interpretation"
        
        return "general_consultation"
    
    def _detect_enhanced_urgency(self, text: str) -> str:
        """Enhanced urgency detection with medical reasoning"""
        
        text_lower = text.lower()
        
        # Critical emergencies
        critical_patterns = [
            "dolor torácico", "dolor precordial", "opresión torácica",
            "dificultad respiratoria severa", "disnea súbita",
            "pérdida de conciencia", "convulsiones", "estado confusional agudo",
            "sangrado masivo", "hematemesis", "melena",
            "dolor abdominal severo", "abdomen agudo"
        ]
        
        for pattern in critical_patterns:
            if pattern in text_lower:
                return "emergency"
        
        # Urgent conditions
        urgent_patterns = [
            "fiebre alta", "temperatura > 39", "dolor intenso",
            "vómitos persistentes", "deshidratación",
            "cambios neurológicos", "alteración conciencia"
        ]
        
        for pattern in urgent_patterns:
            if pattern in text_lower:
                return "urgent"
        
        # Time-based urgency
        time_patterns = ["súbito", "repentino", "desde hace minutos", "desde hace horas"]
        if any(pattern in text_lower for pattern in time_patterns):
            return "urgent"
        
        return "routine"
    
    def _detect_medical_specialty(self, text: str) -> Optional[str]:
        """Detect relevant medical specialty"""
        
        text_lower = text.lower()
        
        specialty_keywords = {
            "cardiology": ["corazón", "cardíaco", "precordial", "angina", "infarto", "arritmia"],
            "neurology": ["cerebro", "neurológico", "convulsión", "parálisis", "cefalea", "mareos"],
            "pulmonology": ["pulmón", "respiratorio", "tos", "disnea", "asma", "neumonía"],
            "gastroenterology": ["estómago", "digestivo", "náusea", "diarrea", "hígado", "abdomen"],
            "endocrinology": ["diabetes", "tiroides", "hormona", "glucosa", "metabolismo"],
            "emergency": ["emergencia", "urgencia", "trauma", "accidente", "lesión"]
        }
        
        for specialty, keywords in specialty_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return specialty
        
        return None
    
    def _extract_comprehensive_context(self, text: str) -> Dict[str, Any]:
        """Extract comprehensive medical context"""
        
        context = {
            "demographics": {},
            "symptoms": [],
            "medical_history": [],
            "medications": [],
            "allergies": [],
            "time_course": {},
            "severity_indicators": [],
            "risk_factors": [],
            "social_history": {}
        }
        
        # Demographics
        age_match = re.search(r'(\d+)\s*años?', text, re.IGNORECASE)
        if age_match:
            context["demographics"]["age"] = int(age_match.group(1))
        
        gender_patterns = {
            "masculino": r'\b(masculino|hombre|varón|macho|paciente.*él)\b',
            "femenino": r'\b(femenino|mujer|paciente.*ella)\b'
        }
        
        for gender, pattern in gender_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                context["demographics"]["gender"] = gender
                break
        
        # Enhanced symptom extraction
        symptom_patterns = [
            r'dolor\s+(?:en\s+)?(?:el\s+|la\s+)?(\w+)',
            r'(\w+)\s+dolor',
            r'molestia\s+(?:en\s+)?(\w+)',
            r'síntomas?\s+de\s+(\w+)',
            r'presenta\s+(\w+)',
            r'sensación\s+de\s+(\w+)',
            r'dificultad\s+para\s+(\w+)'
        ]
        
        for pattern in symptom_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            context["symptoms"].extend(matches)
        
        # Time course extraction
        time_patterns = {
            "duration": r'(?:desde\s+hace|hace|durante)\s+(\d+)\s*(minutos?|horas?|días?|semanas?|meses?|años?)',
            "onset": r'\b(súbito|gradual|progresivo|agudo|crónico|insidioso)\b',
            "frequency": r'(\d+)\s*veces?\s*(?:por|al)\s*(día|semana|mes)',
            "pattern": r'\b(continuo|intermitente|episódico|nocturno|matutino)\b'
        }
        
        for key, pattern in time_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                context["time_course"][key] = matches
        
        # Medical history
        history_patterns = [
            r'diabético|diabetes',
            r'hipertenso|hipertensión',
            r'cardíaco|cardiaco|coronario',
            r'asmático|asma',
            r'alérgico|alergia',
            r'cirugía|operado|intervenido',
            r'cáncer|tumor|neoplasia',
            r'renal|riñón',
            r'hepático|hígado'
        ]
        
        for pattern in history_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                condition = pattern.split('|')[0]
                context["medical_history"].append(condition)
        
        # Severity indicators
        severity_patterns = [
            r'\b(intenso|severo|fuerte|insoportable)\b',
            r'\b(leve|ligero|moderado)\b',
            r'\b(empeora|mejora|estable)\b',
            r'escala.*(\d+).*10'
        ]
        
        for pattern in severity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            context["severity_indicators"].extend(matches)
        
        return context
    
    async def _test_kimi_availability(self) -> bool:
        """Test if Kimi is available"""
        
        if not hasattr(self, '_kimi_last_test'):
            self._kimi_last_test = datetime.min
        
        # Test every 5 minutes
        if (datetime.now() - self._kimi_last_test).seconds < 300:
            return self.kimi_available
        
        try:
            async with self.kimi_client as kimi:
                self.kimi_available = await kimi.test_connection()
            self._kimi_last_test = datetime.now()
            return self.kimi_available
        except:
            self.kimi_available = False
            return False
    
    async def _process_with_kimi(self, query: EnhancedMedicalQuery, image_data: Optional[bytes] = None) -> str:
        """Process query with real Kimi API"""
        
        # Prepare system prompt based on user type
        if query.user_type == "professional":
            system_prompt = f"""Eres un sistema de IA médica avanzada para profesionales de la salud.

PROTOCOLO DE RESPUESTA PROFESIONAL:
- Proporciona análisis clínico detallado con evidencia científica
- Incluye diagnósticos diferenciales con probabilidades estimadas  
- Especifica protocolos de manejo y dosis farmacológicas exactas
- Cita guías clínicas y evidencia actual cuando sea relevante
- Indica criterios de derivación y seguimiento

URGENCIA: {query.urgency_level.upper()}
ESPECIALIDAD: {query.medical_specialty or 'General'}

CONTEXTO MÉDICO:
{json.dumps(query.context, indent=2)}

Responde con precisión técnica apropiada para profesionales médicos."""

        else:
            system_prompt = f"""Eres un sistema de IA médica para educar y orientar a pacientes.

PROTOCOLO DE RESPUESTA PARA PACIENTES:
- Usa lenguaje claro y comprensible
- Proporciona información educativa sin alarmar
- Enfatiza cuándo es importante buscar atención médica
- Incluye medidas de autocuidado apropiadas
- Mantén un tono empático y tranquilizador

URGENCIA: {query.urgency_level.upper()}

CONTEXTO DEL PACIENTE:
{json.dumps(query.context, indent=2)}

Responde de manera comprensible y útil para el paciente."""
        
        # Add emergency protocol if needed
        if query.urgency_level == "emergency":
            system_prompt += "\n\n🚨 PROTOCOLO DE EMERGENCIA ACTIVADO 🚨\nProporciona instrucciones claras de acción inmediata."
        
        async with self.kimi_client as kimi:
            if image_data:
                response = await kimi.analyze_medical_image(
                    image_data, 
                    query.original_text, 
                    query.user_type
                )
            else:
                response = await kimi.generate_medical_consultation(
                    query.original_text,
                    query.context,
                    query.user_type,
                    query.urgency_level
                )
        
        return response
    
    async def _process_with_advanced_local(self, query: EnhancedMedicalQuery) -> str:
        """Process with advanced local AI capabilities"""
        
        response_parts = []
        
        # Emergency protocol activation
        if query.urgency_level == "emergency":
            response_parts.append(self._generate_emergency_protocol(query))
        
        # Medical analysis from reasoning engine
        medical_analysis = query.context.get("medical_analysis", {})
        if medical_analysis.get("conditions_detected"):
            response_parts.append(self._format_medical_analysis(medical_analysis, query.user_type))
        
        # Knowledge-based response
        knowledge_response = self._generate_knowledge_based_response(query)
        if knowledge_response:
            response_parts.append(knowledge_response)
        
        # Specialty-specific guidance
        if query.medical_specialty:
            specialty_guidance = self._generate_specialty_guidance(query)
            if specialty_guidance:
                response_parts.append(specialty_guidance)
        
        # Default comprehensive response if no specific content
        if not response_parts:
            response_parts.append(self._generate_default_comprehensive_response(query))
        
        return "\n\n".join(response_parts)
    
    def _generate_emergency_protocol(self, query: EnhancedMedicalQuery) -> str:
        """Generate emergency protocol response"""
        
        if query.user_type == "professional":
            return """🚨 PROTOCOLO DE EMERGENCIA MÉDICA ACTIVADO

📋 EVALUACIÓN PRIMARIA:
• Evaluación ABCDE inmediata
• Signos vitales completos
• Acceso venoso y oxigenoterapia
• Monitoreo cardíaco continuo
• Preparación para soporte vital avanzado

⏱️ CRONOMETRAJE CRÍTICO:
• ECG < 10 minutos
• Laboratorio urgente < 15 minutos
• Evaluación especialista < 30 minutos

🚨 CRITERIOS DE ACTIVACIÓN DE CÓDIGO:
• Evaluar necesidad de código azul/rojo
• Notificar a equipo de respuesta rápida
• Documentación continua de intervenciones"""

        else:
            return """🚨 EMERGENCIA MÉDICA DETECTADA

⚠️ ACCIÓN INMEDIATA REQUERIDA:
• 📞 Llame al 911 AHORA MISMO
• 🚗 NO conduzca usted mismo al hospital
• 🏠 Manténgase en lugar seguro y cómodo
• 👥 Avise a alguien de confianza
• 📱 Mantenga el teléfono cerca

💊 SI TIENE EN CASA:
• Aspirina: tome 300mg si no es alérgico
• Nitroglicerina: use según prescripción previa

⏰ EL TIEMPO ES CRÍTICO EN EMERGENCIAS MÉDICAS
🏥 Un profesional médico debe evaluarlo INMEDIATAMENTE"""
    
    def _format_medical_analysis(self, analysis: Dict[str, Any], user_type: str) -> str:
        """Format medical analysis results"""
        
        if user_type == "professional":
            output = ["🧠 ANÁLISIS MÉDICO AVANZADO:"]
            
            if analysis.get("conditions_detected"):
                output.append("\n📊 CONDICIONES IDENTIFICADAS:")
                for condition in analysis["conditions_detected"]:
                    output.append(f"• {condition['condition']}: {condition['confidence']:.1%} confianza")
                    output.append(f"  Categoría: {condition['category']}")
                    output.append(f"  Peso de urgencia: {condition['urgency_weight']:.1%}")
            
            if analysis.get("differential_diagnosis"):
                output.append("\n🎯 DIAGNÓSTICO DIFERENCIAL:")
                for dx in analysis["differential_diagnosis"]:
                    output.append(f"• {dx['condition']}: {dx['probability']:.1%} probabilidad")
                    output.append(f"  Fuerza de evidencia: {dx['evidence_strength']}")
            
            if analysis.get("recommended_actions"):
                output.append("\n💡 ACCIONES RECOMENDADAS:")
                for action in analysis["recommended_actions"]:
                    output.append(f"• {action}")
            
            return "\n".join(output)
        
        else:
            # Simplified for patients
            if analysis.get("urgency_score", 0) > 0.7:
                return """🚨 ANÁLISIS MÉDICO:
Se han detectado síntomas que requieren atención médica inmediata.
Por favor, busque ayuda médica profesional sin demora."""
            else:
                return """📋 ANÁLISIS MÉDICO:
Sus síntomas han sido analizados. Se recomienda consulta médica para evaluación completa."""
    
    def _generate_knowledge_based_response(self, query: EnhancedMedicalQuery) -> str:
        """Generate response based on medical knowledge"""
        
        relevant_knowledge = self._search_enhanced_knowledge(query.original_text)
        
        if not relevant_knowledge:
            return ""
        
        response_parts = ["📚 INFORMACIÓN MÉDICA RELEVANTE:"]
        
        for item in relevant_knowledge[:2]:  # Top 2 most relevant
            if item["type"] == "condition":
                response_parts.append(f"\n🏥 {item['name']} ({item.get('icd10', 'N/A')})")
                
                if query.user_type == "professional":
                    response_parts.append(f"📖 {item.get('description', '')}")
                    if item.get('professional_management'):
                        mgmt = item['professional_management']
                        if 'immediate_actions' in mgmt:
                            response_parts.append("⚡ Acciones inmediatas:")
                            for action in mgmt['immediate_actions'][:3]:
                                response_parts.append(f"  • {action}")
                else:
                    # Patient-friendly explanation
                    desc = item.get('description', '').replace('isquemia miocárdica', 'falta de oxígeno al corazón')
                    response_parts.append(f"📖 {desc}")
                    if item.get('patient_guidance'):
                        guidance = item['patient_guidance']
                        if 'emergency_signs' in guidance:
                            response_parts.append("⚠️ Signos de alarma:")
                            for sign in guidance['emergency_signs'][:3]:
                                response_parts.append(f"  • {sign}")
        
        return "\n".join(response_parts)
    
    def _search_enhanced_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Enhanced medical knowledge search"""
        
        query_embedding = self.embedding_model.encode(query.lower())
        results = []
        
        # Search conditions
        for condition_key, condition in self.medical_knowledge["conditions"].items():
            searchable_text = f"{condition['name']} {condition['description']}"
            if 'clinical_presentation' in condition:
                if 'typical' in condition['clinical_presentation']:
                    searchable_text += " " + " ".join(condition['clinical_presentation']['typical'])
            
            condition_embedding = self.embedding_model.encode(searchable_text.lower())
            similarity = np.dot(query_embedding, condition_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(condition_embedding)
            )
            
            if similarity > 0.3:
                result = {
                    "type": "condition",
                    "similarity": similarity,
                    **condition
                }
                results.append(result)
        
        # Search medications
        for med_key, medication in self.medical_knowledge["medications"].items():
            searchable_text = f"{medication['name']} {medication['generic']}"
            if 'indications' in medication:
                searchable_text += " " + " ".join(medication['indications']['cardiovascular'])
            
            med_embedding = self.embedding_model.encode(searchable_text.lower())
            similarity = np.dot(query_embedding, med_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(med_embedding)
            )
            
            if similarity > 0.3:
                result = {
                    "type": "medication",
                    "similarity": similarity,
                    **medication
                }
                results.append(result)
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:5]
    
    def _generate_specialty_guidance(self, query: EnhancedMedicalQuery) -> str:
        """Generate specialty-specific guidance"""
        
        specialty_guidance = {
            "cardiology": {
                "professional": """🫀 ORIENTACIÓN CARDIOLÓGICA:
• Evaluación de factores de riesgo cardiovascular
• Estratificación según scores validados (GRACE, TIMI)
• Considerar biomarcadores cardíacos
• Evaluación de función ventricular
• Plan de revascularización si indicado""",
                "patient": """❤️ CUIDADO CARDÍACO:
• Los problemas del corazón requieren atención especializada
• Mantenga un registro de sus síntomas
• Siga las indicaciones médicas estrictamente
• Evite esfuerzos hasta evaluación completa
• Busque ayuda inmediata si empeoran los síntomas"""
            },
            
            "emergency": {
                "professional": """🚨 MEDICINA DE EMERGENCIA:
• Aplicación de protocolos de triage
• Estabilización hemodinámica prioritaria
• Evaluación sistemática ABCDE
• Coordinación con especialistas
• Documentación continua de intervenciones""",
                "patient": """🆘 SITUACIÓN DE EMERGENCIA:
• Su condición requiere atención médica inmediata
• Siga todas las instrucciones del personal médico
• Mantenga la calma y coopere con el tratamiento
• Informe cualquier cambio en sus síntomas
• Un ser querido debe estar informado de su situación"""
            }
        }
        
        if query.medical_specialty in specialty_guidance:
            return specialty_guidance[query.medical_specialty][query.user_type]
        
        return ""
    
    def _generate_default_comprehensive_response(self, query: EnhancedMedicalQuery) -> str:
        """Generate default comprehensive response"""
        
        if query.user_type == "professional":
            return f"""📋 EVALUACIÓN MÉDICA SISTEMÁTICA:

🎯 ANÁLISIS DE CONSULTA:
• Tipo de consulta: {query.query_type.replace('_', ' ').title()}
• Nivel de urgencia: {query.urgency_level.upper()}
• Especialidad relevante: {query.medical_specialty or 'Medicina General'}

📊 CONTEXTO CLÍNICO IDENTIFICADO:
{json.dumps(query.context, indent=2)}

💡 RECOMENDACIONES GENERALES:
• Evaluación clínica integral con historia clínica completa
• Examen físico dirigido según sintomatología
• Estudios complementarios según indicación clínica
• Seguimiento programado según evolución
• Interconsulta especializada si corresponde

⚠️ CONSIDERACIONES:
• Correlacionar siempre con hallazgos clínicos
• Individualizar manejo según comorbilidades
• Documentar adecuadamente en historia clínica"""

        else:
            return f"""🏥 ORIENTACIÓN MÉDICA GENERAL:

📋 SU CONSULTA:
Hemos analizado su consulta médica y entendemos su preocupación.

💡 RECOMENDACIONES:
• Consulte con su médico de cabecera para evaluación completa
• Mantenga un registro detallado de sus síntomas
• No se automedique sin supervisión médica
• Siga las indicaciones médicas que reciba
• Busque atención médica si los síntomas empeoran

⚠️ CUÁNDO BUSCAR AYUDA INMEDIATA:
• Si los síntomas empeoran rápidamente
• Si aparecen nuevos síntomas preocupantes
• Si tiene dudas sobre su condición
• Si siente que algo no está bien

🏥 RECUERDE:
• Esta información es educativa únicamente
• Un médico debe evaluarlo personalmente
• Cada caso es único y requiere atención individualizada"""
    
    def _generate_enhanced_recommendations(self, query: EnhancedMedicalQuery, 
                                         medical_sources: List[Dict[str, Any]]) -> List[str]:
        """Generate enhanced recommendations"""
        
        recommendations = []
        
        # Urgency-based recommendations
        if query.urgency_level == "emergency":
            if query.user_type == "professional":
                recommendations.extend([
                    "Activación inmediata de protocolo de emergencia",
                    "Evaluación ABCDE y estabilización hemodinámica",
                    "Monitoreo continuo de signos vitales",
                    "Preparación para soporte vital avanzado",
                    "Coordinación con equipo multidisciplinario"
                ])
            else:
                recommendations.extend([
                    "Llamar al 911 inmediatamente",
                    "No demorar la búsqueda de atención médica",
                    "Seguir instrucciones del personal de emergencias",
                    "Mantener la calma y cooperar con el tratamiento"
                ])
        
        elif query.urgency_level == "urgent":
            recommendations.extend([
                "Evaluación médica dentro de 2-4 horas",
                "Estudios diagnósticos prioritarios",
                "Observación clínica estrecha",
                "Reevaluación según evolución"
            ])
        
        else:  # routine
            recommendations.extend([
                "Consulta médica programada",
                "Seguimiento clínico apropiado",
                "Educación sobre signos de alarma"
            ])
        
        # Specialty-specific recommendations
        if query.medical_specialty == "cardiology":
            recommendations.extend([
                "ECG de 12 derivaciones",
                "Evaluación de factores de riesgo cardiovascular",
                "Considerar biomarcadores cardíacos"
            ])
        elif query.medical_specialty == "neurology":
            recommendations.extend([
                "Evaluación neurológica detallada",
                "Considerar neuroimagen si indicada",
                "Escalas de valoración neurológica"
            ])
        
        # Knowledge-based recommendations
        for source in medical_sources[:2]:
            if source["type"] == "condition" and query.user_type == "professional":
                mgmt = source.get("professional_management", {})
                if "immediate_actions" in mgmt:
                    recommendations.extend(mgmt["immediate_actions"][:2])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _generate_enhanced_warnings(self, query: EnhancedMedicalQuery) -> List[str]:
        """Generate enhanced medical warnings"""
        
        warnings = [
            "Esta información es educativa y de apoyo únicamente",
            "NO reemplaza la evaluación médica profesional directa",
            "Cada caso requiere evaluación médica individualizada"
        ]
        
        if query.urgency_level == "emergency":
            warnings.insert(0, "EMERGENCIA MÉDICA - Contacte servicios de urgencia inmediatamente")
        
        if query.user_type == "patient":
            warnings.extend([
                "No se automedique basándose en esta información",
                "Consulte siempre con un profesional de la salud",
                "En caso de duda, busque atención médica"
            ])
        
        return warnings
    
    def _generate_enhanced_followup(self, query: EnhancedMedicalQuery) -> List[str]:
        """Generate enhanced follow-up actions"""
        
        followup = []
        
        if query.user_type == "professional":
            followup.extend([
                "Documentación completa en historia clínica",
                "Plan de seguimiento protocolizado",
                "Reevaluación según evolución clínica",
                "Consideración de interconsulta si no hay mejoría"
            ])
        else:
            followup.extend([
                "Seguimiento médico según indicaciones",
                "Control de síntomas y respuesta",
                "Consulta de control en fechas programadas",
                "Buscar atención si empeoran los síntomas"
            ])
        
        # Urgency-specific follow-up
        if query.urgency_level == "emergency":
            followup.insert(0, "Seguimiento hospitalario hasta estabilización completa")
        elif query.urgency_level == "urgent":
            followup.insert(0, "Reevaluación en 24-48 horas")
        
        return followup
    
    def _update_performance_metrics(self, response: EnhancedMedicalResponse):
        """Update system performance metrics"""
        
        # Update confidence average
        total_responses = sum([
            self.performance_metrics["kimi_requests"],
            self.performance_metrics["local_requests"],
            self.performance_metrics["hybrid_requests"]
        ])
        
        if total_responses > 0:
            current_avg = self.performance_metrics["average_confidence"]
            new_avg = ((current_avg * (total_responses - 1)) + response.confidence) / total_responses
            self.performance_metrics["average_confidence"] = new_avg
        
        # Update response time average
        if total_responses > 0:
            current_avg = self.performance_metrics["average_response_time"]
            new_avg = ((current_avg * (total_responses - 1)) + response.processing_time) / total_responses
            self.performance_metrics["average_response_time"] = new_avg
    
    def get_enhanced_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        
        if not self.session_history:
            return {"message": "No hay consultas en la sesión actual"}
        
        total_queries = len(self.session_history)
        emergency_queries = sum(1 for q, r in self.session_history if q.urgency_level == "emergency")
        professional_queries = sum(1 for q, r in self.session_history if q.user_type == "professional")
        kimi_responses = sum(1 for q, r in self.session_history if r.ai_source == "kimi_real")
        
        specialties = [q.medical_specialty for q, r in self.session_history if q.medical_specialty]
        most_common_specialty = max(set(specialties), key=specialties.count) if specialties else None
        
        return {
            "session_overview": {
                "total_consultations": total_queries,
                "emergency_consultations": emergency_queries,
                "professional_consultations": professional_queries,
                "patient_consultations": total_queries - professional_queries,
                "kimi_powered_responses": kimi_responses,
                "local_ai_responses": total_queries - kimi_responses
            },
            "performance_metrics": self.performance_metrics,
            "medical_insights": {
                "most_common_specialty": most_common_specialty,
                "emergency_rate": f"{(emergency_queries/total_queries)*100:.1f}%" if total_queries > 0 else "0%",
                "professional_usage": f"{(professional_queries/total_queries)*100:.1f}%" if total_queries > 0 else "0%"
            },
            "system_status": {
                "kimi_available": self.kimi_available,
                "advanced_local_active": True,
                "medical_reasoning_active": True,
                "knowledge_base_loaded": True
            },
            "session_duration": str(datetime.now() - self.session_history[0][0].timestamp) if self.session_history else "0:00:00",
            "last_consultation": self.session_history[-1][1].timestamp.isoformat() if self.session_history else None
        }

# Export main class
__all__ = ['EnhancedMedeXAIEngine', 'EnhancedMedicalQuery', 'EnhancedMedicalResponse']