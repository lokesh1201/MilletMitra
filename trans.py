import pandas as pd
import requests
from googletrans import Translator
from fuzzywuzzy import fuzz, process
import time
import logging
import re
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedFoodDataProcessor:
    def __init__(self):
        self.translator = Translator()
        
        # Comprehensive food database with nutritional benefits
        self.food_database = {
            # Millets
            'సామలు': {
                'english': 'Little Millet', 'hindi': 'कुटकी', 'tamil': 'சாமை', 'kannada': 'ಸಾವೆ',
                'category': 'Millet', 'type': 'Ancient Grain',
                'benefits': ['High in fiber', 'Gluten-free', 'Rich in iron', 'Good for diabetes', 'Weight management'],
                'nutrition': {'protein': '7.7g', 'fiber': '7.6g', 'iron': '9.3mg', 'calcium': '17mg'}
            },
            'రాగులు': {
                'english': 'Finger Millet', 'hindi': 'रागी', 'tamil': 'கேழ்வரகு', 'kannada': 'ರಾಗಿ',
                'category': 'Millet', 'type': 'Ancient Grain',
                'benefits': ['High calcium', 'Rich in amino acids', 'Good for bones', 'Natural relaxant', 'Anti-aging'],
                'nutrition': {'protein': '7.3g', 'fiber': '3.6g', 'calcium': '344mg', 'iron': '3.9mg'}
            },
            'వరగు': {
                'english': 'Proso Millet', 'hindi': 'चीना', 'tamil': 'வரகு', 'kannada': 'ವರಗು',
                'category': 'Millet', 'type': 'Ancient Grain',
                'benefits': ['Easy to digest', 'Low glycemic index', 'Antioxidant properties', 'Heart healthy'],
                'nutrition': {'protein': '11.0g', 'fiber': '8.5g', 'magnesium': '153mg', 'phosphorus': '206mg'}
            },
            'కొర్రలు': {
                'english': 'Foxtail Millet', 'hindi': 'कंगनी', 'tamil': 'தினை', 'kannada': 'ನವಣೆ',
                'category': 'Millet', 'type': 'Ancient Grain',
                'benefits': ['Blood sugar control', 'Heart health', 'Weight loss', 'Rich in protein'],
                'nutrition': {'protein': '12.3g', 'fiber': '8.0g', 'iron': '2.8mg', 'zinc': '2.4mg'}
            },
            'అరికేలు': {
                'english': 'Kodo Millet', 'hindi': 'कोदो', 'tamil': 'வரகு', 'kannada': 'ಹಾರಕ',
                'category': 'Millet', 'type': 'Ancient Grain',
                'benefits': ['High antioxidants', 'Reduces cholesterol', 'Good for liver', 'Anti-diabetic'],
                'nutrition': {'protein': '8.3g', 'fiber': '9.0g', 'iron': '0.5mg', 'calcium': '27mg'}
            },
            'బజ్రా': {
                'english': 'Pearl Millet', 'hindi': 'बाजरा', 'tamil': 'கம்பு', 'kannada': 'ಸಜ್ಜೆ',
                'category': 'Millet', 'type': 'Ancient Grain',
                'benefits': ['High energy', 'Rich in iron', 'Prevents anemia', 'Good for heart'],
                'nutrition': {'protein': '11.6g', 'fiber': '1.2g', 'iron': '8.0mg', 'magnesium': '137mg'}
            },
            
            # Pulses/Dals
            'కంది పప్పు': {
                'english': 'Toor Dal', 'hindi': 'तूर दाल', 'tamil': 'துவரம் பருப்பு', 'kannada': 'ತೊಗರಿ ಬೇಳೆ',
                'category': 'Pulse', 'type': 'Legume',
                'benefits': ['High protein', 'Rich in folate', 'Heart healthy', 'Lowers cholesterol', 'Good for digestion'],
                'nutrition': {'protein': '22.3g', 'fiber': '15.5g', 'folate': '449mcg', 'potassium': '1392mg'}
            },
            'పెసర పప్పు': {
                'english': 'Moong Dal', 'hindi': 'मूंग दाल', 'tamil': 'பயத்தம் பருப்பு', 'kannada': 'ಹೆಸರು ಕಾಳು',
                'category': 'Pulse', 'type': 'Legume',
                'benefits': ['Easy to digest', 'Cooling effect', 'Rich in antioxidants', 'Weight loss', 'Skin health'],
                'nutrition': {'protein': '24.0g', 'fiber': '16.3g', 'folate': '625mcg', 'magnesium': '189mg'}
            },
            'మినప పప్పు': {
                'english': 'Urad Dal', 'hindi': 'उड़द दाल', 'tamil': 'உழுந்து', 'kannada': 'ಮಾಷ್ ಪರಿಪ್ಪು',
                'category': 'Pulse', 'type': 'Legume',
                'benefits': ['High protein', 'Good for bones', 'Improves digestion', 'Boosts energy', 'Rich in iron'],
                'nutrition': {'protein': '25.2g', 'fiber': '18.3g', 'iron': '7.6mg', 'calcium': '138mg'}
            },
            'శనగ పప్పు': {
                'english': 'Chana Dal', 'hindi': 'चना दाल', 'tamil': 'கடலை பருப்பு', 'kannada': 'ಕಡಲೆ ಕಾಳು',
                'category': 'Pulse', 'type': 'Legume',
                'benefits': ['High fiber', 'Blood sugar control', 'Heart health', 'Weight management', 'Rich in protein'],
                'nutrition': {'protein': '20.1g', 'fiber': '30.5g', 'folate': '557mcg', 'manganese': '1.7mg'}
            },
            'మసూర పప్పు': {
                'english': 'Masoor Dal', 'hindi': 'मसूर दाल', 'tamil': 'மசூர் பருப்பு', 'kannada': 'ಮಸೂರ್ ದಾಲ್',
                'category': 'Pulse', 'type': 'Legume',
                'benefits': ['High protein', 'Rich in iron', 'Good for heart', 'Weight loss', 'Improves immunity'],
                'nutrition': {'protein': '25.8g', 'fiber': '11.5g', 'iron': '6.6mg', 'folate': '479mcg'}
            },
            
            # Grains
            'గోధుమ': {
                'english': 'Wheat', 'hindi': 'गेहूं', 'tamil': 'கோதுமை', 'kannada': 'ಗೋಧಿ',
                'category': 'Grain', 'type': 'Cereal',
                'benefits': ['High fiber', 'Good for digestion', 'Energy source', 'B vitamins', 'Heart health'],
                'nutrition': {'protein': '11.8g', 'fiber': '12.2g', 'iron': '5.4mg', 'zinc': '4.2mg'}
            },
            'బియ్యం': {
                'english': 'Rice', 'hindi': 'चावल', 'tamil': 'அரிசி', 'kannada': 'ಅಕ್ಕಿ',
                'category': 'Grain', 'type': 'Cereal',
                'benefits': ['Easy to digest', 'Gluten-free', 'Energy source', 'Low sodium', 'Quick energy'],
                'nutrition': {'protein': '6.8g', 'fiber': '0.4g', 'thiamine': '0.07mg', 'niacin': '1.6mg'}
            },
            'క్వినోవా': {
                'english': 'Quinoa', 'hindi': 'क्विनोआ', 'tamil': 'க்வினோவா', 'kannada': 'ಕ್ವಿನೋವಾ',
                'category': 'Grain', 'type': 'Pseudocereal',
                'benefits': ['Complete protein', 'Gluten-free', 'High fiber', 'Rich in minerals', 'Antioxidants'],
                'nutrition': {'protein': '14.1g', 'fiber': '7.0g', 'iron': '4.6mg', 'magnesium': '197mg'}
            },
            'వోట్స్': {
                'english': 'Oats', 'hindi': 'ओट्स', 'tamil': 'ஓட்ஸ்', 'kannada': 'ಓಟ್ಸ್',
                'category': 'Grain', 'type': 'Cereal',
                'benefits': ['Lowers cholesterol', 'Heart health', 'Weight management', 'Stable blood sugar', 'High fiber'],
                'nutrition': {'protein': '16.9g', 'fiber': '10.6g', 'manganese': '4.9mg', 'phosphorus': '523mg'}
            },
            
            # Spices & Seeds
            'మెంతులు': {
                'english': 'Fenugreek', 'hindi': 'मेथी', 'tamil': 'வெந்தயம்', 'kannada': 'ಮೆಂತ್ಯ',
                'category': 'Spice', 'type': 'Seed',
                'benefits': ['Blood sugar control', 'Digestive health', 'Anti-inflammatory', 'Cholesterol reduction'],
                'nutrition': {'protein': '23.0g', 'fiber': '24.6g', 'iron': '33.5mg', 'magnesium': '191mg'}
            },
            'జిలకర్ర': {
                'english': 'Cumin', 'hindi': 'जीरा', 'tamil': 'சீரகம்', 'kannada': 'ಜೀರಿಗೆ',
                'category': 'Spice', 'type': 'Seed',
                'benefits': ['Improves digestion', 'Rich in iron', 'Antioxidant properties', 'Weight loss'],
                'nutrition': {'protein': '17.8g', 'fiber': '10.5g', 'iron': '66.4mg', 'calcium': '931mg'}
            },
            'నువ్వులు': {
                'english': 'Sesame Seeds', 'hindi': 'तिल', 'tamil': 'எள்', 'kannada': 'ಎಳ್ಳು',
                'category': 'Seeds', 'type': 'Oilseed',
                'benefits': ['High calcium', 'Healthy fats', 'Bone health', 'Heart health', 'Skin health'],
                'nutrition': {'protein': '17.7g', 'fiber': '11.8g', 'calcium': '975mg', 'magnesium': '351mg'}
            },
            'చియా సీడ్స్': {
                'english': 'Chia Seeds', 'hindi': 'चिया सीड', 'tamil': 'சியா விதைகள்', 'kannada': 'ಚಿಯಾ ಬೀಜಗಳು',
                'category': 'Seeds', 'type': 'Superfood',
                'benefits': ['Omega-3 fatty acids', 'High fiber', 'Protein rich', 'Antioxidants', 'Weight management'],
                'nutrition': {'protein': '16.5g', 'fiber': '34.4g', 'omega3': '17.8g', 'calcium': '631mg'}
            }
        }
        
        # Phonetic mapping for search
        self.phonetic_mappings = {
            'samalu': 'సామలు', 'ragulu': 'రాగులు', 'varagu': 'వరగు', 'korralu': 'కొర్రలు',
            'arikelu': 'అరికేలు', 'bajra': 'బజ్రా', 'kandi pappu': 'కంది పప్పు',
            'pesara pappu': 'పెసర పప్పు', 'minapa pappu': 'మినప పప్పు',
            'shanaga pappu': 'శనగ పప్పు', 'masoor pappu': 'మసూర పప్పు',
            'godhuma': 'గోధుమ', 'biyyam': 'బియ్యం', 'quinoa': 'క్వినోవా',
            'oats': 'వోట్స్', 'menthulu': 'మెంతులు', 'jilakarra': 'జిలకర్ర',
            'nuvvulu': 'నువ్వులు', 'chia seeds': 'చియా సీడ్స్'
        }

    def search_food_item(self, query):
        """Search for food item by any name (English, Telugu, Hindi, phonetic)"""
        query = query.lower().strip()
        results = []
        
        # Direct search in database
        for telugu_name, data in self.food_database.items():
            # Check all possible matches
            if (query in data['english'].lower() or 
                query in data['hindi'] or 
                query in telugu_name or
                query in str(data.get('tamil', '')).lower() or
                query in str(data.get('kannada', '')).lower()):
                results.append((telugu_name, data))
        
        # Phonetic search
        for phonetic, telugu in self.phonetic_mappings.items():
            if query in phonetic and telugu in self.food_database:
                if (telugu, self.food_database[telugu]) not in results:
                    results.append((telugu, self.food_database[telugu]))
        
        # Fuzzy search if no exact matches
        if not results:
            all_names = []
            for telugu_name, data in self.food_database.items():
                all_names.extend([data['english'].lower(), telugu_name, data['hindi']])
            
            fuzzy_matches = process.extract(query, all_names, limit=3, scorer=fuzz.ratio)
            for match, score in fuzzy_matches:
                if score > 70:  # 70% similarity threshold
                    for telugu_name, data in self.food_database.items():
                        if (match in [data['english'].lower(), telugu_name, data['hindi']] and
                            (telugu_name, data) not in results):
                            results.append((telugu_name, data))
        
        return results

    def get_food_info(self, food_name):
        """Get comprehensive information about a food item"""
        results = self.search_food_item(food_name)
        
        if not results:
            return {"error": f"No information found for '{food_name}'"}
        
        food_info = []
        for telugu_name, data in results:
            info = {
                "telugu": telugu_name,
                "english": data['english'],
                "hindi": data['hindi'],
                "tamil": data.get('tamil', 'N/A'),
                "kannada": data.get('kannada', 'N/A'),
                "category": data['category'],
                "type": data['type'],
                "health_benefits": data['benefits'],
                "nutrition_per_100g": data['nutrition'],
                "retail_display": f"{data['english']} - {data['hindi']} - {telugu_name}"
            }
            food_info.append(info)
        
        return food_info

    def get_category_foods(self, category):
        """Get all foods in a specific category"""
        category_foods = []
        for telugu_name, data in self.food_database.items():
            if data['category'].lower() == category.lower():
                category_foods.append({
                    "telugu": telugu_name,
                    "english": data['english'],
                    "hindi": data['hindi'],
                    "benefits": data['benefits'][:3]  # Show top 3 benefits
                })
        return category_foods

    def create_nutrition_comparison(self, food_names):
        """Compare nutrition of multiple foods"""
        comparison = []
        for food_name in food_names:
            results = self.search_food_item(food_name)
            if results:
                telugu_name, data = results[0]
                comparison.append({
                    "name": data['english'],
                    "nutrition": data['nutrition']
                })
        return comparison

    def generate_meal_suggestions(self, dietary_preference="balanced"):
        """Generate meal suggestions based on dietary preferences"""
        suggestions = {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
            "snacks": []
        }
        
        if dietary_preference.lower() == "diabetic":
            # Low glycemic index foods
            breakfast_foods = ['రాగులు', 'వరగు', 'వోట్స్']
            lunch_foods = ['కంది పప్పు', 'పెసర పప్పు', 'సామలు']
            
        elif dietary_preference.lower() == "weight_loss":
            # High fiber, low calorie foods
            breakfast_foods = ['వోట్స్', 'రాగులు', 'చియా సీడ్స్']
            lunch_foods = ['పెసర పప్పు', 'క్వినోవా', 'సామలు']
            
        else:  # balanced
            breakfast_foods = ['వోట్స్', 'రాగులు', 'గోధుమ']
            lunch_foods = ['కంది పప్పు', 'బియ్యం', 'కొర్రలు']
        
        for food in breakfast_foods:
            if food in self.food_database:
                suggestions["breakfast"].append({
                    "english": self.food_database[food]['english'],
                    "telugu": food,
                    "benefits": self.food_database[food]['benefits'][:2]
                })
        
        for food in lunch_foods:
            if food in self.food_database:
                suggestions["lunch"].append({
                    "english": self.food_database[food]['english'],
                    "telugu": food,
                    "benefits": self.food_database[food]['benefits'][:2]
                })
        
        return suggestions

    def export_to_json(self, filename="food_database.json"):
        """Export database to JSON for easy sharing"""
        export_data = {}
        for telugu_name, data in self.food_database.items():
            export_data[telugu_name] = data
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Database exported to {filename}")

    def create_retail_labels(self, food_names):
        """Create retail-style labels for given foods"""
        labels = []
        for food_name in food_names:
            results = self.search_food_item(food_name)
            if results:
                telugu_name, data = results[0]
                
                # Create attractive retail label
                label = f"""
╔══════════════════════════════════════════════════════════════╗
║  {data['english']:^58} ║
║  {telugu_name:^58} ║
║  {data['hindi']:^58} ║
║                                                              ║
║  Category: {data['category']:<15} Type: {data['type']:<20} ║
║                                                              ║
║  Key Benefits:                                               ║
"""
                for i, benefit in enumerate(data['benefits'][:3], 1):
                    label += f"║  {i}. {benefit:<55} ║\n"
                
                label += f"""║                                                              ║
║  Nutrition Highlights (per 100g):                           ║
║  Protein: {data['nutrition'].get('protein', 'N/A'):<10} Fiber: {data['nutrition'].get('fiber', 'N/A'):<15} ║
╚══════════════════════════════════════════════════════════════╝
"""
                labels.append(label)
        
        return labels

