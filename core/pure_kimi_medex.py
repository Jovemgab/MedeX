#!/usr/bin/env python3
"""
Pure Kimi MedeX - 100% Real Medical AI System
No fallback mode. Pure Moonshot Kimi integration.
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from real_kimi_client import RealKimiClient, KimiRequest

@dataclass
class MedicalContext:
    """Medical context for enhanced AI responses"""
    age: Optional[int] = None
    gender: Optional[str] = None
    symptoms: List[str] = None
    duration: Optional[str] = None
    severity: Optional[str] = None
    medical_history: List[str] = None
    medications: List[str] = None
    allergies: List[str] = None
    vital_signs: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.symptoms is None:
            self.symptoms = []
        if self.medical_history is None:
            self.medical_history = []
        if self.medications is None:
            self.medications = []
        if self.allergies is None:
            self.allergies = []
        if self.vital_signs is None:
            self.vital_signs = {}

class PureKimiMedeX:
    """Pure Kimi-based Medical AI System - No Fallbacks"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.kimi_client = None
        
        # Emergency keywords for immediate detection
        self.emergency_keywords = {
            'cardiac': ['dolor precordial', 'dolor toracico', 'dolor pecho', 'infarto', 'angina', 
                       'palpitaciones', 'taquicardia', 'bradicardia', 'chest pain'],
            'respiratory': ['dificultad respiratoria', 'disnea', 'ahogo', 'falta aire', 'cianosis'],
            'neurological': ['dolor cabeza intenso', 'convulsiones', 'perdida conciencia', 'ictus', 'avc'],
            'trauma': ['accidente', 'traumatismo', 'fractura', 'hemorragia', 'sangrado abundante'],
            'critical': ['emergencia', 'critico', 'grave', 'urgente', '911', 'ambulancia']
        }
        
        # Professional detection patterns
        self.professional_patterns = [
            r'paciente\s+de\s+\d+\s+años',
            r'caso\s+clinico',
            r'diagnostico\s+diferencial',
            r'protocolo\s+de',
            r'tratamiento\s+con',
            r'dosis\s+de',
            r'mg\s+cada',
            r'codigo\s+icd',
            r'manejo\s+de',
            r'seguimiento'
        ]
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.kimi_client = RealKimiClient(self.api_key)
        await self.kimi_client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.kimi_client:
            await self.kimi_client.__aexit__(exc_type, exc_val, exc_tb)
    
    def detect_user_type(self, query: str) -> str:
        """Detect if user is medical professional or patient"""
        query_lower = query.lower()
        
        # Check for professional patterns
        for pattern in self.professional_patterns:
            if re.search(pattern, query_lower):
                return "professional"
        
        # Check for patient indicators
        patient_indicators = ['me duele', 'tengo', 'siento', 'me pasa', 'que sera', 'estoy preocupado']
        for indicator in patient_indicators:
            if indicator in query_lower:
                return "patient"
        
        # Default to patient for safety
        return "patient"
    
    def detect_urgency_level(self, query: str) -> str:
        """Detect urgency level from query"""
        query_lower = query.lower()
        
        # Check for emergency keywords
        for category, keywords in self.emergency_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return "emergency"
        
        # Check for urgent indicators
        urgent_indicators = ['urgente', 'rapido', 'inmediato', 'ahora', 'pronto']
        for indicator in urgent_indicators:
            if indicator in query_lower:
                return "urgent"
        
        return "routine"
    
    def extract_medical_context(self, query: str) -> MedicalContext:
        """Extract medical context from query"""
        context = MedicalContext()
        query_lower = query.lower()
        
        # Extract age
        age_match = re.search(r'(\d{1,3})\s*años?', query_lower)
        if age_match:
            context.age = int(age_match.group(1))
        
        # Extract gender
        if any(word in query_lower for word in ['hombre', 'masculino', 'varón']):
            context.gender = "masculino"
        elif any(word in query_lower for word in ['mujer', 'femenino', 'femenina']):
            context.gender = "femenino"
        
        # Extract duration
        duration_patterns = [
            r'(\d+)\s*horas?',
            r'(\d+)\s*dias?', 
            r'(\d+)\s*semanas?',
            r'(\d+)\s*meses?'
        ]
        for pattern in duration_patterns:
            match = re.search(pattern, query_lower)
            if match:
                context.duration = match.group(0)
                break
        
        # Extract symptoms (basic detection)
        symptom_keywords = [
            'dolor', 'fiebre', 'nauseas', 'vomitos', 'diarrea', 'estreñimiento',
            'mareos', 'fatiga', 'debilidad', 'palpitaciones', 'disnea'
        ]
        for symptom in symptom_keywords:
            if symptom in query_lower:
                context.symptoms.append(symptom)
        
        # Extract medical history indicators
        if 'diabetico' in query_lower or 'diabetes' in query_lower:
            context.medical_history.append('Diabetes Mellitus')
        if 'hipertenso' in query_lower or 'hipertension' in query_lower:
            context.medical_history.append('Hipertensión Arterial')
        if 'cardiaco' in query_lower or 'corazon' in query_lower:
            context.medical_history.append('Antecedentes cardiovasculares')
        
        return context
    
    async def generate_medical_response(self, query: str) -> str:
        """Generate comprehensive medical response using pure Kimi"""
        
        if not self.kimi_client:
            raise RuntimeError("MedeX not initialized. Use 'async with' context manager.")
        
        # Analyze query
        user_type = self.detect_user_type(query)
        urgency_level = self.detect_urgency_level(query)
        medical_context = self.extract_medical_context(query)
        
        # Convert medical context to dict for API
        context_dict = {
            "age": medical_context.age,
            "gender": medical_context.gender,
            "symptoms": medical_context.symptoms,
            "duration": medical_context.duration,
            "medical_history": medical_context.medical_history,
            "medications": medical_context.medications,
            "urgency_level": urgency_level,
            "user_type": user_type
        }
        
        # Generate response using real Kimi API
        response = await self.kimi_client.generate_medical_consultation(
            query=query,
            medical_context=context_dict,
            user_type=user_type,
            urgency_level=urgency_level
        )
        
        return response
    
    async def analyze_medical_image(self, image_data: bytes, context: str, user_type: str = None) -> str:
        """Analyze medical images using Kimi Vision"""
        
        if not self.kimi_client:
            raise RuntimeError("MedeX not initialized. Use 'async with' context manager.")
        
        if user_type is None:
            user_type = self.detect_user_type(context)
        
        response = await self.kimi_client.analyze_medical_image(
            image_data=image_data,
            clinical_context=context,
            user_type=user_type
        )
        
        return response
    
    async def test_system(self) -> Dict[str, Any]:
        """Test the pure Kimi system"""
        
        results = {
            "connection": False,
            "patient_response": False,
            "professional_response": False,
            "emergency_response": False,
            "errors": []
        }
        
        try:
            # Test basic connection
            if self.kimi_client:
                results["connection"] = await self.kimi_client.test_connection()
            
            if results["connection"]:
                # Test patient response
                try:
                    patient_response = await self.generate_medical_response(
                        "Me duele el pecho desde hace 2 horas"
                    )
                    results["patient_response"] = len(patient_response) > 0
                    results["patient_sample"] = patient_response[:200] + "..."
                except Exception as e:
                    results["errors"].append(f"Patient test: {e}")
                
                # Test professional response
                try:
                    pro_response = await self.generate_medical_response(
                        "Paciente de 55 años, diabético, con dolor precordial de 2 horas de evolución"
                    )
                    results["professional_response"] = len(pro_response) > 0
                    results["professional_sample"] = pro_response[:200] + "..."
                except Exception as e:
                    results["errors"].append(f"Professional test: {e}")
                
                # Test emergency detection
                try:
                    emergency_response = await self.generate_medical_response(
                        "Dolor torácico intenso con sudoración y dificultad respiratoria"
                    )
                    results["emergency_response"] = "emergencia" in emergency_response.lower()
                    results["emergency_sample"] = emergency_response[:200] + "..."
                except Exception as e:
                    results["errors"].append(f"Emergency test: {e}")
        
        except Exception as e:
            results["errors"].append(f"System error: {e}")
        
        return results

# Standalone testing function
async def test_pure_kimi_medex():
    """Test the pure Kimi MedeX system"""
    
    print("🧪 TESTING PURE KIMI MEDEX SYSTEM")
    print("=" * 60)
    
    api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
    
    async with PureKimiMedeX(api_key) as medex:
        results = await medex.test_system()
        
        print(f"📡 Connection: {'✅' if results['connection'] else '❌'}")
        print(f"👤 Patient Response: {'✅' if results['patient_response'] else '❌'}")
        print(f"👨‍⚕️ Professional Response: {'✅' if results['professional_response'] else '❌'}")
        print(f"🚨 Emergency Detection: {'✅' if results['emergency_response'] else '❌'}")
        
        if results.get('errors'):
            print(f"\n❌ Errors found:")
            for error in results['errors']:
                print(f"   - {error}")
        
        if results.get('patient_sample'):
            print(f"\n👤 Patient Sample:")
            print(f"   {results['patient_sample']}")
        
        if results.get('professional_sample'):
            print(f"\n👨‍⚕️ Professional Sample:")
            print(f"   {results['professional_sample']}")
        
        return results

if __name__ == "__main__":
    asyncio.run(test_pure_kimi_medex())