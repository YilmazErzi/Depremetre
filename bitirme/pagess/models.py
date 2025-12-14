from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Department = models.CharField(max_length=30)
    person_mail = models.EmailField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BuildingAssessment(models.Model):
    # --- OPTIONS IN ENGLISH ---
    YEAR_CHOICES = [
        (30, '2019 and later (New Regulations)'),
        (20, 'Between 2000 - 2018'),
        (5, 'Between 1980 - 1999'),
        (0, 'Before 1980'),
    ]

    GROUND_CHOICES = [
        (20, 'Rocky / Hard Ground'),
        (10, 'Normal / Firm Soil'),
        (0, 'Fill / Riverbed / Soft Soil'),
    ]

    SOFT_STORY_CHOICES = [
        (15, 'Residential Entry (Walls present)'),
        (0, 'Commercial Entry (Large glass windows/Shop)'),
    ]

    DAMAGE_CHOICES = [
        (15, 'No visible damage/cracks'),
        (8, 'Hairline cracks / Plaster cracks'),
        (0, 'Deep cracks in columns / Rusted iron (Corrosion)'),
    ]
    
    FLOOR_CHOICES = [
        (10, '1 - 3 Floors'),
        (5, '4 - 7 Floors'),
        (3, '8 Floors and above'),
    ]
    
    SHAPE_CHOICES = [
        (10, 'Symmetrical (Square/Rectangle)'),
        (5, 'Irregular (L-Shape, U-Shape, Recessed)'),
    ]

    # --- FIELDS WITH ENGLISH LABELS ---
    created_at = models.DateTimeField(auto_now_add=True)
    building_name = models.CharField(max_length=100, verbose_name="Building Name/ID")
    
    score_year = models.IntegerField(choices=YEAR_CHOICES, verbose_name="Building Age")
    score_ground = models.IntegerField(choices=GROUND_CHOICES, verbose_name="Ground Condition")
    score_soft_story = models.IntegerField(choices=SOFT_STORY_CHOICES, verbose_name="Ground Floor Status (Soft Story)")
    score_damage = models.IntegerField(choices=DAMAGE_CHOICES, verbose_name="Current Damage Status")
    score_floor = models.IntegerField(choices=FLOOR_CHOICES, verbose_name="Number of Floors")
    score_shape = models.IntegerField(choices=SHAPE_CHOICES, verbose_name="Building Shape")

    def calculate_total_score(self):
        total = (
            self.score_year +
            self.score_ground +
            self.score_soft_story +
            self.score_damage +
            self.score_floor +
            self.score_shape
        )
        return total

    def get_risk_level(self):
        score = self.calculate_total_score()
        
        # --- RESULTS IN ENGLISH ---
        if score >= 80:
            return {
                "level": "Low Risk", 
                "color": "#198754", 
                "message": "The building data looks promising, but expert inspection is still required for a final verdict."
            }
        elif score >= 50:
            return {
                "level": "Moderate Risk", 
                "color": "#ffc107", 
                "message": "There are some risk factors (like age or ground). Strengthening/Retrofitting might be needed."
            }
        else:
            return {
                "level": "High Risk", 
                "color": "#dc3545", 
                "message": "Urgent professional earthquake performance analysis is highly recommended!"
            }

    def __str__(self):
        return f"{self.building_name} - Score: {self.calculate_total_score()}"