def main():
    """Interactive demo of the enhanced food processor"""
    processor = EnhancedFoodDataProcessor()
    
    print("🌾 Enhanced Multilingual Food Data Processor 🌾")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Search for a food item")
        print("2. Get foods by category")
        print("3. Compare nutrition")
        print("4. Get meal suggestions")
        print("5. Create retail labels")
        print("6. Export database")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            food_name = input("Enter food name (in any language): ").strip()
            info = processor.get_food_info(food_name)
            
            if "error" in info:
                print(f"❌ {info['error']}")
            else:
                for item in info:
                    print(f"\n🌾 {item['english']} ({item['telugu']})")
                    print(f"   Hindi: {item['hindi']}")
                    print(f"   Category: {item['category']} | Type: {item['type']}")
                    print(f"   Benefits: {', '.join(item['health_benefits'][:3])}")
                    print(f"   Key Nutrition: {item['nutrition_per_100g']}")
        
        elif choice == "2":
            category = input("Enter category (Millet/Pulse/Grain/Spice/Seeds): ").strip()
            foods = processor.get_category_foods(category)
            
            if foods:
                print(f"\n{category.upper()} Foods:")
                for food in foods:
                    print(f"• {food['english']} ({food['telugu']}) - {food['hindi']}")
                    print(f"  Benefits: {', '.join(food['benefits'])}")
            else:
                print(f"No foods found in category: {category}")
        
        elif choice == "3":
            foods_input = input("Enter food names separated by commas: ").strip()
            food_names = [name.strip() for name in foods_input.split(',')]
            comparison = processor.create_nutrition_comparison(food_names)
            
            print("\nNutrition Comparison:")
            for item in comparison:
                print(f"• {item['name']}: {item['nutrition']}")
        
        elif choice == "4":
            preference = input("Enter dietary preference (balanced/diabetic/weight_loss): ").strip()
            suggestions = processor.generate_meal_suggestions(preference)
            
            print(f"\n🍽️ Meal Suggestions for {preference.title()} Diet:")
            for meal_type, foods in suggestions.items():
                if foods:
                    print(f"\n{meal_type.title()}:")
                    for food in foods:
                        print(f"• {food['english']} ({food['telugu']})")
                        print(f"  Benefits: {', '.join(food['benefits'])}")
        
        elif choice == "5":
            foods_input = input("Enter food names for labels (comma-separated): ").strip()
            food_names = [name.strip() for name in foods_input.split(',')]
            labels = processor.create_retail_labels(food_names)
            
            print("\n🏷️ Retail Labels:")
            for label in labels:
                print(label)
        
        elif choice == "6":
            filename = input("Enter filename (default: food_database.json): ").strip()
            if not filename:
                filename = "food_database.json"
            processor.export_to_json(filename)
            print(f"✅ Database exported to {filename}")
        
        elif choice == "7":
            print("Thank you for using Enhanced Food Data Processor! 🌾")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()