# Example usage
def main():
  # Initialize the engine
  visa_engine = VisaApplicationEngine()

  # Sample application data
  application_data = {
      'age': 30,
      'income': 45000,
      'travel_history': ['UK', 'France'],
      'bank_balance': 15000,
      'employment_duration': 5,
      'previous_rejections': 0,
      'has_previous_visa': True,
      'has_property': True,
      'has_strong_ties': True,
      'documents': {
          'passport': {
              'expiry_date': '2025-12-31',
              'issue_date': '2020-01-01',
              'nationality': 'India'
          },
          'financial': {
              'bank_statements': True,
              'income_proof': True
          },
          'purpose': {
              'invitation_letter': True,
              'travel_itinerary': True
          },
          'personal': {
              'employment_status': 'Employed',
              'travel_history': True
          }
      }
  }

  # Get prediction
  result = visa_engine.predict_approval_probability(application_data)

  # Print results
  print("\nVisa Application Analysis Results:")
  print("==================================")
  print(f"Status: {result['status']}")
  print(f"Approval Probability: {result['probability']}%")
  print(f"Risk Score: {result['risk_score']}%")

  if result['recommendations']:
      print("\nRecommendations:")
      for rec in result['recommendations']:
          print(f"- {rec}")

if __name__ == "__main__":
  main()