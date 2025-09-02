#!/usr/bin/env python3
"""
Real Kimi/Moonshot Client Integration
Complete integration with Moonshot Kimi API for true medical AI
"""

import asyncio
import json
import aiohttp
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

@dataclass
class KimiRequest:
    """Structured request for Kimi API"""
    prompt: str
    system_prompt: str
    temperature: float = 0.3
    max_tokens: int = 2000
    model: str = "moonshot-v1-32k"
    stream: bool = False

@dataclass
class KimiResponse:
    """Structured response from Kimi API"""
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str
    timestamp: datetime

class RealKimiClient:
    """Real Moonshot Kimi API client for medical AI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.moonshot.ai/v1"
        self.models = {
            "text": "moonshot-v1-32k",
            "vision": "moonshot-v1-32k",  # Assuming multimodal capability
            "fast": "moonshot-v1-8k"
        }
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def generate_medical_response(self, 
                                       request: KimiRequest, 
                                       image_data: Optional[bytes] = None) -> KimiResponse:
        """Generate medical response using real Kimi API"""
        
        if not self.session:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        
        # Prepare messages for Kimi API
        messages = [
            {"role": "system", "content": request.system_prompt}
        ]
        
        # Handle text + image multimodal requests
        if image_data:
            # Convert image to base64 for multimodal processing
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            user_message = {
                "role": "user",
                "content": [
                    {"type": "text", "text": request.prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    }
                ]
            }
        else:
            # Text-only request
            user_message = {
                "role": "user", 
                "content": request.prompt
            }
        
        messages.append(user_message)
        
        # Prepare API request payload
        payload = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": request.stream
        }
        
        try:
            # Make API request to Moonshot
            async with self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    # Extract response content
                    choice = result["choices"][0]
                    content = choice["message"]["content"]
                    usage = result.get("usage", {})
                    
                    return KimiResponse(
                        content=content,
                        model=result["model"],
                        usage=usage,
                        finish_reason=choice.get("finish_reason", "stop"),
                        timestamp=datetime.now()
                    )
                
                else:
                    # Handle API errors
                    error_text = await response.text()
                    raise Exception(f"Kimi API Error {response.status}: {error_text}")
                    
        except Exception as e:
            raise Exception(f"Error communicating with Kimi API: {str(e)}")
    
    async def test_connection(self) -> bool:
        """Test connection to Kimi API"""
        
        test_request = KimiRequest(
            prompt="Test medical AI connection",
            system_prompt="You are a medical AI assistant. Respond briefly to confirm functionality.",
            max_tokens=50
        )
        
        try:
            response = await self.generate_medical_response(test_request)
            return len(response.content) > 0
        except Exception as e:
            print(f"❌ Kimi API connection test failed: {e}")
            return False
    
    async def analyze_medical_image(self, 
                                   image_data: bytes, 
                                   clinical_context: str,
                                   user_type: str = "professional") -> str:
        """Analyze medical image with Kimi Vision"""
        
        if user_type == "professional":
            system_prompt = """Eres un sistema de IA médica especializado en análisis de imágenes médicas.
Proporciona análisis técnico detallado para profesionales médicos, incluyendo:
- Hallazgos observables específicos
- Diagnósticos diferenciales
- Recomendaciones de estudios adicionales
- Correlación clínica necesaria

Usa terminología médica apropiada y incluye disclaimers sobre limitaciones del análisis por IA."""
            
            user_prompt = f"""Analiza esta imagen médica con el siguiente contexto clínico:

CONTEXTO CLÍNICO: {clinical_context}

Proporciona un análisis profesional detallado incluyendo:
1. Descripción de hallazgos observables
2. Posibles diagnósticos diferenciales
3. Correlación clínica recomendada
4. Estudios complementarios sugeridos

Recuerda incluir disclaimers apropiados sobre limitaciones del análisis por IA."""
        
        else:
            system_prompt = """Eres un sistema de IA médica que ayuda a pacientes a entender sus estudios médicos.
Proporciona explicaciones claras y comprensibles, evitando alarmar innecesariamente.
Enfatiza la importancia de consultar con el médico para interpretación completa."""
            
            user_prompt = f"""Ayuda a explicar esta imagen médica de manera comprensible:

CONTEXTO: {clinical_context}

Proporciona una explicación clara y tranquilizadora que incluya:
1. Qué tipo de estudio es
2. Qué se puede observar en términos generales
3. Importancia de consultar con el médico
4. Qué preguntas hacer al médico

