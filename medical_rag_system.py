#!/usr/bin/env python3
"""
🔍 Medical RAG System - Sistema de Recuperación Aumentada por Generación Médica
Sistema vectorial avanzado para búsqueda semántica en conocimiento médico

Características:
- Vectorización semántica con sentence-transformers
- Búsqueda por similitud coseno
- Indexación de conocimiento médico
- Búsqueda contextual inteligente
- Cache de embeddings para eficiencia
"""

import numpy as np
import json
import pickle
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import asyncio

# Verificar e instalar dependencias
def check_and_install_dependencies():
    """Verifica e instala dependencias del RAG"""
    required_packages = [
        "sentence-transformers",
        "scikit-learn", 
        "numpy"
    ]
    
    import subprocess
    import sys
    
    for package in required_packages:
        try:
            if package == "sentence-transformers":
                import sentence_transformers
            elif package == "scikit-learn":
                import sklearn
            elif package == "numpy":
                import numpy
            print(f"✅ {package} ya está disponible")
        except ImportError:
            print(f"📦 Instalando {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
                print(f"✅ {package} instalado correctamente")
            except:
                print(f"❌ Error instalando {package}")
                return False
    return True

# Verificar dependencias
print("🔧 Verificando dependencias del sistema RAG...")
if not check_and_install_dependencies():
    print("❌ Error en dependencias. Saliendo...")
    exit(1)

# Importar después de verificar
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("✅ Dependencias RAG importadas correctamente")
except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
    print("💡 Intenta reiniciar el terminal y ejecutar de nuevo")
    exit(1)

from medical_knowledge_base import MedicalKnowledgeBase

@dataclass
class MedicalDocument:
    """Documento médico para RAG"""
    id: str
    title: str
    content: str
    category: str
    source: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None

@dataclass
class SearchResult:
    """Resultado de búsqueda RAG"""
    document: MedicalDocument
    similarity_score: float
    relevance_rank: int

class MedicalRAGSystem:
    """Sistema RAG médico avanzado"""
    
    def __init__(self, cache_dir: str = "./rag_cache"):
        self.cache_dir = cache_dir
        self.documents = {}
        self.embeddings_cache = {}
        self.knowledge_base = MedicalKnowledgeBase()
        
        # Crear directorio de cache
        os.makedirs(cache_dir, exist_ok=True)
        
        # Inicializar modelo de embeddings
        print("🧠 Inicializando modelo de embeddings médicos...")
        try:
            # Usar modelo optimizado para textos médicos/científicos
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Modelo de embeddings cargado correctamente")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            print("📦 Instalando modelo base...")
            try:
                self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
                print("✅ Modelo base cargado")
            except:
                print("❌ Error crítico con modelos de embeddings")
                raise
        
        # Vectorizador TF-IDF como fallback
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Inicializar con conocimiento base
        self._initialize_medical_knowledge()
    
    def _initialize_medical_knowledge(self):
        """Inicializa el sistema con conocimiento médico base"""
        print("📚 Indexando conocimiento médico base...")
        
        # Indexar condiciones médicas
        for code, condition in self.knowledge_base.conditions.items():
            doc = MedicalDocument(
                id=f"condition_{code}",
                title=condition.name,
                content=self._create_condition_text(condition),
                category="conditions",
                source="knowledge_base",
                metadata={
                    "icd10_code": condition.icd10_code,
                    "category": condition.category,
                    "emergency_signs": condition.emergency_signs
                }
            )
            self.add_document(doc)
        
        # Indexar medicamentos
        for name, medication in self.knowledge_base.medications.items():
            doc = MedicalDocument(
                id=f"medication_{name}",
                title=medication.name,
                content=self._create_medication_text(medication),
                category="medications",
                source="knowledge_base",
                metadata={
                    "generic_name": medication.generic_name,
                    "category": medication.category,
                    "pregnancy_category": medication.pregnancy_category
                }
            )
            self.add_document(doc)
        
        # Indexar protocolos
        for name, protocol in self.knowledge_base.protocols.items():
            doc = MedicalDocument(
                id=f"protocol_{name}",
                title=protocol.name,
                content=self._create_protocol_text(protocol),
                category="protocols",
                source="knowledge_base",
                metadata={
                    "category": protocol.category,
                    "evidence_level": protocol.evidence_level
                }
            )
            self.add_document(doc)
        
        # Indexar procedimientos
        for name, procedure in self.knowledge_base.procedures.items():
            doc = MedicalDocument(
                id=f"procedure_{name}",
                title=procedure.name,
                content=self._create_procedure_text(procedure),
                category="procedures",
                source="knowledge_base",
                metadata={
                    "category": procedure.category,
                    "cost_range": procedure.cost_range
                }
            )
            self.add_document(doc)
        
        print(f"✅ Indexados {len(self.documents)} documentos médicos")
    
    def _create_condition_text(self, condition) -> str:
        """Crea texto searchable para condición médica"""
        text_parts = [
            f"Condición médica: {condition.name}",
            f"Código ICD-10: {condition.icd10_code}",
            f"Categoría: {condition.category}",
            f"Descripción: {condition.description}",
            f"Síntomas: {', '.join(condition.symptoms)}",
            f"Factores de riesgo: {', '.join(condition.risk_factors)}",
            f"Complicaciones: {', '.join(condition.complications)}",
            f"Criterios diagnósticos: {', '.join(condition.diagnostic_criteria)}",
            f"Diagnóstico diferencial: {', '.join(condition.differential_diagnosis)}",
            f"Protocolo de tratamiento: {', '.join(condition.treatment_protocol)}",
            f"Signos de emergencia: {', '.join(condition.emergency_signs)}",
            f"Pronóstico: {condition.prognosis}",
            f"Seguimiento: {', '.join(condition.follow_up)}"
        ]
        return " ".join(text_parts)
    
    def _create_medication_text(self, medication) -> str:
        """Crea texto searchable para medicamento"""
        text_parts = [
            f"Medicamento: {medication.name}",
            f"Nombre genérico: {medication.generic_name}",
            f"Categoría: {medication.category}",
            f"Indicaciones: {', '.join(medication.indications)}",
            f"Contraindicaciones: {', '.join(medication.contraindications)}",
            f"Dosis adulto: {medication.dosage_adult}",
            f"Dosis pediátrica: {medication.dosage_pediatric}",
            f"Efectos secundarios: {', '.join(medication.side_effects)}",
            f"Interacciones: {', '.join(medication.interactions)}",
            f"Monitoreo: {', '.join(medication.monitoring)}",
            f"Categoría embarazo: {medication.pregnancy_category}"
        ]
        return " ".join(text_parts)
    
    def _create_protocol_text(self, protocol) -> str:
        """Crea texto searchable para protocolo"""
        text_parts = [
            f"Protocolo clínico: {protocol.name}",
            f"Categoría: {protocol.category}",
            f"Indicación: {protocol.indication}",
            f"Pasos: {', '.join(protocol.steps)}",
            f"Puntos de decisión: {', '.join(protocol.decision_points)}",
            f"Modificaciones de emergencia: {', '.join(protocol.emergency_modifications)}",
            f"Nivel de evidencia: {protocol.evidence_level}"
        ]
        return " ".join(text_parts)
    
    def _create_procedure_text(self, procedure) -> str:
        """Crea texto searchable para procedimiento"""
        text_parts = [
            f"Procedimiento diagnóstico: {procedure.name}",
            f"Categoría: {procedure.category}",
            f"Indicaciones: {', '.join(procedure.indications)}",
            f"Contraindicaciones: {', '.join(procedure.contraindications)}",
            f"Preparación: {', '.join(procedure.preparation)}",
            f"Pasos del procedimiento: {', '.join(procedure.procedure_steps)}",
            f"Interpretación: {', '.join(procedure.interpretation)}",
            f"Complicaciones: {', '.join(procedure.complications)}"
        ]
        return " ".join(text_parts)
    
    def add_document(self, document: MedicalDocument):
        """Añade documento al índice RAG"""
        self.documents[document.id] = document
        
        # Generar embedding
        try:
            embedding = self.embedding_model.encode(document.content)
            document.embedding = embedding
            
            # Cache embedding
            self.embeddings_cache[document.id] = embedding
            
        except Exception as e:
            print(f"⚠️ Error generando embedding para {document.id}: {e}")
    
    def search_similar_documents(self, query: str, 
                               top_k: int = 5,
                               category_filter: Optional[str] = None,
                               similarity_threshold: float = 0.1) -> List[SearchResult]:
        """Busca documentos similares usando embeddings"""
        
        try:
            # Generar embedding de la consulta
            query_embedding = self.embedding_model.encode(query)
            
            # Buscar documentos similares
            similarities = []
            
            for doc_id, document in self.documents.items():
                # Filtrar por categoría si se especifica
                if category_filter and document.category != category_filter:
                    continue
                
                if document.embedding is not None:
                    # Calcular similitud coseno
                    similarity = cosine_similarity(
                        query_embedding.reshape(1, -1),
                        document.embedding.reshape(1, -1)
                    )[0][0]
                    
                    if similarity >= similarity_threshold:
                        similarities.append((doc_id, similarity))
            
            # Ordenar por similitud descendente
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Crear resultados
            results = []
            for i, (doc_id, similarity) in enumerate(similarities[:top_k]):
                result = SearchResult(
                    document=self.documents[doc_id],
                    similarity_score=similarity,
                    relevance_rank=i + 1
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ Error en búsqueda semántica: {e}")
            return []
    
    def search_by_symptoms(self, symptoms: List[str], top_k: int = 5) -> List[SearchResult]:
        """Busca condiciones por síntomas específicos"""
        
        # Crear query de síntomas
        symptoms_query = f"síntomas: {', '.join(symptoms)}"
        
        # Buscar en condiciones médicas
        results = self.search_similar_documents(
            query=symptoms_query,
            top_k=top_k,
            category_filter="conditions"
        )
        
        return results
    
    def search_treatment_protocols(self, condition: str, top_k: int = 3) -> List[SearchResult]:
        """Busca protocolos de tratamiento para una condición"""
        
        treatment_query = f"tratamiento protocolo manejo {condition}"
        
        # Buscar en protocolos y condiciones
        protocol_results = self.search_similar_documents(
            query=treatment_query,
            top_k=top_k,
            category_filter="protocols"
        )
        
        condition_results = self.search_similar_documents(
            query=treatment_query,
            top_k=top_k,
            category_filter="conditions"
        )
        
        # Combinar resultados
        all_results = protocol_results + condition_results
        all_results.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return all_results[:top_k]
    
    def search_medication_info(self, medication_name: str, context: str = "") -> List[SearchResult]:
        """Busca información de medicamentos"""
        
        med_query = f"medicamento {medication_name} {context}"
        
        results = self.search_similar_documents(
            query=med_query,
            top_k=5,
            category_filter="medications"
        )
        
        return results
    
    def search_emergency_protocols(self, emergency_type: str) -> List[SearchResult]:
        """Busca protocolos de emergencia"""
        
        emergency_query = f"emergencia urgencia protocolo {emergency_type}"
        
        # Buscar en todas las categorías
        results = self.search_similar_documents(
            query=emergency_query,
            top_k=5
        )
        
        # Filtrar documentos con información de emergencia
        emergency_results = []
        for result in results:
            doc = result.document
            if (hasattr(doc.metadata, 'emergency_signs') and doc.metadata.get('emergency_signs')) or \
               'emergencia' in doc.content.lower() or \
               'urgencia' in doc.content.lower():
                emergency_results.append(result)
        
        return emergency_results[:3]
    
    def get_contextual_information(self, query: str, 
                                 user_type: str = "patient",
                                 urgency_level: str = "routine") -> Dict[str, Any]:
        """Obtiene información contextual para una consulta"""
        
        # Búsqueda general
        general_results = self.search_similar_documents(query, top_k=5)
        
        # Búsquedas específicas basadas en urgencia
        emergency_results = []
        if urgency_level == "emergency":
            emergency_results = self.search_emergency_protocols(query)
        
        # Formatear resultados según tipo de usuario
        formatted_results = self._format_results_for_user(
            general_results, 
            user_type,
            urgency_level
        )
        
        return {
            "general_results": formatted_results,
            "emergency_results": emergency_results,
            "total_documents": len(self.documents),
            "search_query": query,
            "user_type": user_type,
            "urgency_level": urgency_level
        }
    
    def _format_results_for_user(self, results: List[SearchResult], 
                               user_type: str, 
                               urgency_level: str) -> List[Dict[str, Any]]:
        """Formatea resultados según el tipo de usuario"""
        
        formatted = []
        for result in results:
            doc = result.document
            
            # Información base
            info = {
                "title": doc.title,
                "category": doc.category,
                "similarity_score": result.similarity_score,
                "source": doc.source
            }
            
            # Adaptar contenido según usuario
            if user_type == "professional":
                info.update({
                    "full_content": doc.content,
                    "metadata": doc.metadata,
                    "technical_details": True
                })
            else:
                # Para pacientes, simplificar información
                info.update({
                    "simplified_content": self._simplify_content_for_patient(doc.content),
                    "patient_friendly": True
                })
            
            # Marcar información de emergencia
            if urgency_level == "emergency":
                info["emergency_relevant"] = self._is_emergency_relevant(doc)
            
            formatted.append(info)
        
        return formatted
    
    def _simplify_content_for_patient(self, content: str) -> str:
        """Simplifica contenido técnico para pacientes"""
        
        # Extraer información más relevante para pacientes
        patient_keywords = [
            "síntomas", "signos", "cuidado", "tratamiento básico",
            "cuándo consultar", "prevención", "factores de riesgo"
        ]
        
        simplified_parts = []
        for line in content.split('.'):
            for keyword in patient_keywords:
                if keyword in line.lower():
                    simplified_parts.append(line.strip())
                    break
        
        if simplified_parts:
            return '. '.join(simplified_parts[:3])  # Máximo 3 puntos clave
        else:
            return content[:200] + "..."  # Fallback a primeros 200 caracteres
    
    def _is_emergency_relevant(self, document: MedicalDocument) -> bool:
        """Determina si un documento es relevante para emergencias"""
        
        emergency_keywords = [
            "emergencia", "urgencia", "crítico", "grave", "inmediato",
            "shock", "paro", "convulsiones", "sangrado", "dolor severo"
        ]
        
        content_lower = document.content.lower()
        for keyword in emergency_keywords:
            if keyword in content_lower:
                return True
        
        return False
    
    def save_index(self, filepath: str = None):
        """Guarda el índice RAG en disco"""
        
        if filepath is None:
            filepath = os.path.join(self.cache_dir, "rag_index.pkl")
        
        try:
            save_data = {
                "documents": self.documents,
                "embeddings_cache": self.embeddings_cache,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(save_data, f)
            
            print(f"✅ Índice RAG guardado en {filepath}")
            
        except Exception as e:
            print(f"❌ Error guardando índice: {e}")
    
    def load_index(self, filepath: str = None):
        """Carga el índice RAG desde disco"""
        
        if filepath is None:
            filepath = os.path.join(self.cache_dir, "rag_index.pkl")
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    save_data = pickle.load(f)
                
                self.documents = save_data["documents"]
                self.embeddings_cache = save_data["embeddings_cache"]
                
                print(f"✅ Índice RAG cargado desde {filepath}")
                print(f"📚 {len(self.documents)} documentos cargados")
                
            else:
                print(f"⚠️ Archivo de índice no encontrado: {filepath}")
                
        except Exception as e:
            print(f"❌ Error cargando índice: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema RAG"""
        
        category_counts = {}
        for doc in self.documents.values():
            category = doc.category
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_documents": len(self.documents),
            "categories": category_counts,
            "embeddings_cached": len(self.embeddings_cache),
            "model_name": self.embedding_model.get_sentence_embedding_dimension() if hasattr(self.embedding_model, 'get_sentence_embedding_dimension') else "Unknown",
            "cache_directory": self.cache_dir
        }

# Función de prueba del sistema RAG
def test_rag_system():
    """Prueba el sistema RAG médico"""
    
    print("🧪 PROBANDO SISTEMA RAG MÉDICO")
    print("=" * 60)
    
    # Inicializar sistema
    rag = MedicalRAGSystem()
    
    # Prueba 1: Búsqueda por síntomas
    print("\n🔍 PRUEBA 1: Búsqueda por síntomas")
    print("-" * 40)
    
    symptoms = ["dolor torácico", "disnea"]
    results = rag.search_by_symptoms(symptoms)
    
    print(f"Síntomas: {symptoms}")
    for i, result in enumerate(results[:3], 1):
        print(f"{i}. {result.document.title} (similitud: {result.similarity_score:.3f})")
    
    # Prueba 2: Búsqueda de protocolos de tratamiento
    print("\n🔍 PRUEBA 2: Protocolos de tratamiento")
    print("-" * 40)
    
    treatment_results = rag.search_treatment_protocols("hipertensión")
    for i, result in enumerate(treatment_results[:3], 1):
        print(f"{i}. {result.document.title} (similitud: {result.similarity_score:.3f})")
    
    # Prueba 3: Información de medicamentos
    print("\n🔍 PRUEBA 3: Información de medicamentos")
    print("-" * 40)
    
    med_results = rag.search_medication_info("aspirina", "dolor")
    for i, result in enumerate(med_results[:3], 1):
        print(f"{i}. {result.document.title} (similitud: {result.similarity_score:.3f})")
    
    # Prueba 4: Información contextual
    print("\n🔍 PRUEBA 4: Información contextual")
    print("-" * 40)
    
    context_info = rag.get_contextual_information(
        "dolor de cabeza severo", 
        user_type="patient",
        urgency_level="urgent"
    )
    
    print(f"Query: {context_info['search_query']}")
    print(f"Resultados encontrados: {len(context_info['general_results'])}")
    
    # Estadísticas
    print("\n📊 ESTADÍSTICAS DEL SISTEMA")
    print("-" * 40)
    
    stats = rag.get_statistics()
    print(f"Total documentos: {stats['total_documents']}")
    print(f"Categorías: {stats['categories']}")
    print(f"Embeddings en cache: {stats['embeddings_cached']}")
    
    # Guardar índice
    rag.save_index()
    
    print("\n✅ Pruebas del sistema RAG completadas")

if __name__ == "__main__":
    test_rag_system()