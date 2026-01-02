"""
Testing and Validation Script
Compares generated tickets against expected classifications
"""

import pandas as pd
import os
from datetime import datetime


class SystemValidator:
    """Validates system output against expected results"""
    
    def __init__(self):
        self.expected_df = None
        self.generated_df = None
        self.results = {
            'total_items': 0,
            'correct_categories': 0,
            'correct_priorities': 0,
            'category_accuracy': 0.0,
            'priority_accuracy': 0.0,
            'details': []
        }
    
    def load_data(self):
        """Load expected and generated data"""
        try:
            self.expected_df = pd.read_csv('expected_classifications.csv')
            print(f"✅ Loaded {len(self.expected_df)} expected classifications")
            
            if not os.path.exists('generated_tickets.csv'):
                print("❌ generated_tickets.csv not found")
                print("Run the system first: python feedback_analysis_system.py")
                return False
            
            self.generated_df = pd.read_csv('generated_tickets.csv')
            print(f"✅ Loaded {len(self.generated_df)} generated tickets")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def extract_category_from_result(self, result_text):
        """Extract category from processing result"""
        result_lower = result_text.lower()
        
        if 'bug' in result_lower:
            return 'Bug'
        elif 'feature request' in result_lower or 'feature' in result_lower:
            return 'Feature Request'
        elif 'praise' in result_lower:
            return 'Praise'
        elif 'complaint' in result_lower:
            return 'Complaint'
        elif 'spam' in result_lower:
            return 'Spam'
        else:
            return 'Unknown'
    
    def extract_priority_from_result(self, result_text):
        """Extract priority from processing result"""
        result_lower = result_text.lower()
        
        if 'critical' in result_lower:
            return 'Critical'
        elif 'high' in result_lower:
            return 'High'
        elif 'medium' in result_lower:
            return 'Medium'
        elif 'low' in result_lower:
            return 'Low'
        else:
            return 'Unknown'
    
    def validate(self):
        """Validate generated tickets against expected results"""
        
        if not self.load_data():
            return
        
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60 + "\n")
        
        matched_items = 0
        
        for _, expected_row in self.expected_df.iterrows():
            source_id = expected_row['source_id']
            expected_category = expected_row['category']
            expected_priority = expected_row['priority']
            
            # Find corresponding generated ticket
            generated_row = self.generated_df[self.generated_df['source_id'] == source_id]
            
            if generated_row.empty:
                print(f"⚠️  {source_id}: Not processed")
                self.results['details'].append({
                    'source_id': source_id,
                    'status': 'Not processed',
                    'category_match': False,
                    'priority_match': False
                })
                continue
            
            matched_items += 1
            result_text = generated_row.iloc[0]['processing_result']
            
            # Extract category and priority from result
            generated_category = self.extract_category_from_result(result_text)
            generated_priority = self.extract_priority_from_result(result_text)
            
            # Compare
            category_match = generated_category == expected_category
            priority_match = generated_priority == expected_priority
            
            if category_match:
                self.results['correct_categories'] += 1
            
            if priority_match:
                self.results['correct_priorities'] += 1
            
            # Print result
            status_icon = "✅" if (category_match and priority_match) else "⚠️"
            print(f"{status_icon} {source_id}:")
            print(f"   Category: {generated_category} (expected: {expected_category}) {'✓' if category_match else '✗'}")
            print(f"   Priority: {generated_priority} (expected: {expected_priority}) {'✓' if priority_match else '✗'}")
            print()
            
            self.results['details'].append({
                'source_id': source_id,
                'expected_category': expected_category,
                'generated_category': generated_category,
                'category_match': category_match,
                'expected_priority': expected_priority,
                'generated_priority': generated_priority,
                'priority_match': priority_match,
                'status': 'Match' if (category_match and priority_match) else 'Mismatch'
            })
        
        # Calculate accuracy
        self.results['total_items'] = matched_items
        if matched_items > 0:
            self.results['category_accuracy'] = (self.results['correct_categories'] / matched_items) * 100
            self.results['priority_accuracy'] = (self.results['correct_priorities'] / matched_items) * 100
        
        # Print summary
        print("="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total Items Validated: {matched_items}")
        print(f"Category Accuracy: {self.results['category_accuracy']:.1f}%")
        print(f"Priority Accuracy: {self.results['priority_accuracy']:.1f}%")
        print(f"Overall Success: {self.results['correct_categories']} correct categories, {self.results['correct_priorities']} correct priorities")
        print("="*60 + "\n")
        
        # Save validation report
        self.save_report()
    
    def save_report(self):
        """Save validation report to CSV"""
        try:
            details_df = pd.DataFrame(self.results['details'])
            report_filename = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            details_df.to_csv(report_filename, index=False)
            print(f"📊 Validation report saved to: {report_filename}")
            
            # Save summary
            summary = {
                'timestamp': [datetime.now().isoformat()],
                'total_items': [self.results['total_items']],
                'correct_categories': [self.results['correct_categories']],
                'correct_priorities': [self.results['correct_priorities']],
                'category_accuracy': [f"{self.results['category_accuracy']:.2f}%"],
                'priority_accuracy': [f"{self.results['priority_accuracy']:.2f}%"]
            }
            summary_df = pd.DataFrame(summary)
            summary_filename = f"validation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            summary_df.to_csv(summary_filename, index=False)
            print(f"📊 Summary saved to: {summary_filename}")
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("SYSTEM VALIDATION TOOL")
    print("="*60 + "\n")
    
    validator = SystemValidator()
    validator.validate()


if __name__ == "__main__":
    main()