Usa lenguaje simple y evita crear ansiedad innecesaria."""
        
        request = KimiRequest(
            prompt=user_prompt,
            system_prompt=system_prompt,
            model=self.models["vision"],
            temperature=0.2,  # Lower temperature for medical accuracy
            max_tokens=1500
        )
        
        response = await self.generate_medical_response(request, image_data)
        return response.content
    
    async def generate_medical_consultation(self,
                                          query: str,
                                          medical_context: Dict[str, Any],
                                          user_type: str,
                                          urgency_level: str) -> str:
        """Generate comprehensive medical consultation response"""
        
        # Prepare context-aware system prompt
        if user_type == "professional":
            system_prompt = f"""Eres un sistema de IA médica avanzada diseñado para asistir a profesionales de la salud.

PROTOCOLO DE RESPUESTA PROFESIONAL:
- Proporciona análisis clínico detallado con evidencia científica
- Incluye diagnósticos diferenciales con probabilidades estimadas
- Especifica protocolos de manejo y dosis farmacológicas exactas
- Cita guías clínicas y evidencia actual cuando sea relevante
- Indica criterios de derivación y seguimiento

NIVEL DE URGENCIA: {urgency_level.upper()}

Si es EMERGENCIA, activa protocolos de urgencia médica inmediatos.

INFORMACIÓN CONTEXTUAL DISPONIBLE:
{json.dumps(medical_context, indent=2)}

Responde con precisión técnica apropiada para profesionales médicos."""

        else:
            system_prompt = f"""Eres un sistema de IA médica diseñado para educar y orientar a pacientes.

PROTOCOLO DE RESPUESTA PARA PACIENTES:
- Usa lenguaje claro y comprensible
- Proporciona información educativa sin alarmar
- Enfatiza cuándo es importante buscar atención médica
- Incluye medidas de autocuidado apropiadas
- Mantén un tono empático y tranquilizador

NIVEL DE URGENCIA: {urgency_level.upper()}

Si es EMERGENCIA, proporciona instrucciones claras de acción inmediata.

CONTEXTO DEL PACIENTE:
{json.dumps(medical_context, indent=2)}

Responde de manera comprensible y útil para el paciente."""
        
        # Add urgency-specific instructions
        if urgency_level == "emergency":
            emergency_addition = """
🚨 PROTOCOLO DE EMERGENCIA ACTIVADO 🚨

INSTRUCCIONES CRÍTICAS:
- Evalúa si se requiere atención médica inmediata
- Proporciona pasos de acción específicos y claros
- Incluye cuándo llamar al 911
- No minimices síntomas potencialmente graves
"""
            system_prompt += emergency_addition
        
        request = KimiRequest(
            prompt=query,
            system_prompt=system_prompt,
            temperature=0.1 if urgency_level == "emergency" else 0.3,
            max_tokens=2000
        )
        
        response = await self.generate_medical_response(request)
        return response.content

# Utility functions for integration
async def test_kimi_integration(api_key: str) -> Dict[str, Any]:
    """Test complete Kimi integration"""
    
    results = {
        "connection": False,
        "text_generation": False,
        "error": None
    }
    
    try:
        async with RealKimiClient(api_key) as kimi:
            # Test basic connection
            results["connection"] = await kimi.test_connection()
            
            if results["connection"]:
                # Test medical consultation
                test_response = await kimi.generate_medical_consultation(
                    query="Test medical consultation functionality",
                    medical_context={"test": True},
                    user_type="professional",
                    urgency_level="routine"
                )
                
                results["text_generation"] = len(test_response) > 0
                results["sample_response"] = test_response[:200] + "..." if test_response else ""
    
    except Exception as e:
        results["error"] = str(e)
    
    return results

if __name__ == "__main__":
    # Test the Kimi client
    async def main():
        print("🧪 Testing Real Kimi Integration...")
        
        # Use the provided API key
        api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
        
        results = await test_kimi_integration(api_key)
        
        print(f"📡 Connection: {'✅' if results['connection'] else '❌'}")
        print(f"💬 Text Generation: {'✅' if results['text_generation'] else '❌'}")
        
        if results.get('error'):
            print(f"❌ Error: {results['error']}")
        
        if results.get('sample_response'):
            print(f"📝 Sample Response: {results['sample_response']}")
    
    asyncio.run(main())