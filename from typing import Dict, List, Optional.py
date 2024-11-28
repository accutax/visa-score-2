from typing import Dict, List, Optional
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

class VisaApplicationEngine:
  def __init__(self):
      self.model = None
      self.scaler = StandardScaler()
      self.required_documents = {
          'passport': ['expiry_date', 'issue_date', 'nationality'],
          'financial': ['bank_statements', 'income_proof'],
          'purpose': ['invitation_letter', 'travel_itinerary'],
          'personal': ['employment_status', 'travel_history']
      }

  def validate_documents(self, documents: Dict) -> tuple[bool, List[str]]:
      """Validates if all required documents are present"""
      missing_docs = []
      for category, required in self.required_documents.items():
          if category not in documents:
              missing_docs.extend(required)
          else:
              for doc in required:
                  if doc not in documents[category]:
                      missing_docs.append(doc)
      return len(missing_docs) == 0, missing_docs

  def extract_features(self, application_data: Dict) -> pd.DataFrame:
      """Extract relevant features from application data"""
      features = {
          'age': application_data.get('age', 0),
          'income': application_data.get('income', 0),
          'travel_history_count': len(application_data.get('travel_history', [])),
          'bank_balance': application_data.get('bank_balance', 0),
          'employment_duration': application_data.get('employment_duration', 0),
          'previous_visa_rejections': application_data.get('previous_rejections', 0),
      }
      return pd.DataFrame([features])

  def calculate_risk_score(self, features: pd.DataFrame) -> float:
      """Calculate risk score based on features"""
      risk_factors = {
          'low_income': features['income'].iloc[0] < 30000,
          'no_travel_history': features['travel_history_count'].iloc[0] == 0,
          'previous_rejections': features['previous_visa_rejections'].iloc[0] > 0,
          'low_bank_balance': features['bank_balance'].iloc[0] < 5000,
      }
      risk_score = sum(risk_factors.values()) / len(risk_factors)
      return risk_score

  def predict_approval_probability(self, application_data: Dict) -> Dict:
      """Predict visa approval probability"""
      # Validate documents
      docs_valid, missing_docs = self.validate_documents(application_data.get('documents', {}))
      if not docs_valid:
          return {
              'status': 'incomplete',
              'missing_documents': missing_docs,
              'probability': 0.0
          }

      # Extract features
      features = self.extract_features(application_data)

      # Calculate risk score
      risk_score = self.calculate_risk_score(features)

      # Calculate base probability
      base_probability = 1.0 - risk_score

      # Adjust probability based on specific factors
      adjustments = self._calculate_adjustments(application_data)
      final_probability = min(max(base_probability + adjustments, 0.0), 1.0)

      return {
          'status': 'complete',
          'probability': round(final_probability * 100, 2),
          'risk_score': round(risk_score * 100, 2),
          'recommendations': self._generate_recommendations(final_probability, application_data)
      }

  def _calculate_adjustments(self, application_data: Dict) -> float:
      """Calculate probability adjustments based on specific factors"""
      adjustments = 0.0

      # Positive adjustments
      if application_data.get('has_previous_visa', False):
          adjustments += 0.1
      if application_data.get('has_property', False):
          adjustments += 0.05
      if application_data.get('has_strong_ties', False):
          adjustments += 0.1

      # Negative adjustments
      if application_data.get('previous_overstay', False):
          adjustments -= 0.2
      if application_data.get('criminal_record', False):
          adjustments -= 0.3

      return adjustments

  def _generate_recommendations(self, probability: float, application_data: Dict) -> List[str]:
      """Generate recommendations based on probability and application data"""
      recommendations = []

      if probability < 0.5:
          if application_data.get('income', 0) < 30000:
              recommendations.append("Consider providing additional proof of financial stability")
          if not application_data.get('has_strong_ties', False):
              recommendations.append("Strengthen documentation of ties to home country")
          if application_data.get('travel_history', []) == []:
              recommendations.append("Include detailed travel itinerary and purpose of visit")

      return recommendations