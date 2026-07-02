import unittest
import sys
import os

# Add the project root to sys.path so we can import app.py correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, apply_policy_rules

class TestCreditCardApproval(unittest.TestCase):

    def setUp(self):
        """Set up Flask test client and enable testing mode."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()

    # =========================================================================
    # UNIT TESTS FOR POLICY RULES ENGINE
    # =========================================================================
    
    def test_policy_income_floor(self):
        """Rule 1: Rejects applicants with income below the $15,000 floor."""
        # 14900 income, 30 age, 5 employment, working (0)
        reject, reason = apply_policy_rules(14900, 30, 5.0, 0)
        self.assertTrue(reject)
        self.assertIn("below the minimum required threshold", reason)

        # 15000 income, 30 age, 5 employment, working (0) - Should not trigger rule 1
        reject, reason = apply_policy_rules(15000, 30, 5.0, 0)
        # It shouldn't trigger any other policy rules either
        self.assertFalse(reject)

    def test_policy_unemployed_student(self):
        """Rule 2: Rejects student applicants with no employment history."""
        # Student (4), 0 years employment, age 20, income 25000
        reject, reason = apply_policy_rules(25000, 20, 0.0, 4)
        self.assertTrue(reject)
        self.assertIn("Student applicants with no employment history", reason)

        # Student (4), 1 year employment, age 20, income 25000 - Should not trigger rule 2
        reject, reason = apply_policy_rules(25000, 20, 1.0, 4)
        self.assertFalse(reject)

    def test_policy_underage_unemployed(self):
        """Rule 3: Rejects applicants aged 18 or younger with no employment history."""
        # age 18, 0 years employment, income 18000, working (0)
        reject, reason = apply_policy_rules(18000, 18, 0.0, 0)
        self.assertTrue(reject)
        self.assertIn("aged 18 or younger with no employment history", reason)

        # age 19, 0 years employment, income 18000, working (0) - Should not trigger rule 3
        reject, reason = apply_policy_rules(18000, 19, 0.0, 0)
        self.assertFalse(reject)

    def test_policy_low_income_student(self):
        """Rule 4: Rejects student applicants with annual income below $20,000."""
        # Student (4), 2 years employment, age 21, income 18000
        reject, reason = apply_policy_rules(18000, 21, 2.0, 4)
        self.assertTrue(reject)
        self.assertIn("Student applicants with an annual income below $20,000", reason)

        # Student (4), 2 years employment, age 21, income 21000 - Should not trigger rule 4
        reject, reason = apply_policy_rules(21000, 21, 2.0, 4)
        self.assertFalse(reject)

    # =========================================================================
    # INTEGRATION TESTS FOR WEB ENDPOINTS
    # =========================================================================

    def test_home_page_route(self):
        """Verify the underwriting home page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Automated Credit Card Decisioning System", response.data)

    def test_predict_endpoint_policy_reject(self):
        """Verify prediction endpoint returns REJECTED status when policy rules trigger."""
        payload = {
            'gender': '1',
            'own_car': '0',
            'own_realty': '0',
            'income_type': '4',          # Student
            'education': '1',
            'family_status': '2',
            'housing_type': '3',
            'occupation': '18',
            'annual_income': '12000',    # Below $15,000 floor
            'age': '18',
            'employment_days': '0',      # Unemployed student/youth
            'family_members': '1'
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        
        # Should be rejected
        self.assertIn(b"REJECTED", response.data)
        # Should explicitly print the policy reason
        self.assertIn(b"below the minimum required threshold of $15,000", response.data)

    def test_predict_endpoint_ml_approval(self):
        """Verify prediction endpoint returns APPROVED status for a stable, high-income profile."""
        payload = {
            'gender': '1',
            'own_car': '1',
            'own_realty': '1',
            'income_type': '1',          # Commercial associate
            'education': '0',            # Higher education
            'family_status': '1',        # Married
            'housing_type': '1',         # House
            'occupation': '10',          # Manager
            'annual_income': '100000',   # High income
            'age': '38',
            'employment_days': '8.5',    # Well employed
            'family_members': '3'
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        
        # High likelihood of approval
        self.assertIn(b"APPROVED", response.data)
        # No policy reject should be reported
        self.assertNotIn(b"Policy Hard Reject Triggered", response.data)

if __name__ == '__main__':
    unittest.main()
